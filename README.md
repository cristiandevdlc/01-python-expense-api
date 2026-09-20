# Python Expense API

API REST pequeña para registrar gastos sin dependencias externas.

```powershell
python app.py
curl http://localhost:8081/expenses
curl -X POST http://localhost:8081/expenses -H "Content-Type: application/json" -d '{"description":"Dominio","amount":25.5,"category":"software"}'
```

Persistencia local en `expenses.json`. Siguiente mejora: autenticación y base de datos.
