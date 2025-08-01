filename: main.py

import logging import requests from bs4 import BeautifulSoup from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

🔐 Replace this with your bot token

BOT_TOKEN = "8450532503:AAHrYXXvUmem6tJyMIBUpJV2pi5-oora-_s"

📜 Logging

logging.basicConfig(level=logging.INFO)

🎮 Movie Sources (You can add more trusted sites here)

MOVIE_SITES = [ "https://filmyfly.in", "https://movie4u.guru", "https://moviezip.odoo.com/hi" ]

🔍 Scrape function (auto picks latest link from source)

def search_movie(query): results = [] for site in MOVIE_SITES: try: response = requests.get(f"{site}/?s={query}", timeout=10) soup = BeautifulSoup(response.text, "html.parser") posts = soup.find_all("h2", class_="title") for post in posts[:5]: title = post.text.strip() link = post.find("a")["href"] results.append((title, link)) except Exception as e: continue return results

🏋 Start Command

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): keyboard = [ [ InlineKeyboardButton("🎮 Web Series", callback_data="webseries"), InlineKeyboardButton("🎞 Animated", callback_data="animated") ], [ InlineKeyboardButton("👶 Cartoon", callback_data="cartoon"), InlineKeyboardButton("🔥 Latest", callback_data="latest") ] ] await update.message.reply_text("Welcome to MovieHub Bot 🍿\nChoose a category:", reply_markup=InlineKeyboardMarkup(keyboard))

🔀 Handle Button Press

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer() data = query.data if data == "latest": movies = search_movie("latest hindi") elif data == "webseries": movies = search_movie("web series hindi") elif data == "animated": movies = search_movie("animated movie hindi") elif data == "cartoon": movies = search_movie("cartoon movie hindi") else: movies = []

if not movies:
    await query.edit_message_text("😕 No results found.")
    return

for title, link in movies:
    button = InlineKeyboardMarkup([[InlineKeyboardButton("🎮 Download Now", url=link)]])
    await query.message.reply_text(f"🎥 *{title}*", reply_markup=button, parse_mode="Markdown")

🔎 Search by typing

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): text = update.message.text results = search_movie(text)

if not results:
    await update.message.reply_text("🚫 No results found.")
    return

for title, link in results:
    button = InlineKeyboardMarkup([[InlineKeyboardButton("🎮 Download Now", url=link)]])
    await update.message.reply_text(f"🎥 *{title}*", reply_markup=button, parse_mode="Markdown")

⚖️ Main App Setup

app = ApplicationBuilder().token(BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) app.add_handler(MessageHandler(filters.COMMAND, start)) app.add_handler(MessageHandler(filters.ALL, handle_message)) app.add_handler(MessageHandler(filters.UpdateType.CALLBACK_QUERY, handle_callback))

if name == "main": app.run_polling()

