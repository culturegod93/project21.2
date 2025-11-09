from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
from urllib.parse import parse_qs


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обработка GET-запросов"""
        # Всегда возвращаем страницу контактов
        try:
            with open('contacts.html', 'rb') as file:
                content = file.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def do_POST(self):
        """Обработка POST-запросов (дополнительное задание)"""
        # Получаем длину тела запроса
        content_length = int(self.headers['Content-Length'])
        # Читаем тело запроса
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Парсим данные формы
        parsed_data = parse_qs(post_data)

        # Печатаем данные в консоль
        print("=" * 50)
        print("Получены POST-данные:")
        for key, value in parsed_data.items():
            print(f"{key}: {value[0]}")
        print("=" * 50)

        # Отправляем ответ
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # Создаем простую страницу ответа
        response_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Спасибо!</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="alert alert-success">
                    <h2>Спасибо за ваше сообщение!</h2>
                    <p>Мы получили ваши данные и скоро свяжемся с вами.</p>
                    <a href="/" class="btn btn-primary">Вернуться на главную</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(response_html.encode('utf-8'))


def run_server():
    """Запуск сервера"""
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Сервер запущен на http://localhost:8000")
    print("Для остановки сервера нажмите Ctrl+C")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()
