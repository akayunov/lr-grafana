from aiohttp import web


async def handle_post(request):
    try:
        # Пытаемся получить данные в формате JSON
        data = await request.json()
        print(f"Получены данные: {data}")

        # Логика обработки...
        response_data = {
            "status": "success",
            "received": data
        }
        return web.json_response(response_data, status=200)

    except Exception as e:
        # Если пришел не JSON или произошла ошибка
        return web.json_response({"error": str(e)}, status=400)


app = web.Application()
# Регистрируем маршрут для POST запроса
app.add_routes([web.post('', handle_post)])

if __name__ == '__main__':
    print("Сервер запущен на http://localhost:8808")
    web.run_app(app, host='0.0.0.0', port=8808)