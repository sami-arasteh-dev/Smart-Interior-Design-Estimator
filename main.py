import base64
import json
import io
import re
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from openai import OpenAI
import PyPDF2

# راه‌اندازی کلاینت هوش مصنوعی
client = OpenAI(
    base_url="https://api.gapgpt.app/v1",
    api_key="sk-gJI1851Li5z70HphGjIjkxjNGjNGMIGdZ1y3Y4NtI11SvUWa"
)

app = FastAPI(title="Smart Interior Design Estimator 🚀")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# اندپوینت اختصاصی برای تحلیل تصویر و استخراج متریال‌ها
@app.post("/analyze")
async def analyze_endpoint(
    images: List[UploadFile] = File(...), # پشتیبانی از چندین عکس
    length: str = Form(default=""),
    width: str = Form(default=""),
    height: str = Form(default=""),
    description: str = Form(default="") # دریافت توضیحات کاربر
):
    try:
        user_content = []
        
        # پردازش تمام عکس‌های آپلود شده
        for img in images:
            file_bytes = await img.read()
            base64_image = base64.b64encode(file_bytes).decode('utf-8')
            image_url = f"data:{img.content_type};base64,{base64_image}"
            user_content.append({"type": "image_url", "image_url": {"url": image_url}})

        # پرامپت اصلاح شده برای زبان فارسی، جزئیات دقیق و استفاده از توضیحات
        system_prompt = f"""شما یک معمار ارشد، طراح دکوراسیون داخلی و برآوردکننده حرفه‌ای هزینه هستید.
کاربر یک یا چند تصویر از پروژه (طرح سه‌بعدی یا پلان) ارسال کرده است.

اطلاعات فنی اعلام شده توسط کاربر:
- طول: {length or 'خالی'} متر
- عرض: {width or 'خالی'} متر
- ارتفاع: {height or 'خالی'} متر
- توضیحات و راهنمای کاربر: {description or 'توضیحی داده نشده است.'}

قوانین بسیار مهم:
۱. زبان خروجی: بخش تحلیل (analysis) باید **فقط و فقط به زبان فارسی**، روان و بسیار حرفه‌ای نوشته شود. استفاده از کلمات انگلیسی فقط برای اصطلاحات تخصصی (آن هم در کنار معادل فارسی) مجاز است.
۲. جزئیات تحلیل: در بخش تحلیل، به طور مفصل درباره عناصر به کار رفته در تصاویر (سقف، کف‌سازی، دیوارپوش‌ها، نورپردازی، مبلمان و رنگ‌بندی) صحبت کنید. علت تخمین مقادیر متریال‌ها، فرمول‌های محاسبه، و در صورت خالی بودن ابعاد، فرضیات خود (مثلاً ارتفاع استاندارد ۲.۸ متر) را با ذکر دلیل مهندسی به طور کامل توضیح دهید. توضیحات کاربر را حتما در تحلیل خود لحاظ کنید.
۳. خروجی باید **فقط و فقط** یک شیء JSON با فرمت دقیق زیر باشد و هیچ متن اضافه‌ای خارج از این ساختار تولید نکنید:
{{
  "analysis": "متن تحلیل جامع شما به زبان فارسی در اینجا قرار می‌گیرد...",
  "materials": [
    {{"name": "نام متریال", "quantity": "مقدار تخمینی به همراه واحد (مثلاً ۲۰ متر مربع)"}}
  ]
}}"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content} # ارسال تمام عکس‌ها به مدل
            ],
            temperature=0.2 # دمای پایین برای حفظ دقت مهندسی
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # پاکسازی مارک‌داون‌های احتمالی برای استخراج JSON تمیز
        ai_response = re.sub(r'^```json\s*', '', ai_response)
        ai_response = re.sub(r'^```\s*', '', ai_response)
        ai_response = re.sub(r'\s*```$', '', ai_response)
        
        result_data = json.loads(ai_response)
        return {"status": "success", "data": result_data}

    except Exception as e:
        print(f"Analysis Error: {str(e)}")
        raise HTTPException(status_code=500, detail="خطا در تحلیل تصاویر یا فرمت خروجی. لطفا دوباره تلاش کنید.")

# اندپوینت چت (برای پنل شناور)
@app.post("/chat")
async def chat_endpoint(
    message: str = Form(...),
    memory_limit: int = Form(...),
    history: str = Form(...),
    project_context: str = Form(default=""),
    files: List[UploadFile] = File(default=[])
):
    try:
        chat_history = json.loads(history)
        if memory_limit > 0 and len(chat_history) > memory_limit:
            chat_history = chat_history[-memory_limit:]
        elif memory_limit == 0:
            chat_history = []

        current_content = []
        combined_pdf_texts = ""
        
        for file in files:
            if not file.filename: continue
            file_bytes = await file.read()
            if file.content_type == "application/pdf":
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                extracted_text = f"--- فایل: {file.filename} ---\n"
                for page in pdf_reader.pages: extracted_text += page.extract_text() + "\n"
                combined_pdf_texts += extracted_text
            elif file.content_type.startswith("image/"):
                base64_img = base64.b64encode(file_bytes).decode('utf-8')
                current_content.append({"type": "image_url", "image_url": {"url": f"data:{file.content_type};base64,{base64_img}"}})
            else:
                raise HTTPException(status_code=400, detail="فرمت فایل پشتیبانی نمی‌شود.")

        final_msg = f"متن فایل(ها):\n{combined_pdf_texts}\nپیام: {message}" if combined_pdf_texts else message
        current_content.insert(0, {"type": "text", "text": final_msg})

        messages_payload = []
        
        if project_context:
            system_msg = f"شما دستیار هوشمند دکوراسیون هستید. کاربر درباره پروژه جاری با مشخصات زیر صحبت می‌کند:\n{project_context}\nاگر کاربر نظر شما را پرسید، منظور او همین پروژه و متریال‌های آن است."
            messages_payload.append({"role": "system", "content": system_msg})

        messages_payload.extend(chat_history)
        messages_payload.append({"role": "user", "content": current_content})

        response = client.chat.completions.create(model="gpt-4o", messages=messages_payload, temperature=0.5)
        return {"status": "success", "response": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
