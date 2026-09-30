using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StockApi.Data;
using StockApi.Domain;
using StockApi.Services;

namespace StockApi.Controllers;

public record PlaceOrderRequest(
    int ProductId,
    [Range(1, int.MaxValue)] int Quantity);

[ApiController]
[Route("api/orders")]
public class OrdersController(OrderService orders, StockDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<List<Order>> List([FromQuery] int? productId, CancellationToken ct) =>
        await db.Orders.AsNoTracking()
            .Where(o => productId == null || o.ProductId == productId)
            .OrderByDescending(o => o.CreatedAt)
            .ToListAsync(ct);

    [HttpPost]
    public async Task<ActionResult<Order>> Place(PlaceOrderRequest request, CancellationToken ct)
    {
        var result = await orders.PlaceAsync(request.ProductId, request.Quantity, ct);
        return result.Status switch
        {
            PlaceOrderStatus.Created => Created($"/api/orders/{result.Order!.Id}", result.Order),
            PlaceOrderStatus.ProductNotFound => NotFound(new ProblemDetails
            {
                Title = "Product not found",
                Status = StatusCodes.Status404NotFound
            }),
            _ => Conflict(new ProblemDetails
            {
                Title = "Insufficient stock",
                Status = StatusCodes.Status409Conflict
            })
        };
    }
}
