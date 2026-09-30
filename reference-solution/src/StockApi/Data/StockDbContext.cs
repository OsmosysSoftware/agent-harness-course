using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using StockApi.Domain;

namespace StockApi.Data;

public class StockDbContext(DbContextOptions<StockDbContext> options) : DbContext(options)
{
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Order> Orders => Set<Order>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Product>().HasIndex(p => p.Sku).IsUnique();

        // SQLite can't ORDER BY DateTimeOffset; see docs/ai/conventions.md
        modelBuilder.Entity<Order>().Property(o => o.CreatedAt).HasConversion(new DateTimeOffsetToBinaryConverter());
    }
}
