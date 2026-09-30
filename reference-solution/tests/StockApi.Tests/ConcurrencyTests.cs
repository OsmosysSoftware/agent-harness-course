using System.Net;
using System.Net.Http.Json;
using StockApi.Domain;

namespace StockApi.Tests;

public class ConcurrencyTests : IClassFixture<FileStockApiFactory>
{
    private readonly HttpClient _client;

    public ConcurrencyTests(FileStockApiFactory factory) => _client = factory.CreateClient();

    [Fact]
    public async Task PlaceOrder_TwelveConcurrentOrdersForThreeUnits_ExactlyThreeSucceed()
    {
        var product = await _client.CreateProductAsync("CONC-1", 3);

        // Hold every request at a gate and release them together so they really overlap.
        var gate = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
        var inFlight = Enumerable.Range(0, 12).Select(_ => Task.Run(async () =>
        {
            await gate.Task;
            return await _client.PostAsJsonAsync("/api/orders", new { productId = product.Id, quantity = 1 });
        })).ToList();
        gate.SetResult();
        var responses = await Task.WhenAll(inFlight);

        Assert.Equal(3, responses.Count(r => r.StatusCode == HttpStatusCode.Created));
        Assert.Equal(9, responses.Count(r => r.StatusCode == HttpStatusCode.Conflict));
        var after = await _client.GetFromJsonAsync<Product>($"/api/products/{product.Id}");
        Assert.Equal(0, after!.Stock);
    }
}
