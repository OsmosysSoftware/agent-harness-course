---
name: new-endpoint
description: Add a new endpoint or resource by copying the reference shape (ProductsController and its tests). Use when a plan slice adds or changes an HTTP endpoint.
---

# New endpoint

The reference shape is `src/StockApi/Controllers/ProductsController.cs` plus
`tests/StockApi.Tests/ProductsTests.cs`. Read both first, then copy their shape. Do not invent a new one.

1. **Controller**: HTTP only. Validate the input, call a service, and map the result to 200/201/404/409 `ProblemDetails`.
   No `DbContext` in controllers except for simple reads that match `ProductsController`.
2. **Service**: rules and transactions. Any stock change follows docs/ai/invariants.md (one guarded UPDATE).
3. **DTOs**: `record` request and response types next to the controller; never return entities.
4. **Tests first**: add the failing integration tests in `tests/StockApi.Tests/<Resource>Tests.cs` using
   `StockApiFactory`: the happy path, 404, 409 and 400. If the endpoint changes stock, also add a case to
   `ConcurrencyTests`.
5. Run the `quality-gate` skill. Then ask for a review by `test-reviewer`, plus `stock-invariant-reviewer`
   if stock changed.
