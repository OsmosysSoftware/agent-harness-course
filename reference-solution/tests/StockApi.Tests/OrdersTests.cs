using System.Net;
using System.Net.Http.Json;
using StockApi.Domain;

namespace StockApi.Tests;

public class OrdersTests : IClassFixture<StockApiFactory>
{
    private readonly HttpClient _client;

    public OrdersTests(StockApiFactory factory) => _client = factory.CreateClient();

    [Fact]
    public async Task PlaceOrder_SufficientStock_Returns201AndDecrementsStock()
    {
        var product = await _client.CreateProductAsync("ORDER-OK", 10);

        var response = await _client.PostAsJsonAsync("/api/orders", new { productId = product.Id, quantity = 3 });

        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        var after = await _client.GetFromJsonAsync<Product>($"/api/products/{product.Id}");
        Assert.Equal(7, after!.Stock);
    }

    [Fact]
    public async Task PlaceOrder_InsufficientStock_Returns409AndKeepsStock()
    {
        var product = await _client.CreateProductAsync("ORDER-LOW", 2);

        var response = await _client.PostAsJsonAsync("/api/orders", new { productId = product.Id, quantity = 3 });

        Assert.Equal(HttpStatusCode.Conflict, response.StatusCode);
        var after = await _client.GetFromJsonAsync<Product>($"/api/products/{product.Id}");
        Assert.Equal(2, after!.Stock);
    }

    [Fact]
    public async Task PlaceOrder_MissingProduct_Returns404()
    {
        var response = await _client.PostAsJsonAsync("/api/orders", new { productId = 999_999, quantity = 1 });

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }

    [Fact]
    public async Task PlaceOrder_ZeroQuantity_Returns400AndKeepsStock()
    {
        var product = await _client.CreateProductAsync("ORDER-ZERO", 4);

        var response = await _client.PostAsJsonAsync("/api/orders", new { productId = product.Id, quantity = 0 });

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        var after = await _client.GetFromJsonAsync<Product>($"/api/products/{product.Id}");
        Assert.Equal(4, after!.Stock);
    }

    [Fact]
    public async Task ListOrders_MultipleOrders_ReturnsNewestFirst()
    {
        var product = await _client.CreateProductAsync("HIST-ORDER", 10);
        var first = await PlaceAsync(product.Id, 1);
        var second = await PlaceAsync(product.Id, 1);
        var third = await PlaceAsync(product.Id, 1);

        var orders = await _client.GetFromJsonAsync<List<Order>>($"/api/orders?productId={product.Id}");

        Assert.Equal([third.Id, second.Id, first.Id], orders!.Select(o => o.Id));
    }

    [Fact]
    public async Task ListOrders_FilteredByProduct_ReturnsOnlyThatProductsOrders()
    {
        var a = await _client.CreateProductAsync("HIST-A", 5);
        var b = await _client.CreateProductAsync("HIST-B", 5);
        var orderA = await PlaceAsync(a.Id, 1);
        await PlaceAsync(b.Id, 1);

        var orders = await _client.GetFromJsonAsync<List<Order>>($"/api/orders?productId={a.Id}");

        Assert.Equal([orderA.Id], orders!.Select(o => o.Id));
    }

    private async Task<Order> PlaceAsync(int productId, int quantity)
    {
        var response = await _client.PostAsJsonAsync("/api/orders", new { productId, quantity });
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        return (await response.Content.ReadFromJsonAsync<Order>())!;
    }
}
