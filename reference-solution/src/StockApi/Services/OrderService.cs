using Microsoft.EntityFrameworkCore;
using StockApi.Data;
using StockApi.Domain;

namespace StockApi.Services;

public enum PlaceOrderStatus { Created, ProductNotFound, InsufficientStock }

public record PlaceOrderResult(PlaceOrderStatus Status, Order? Order = null);

public class OrderService(StockDbContext db)
{
    public async Task<PlaceOrderResult> PlaceAsync(int productId, int quantity, CancellationToken ct = default)
    {
        await using var tx = await db.Database.BeginTransactionAsync(ct);

        // Atomic guarded UPDATE, never read-then-write: see docs/decisions/0001.
        var updated = await db.Products
            .Where(p => p.Id == productId && p.Stock >= quantity)
            .ExecuteUpdateAsync(s => s.SetProperty(p => p.Stock, p => p.Stock - quantity), ct);

        if (updated == 0)
        {
            var exists = await db.Products.AnyAsync(p => p.Id == productId, ct);
            return new PlaceOrderResult(exists ? PlaceOrderStatus.InsufficientStock : PlaceOrderStatus.ProductNotFound);
        }

        var order = new Order { ProductId = productId, Quantity = quantity, CreatedAt = DateTimeOffset.UtcNow };
        db.Orders.Add(order);
        await db.SaveChangesAsync(ct);
        await tx.CommitAsync(ct);

        return new PlaceOrderResult(PlaceOrderStatus.Created, order);
    }
}
