# Импорт необходимых модулей из библиотеки tkinter
from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
import threading


# Функция для скачивания видео
def download_video():
    try:
        # Получение URL видео из текстового поля
        video_link = url_entry.get()
        # Получение разрешения видео из выпадающего списка
        resolution = video_resolution.get()
        # Проверка, пусты ли поле ввода и выпадающий список
        if resolution == '' and video_link == '':
            showerror(title='Ошибка', message='Пожалуйста, укажите и URL видео, и разрешение!!')
        # Проверка, пусто ли поле разрешения
        elif resolution == '':
            showerror(title='Ошибка', message='Пожалуйста, выберите разрешение видео!!')
        # Проверка, не является ли значение "None" выбранным в выпадающем списке
        elif resolution == 'None':
            showerror(title='Ошибка', message='None - недопустимое разрешение видео!!\n'\
                    'Пожалуйста, выберите допустимое разрешение видео')
        else:
            # Попытка скачать видео
            try:
                def on_progress(stream, chunk, bytes_remaining):
                    total_size = stream.filesize

                    def get_formatted_size(total_size, factor=1024, suffix='B'):
                        for unit in ["", "КБ", "МБ", "ГБ", "ТБ", "P", "E", "Z"]:
                            if total_size < factor:
                                return f"{total_size:.2f}{unit}{suffix}"
                            total_size /= factor
                        return f"{total_size:.2f}Y{suffix}"

                    formatted_size = get_formatted_size(total_size)
                    bytes_downloaded = total_size - bytes_remaining
                    percentage_completed = round(bytes_downloaded / total_size * 100)
                    progress_bar['value'] = percentage_completed
                    progress_label.config(text=str(percentage_completed) + '%, Размер файла: ' + formatted_size)
                    window.update()

                video = YouTube(video_link, on_progress_callback=on_progress)
                video.streams.filter(res=resolution).first().download()
                showinfo(title='Скачивание завершено', message='Видео успешно скачано.')
                progress_label.config(text='')
                progress_bar['value'] = 0
            except:
                showerror(title='Ошибка скачивания', message='Не удалось скачать видео с выбранным разрешением')
                progress_label.config(text='')
                progress_bar['value'] = 0
    except:
        showerror(title='Ошибка скачивания', message='Произошла ошибка во время попытки скачивания видео\n' \
                    'Возможные причины:\n-> Неверная ссылка\n-> Отсутствие интернет-соединения\n'\
                     'Убедитесь, что у вас есть стабильное интернет-соединение и корректная ссылка на видео')
        progress_label.config(text='')
        progress_bar['value'] = 0


# Функция для поиска разрешений видео
def searchResolution():
    # Получение URL видео из текстового поля
    video_link = url_entry.get()
    # Проверка, пуст ли URL видео
    if video_link == '':
        showerror(title='Ошибка', message='Пожалуйста, укажите ссылку на видео!')
    # Если URL видео не пустой, выполняется поиск разрешений
    else:
        try:
            # Создание объекта YouTube
            video = YouTube(video_link)
            # Пустой список для хранения всех разрешений видео
            resolutions = []
            # Перебор потоков видео
            for i in video.streams.filter(file_extension='mp4'):
                # Добавление разрешений видео в список resolutions
                resolutions.append(i.resolution)
            # Добавление разрешений в выпадающий список
            video_resolution['values'] = resolutions
            # По завершению поиска уведомление пользователю
            showinfo(title='Поиск завершен', message='Проверьте выпадающий список для доступных разрешений видео')
        # Обработка ошибок, если они возникнут
        except:
            # Уведомление пользователя об ошибке
            showerror(title='Ошибка', message='Произошла ошибка при поиске разрешений видео!\n'\
                'Причины могут быть следующими:\n-> Нестабильное интернет-соединение\n-> Неверная ссылка')


# the function to run the searchResolution function as a thread
def searchThread():
    t1 = threading.Thread(target=searchResolution)
    t1.start()


# the function to run the download_video function as a thread
def downloadThread():
    t2 = threading.Thread(target=download_video)
    t2.start()


# Создание главного окна
window = Tk()
window.title('Загрузка Видео С Ютуба')  # Установка заголовка окна
window.geometry('500x460+430+180')  # Установка размеров и позиции окна
window.resizable(False, False)  # Запрет изменения размеров окна

# Создание холста для размещения виджетов
canvas = Canvas(window, width=500, height=400)
canvas.pack()

# Загрузка логотипа
logo = PhotoImage(file='ютуб.png')
# Уменьшение размера логотипа
logo = logo.subsample(4, 4)
# Добавление логотипа на холст
canvas.create_image(250, 80, image=logo)

"""Стили для виджетов"""
# Стиль для метки (label)
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 15))
# Стиль для текстового поля (entry)
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))
# Стиль для кнопки
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font='DotumChe')

# Создание метки для ввода URL видео
url_label = ttk.Label(window, text='Введите URL видео:', style='TLabel')
# Создание текстового поля для ввода URL
url_entry = ttk.Entry(window, width=76, style='TEntry')
# Размещение метки на холсте
canvas.create_window(114, 200, window=url_label)
# Размещение текстового поля на холсте
canvas.create_window(250, 230, window=url_entry)

# Создание метки для выбора разрешения видео
resolution_label = Label(window, text='Разрешение:')
# Размещение метки на холсте
canvas.create_window(50, 260, window=resolution_label)
# Создание выпадающего списка для выбора разрешения видео
video_resolution = ttk.Combobox(window, width=10)
# Размещение выпадающего списка на холсте
canvas.create_window(60, 280, window=video_resolution)



# Создание кнопки для поиска разрешений
search_resolution = ttk.Button(window, text='Поиск Разрешения', command=searchThread)

# Размещение кнопки на холсте
canvas.create_window(90, 315, window=search_resolution)

# Создание пустой метки для отображения прогресса загрузки
progress_label = Label(window, text='')
# Размещение метки на холсте
canvas.create_window(240, 360, window=progress_label)
# Создание полосы прогресса для отображения хода загрузки
progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=450, mode='determinate')
# Размещение полосы прогресса на холсте
canvas.create_window(250, 380, window=progress_bar)
# Создание кнопки для загрузки видео
download_button = ttk.Button(window, text='Скачать видео', style='TButton', command=downloadThread)
# Размещение кнопки на холсте
canvas.create_window(240, 410, window=download_button)






# Запуск главного цикла отображения окна
window.mainloop()


















# from pytube import YouTube
#
# def video_downloader(video_url):
#     my_video = YouTube(video_url)
#     my_video.streams.get_highest_resolution().download()
#
#     return my_video.title
#
# try:
#     youtube_link = input('Введите ссылка на видео:')
#     print(f'Видео скачивается, пожалуйста подождите......')
#
#     video = video_downloader(youtube_link)
#     print(f'"{video}" успешно скачано')
# except:
#     print(f'При загрузке видео возникла ошибка, пожалуйста попробуйте снова')