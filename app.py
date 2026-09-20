from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
from uuid import uuid4

PORT = 8081
STORE = Path(__file__).with_name("expenses.json")


def load_expenses():
    if not STORE.exists():
        return []
    return json.loads(STORE.read_text(encoding="utf-8"))


def save_expenses(expenses):
    STORE.write_text(json.dumps(expenses, indent=2, ensure_ascii=False), encoding="utf-8")


class ExpenseHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            return self.send_json(200, {"status": "ok", "service": "expense-api"})
        if self.path == "/expenses":
            return self.send_json(200, load_expenses())
        self.send_json(404, {"error": "Ruta no encontrada"})

    def do_POST(self):
        if self.path != "/expenses":
            return self.send_json(404, {"error": "Ruta no encontrada"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or b"{}")
            description = str(data.get("description", "")).strip()
            amount = float(data.get("amount", 0))
            if not description or amount <= 0:
                raise ValueError("description y amount positivo son obligatorios")
            expenses = load_expenses()
            expense = {"id": str(uuid4()), "description": description,
                       "amount": round(amount, 2), "category": data.get("category", "general")}
            expenses.append(expense)
            save_expenses(expenses)
            self.send_json(201, expense)
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self.send_json(400, {"error": str(error)})

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


if __name__ == "__main__":
    print(f"Expense API escuchando en http://localhost:{PORT}")
    HTTPServer(("localhost", PORT), ExpenseHandler).serve_forever()
