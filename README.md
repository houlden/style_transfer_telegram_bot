# Style Transfer Telegram Bot

В данном проекте реализована модульная структура асинхронного telegram-бота, предназначенного для нейронной стилизации изображений. Архитектура бота позволяет легко расширить его функционал дополнительными алгоритмами машинного обучения.

## Основные инструменты

***Бот:***

* [aiogram](https://docs.aiogram.dev/en/latest/)
* [asyncio](https://docs.python.org/3/library/asyncio.html)
* [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)

***Машинное обучение:***

* [PyTorch](https://pytorch.org/)

***Обработка изображений:***

* [Pillow](https://pypi.org/project/Pillow/)

## Архитектура бота

* `main.py` - точка входа в программу
* `config.py` - конфигуратор бота (содержит основные константы, получает переменные среды из `.env`)
* `.env` - файл с приватными переменными среды (token бота и т.п.)
* `bot_init.py` - инициализатор `aiogram.Bot`, `aiogram.Dispatcher`, `aiogram.contrib.fsm_storage.memory.MemoryStorage` для обеспечения доступа к ним из разных модулей
* `handlers` - пакет с обработчиками событий для пользователей разных групп (в настоящий момент только для `user`)
* `keyboards` - пакет с интерактивными клавиатурами (`standard` и `inline`)
* `ml_models` - пакет с различными моделями (в данный момент реализован только [алгоритм Гатиса](https://arxiv.org/abs/1508.06576))

## Запуск бота

Для работы бота необходимо добавить в окружение следующие переменные среды (или создать в корневой директории файл `.env`):

* *BOT_TOKEN=**your telegram bot token***
* *ADMIN_ID=**your telegram account ID***
* *WEBHOOK_URL=**your webhook url***
* *WEBHOOK_PATH=**your webhook path***
* *HOST=**your host***

## ML Models

### Neural Style Transfer (Gatys algorithm)

Пакетная реализация [алгоритма Гатиса](https://arxiv.org/abs/1508.06576) на основе кода из официального туториала [NEURAL TRANSFER USING PYTORCH](https://pytorch.org/tutorials/advanced/neural_style_tutorial.html).

Для переноса стиля используются первые 11 слоев предобученной VGG19 (`ml_models/nst_gatys/pretrained_models/vgg19_first_11_layers.pth`).

#### Примеры

![Результат переноса стиля](https://raw.githubusercontent.com/houlden/style_transfer_telegram_bot/main/examples/nst_gatys/results.jpg)

#### Архитектура

`ml_models.nst_gatys.*module_name*`

* `settings.py` - основные настройки модели вынесены в отдельный модуль
* `run_style_transfer.py` - модуль, запускающий перенос стиля
* `train_loop.py` - цикл оптимизации изображения
* `optimizer.py` - инициализация оптимизатора
* `build_style_transfer_model.py` - сбор модели для переноса стиля из предобученной сети и пользовательских слоев, реализующих подсчет style и content loss-ов
* `custom_layers.py` - модуль пользовательских слоев, реализующих подсчет loss-ов и нормализацию изображений
* `image_preparation.py` - модуль с функциями для преобразования изображений

## Дальнейшие планы

1. Добавить padding к изображениям, чтобы иметь возможность сохранения пропорций изначальной картинки в NST-Gatys.
2. Добавить возможность переноса нескольких стилей на одно изображение в NST-Gatys.
3. Добавить реализации [AdaIN](https://arxiv.org/abs/1703.06868) и [UltraST](https://arxiv.org/abs/2003.08436) для RealTime переноса стиля.
4. Добавить реализацию [CycleGAN](https://arxiv.org/abs/1703.10593).
5. Реализовать очередь обработки (в настоящий момент бот работает асинхронно, но запускает новую обработку вне зависимости от того, сколько процессов уже запущено - это может привести к зависанию).
6. Добавить логирование.
