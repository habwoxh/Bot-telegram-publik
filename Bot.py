from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8488026141:AAFWF2ZuOIFOF6HsZi5Y07_5Trxbgw7gtsk"
CHANNEL_ID = "@ch4groupfreefile"

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ketik /fb lalu kirim fotomu.")

async def fb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_user.id] = "waiting_photo"
    await update.message.reply_text("📸 Silakan kirim foto kamu sekarang!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if user_state.get(uid) == "waiting_photo":
        photo = update.message.photo[-1].file_id
        await context.bot.send_photo(chat_id=CHANNEL_ID, photo=photo,
                                     caption=f"📷 Dari @{update.effective_user.username or 'user'}")
        await update.message.reply_text("✅ Foto berhasil dikirim ke channel!")
        user_state.pop(uid)
    else:
        await update.message.reply_text("❗Ketik /fb dulu sebelum kirim foto.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("fb", fb))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
