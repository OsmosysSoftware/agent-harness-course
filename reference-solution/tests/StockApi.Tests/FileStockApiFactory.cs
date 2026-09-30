using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using StockApi.Data;

namespace StockApi.Tests;

/// <summary>Real SQLite on a unique temp file: a shared in-memory connection is not thread-safe, so concurrency tests need a file.</summary>
public class FileStockApiFactory : WebApplicationFactory<Program>
{
    private readonly string _path = Path.Combine(Path.GetTempPath(), $"stockapi-{Guid.NewGuid():N}.db");

    protected override void ConfigureWebHost(IWebHostBuilder builder) =>
        builder.ConfigureServices(services =>
        {
            var existing = services.Single(d => d.ServiceType == typeof(DbContextOptions<StockDbContext>));
            services.Remove(existing);
            services.AddDbContext<StockDbContext>(o => o.UseSqlite($"Data Source={_path};Default Timeout=30"));
        });

    protected override void Dispose(bool disposing)
    {
        base.Dispose(disposing);
        if (!disposing) return;
        Microsoft.Data.Sqlite.SqliteConnection.ClearAllPools();
        foreach (var suffix in new[] { "", "-wal", "-shm" })
            File.Delete(_path + suffix);
    }
}
