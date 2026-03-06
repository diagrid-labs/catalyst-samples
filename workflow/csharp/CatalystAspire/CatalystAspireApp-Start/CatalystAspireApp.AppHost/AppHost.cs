using System.Reflection;
using CommunityToolkit.Aspire.Hosting.Dapr;
using Microsoft.AspNetCore.Components.Authorization;

var builder = DistributedApplication.CreateBuilder(args);

builder.AddDapr();

string executingPath = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) ?? throw new("Where am I?");

var cachePassword = builder.AddParameter("cache-password", "zxczxc123", secret: true);
var cache = builder
    .AddValkey("cache", 16379, cachePassword)
    .WithContainerName("workflow-state")
    .WithDataVolume("workflow-state-data")
    ;

var apiService = builder.AddProject<Projects.CatalystAspireApp_ApiService>("apiservice")
    .WithDaprSidecar(new DaprSidecarOptions
        {
            LogLevel = "debug",
            ResourcesPaths =
            [
                Path.Join(executingPath, "Resources"),
            ],
        }
    );

apiService.WaitFor(cache);

builder
    .AddContainer("diagrid-dashboard", "ghcr.io/diagridio/diagrid-dashboard:latest")
    .WithContainerName("diagrid-dashboard")
    .WithBindMount(Path.Join(executingPath, "Resources"), "/app/components")
    .WithEnvironment("COMPONENT_FILE", "/app/components/statestore-dashboard.yaml")
    .WithEnvironment("APP_ID", "diagrid-dashboard")
    .WithHttpEndpoint(targetPort: 8080)
    .WithReference(cache)
    ;


builder.AddProject<Projects.CatalystAspireApp_Web>("webfrontend")
    .WithExternalHttpEndpoints()
    .WithHttpHealthCheck("/health")
    .WithReference(apiService)
    .WaitFor(apiService);

builder.Build().Run();
