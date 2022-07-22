# Speech recognizer
Проект, состоящий из телеграм и вконтакте ботов, призванных автоматизировать работу служб поддержки.

### Иллюстрация к проекту
![img.png](illustration/demo_vk_bot.gif)

### Как использовать

Для работы скрипта необходим установленный интерпретатор Python3. Затем загрузите зависимости с помощью "pip" (либо "pip3", в случае конфликтов с Python2):  

    pip install -r requirements.txt

### Переменные окружения
Создайте файл .env и разместите в нем следующие переменные окружения:
- <b>TELEGRAM_BOT_TOKEN</b>. Его можно получить, написав [Отцу ботов](https://telegram.me/BotFather)
- <b>TELEGRAM_ID</b>. Узнать можно у бота  <i>@username_to_id_bot</i> в Telegram
- <b>PROJECT_ID</b>. Для этого, сначала [создайте проект](https://cloud.google.com/dialogflow/docs/quick/setup) в Dialogflow.
- <b>GOOGLE_APPLICATION_CREDENTIALS</b>. Получить можно [здесь](https://cloud.google.com/docs/authentication/getting-started)
- <b>VK_BOT_TOKEN</b>. Этот токен  можно получить после создания группы вконтакте.

### Пример использования
Запустить одного из ботов можно с помощью соответствующих команд.
Телеграм:

    python telegram_bot.py

Вконтакте:

    python vk_bot.py

После запуска одного из ботов вам придёт уведомление в телеграм.

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).
