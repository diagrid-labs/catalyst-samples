using Diagrid.Aspire.Hosting.Catalyst;
using Microsoft.AspNetCore.Components.Authorization;

var builder = DistributedApplication.CreateBuilder(args);

var catalystProject = builder.AddCatalystProject("catalyst-aspire")
    .WithCatalystKvStore();

var apiService = builder.AddProject<Projects.CatalystAspireApp_ApiService>("apiservice")
    .WithCatalyst(catalystProject);

builder.AddProject<Projects.CatalystAspireApp_Web>("webfrontend")
    .WithExternalHttpEndpoints()
    .WithHttpHealthCheck("/health")
    .WithReference(apiService)
    .WaitFor(apiService);

builder.Build().Run();