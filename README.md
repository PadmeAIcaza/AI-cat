# 🐈‍⬛ VoidCat

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Google Gemini](https://img.shields.io/badge/AI-Google_Gemini-4285F4)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-In_Development-orange)

An interactive AI-powered desktop companion that brings a virtual cat to life. 

VoidCat is a Python desktop application that combines a fully animated virtual pet with Google's Gemini AI to create a desktop companion capable of natural conversations. Unlike traditional chatbots, VoidCat has its own personality, expressive animations, and conversational memory, making interactions feel more like talking to a living companion than a standard AI assistant.

#### Note: Some Tkinter features are platform-dependent. On Linux, transparent window backgrounds (-transparentcolor) are not supported, so the cat and chat window backgrounds may appear magenta instead of transparent.

---

## ✨ Features

* 🤖 Powered by Google Gemini API
* 🐈 Fully animated desktop cat with multiple sprite animations
* 💬 Real-time conversational AI
* 🧠 Persistent conversation memory during each session
* 🎭 Custom personality loaded from an external configuration file
* ⚡ Background AI processing to keep the interface responsive
* 🔐 Secure API key management using environment variables
* 🖱️ Interactive desktop companion

---

## 📸 Preview

<img width="500" height="411" alt="Animation" src="https://github.com/user-attachments/assets/9fee156b-2381-4f4c-b149-de62bc4753f9" />


---

## 🛠️ Built With

* Python 3
* Google Gemini API
* Tkinter
* Pillow (PIL)
* Python threading
* Queue
* python-dotenv

---

## 📂 Project Structure

```text
VoidCat/
│
├── assets/
│   ├── sprites/             # Sprite sheets and animations
│   └── ...
│
├── src/
│   ├── main.py              # Application entry point
│   ├── cat.py               # Desktop pet animations and behavior
│   ├── AIchat.py            # Chat window and AI interaction
│   ├── ai.py                # Gemini API wrapper
│   ├── personality.txt      # VoidCat's personality prompt
│   └── ...
│
├── .env                     # API configuration (not committed)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/PadmeAIcaza/AI-cat.git
cd VoidCat
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here

# Optional
GEMINI_MODEL=gemini-3.6-flash
```

### 4. Run the application

```bash
cd .\src
python main.py
```

---

## 🧠 Personality System

VoidCat's behavior is controlled through a simple text file.

Example:

```text
You are VoidCat, a mysterious but friendly virtual cat.
You enjoy helping users learn programming.
Stay playful while giving accurate and detailed explanations.
Occasionally use cat-like expressions.
```

Because the personality is stored separately from the code, it can be modified without changing the application itself.

---

## ⚙️ How It Works

1. The user opens VoidCat's chat window.
2. A message is sent to a background thread.
3. Gemini generates a response while the UI remains responsive.
4. Responses are safely returned through a thread-safe queue.
5. VoidCat displays the answer while updating its animations.

This architecture allows smooth conversations without freezing the desktop application.

---

## 🎮 Controls

| Action | Function |
|---------|----------|
| Left Click | Open AI chat |
| Drag Window | Move the chat window |
| Enter Key | Send message |
| Talk Button | Send message to Gemini |

---

## 🔒 Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Your Google Gemini API key |
| `GEMINI_MODEL` | *(Optional)* Gemini model to use |

---

## 📄 License

This project is licensed under the MIT License.
