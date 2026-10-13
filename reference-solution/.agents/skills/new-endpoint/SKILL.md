---
name: new-endpoint
description: Add a new endpoint or resource by copying the reference shape (ProductsController and its tests). Use when a plan slice adds or changes an HTTP endpoint.
---

# New endpoint

The reference shape is `src/StockApi/Controllers/ProductsController.cs` plus
`tests/StockApi.Tests/ProductsTests.cs`. Read both first, then copy their shape. Do not invent a new one.

1. **Tests first**: add the failing integration tests to the reference test file, in its shape, using
   `StockApiFactory`: the happy path, 404, 409 and 400. If the endpoint changes stock, also add a case to
   `ConcurrencyTests`. Run them and show they fail for the right reason.
2. **Controller**: validate the input and map results to 200/201/404/409 `ProblemDetails`. Simple reads and
   creates may use `StockDbContext` directly, as `ProductsController` does; anything that changes stock calls a service.
3. **Service**: rules and transactions. Any stock change follows docs/ai/invariants.md (one guarded UPDATE).
4. **DTOs**: `record` request types next to the controller. Responses may return the entity, as `ProductsController`
   does; add a response record only when the entity would leak something.
5. **Check**: unless the `ship-slice` skill called this one (it runs these steps itself), run the `quality-gate`
   skill, then ask for a review by `test-reviewer`, plus `stock-invariant-reviewer` if stock changed.
