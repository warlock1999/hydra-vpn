import os
import logging
import asyncio
import json
import base64
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- CONFIG ---
TOKEN = os.getenv("TG_BOT_TOKEN")
ADMIN_ID = int(os.getenv("TG_ADMIN_ID"))
UUID = os.getenv("HYDRA_UUID")
DOMAIN = os.getenv("VPN_DOMAIN")

# --- VMESS LINK GENERATOR ---
def generate_vmess():
    # Construct the VMess JSON
    vmess_config = {
        "v": "2",
        "ps": "🛡️ HYDRA ONION",
        "add": DOMAIN,
        "port": "443",
        "id": UUID,
        "aid": "0",
        "scy": "auto",
        "net": "ws",
        "type": "none",
        "host": DOMAIN,
        "path": "/hydra",
        "tls": "tls",
        "sni": DOMAIN,
        "alpn": ""
    }
    # Encode to Base64
    json_str = json.dumps(vmess_config)
    b64_str = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
    return f"vmess://{b64_str}"

# --- BOT COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return # Ignore strangers

    link = generate_vmess()
    msg = (
        "<b>🐲 Hydra Anonymity System Online</b>\n\n"
        "Here is your strict-node connection link:\n"
        f"<code>{link}</code>"
    )
    await update.message.reply_text(msg, parse_mode="HTML")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    await update.message.reply_text("🟢 System Operational. Tor Circuit Active.")

# --- MAIN LOOP ---
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    
    print("Bot is running...")
    app.run_polling()
