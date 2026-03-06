using Dapr.Workflow;

namespace CatalystAspireApp.ApiService;

public class FirstWorkflow : Workflow<FirstWorkflow.Input, FirstWorkflow.Output>
{
    public record Input
    {
        public required int Left { get; init; }
        public required int Right { get; init; }
    }

    public record Output
    {
        public required int Value { get; init; }
    }

    public override async Task<Output> RunAsync(WorkflowContext context, Input input)
    {
        var firstActivityResult = await context.CallActivityAsync<FirstActivity.Output>(
            nameof(FirstActivity), 
            new FirstActivity.Input
            {
                Left = input.Left,
                Right = input.Right,
            });

        await context.CreateTimer(TimeSpan.FromSeconds(3));
        
        var secondActivityResult = await context.CallActivityAsync<SecondActivity.Output>(
            nameof(SecondActivity),
            new SecondActivity.Input
            {
                Value = firstActivityResult.Sum,
            });
        
        return new()
        {
            Value = secondActivityResult.Value,
        };
    }
}