import pytesseract
from PIL import Image
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#function to  convert image to text
def i2t(update,context):
    #get the image sent to bot and store it in file object
    file = context.bot.getFile(update.message.photo[-1].get_file())

    #download the file in order to extract the text
    file.download('image_to_text.png')
    print('file downloaded')

    #open the image using Image function in PIL module
    img = Image.open('image_to_text.png')
    try:
        #tesseract is OCR software which extracts text from the image
        #Download the tesseract software from https://sourceforge.net/projects/tesseract-ocr-alt/files/
        #configure the tesseract.exe file, In my pc i installed tesserat in  'c:\Program Files\'
        pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files\\Tesseract-OCR\\tesseract'

        #send the img object to pytesseract
        result = pytesseract.image_to_string(img)
        print(result)

        #send the extracted text back to user
        update.message.reply_text(result)
    # exception handling can be used in this manner as using tesseract with non-clear images will give you many errors.
    #Make sure the image and text is clear.This works accurately when image background is white
    #For improving the accuracy of tesseract you can refer to  https://stackoverflow.com/questions/58327383/how-to-recognize-text-with-colored-background-images
    except Exception as e:
        print(e)
        update.message.reply_text("Sorry the image isn't clear enough to process  😔 ! Please make sure the image is clear ")

#default commands handlers
#triggered when the bot receives '/start' command
def start(update,context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello !!\nI am an Image to Text Converter Bot made by Himmalay Devulapalli.\nSend an image to me and i will convert it into text\nPlease make sure the image is clear ')

#triggered when the bot receives '/help' command
def help_command(update,context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Hello !!\nI am an Image to Text Converter Bot made by Himmalay Devulapalli.\nSend an image to me and i will convert it into text\nPlease make sure the image is clear ')

#main handler, heart of the bot where you filter the voice message and handle them
# refer https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.html for documentation
def main():
    try:
        # configure the updater with your bot token
        updater = Updater('1828787854:AAFode-P3QUQrrcUFPGlq5JbxBWIJsr_rP4', use_context=True)

        # configure a dispatcher (responsible for receiving messages from bot )
        dp = updater.dispatcher

        """
        telegram bots have a default command '/start', 
        when you try to make a conversation with the bot for the first time, you can use the /start command
        You can add your custom commands using add_handler method.
        CommandHandler is responsible for handling the command type messages, they usually look like /start,/help,etc
        """
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help_command))

        """
        Just like command handler, we have MessageHandler which takes care of all the incoming messages other than commands
        we can filter out the various messages using Filters.text or Filters.photo
        where Filters.text will handle all the plain text messages sent to the bot     
        """
        dp.add_handler(MessageHandler(Filters.text,start))

        #where Filters.photo will handle all the images sent to the bot
        dp.add_handler(MessageHandler(Filters.photo, i2t))  #triggering the i2t function when the bot  receives the image

        # Start the Bot
        updater.start_polling()

        updater.idle()
    except:
        main()


#call the main function
if __name__ == '__main__':
    print("running server")
    main()

#https://stackoverflow.com/questions/58327383/how-to-recognize-text-with-colored-background-images
