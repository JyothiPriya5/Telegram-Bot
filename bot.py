import os
import io
from dotenv import load_dotenv
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from db import users_collection, chats_collection, files_collection
import google.generativeai as genai
from pymongo import DESCENDING
import requests
from PIL import Image
from pdf2image import convert_from_bytes


# Load API keys from .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Register User Function
async def register_user(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat_id = update.message.chat_id

    if users_collection.find_one({"chat_id": chat_id}):
        await update.message.reply_text("You're already registered!")
        return

    user_data = {
        "chat_id": chat_id,
        "first_name": user.first_name,
        "username": user.username,
    }
    users_collection.insert_one(user_data)

    await update.message.reply_text(f"Welcome {user.first_name}, you've been registered!")

# Gemini Chat Function
async def gemini_chat(update: Update, context: CallbackContext):
    user_message = update.message.text
    chat_id = update.message.chat_id
    timestamp= update.message.date

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_message).text

    chats_collection.insert_one({
        "chat_id": chat_id,
        "user_message": user_message,
        "bot_response": response,
        "time_stamp": timestamp
    })

    await update.message.reply_text(response)

#Image analysis
async def image_analysis(update: Update, context: CallbackContext):
    """Handles image uploads (JPG, PNG, PDF) and provides AI-generated analysis."""
    user = update.message.from_user
    # Get the uploaded file
    photo_file = await update.message.effective_attachment.get_file()
    file_stream = io.BytesIO()
    await photo_file.download_to_memory(file_stream)
    # Determine file type and process accordingly
    file_stream.seek(0)
    file_extension = photo_file.file_path.split('.')[-1].lower()
    if file_extension in ["jpg", "jpeg", "png"]:
        image = Image.open(file_stream)  # Open the image
    elif file_extension == "pdf":
        # Convert first page of PDF to an image
        images = convert_from_bytes(file_stream.getvalue(), first_page=0, last_page=1)
        image = images[0]
    else:
        await update.message.reply_text("⚠️ Unsupported file format. Please upload JPG, PNG, or PDF.")
        return
    # Convert image to bytes and send to Gemini API
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    model = genai.GenerativeModel("gemini-pro-vision")
    try:
        response = model.generate_content([img_byte_arr.getvalue()])  # Pass raw image bytes
        description = response.text if response.text else "⚠️ Could not analyze the image."
    except Exception as e:
        description = f"⚠️ Error analyzing image: {str(e)}"

    await update.message.reply_text(f"🖼 **Image Analysis Result:**\n{description}")


# Web Search Function
async def web_search(update: Update, context: CallbackContext):
    GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")  
    GOOGLE_SEARCH_CX = os.getenv("GOOGLE_SEARCH_CX") 

    if not GOOGLE_SEARCH_API_KEY or not GOOGLE_SEARCH_CX:
        await update.message.reply_text("Search API keys are missing. Please configure them properly.")
        return

    # Get the search query from user input
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please enter a search query. Example: /websearch AI trends")
        return

    # Construct the API request
    search_url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": GOOGLE_SEARCH_CX,
        "num": 5,  # Limit to 5 results
    }

    try:
        response = requests.get(search_url, params=params).json()

        if "items" in response:
            results = "\n".join([f"{i+1}. {item['title']} - {item['link']}" for i, item in enumerate(response["items"][:5])])
        else:
            results = "No results found."

        await update.message.reply_text(results)

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


# Main Function to Start Bot
def main():
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", register_user))
    app.add_handler(CommandHandler("websearch", web_search))

    # Handlers for messages & images
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gemini_chat))
    app.add_handler(MessageHandler(filters.PHOTO, image_analysis))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
