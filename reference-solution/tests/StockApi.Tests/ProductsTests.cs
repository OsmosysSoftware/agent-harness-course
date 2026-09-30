using System.Net;
using System.Net.Http.Json;
using StockApi.Domain;

namespace StockApi.Tests;

public class ProductsTests : IClassFixture<StockApiFactory>
{
    private readonly HttpClient _client;

    public ProductsTests(StockApiFactory factory) => _client = factory.CreateClient();

    [Fact]
    public async Task CreateProduct_ThenGet_ReturnsIt()
    {
        var created = await _client.CreateProductAsync("CREATE-1", 5);

        var response = await _client.GetAsync($"/api/products/{created.Id}");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var fetched = await response.Content.ReadFromJsonAsync<Product>();
        Assert.Equal("CREATE-1", fetched!.Sku);
        Assert.Equal(5, fetched.Stock);
    }

    [Fact]
    public async Task CreateProduct_DuplicateSku_Returns409()
    {
        await _client.CreateProductAsync("DUP-1", 1);

        var response = await _client.PostAsJsonAsync("/api/products", new { sku = "DUP-1", name = "Again", stock = 1 });

        Assert.Equal(HttpStatusCode.Conflict, response.StatusCode);
    }

    [Fact]
    public async Task LowStock_DefaultThreshold_ReturnsProductsAtOrBelowFiveOrderedByStockThenSku()
    {
        await _client.CreateProductAsync("LS-D-HIGH", 6);
        await _client.CreateProductAsync("LS-D-B", 2);
        await _client.CreateProductAsync("LS-D-A", 2);
        await _client.CreateProductAsync("LS-D-EDGE", 5);

        var products = await _client.GetFromJsonAsync<List<Product>>("/api/products/low-stock");

        var ours = products!.Where(p => p.Sku.StartsWith("LS-D-")).Select(p => p.Sku);
        Assert.Equal(["LS-D-A", "LS-D-B", "LS-D-EDGE"], ours);
    }

    [Fact]
    public async Task LowStock_CustomThreshold_ReturnsOnlyProductsAtOrBelowIt()
    {
        await _client.CreateProductAsync("LS-C-0", 0);
        await _client.CreateProductAsync("LS-C-1", 1);
        await _client.CreateProductAsync("LS-C-2", 2);

        var products = await _client.GetFromJsonAsync<List<Product>>("/api/products/low-stock?threshold=1");

        var ours = products!.Where(p => p.Sku.StartsWith("LS-C-")).Select(p => p.Sku);
        Assert.Equal(["LS-C-0", "LS-C-1"], ours);
    }

    [Theory]
    [InlineData(-1)]
    [InlineData(1001)]
    public async Task LowStock_ThresholdOutOfRange_Returns400(int threshold)
    {
        var response = await _client.GetAsync($"/api/products/low-stock?threshold={threshold}");

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }
}
