from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests

###################### START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text(
            f'Thank You! {update.effective_user.first_name}\nFor Joining Us\nNote - Only send the url of Songs  not a video'
        )
    except Exception as e:
        print(
            f"Error {e}"
        )



############################## HANDLE MESSAGE
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user_message = update.message.text
    chat_type = update.message.chat.type
    message_id = update.message.message_id
    chat_id = update.effective_chat.id

    first_name = update.effective_user.first_name if update.effective_user.first_name else ""
    last_name = update.effective_user.last_name if update.effective_user.last_name else ""
    username = f"{first_name} {last_name}".strip() or update.effective_user.username

    # print(chat_type)
    # print(message_id)
    # print(chat_id)
    


    if user_message.startswith(
            "https://www.youtube.com/") or user_message.startswith(
                "https://youtube.com/") or user_message.startswith(
                    "https://music.youtube.com/") or user_message.startswith("https://youtu.be/"):

        # if "&" in user_message:
        #     user_message = user_message.split("&")[0]
        #     # print(user_message)

        # elif "?" in user_message:
        #     user_message = user_message.split("?")[0]
        
        url = "https://add-music-server.onrender.com/api/add/music"
        
        data = {
            "URL": user_message,
            "createdBy": username
        }
        
        # Send the PUT request with the JSON data
        response = requests.post(url, json=data)

        # Handle the response
        if response.status_code == 201:
            # print("Request successful")
            # print(response.json())
            await update.message.reply_text("Request successful Url Added")
            
        else:
            # print(f"Request failed with status code: {response.status_code}")
            # print(response.text)
            
            await update.message.reply_text(f"Request failed with status code: {response.status_code} , {response.text}")
            
    else:
        await update.message.reply_text("URL IS NOT SUPPORTED")
            
            
################# APP
if __name__ == "__main__":

    # TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    app = ApplicationBuilder().token("7445051215:AAFop3_6HqLEvoUscwTJ4EikENtTvlvx3K4").build()
    # app.api_kwargs = {'timeout': 500}  # Increase timeout to 60 seconds

    ################## Handelers
    app.add_handler(CommandHandler("start", start))
    # app.add_handler(CommandHandler("help", help))
    # app.add_handler(CommandHandler("about", about))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # app.add_handler(CallbackQueryHandler(button_handler))

    ####### MAIN
    print("Bot is running...")
    app.run_polling()
