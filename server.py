from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

# Базовая ссылка на ваш репозиторий (замените на ваш логин и название репозитория!)
GITHUB_BASE_URL = "https://raw.githubusercontent.com/Sergey-Shinkevich/Home_Work_6_Course/home_work/templates/"


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Словарь маршрутов
        routes = {"/": "contact.html", "/contact": "contact.html", "/403": "403.html", "/500": "500.html"}

        filename = routes.get(self.path)

        if filename:
            # Формируем полную ссылку на файл в GitHub
            url = GITHUB_BASE_URL + filename

            # Скачиваем содержимое через requests
            response = requests.get(url)

            if response.status_code == 200:
                self.send_response(200 if self.path in ["/", "/contact"] else (403 if self.path == "/403" else 500))
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(response.text.encode("utf-8"))
            else:
                self.send_error(500, "Не удалось загрузить страницу с GitHub")
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h1>404 Not Found</h1>".encode("utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer(("localhost", 8080), MyServer)
    print("Server started http://localhost:8080")
    webServer.serve_forever()
    print("Server stopped http://localhost:8080")
