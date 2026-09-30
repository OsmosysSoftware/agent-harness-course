using Microsoft.EntityFrameworkCore;
using StockApi.Data;
using StockApi.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddProblemDetails();
builder.Services.AddDbContext<StockDbContext>(o =>
    o.UseSqlite(builder.Configuration.GetConnectionString("Stock")));
builder.Services.AddScoped<OrderService>();

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    scope.ServiceProvider.GetRequiredService<StockDbContext>().Database.EnsureCreated();
}

app.UseExceptionHandler();
app.UseStatusCodePages();
app.MapControllers();

app.Run();

public partial class Program { }
