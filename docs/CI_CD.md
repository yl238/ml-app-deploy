# CI/CD Pipeline

## Core concepts

### Single Source Repository

<img src="figures/CI1-Branching_2.png" width=800>
Git branching

### Automating the Build

<img src="figures/CI1-BreakingChange.png" width=800>

### Automated Testing

* Cover every new function with a unit test

### Use an External Continuous Integration Service

<img src="figures/CI-Testing_1.png" width=800>

### Testing in a Stagin Environment

The development environment should replicate production conditions as closely as possible. This setup is often called *DEV/PROD parity*. Keep the environment on your local computer as similar as possible to the DEV and PROD environments to minimize anomalies when deploying applications.

<img src="figures/DEV_PROD_2_2.png" width=800>