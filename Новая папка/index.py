import telebot
import instaloader
import os
import shutil

# Инициализация бота с использованием вашего токена
bot = telebot.TeleBot('7472527476:AAEEKng0SloJjuC_etNp80DBD08Q-DUI4eE')

# Инициализация instaloader
loader = instaloader.Instaloader()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Отправьте ссылку на видео в Instagram.")

@bot.message_handler(func=lambda message: True)
def download_instagram_video(message):
    url = message.text

    try:
        # Создание папки, если она не существует
        download_dir = 'downloads'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Скачивание видео
        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        loader.download_post(post, target=download_dir)
        
        # Поиск видеофайла в загруженной папке
        for filename in os.listdir(download_dir):
            if filename.endswith('.mp4'):
                video_path = os.path.join(download_dir, filename)
                
                # Отправка видео пользователю
                with open(video_path, 'rb') as video_file:
                    bot.send_video(message.chat.id, video_file)
        
        # Удаление всех файлов в папке загрузки
        for filename in os.listdir(download_dir):
            file_path = os.path.join(download_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        
        # Удаление папки после очистки
        os.rmdir(download_dir)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

# Запуск бота
bot.polling()
