using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using StockApi.Data;

namespace StockApi.Tests;

/// <summary>Real SQLite in memory: one shared open connection keeps the database alive for the factory's lifetime.</summary>
public class StockApiFactory : WebApplicationFactory<Program>
{
    private readonly SqliteConnection _connection = new("Filename=:memory:");

    public StockApiFactory() => _connection.Open();

    protected override void ConfigureWebHost(IWebHostBuilder builder) =>
        builder.ConfigureServices(services =>
        {
            var existing = services.Single(d => d.ServiceType == typeof(DbContextOptions<StockDbContext>));
            services.Remove(existing);
            services.AddDbContext<StockDbContext>(o => o.UseSqlite(_connection));
        });

    protected override void Dispose(bool disposing)
    {
        base.Dispose(disposing);
        if (disposing) _connection.Dispose();
    }
}
