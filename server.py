from http.server import BaseHTTPRequestHandler, HTTPServer


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        # Определяем пути для страниц
        routes = {
            "/": "templates/contact.html",
            "/contact": "templates/contact.html",
            "/403": "templates/403.html",
            "/500": "templates/500.html",
        }

        # Получаем путь, если его нет в списке — считаем, что это ошибка
        file_path = routes.get(self.path)

        if file_path:
            self.send_response(200 if self.path in ["/", "/contact"] else (403 if self.path == "/403" else 500))
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open(file_path, "r", encoding="utf-8") as file:
                self.wfile.write(file.read().encode("utf-8"))
        else:
            # Если страница не найдена, просто вернем 404
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")


if __name__ == "__main__":
    webServer = HTTPServer(("localhost", 8080), MyServer)
    print("Server started http://localhost:8080")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped http://localhost:8080")
