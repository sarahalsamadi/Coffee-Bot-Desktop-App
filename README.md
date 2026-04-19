# ☕Smart Coffee Shop & AI Assistant

A sophisticated desktop application designed for coffee enthusiasts and cafe management. This app combines a modern user interface with an **AI-powered assistant** to provide a seamless experience from browsing the menu to chatting about your favorite beverage.

## 🚀 Overview
BrewMaster is more than just a shop; it's an interactive platform where users can:
- **Manage Accounts:** Create accounts and log in securely via MongoDB.
- **Browse Menu:** Explore a variety of drinks and add them to a virtual cart.
- **AI Chatbot:** An integrated assistant specialized *only* in coffee and tea, using Google's Gemini Pro.
- **Voice Interaction:** Supports voice commands and text-to-speech for an accessible experience.

## 🛠️ Tech Stack
- **Frontend:** `PyQt6` (Python GUI) & Qt Designer for `.ui` files.
- **Backend:** `Python` with a modular architecture.
- **Database:** `MongoDB` for storing user data and conversation history.
- **AI Engine:** `Google Generative AI` (Gemini Pro).
- **Speech Features:** `gTTS` (Google Text-to-Speech) & `SpeechRecognition`.

## 📊 Project Structure
- `main.py`: The entry point managing windows (Home, Login, Menu, Cart).
- `chatbot.py`: Logic for the AI assistant and voice processing.
- `managedb.py`: MongoDB connection and conversation logging.
- `*.ui` files: XML-based UI designs for a professional look.

## ⚙️ Installation & Usage
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/BrewMaster-AI-Shop.git](https://github.com/YourUsername/BrewMaster-AI-Shop.git)

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Database Setup:**
   Ensure MongoDB is running locally on localhost:27017.

4. **Run the Application:**
   ```bash
   python main.py

## 📝 Key Features
. **Context-Aware AI:** The chatbot is strictly prompted to discuss only beverages, ensuring a focused user experience.
. **Voice-to-Text & Text-to-Voice:** Talk to the app and hear the responses, making it more interactive.
. **Dynamic UI:** A frameless, modern dark-themed interface with smooth transitions between windows.
. **Persistent Storage:** Saves your chats and user data to a database for long-term use.
