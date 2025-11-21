import time
import logging
logger = logging.getLogger("api")


class RequestTimerMiddleware:
    def __init__(self, get_response):
        # вызывается один раз при старте сервера
        logger.info("Сервер запущен, RequestTimerMiddleware инициализирован")
        self.get_response = get_response

    def __call__(self, request):
        # вызывается при каждом запросе
        logger.info(f"Запрос пришёл: {request.path}")

        # передаём запрос дальше
        response = self.get_response(request)

        # выполняем что-то после обработки view
        logger.info(f"Ответ готов: {response.status_code}")

        # возвращаем ответ пользователю
        return response
