# CatalystAspireApp

An Aspire starter application with a Dapr workflow. This solution demonstrates how to use [Dapr Workflow](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-overview/) with  Aspire orchestration. It provides a starting point to add the [Catalyst Aspire integration](https://github.com/diagrid-labs/catalyst-aspire) to run workflows managed by Diagrid Catalyst.

The application consists of:

- **AppHost** — The Aspire orchestrator that configures Dapr sidecars, a Valkey state store, and the Diagrid dashboard.
- **ApiService** — A web API that registers and runs a Dapr workflow (`FirstWorkflow`) with two activities (`FirstActivity` and `SecondActivity`).
- **Web** — A Blazor frontend that connects to the API service.
- **ServiceDefaults** — Shared service configuration (OpenTelemetry, health checks, service discovery).

## Prerequisites

For running this locally with Dapr you need:
- A container runtime such as [Docker Desktop](https://www.docker.com/products/docker-desktop) or [Podman](https://podman.io/)
- [.NET 10](https://dotnet.microsoft.com/en-us/download)
- [Aspire CLI](https://aspire.dev/get-started/install-cli/)
- [Dapr](https://docs.dapr.io/getting-started/install-dapr-cli/)

For adding the Catalyst Aspire integration, you'll need:
- [A Diagrid Catalyst account](https://www.diagrid.io/catalyst)
- [Diagrid CLI](/references/catalyst/catalyst-cli-intro)

## Running the application

```bash
aspire run
```

![Aspire Traces](img/dotnet-aspire-traces.png)

![Aspire Resources](img/dotnet-aspire-resources.png)

![Diagrid Dev Dashboard](img/diagrid-dev-dashboard.png)
