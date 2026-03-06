using Dapr.Workflow;

namespace CatalystAspireApp.ApiService;

public class FirstActivity : WorkflowActivity<FirstActivity.Input, FirstActivity.Output>
{
    public record Input
    {
        public required int Left { get; init; }
        public required int Right { get; init; }
    }

    public record Output
    {
        public required int Sum { get; init; }
    }

    public override async Task<Output> RunAsync(WorkflowActivityContext context, Input input)
    {
        return new()
        {
            Sum = input.Left + input.Right,
        };
    }
}