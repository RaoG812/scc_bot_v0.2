from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import gspread

# Authorize Google Sheets API
gc = gspread.service_account(filename='path.json')
sheet = gc.open("MembershipDB").sheet1

async def start(update: Update, context):
    await update.message.reply_text('Welcome! Please provide your membership card number.')

# Function to validate membership
async def check_membership(update: Update, context):
    card_number = update.message.text
    try:
        # Find the row containing the user's card number
        records = sheet.get_all_records()
        for record in records:
            if str(record['Card Number']) == card_number:
                tier = record['Tier']
                main_channel = record['Main Channel']
                shopping_branch = record['Shopping Branch']
                private_chat = record['Private Chat']
                
                # Send tier-specific links
                await update.message.reply_text(f"Welcome {record['Name']}! You are a {tier} member.")
                
                links_msg = f"Here are your links:\nMain Channel: {main_channel}\n"
                if tier in ['Gold', 'Supreme']:
                    links_msg += f"Shopping Branch: {shopping_branch}\n"
                if tier == 'Supreme':
                    links_msg += f"Private Chat: {private_chat}"
                
                await update.message.reply_text(links_msg)
                return
        
        # If card number not found
        await update.message.reply_text("Sorry, your membership card number is invalid.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    application = Application.builder().token('YOUR_BOT_TOKEN').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, check_membership))

    application.run_polling()

if __name__ == '__main__':
    main()
