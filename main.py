import os
import logging

from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

openai = OpenAI() # defaults to getting the key using os.environ.get("OPENAI_API_KEY")
tg_bot_token = os.getenv('TG_BOT_TOKEN')
# tg_bot_token = "https://api.telegram.org/" + os.getenv('API_KEY') + "/getMe"

messages = [
    {"role": "system", "content": "You are a helpful assistant that answers questions."}
]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def post_init(application):
    commands = [
        ("start", "Start the bot.")
        # ("chat", "Use chatGPT. Unfortunately every message needs to start with /chat your text here.")
        # BotCommand("help", "Get the list of available commands.")
    ]
    await application.bot.set_my_commands(commands)


# async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     messages.append({"role": "user", "content": update.message.text})
#     completion = openai.chat.completions.create(
#         model="gpt-3.5-turbo", messages=messages
#     )
#     completion_answer = completion.choices[0].message
#     messages.append(completion_answer)

#     await context.bot.send_message(
#         chat_id=update.effective_chat.id, text=completion_answer.content
#     )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot with chatGPT 3.5 running behind the scenes. Start chatting as you would with chatGPT."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user_message = update.message.text
    # Here, you can process the user_message and generate a response.
    # For example, you could send this message to the OpenAI API and return the response.
    # response_message = "You said: " + user_message  # Placeholder for actual response generation
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=response_message)
    messages.append({"role": "user", "content": update.message.text})
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )
    completion_answer = completion.choices[0].message
    messages.append(completion_answer)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=completion_answer.content
    )


if __name__ == "__main__": 
    # creates a new application instance for the bot using the bot token
    application = ApplicationBuilder().token(tg_bot_token).post_init(post_init).build()
    
    # defines a command handler that listens for the "/start" command and is linked to the start function, which sends a greeting message.
    start_handler = CommandHandler("start", start)
    # chat_handler = CommandHandler("chat", chat)
    # help_handler = CommandHandler("help", help)


    # register the handler(s) with the application
    application.add_handler(start_handler)
    # application.add_handler(chat_handler)
    # application.add_handler(help_handler)

    # Add a MessageHandler for text messages
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(text_handler)

    # start the bot and begins polling for updates.
    application.run_polling()
    # Immediately after starting the bot, set the commands.

    