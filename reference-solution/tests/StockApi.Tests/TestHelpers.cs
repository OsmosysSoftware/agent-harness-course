using System.Net;
using System.Net.Http.Json;
using StockApi.Domain;

namespace StockApi.Tests;

internal static class TestHelpers
{
    public static async Task<Product> CreateProductAsync(this HttpClient client, string sku, int stock)
    {
        var response = await client.PostAsJsonAsync("/api/products", new { sku, name = $"Product {sku}", stock });
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        return (await response.Content.ReadFromJsonAsync<Product>())!;
    }
}
