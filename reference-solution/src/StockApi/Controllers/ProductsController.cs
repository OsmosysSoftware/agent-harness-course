using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StockApi.Data;
using StockApi.Domain;

namespace StockApi.Controllers;

public record CreateProductRequest(
    [Required] string Sku,
    [Required] string Name,
    [Range(0, int.MaxValue)] int Stock);

[ApiController]
[Route("api/products")]
public class ProductsController(StockDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<List<Product>> List(CancellationToken ct) =>
        await db.Products.AsNoTracking().OrderBy(p => p.Id).ToListAsync(ct);

    [HttpGet("low-stock")]
    public async Task<List<Product>> LowStock([Range(0, 1000)] int threshold = 5, CancellationToken ct = default) =>
        await db.Products.AsNoTracking()
            .Where(p => p.Stock <= threshold)
            .OrderBy(p => p.Stock).ThenBy(p => p.Sku)
            .ToListAsync(ct);

    [HttpGet("{id:int}")]
    public async Task<ActionResult<Product>> Get(int id, CancellationToken ct)
    {
        var product = await db.Products.AsNoTracking().FirstOrDefaultAsync(p => p.Id == id, ct);
        return product is null ? NotFound() : product;
    }

    [HttpPost]
    public async Task<ActionResult<Product>> Create(CreateProductRequest request, CancellationToken ct)
    {
        if (await db.Products.AnyAsync(p => p.Sku == request.Sku, ct))
            return Conflict(new ProblemDetails { Title = "SKU already exists", Status = StatusCodes.Status409Conflict });

        var product = new Product { Sku = request.Sku, Name = request.Name, Stock = request.Stock };
        db.Products.Add(product);
        try
        {
            await db.SaveChangesAsync(ct);
        }
        catch (DbUpdateException)
        {
            // Lost a race against the unique index on Sku.
            return Conflict(new ProblemDetails { Title = "SKU already exists", Status = StatusCodes.Status409Conflict });
        }

        return CreatedAtAction(nameof(Get), new { id = product.Id }, product);
    }
}
