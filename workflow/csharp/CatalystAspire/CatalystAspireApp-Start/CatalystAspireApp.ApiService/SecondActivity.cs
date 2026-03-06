using Dapr.Workflow;

namespace CatalystAspireApp.ApiService;

public class SecondActivity : WorkflowActivity<SecondActivity.Input, SecondActivity.Output>
{
    public record Input
    {
        public required int Value { get; init; }
    }

    public record Output
    {
        public required int Value { get; init; }
    }

    public override async Task<Output> RunAsync(WorkflowActivityContext context, Input input)
    {
        return new()
        {
            Value = input.Value * 1000,
        };
    }
}