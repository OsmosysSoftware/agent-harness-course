# StockApi — Product Brief

StockApi — a tiny inventory service. Products have a unique SKU and a stock count. Placing an order reserves stock.

**Invariant:** stock never goes below zero, even under concurrent orders — N concurrent orders for a product with S units must produce at most S successful units.

**Out of scope:** authentication, UI, payments.

**Stack:** .NET 8, ASP.NET Core controllers, EF Core + SQLite, xUnit.
