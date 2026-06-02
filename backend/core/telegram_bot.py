from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from coingecko_sdk import AsyncCoingecko

app = ApplicationBuilder().token("8674188699:AAEhmJ0wyNsTV2tpxelPievn82b0DO4Opc8").build()
coin_gecko = AsyncCoingecko(demo_api_key = "CG-wYoN8tgMXAkVSKceKviwvNGn", environment="demo")





async def btc_price(update:Update, context:ContextTypes.DEFAULT_TYPE):
    price = await coin_gecko.simple.price.get(ids='bitcoin', vs_currencies='usd')

    # btc_price = 
   
    
    # {'bitcoin': PriceGetResponseItem(last_updated_at=None, usd=76423.0, usd_24h_change=None, usd_24h_vol=None, usd_market_cap=None)}
    await update.message.reply_text(f"Bitcon price is ${price['bitcoin'].usd}")

if name == 'main':
    
    # # Add a handler to listen for the /start command
    # start_handler = CommandHandler('start', start)
    get_price_ether = CommandHandler('ETH', ETH)
    get_price_bnb = CommandHandler('BNB', BNB)
    get_price_sol = CommandHandler('SOL', SOL)


    get_price_btc = CommandHandler('BTC', btc_price)

    app.add_handler(get_price_btc)
    
    # Run the bot until you press Ctrl-C
    app.run_polling()