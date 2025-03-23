import telebot#Импортируем бота
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

#Вставляем бот
bot = telebot.TeleBot("TOKEN")

#Первая, стартовая команда
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Telegram бот, который расскажет тебе про глобальное потепление.Напиши /commands, чтобы узнать все про эту тему")

#Комнада про команды
@bot.message_handler(commands=['commands'])
def commands(message):
    bot.reply_to(message, "/global_warming - это команда расскажет тебе про глобальное потепление, /problems - эта расскажет о последствиях потепление, /caused - расскажет чем оно вызвано, /prevent - как предатвротить потепление")

#Команада про потепление
@bot.message_handler(commands=['global_warming'])
def warming(message):
    photo = open("warming.png", 'rb')
    bot.send_photo(message.chat.id, photo, caption="Глоба́льное потепле́ние — длительное повышение средней температуры климатической системы Земли, происходящее уже более века. Повышение температуры поверхности Земли с конца XIX века, начиная с 1850 года, в десятилетнем масштабе температура воздуха в каждое десятилетие была выше, чем в любое предшествующее десятилетие. С 1750—1800 годов человек ответственен за повышение средней глобальной температуры на 0,8—1,2 °C. Вероятная величина дальнейшего роста температуры на протяжении XXI века на основе климатических моделей составляет 0,3—1,7 °C для минимального сценария эмиссии парниковых газов, 2,6—4,8 °C — для сценария максимальной эмиссии.")

#Команда про последствия
@bot.message_handler(commands=['problems'])
def problems(message):
    photo_2 = open("ttt.png", 'rb')
    bot.send_photo(message.chat.id, photo_2, caption="Воздействие глобального потепления на окружающую среду является широким и далеко идущим. Оно включает в себя следующие разнообразные эффекты: таяние арктических льдов, повышение уровня моря, отступление ледников, увеличение количества аллергий и астмы, исчезновение и миграция рыбы, ухудшение сна, влияние на психическое здоровье. ")

#Чем оно вызвано
@bot.message_handler(commands=['caused'])
def caused(message):
    bot.reply_to(message, "Глобальное потепление вызвано преимущественно деятельностью человека, которая приводит к увеличению концентрации парниковых газов в атмосфере - это происходит из-за сжигания топлива, вырубке лесов, промышленности, выбросов N2O и CO2.")

#Как предатвродить потмепление
@bot.message_handler(commands=['prevent'])
def prevent(message):
    photo_3 = open("i.png", "rb")
    bot.send_photo(message.chat.id, photo_3, caption="Чтобы остановить глобальное потепление, нужно: 1.перейти на зеленую энергию: Солнце, ветер, вода вместо угля и нефти; 2.экологичный транспорт: Электромобили, велосипеды, общественный транспорт; 3.сажать леса; 4.Сортировать отходы; 5.сокращение пищевых отходов на всех этапах производства и потребления.")

#Нейронка по сортировке мусора
def ai_image():

    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("keras_model.h5", compile=False)

    # Load the labels
    class_names = open("labels.txt", "r", encoding='UTF-8').readlines()

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open("image.png").convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)
    return class_name[2:]


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('image.png', 'wb') as file:
        file.write(downloaded_file)
    name = ai_image()
    bot.reply_to(message, "Это:" + name)
    if name.strip() == "Стекло":
        bot.reply_to(message, "Как сортировать стекло? Сортировка стекла начинается с отделения его от других отходов. Затем необходимо разделить стекло по цветам: прозрачное, зеленое и тд. Удалите крышки, пробки и этикетки. Вымойте стекло, чтобы удалить остатки пищи и другие загрязнения. Разбейте крупные куски стекла только если это необходимо для удобства хранения и транспортировки. Поместите отсортированное стекло в специальные контейнеры для раздельного сбора отходов или сдайте в пункты приема вторсырья.")
    elif name.strip() == "Пластик":
        bot.reply_to(message, "Как сортировать пластик? Отделите перерабатываемый пластик от неперерабатываемого, опустошите и тщательно промойте контейнеры, удалите крышки и этикетки, если возможно, и сплющите их для экономии места. Поместите подготовленный пластик в контейнер для раздельного сбора. ")
    elif name.strip() == "Макулатура":
        bot.reply_to(message, "Как сортировать макулатуру? Сортировка макулатуры начинается с отделения бумаги от других отходов, исключая загрязненную пищей, жидкостями или жиром, а также ламинированную, вощеную или фольгированную бумагу, чеки, бумажные полотенца и туалетную бумагу. Подходящую макулатуру (газеты, журналы, картон, офисную бумагу, книги без твердых обложек) следует разделить на типы, если этого требует пункт приема, удалить скобы и скрепки, поместить в контейнер для раздельного сбора макулатуры или сдать в пункт приема вторсырья.")
    elif name.strip() == "Металл":
        bot.reply_to(message, "Как сортировать металл? Сортировка металла начинается с отделения металлических предметов от других отходов, затем необходимо разделить металлы на черные (чугун, сталь) и цветные (алюминий, медь, латунь). Очистите металлические предметы от остатков пищи, краски и других загрязнений, по возможности удалите пластиковые и другие неметаллические элементы. Сдавайте металл в специализированные пункты приема вторсырья или используйте контейнеры для раздельного сбора металла.")
    
        
#Запускаем бота 
bot.polling()
