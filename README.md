# Smart Interior Design Estimator

An AI-powered web application that analyzes interior design images (renders/floor plans) to automatically generate material estimates and professional pre-invoices. Built with FastAPI and OpenAI GPT-4o.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Technical Notes](#technical-notes)

## ✨ Features

- **Image Analysis:** Accepts multiple image uploads (renders/plans) and extracts material lists.
- **Dimension Integration:** Uses user-provided room dimensions (length, width, height) to refine quantity estimates.
- **Smart Chatbot:** A context-aware assistant that understands the current project's details and history.
- **Dynamic Invoicing:** Generates an editable pre-invoice table with auto-calculated totals, discounts, and taxes.
- **Print-Ready Output:** CSS media queries ensure clean printing of invoices without UI clutter.
- **JSON Output:** AI responses are strictly formatted as JSON for reliable frontend parsing.

## 🛠 Tech Stack

- **Backend:** Python 3.8+, FastAPI, Uvicorn
- **AI Service:** OpenAI API (GPT-4o)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Libraries:** `openai`, `PyPDF2`, `fastapi`, `uvicorn`

## 🏗 Architecture

The application follows a simple client-server architecture:

1.  **Frontend (`index.html`):** Served statically by FastAPI. Handles user input, image preview, and dynamic DOM manipulation for the invoice table and chat interface.
2.  **Backend (`main.py`):**
    -   Serves the frontend.
    -   `/analyze`: Receives images and form data, sends them to OpenAI GPT-4o for material extraction, and returns structured JSON.
    -   `/chat`: Handles conversational AI, maintaining context via history and project metadata.

## 📦 Prerequisites

-   Python 3.8 or higher
-   `pip` package manager
-   An OpenAI API Key (configured in `main.py`)

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd smart-interior-design-estimator
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If `requirements.txt` is not provided, install manually:*
    ```bash
    pip install fastapi uvicorn openai PyPDF2
    ```

4.  **Configure API Key:**
    Open `main.py` and update the `api_key` in the `OpenAI` client initialization:
    ```python
    client = OpenAI(
        base_url="https://api.gapgpt.app/v1", # Or your preferred provider
        api_key="YOUR_ACTUAL_API_KEY_HERE"
    )
    ```

## ⚙️ Configuration

-   **Port:** The server runs on port `8765` by default. Change this in `main.py` under `uvicorn.run()`.
-   **AI Model:** The application uses `gpt-4o`. You can change the model name in the `client.chat.completions.create()` calls if needed.
-   **Memory Limit:** The chat history limit is set to `10` messages by default in the frontend. Adjust `memory_limit` in `sendMessage()` if necessary.

## 💻 Usage

1.  **Start the server:**
    ```bash
    python main.py
    ```

2.  **Access the application:**
    Open your browser and navigate to `http://localhost:8765`.

3.  **Analyze a Project:**
    -   Fill in project details (Buyer Name, Project Name, Date).
    -   Enter room dimensions (Length, Width, Height).
    -   Upload one or more images of the interior design.
    -   Add any specific notes in the description field.
    -   Click **"تحلیل هوشمند تصویر و تولید پیش‌فاکتور"** (Smart Image Analysis & Invoice Generation).

4.  **Use the Chatbot:**
    -   Use the floating chat panel on the right to ask questions about the project. The bot has context about the uploaded images and dimensions.

5.  **Print Invoice:**
    -   After analysis, the invoice table will populate.
    -   Edit prices, discounts, or tax rates as needed.
    -   Click the **"🖨 چاپ پیش‌فاکتور"** button to print or save as PDF.

## 🔌 API Endpoints

### `POST /analyze`
Analyzes uploaded images and form data to extract materials.

**Parameters:**
-   `images`: List of image files (`multipart/form-data`)
-   `length`: String (optional)
-   `width`: String (optional)
-   `height`: String (optional)
-   `description`: String (optional)

**Response:**
```json
{
  "status": "success",
  "data": {
    "analysis": "Detailed analysis in Persian...",
    "materials": [
      { "name": "Material Name", "quantity": "10 sqm" }
    ]
  }
}
```

### `POST /chat`
Handles chatbot interactions.

**Parameters:**
-   `message`: String
-   `memory_limit`: Integer
-   `history`: JSON string of previous messages
-   `project_context`: String (project details)
-   `files`: List of files (optional, for PDF/image context)

**Response:**
```json
{
  "status": "success",
  "response": "Bot's reply..."
}
```

## 📂 Project Structure

```
.
├── main.py          # FastAPI backend application
├── index.html       # Frontend UI and client-side logic
└── requirements.txt # Python dependencies (if applicable)
```

## 🔍 Technical Notes

-   **AI Prompting:** The backend uses a detailed system prompt to ensure the AI outputs valid JSON and provides professional analysis in Persian. Markdown code blocks are stripped before JSON parsing.
-   **Image Handling:** Images are converted to Base64 strings and sent to the OpenAI API as `image_url` content.
-   **Invoice Calculation:** All financial calculations (subtotal, discount, tax, grand total) are performed client-side in JavaScript for immediate feedback.
-   **Print Styles:** CSS `@media print` rules hide non-essential UI elements (chat, inputs) to ensure a clean printout.

## 🤝 Development

To contribute or modify the application:

1.  Edit `main.py` to change AI logic or add new endpoints.
2.  Edit `index.html` to update UI/UX or client-side logic.
3.  Ensure the OpenAI API key is valid and has access to GPT-4o.

## 📜 License

This project is for internal or commercial use as per the user's agreement. No specific open-source license is declared in the source files.
