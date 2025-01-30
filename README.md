🤖 Telegram-Bot with Gemini AI & MongoDB

Welcome to the Telegram AI Chatbot repository! 🚀 This bot is designed to provide AI-powered responses, handle user interactions, perform image analysis, and conduct web searches using Gemini AI, MongoDB, and Google CX API.

✨ Features

📝 User Registration: Stores user details (first name, username, chat ID) in MongoDB.

🤖 AI-Powered Chat: Utilizes Google Gemini API to respond to user queries intelligently.

📷 Image & File Analysis: Analyzes images/files (JPG, PNG, PDF) and extracts meaningful descriptions using Gemini.

🔍 Web Search: Uses Google CX API for fetching AI-powered web search results.

📊 Database Support: Stores chat history, file metadata, and user interactions in MongoDB.

Ensure python,MongoDB are installed

🚀 Getting Started

1️⃣ Clone the Repository

git clone https://github.com/JyothiPriya5/Telegram-Bot.git
cd Telegram-Bot

2️⃣ Install Dependencies

Ensure Python is installed, then install required packages:

pip install python-telegram-bot pymongo google-generativeai requests

3️⃣ Set Up Environment Variables

Create a .env file and add your credentials:

BOT_TOKEN=your_telegram_bot_token               //Get from telegram BotFather
MONGO_URI=your_mongodb_connection_string        // download here https://www.mongodb.com/try/download/community and install MongoDB compass(ensure to enable automatically download)
GEMINI_API_KEY=your_google_gemini_api_key       // create api key from https://aistudio.google.com/
GOOGLE_SEARCH_API_KEY=your_google_cx_api_key    // create api key from Google Cloud Console.
GOOGLE_SEARCH_CX=your_google_cx_engine_id       // create cx id here https://cse.google.com/cse/

4️⃣ Run the Bot

python bot.py

Your bot is now live and ready to assist users! 🎉

📌 Usage Guide

Interact with the bot using the following commands:

/start - Register and start the bot

/websearch <query> - Perform AI-powered web searches

🛠 Technologies Used

Python 🐍

Telegram Bot API 🤖

MongoDB 🗄️

Google Gemini API 🧠

Google CX API 🔍

🏗️ Future Enhancements

✅ Sentiment analysis for better responses 💡✅ Auto-translation for multilingual support 🌍✅ Dashboard for user analytics 📊

🤝 Contributing

Want to improve this bot? Follow these steps:

Fork the repository 🍴

Create a new branch 🔀

Make your changes ✨

Submit a pull request ✅

📩 Contact

💡 Found an issue or have suggestions? Feel free to open an issue or contribute to the project!

GitHub: JyothiPriya5

🚀 Let's build something amazing together! 🚀

