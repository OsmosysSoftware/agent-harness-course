# Plan

Approved by: <your name>, <date>. Committed on its own, before any code.

## Goal
<one sentence from the brief>

## Slices (one commit each; tick when committed)
- [x] products: low-stock endpoint `GET /api/products/low-stock?threshold=` (tests: default 5, 400 on out-of-range, ordered by stock then SKU)
- [x] orders: history `GET /api/orders` newest first (tests: order, productId filter). Note: SQLite DateTimeOffset converter (docs/ai/conventions.md)
- [ ] <next slice>

## Decisions made by the human
- <date>: <problem> → chose <option> because <reason> (1-3-1)

## Changes to this plan
- <date>: <what changed and why> (committed as `docs(plan): …`)
