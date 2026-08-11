# PrajaConnectAI — Your Gateway to Govt Benefits

> **"One platform. Many benefits. Every scheme. Every citizen. One tap away."**

PrajaConnectAI is an AI-powered 2-in-1 citizen benefit platform built for hackathons. It seamlessly connects citizens with government welfare schemes and local health checkup camps, featuring an intelligent RAG (Retrieval-Augmented Generation) AI assistant powered by local Ollama (**Gemma 3:1b**) and cloud **Mistral AI**.

---

## 🌟 Key Features

- **2-in-1 Portal**: Discover both Government Welfare Schemes and Health & Wellness Camps in a unified interface.
- **Reference-Accurate Visual Design**: Custom responsive glassmorphism aesthetic tailored directly from official interface references.
- **Local & Cloud AI Assistant**: Hybrid AI architecture supporting local execution via Ollama (`gemma3:1b`) and cloud execution via `Mistral API`.
- **Database Grounding (RAG)**: AI responses are grounded strictly in the SQLite database to prevent hallucinations and fake scheme details.
- **Multilingual Support**: Interactive support for **English**, **Telugu (తెలుగు)**, **Hindi (हिन्दी)**, **Tamil (தமிழ்)**, **Kannada (ಕನ್ನಡ)**, and **Malayalam (മലയാളം)**.
- **Instant Application Tracking**: Apply for government schemes with one tap and track application progress (Draft → Started → Submitted → Completed) stored securely in SQLite.
- **Turn-by-Turn Health Camp Directions**: One-click Google Maps integration for health camp locations.
- **Public & Multi-User Access**: Zero friction browsing for all visitors with session-isolated user workspaces.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, Flask, Jinja2
- **Database**: SQLite3 (`data/prajaconnect.db`)
- **AI Providers**:
  - Local AI: Ollama (`gemma3:1b`)
  - Cloud AI: Mistral API (`mistral-small-latest`)
- **Frontend**: HTML5, CSS3 (Vanilla Glassmorphism UI), JavaScript (ES6+), Bootstrap Icons
- **Environment & Config**: `python-dotenv`

---

## 🚀 Quick Setup & Installation Guide

### 1. Environment Setup (Windows)

```powershell
# Clone or navigate to the project directory
cd PrajaConnectAI

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### 2. Environment Variables Configuration

Create a `.env` file in the root directory:

```env
FLASK_SECRET_KEY=prajaconnect_hackathon_super_secret_key_2026
MISTRAL_API_KEY=your_mistral_api_key_here  # Optional
MISTRAL_MODEL=mistral-small-latest
PORT=5000
```

> **Note**: If `MISTRAL_API_KEY` is not set, the app automatically falls back to Local AI (Ollama Gemma) without breaking.

### 3. Local Ollama Setup (Optional for Local AI)

To use the local Gemma 3:1b model:

```powershell
# Pull the Gemma model via Ollama
ollama pull gemma3:1b

# Ensure Ollama service is running
ollama serve
```

### 4. Launch the Web Application

```powershell
python app.py
```

Open your browser and navigate to:
**`http://127.0.0.1:5000`**

---

## 📁 Project Structure

```
PrajaConnectAI/
│
├── app.py                      # Main Flask application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── .env                        # Local environment variables
├── .gitignore                  # Git exclusions
│
├── data/
│   └── prajaconnect.db         # Auto-initialized SQLite Database
│
├── database/
│   ├── db.py                   # SQLite helpers & connection context
│   └── seed_data.py            # Initial seed data for schemes and health camps
│
├── services/
│   ├── ai_service.py           # RAG context builder, Ollama & Mistral API client
│   └── search_service.py       # Full-text SQLite search engine
│
├── templates/
│   ├── base.html               # Master layout with navbar & floating bottom nav
│   ├── index.html              # Home page styled after Image 2 reference
│   ├── schemes.html            # Government schemes listing & filters
│   ├── scheme_detail.html      # Scheme overview & application submission
│   ├── camps.html              # Health camps discovery
│   ├── camp_detail.html        # Health camp overview & Google Maps directions
│   ├── applications.html       # Application tracker & status updates
│   ├── profile.html            # Citizen profile management
│   ├── assistant.html          # Interactive AI Assistant chat page
│   ├── search.html             # Global search results page
│   ├── 404.html                # Custom 404 page
│   └── 500.html                # Custom 500 page
│
└── static/
    ├── css/
    │   └── style.css           # Glassmorphism aesthetic & responsive grid
    ├── js/
    │   ├── app.js              # UI handlers, voice search, modals & toasts
    │   └── chatbot.js          # Asynchronous AI chat script
    └── images/
        ├── logo.png            # Official PrajaConnectAI logo
        └── ui_ref.jpg          # Reference design image
```

---

## 🔒 Security & Guidelines

- Secrets and API keys are loaded strictly via `.env`.
- `.env` and `*.db` are included in `.gitignore`.
- Raw Python exceptions are intercepted and replaced with user-friendly error notifications.

---

## 🏆 Hackathon Demonstration Checklist

1. Open `/` to view the 2-in-1 Citizen Benefit homepage.
2. Filter schemes under `/schemes` by category (Farmers, Women, Students, Workers) or age group.
3. Open a scheme detail and click **Apply Now** to create a live application record in SQLite.
4. Go to `/applications` to verify application creation and update status to **Submitted**.
5. Explore `/camps` and click **Get Directions** to trigger Google Maps direction URL.
6. Open `/assistant`, test prompts in **English** and **Telugu**, and toggle between **Local AI** and **Mistral Cloud AI**.
