# Cloud SQL Best Practices with Python

This repository demonstrates best practices and different approaches for deploying Python services on Google Cloud and connecting them securely to Cloud SQL. It covers three common deployment scenarios:

- **Cloud Functions (Gen 1)**
- **Cloud Functions (Gen 2)**
- **Cloud Run**

## Project Structure

- **`run-functions/python-example`**: Contains the Python code for the example application.
  - `app.py`: Flask app for Cloud Run deployment.
  - `main.py`: Entry point for Cloud Functions deployments.
  - `db_helper.py`: Helper functions for connecting to Cloud SQL and interacting with the database.
  - `utils.py`: Utility functions, including accessing secrets from Secret Manager.

## Best Practices Demonstrated

- **Securely storing credentials**: Using Google Cloud Secret Manager to store database credentials instead of hardcoding them.
- **Connection pooling**: Utilizing SQLAlchemy's connection pooling mechanism to improve performance and resource utilization.
- **IAM authentication**: Connecting to Cloud SQL using IAM authentication for enhanced security.
- **Private IP connectivity**: Configuring services to connect to Cloud SQL using private IP addresses for improved security and reduced latency.
- **Environment-based configuration**: Using environment variables to configure application settings for different environments.
- **Connection Limits and Pools**: Implementing best practices for managing database connections in Cloud Functions and Cloud Run, including connection limits and connection pools.

## Optimizing for Cold Starts and Latency

This project also demonstrates techniques for minimizing cold starts and reducing latency in Cloud Run and Cloud Functions:
- **Startup CPU Boost**: Enable startup CPU boost to decrease instance startup time.
- **Minimum Instances**: Configure minimum instances to ensure your service is always ready to handle requests, minimizing cold starts.
- **Global Variables**: Leverage global variables to preserve state between invocations within the same instance.

## Key Concepts

- **Cloud SQL**: A fully managed relational database service on Google Cloud.
- **Cloud Functions**: A serverless compute platform for building event-driven applications.
- **Cloud Run**: A fully managed serverless platform for deploying containerized applications.
- **Secret Manager**: A secure and convenient service for storing API keys, passwords, and other sensitive data.
- **IAM**: Identity and Access Management, Google Cloud's identity and access control system.
- **Pub/Sub**: A real-time messaging service that allows you to send and receive messages between independent applications.
- **Cloud Build**: A serverless CI/CD platform that lets you build, test, and deploy applications on Google Cloud.

## Comparison Tables


### Cloud Functions (Gen 1) vs. Cloud Run Functions (Gen 2)

| Feature | Cloud Run functions (1st gen) | Cloud Run functions |
|---|---|---|
| Image registry | Container Registry or Artifact Registry | Artifact Registry only |
| Request timeout | Up to 9 minutes | Up to 60 minutes for HTTP-triggered functions<br>Up to 9 minutes for event-triggered functions |
| Instance size | Up to 8GB RAM with 2 vCPU | Up to 16GiB RAM with 4 vCPU |
| Concurrency | 1 concurrent request per function instance | Up to 1000 concurrent requests per function instance |
| Traffic splitting | Not supported | Supported |
| Event types | Direct support for events from 7 sources | Support for any event type supported by Eventarc, including 90+ event sources via Cloud Audit Logs |
| CloudEvents | Supported only in Ruby, .NET, and PHP runtimes | Supported in all language runtimes |

### Cloud Functions vs. Cloud Run

| Feature | Cloud Functions | Cloud Run |
|---|---|---|
| Deployment | Function code | Container image |
| Scaling | Automatic and scales to zero | Automatic and can be configured with minimum instances |
| Cold starts | More likely, especially with Gen 1 | Less likely with minimum instances and optimized containers |
| Networking | VPC connector | Direct VPC egress, Serverless VPC Access connector, or public internet |
| Ingress | Public or internal (Gen 2) | Public or internal |
| Trigger types | HTTP, Pub/Sub, Storage, Firestore, etc. | HTTP, Pub/Sub (with internal ingress), and other events via Eventarc |
| Connection Pooling | Limited to 1 connection | Can have larger connection pools (e.g., 100) |
| Execution Environment | Managed by Google | More control over the container environment |

### Direct VPC Egress vs. Serverless VPC Access Connector

| Feature | Direct VPC egress | Serverless VPC Access connector |
|---|---|---|
| Latency | Lower | Higher |
| Throughput | Higher | Lower |
| IP allocation | Uses more IP addresses in most cases | Uses fewer IP addresses |
| Cost | No additional VM charges | Incurs additional VM charges |
| Scaling speed | Instance autoscaling is slower during traffic surges while new VPC network interfaces are created. | Network latency occurs during VPC network traffic surges while more connector instances are created. |
| Network tags | Finer granularity. Each service or job can have its own unique sets of tags; firewall rules applied separately. | Less granularity. Shared across services and jobs that use the same connectors; firewall rules applied at the connector level. |
| Google Cloud console | Supported | Supported |
| Google Cloud CLI | Supported | Supported |
| Launch stage | GA (with the exception of Cloud Run jobs) | GA |

## Getting Started

1. **Clone this repository**: `git clone https://github.com/deyvidm18/cloudsql-best-practices.git`
2. **Set up your Google Cloud project**: Create a new project or use an existing one.
3. **Enable necessary APIs**: Enable the Cloud SQL Admin API, Secret Manager API, Cloud Functions API (if applicable), and Cloud Run API (if applicable).
4. **Create a Cloud SQL instance**: Create a new Cloud SQL instance for your database.
5. **Store your database credentials in Secret Manager**: Create a new secret in Secret Manager and store your database connection details.
6. **Deploy your Python services**: This project is set up for automated deployment using Cloud Build and is triggered by GitHub. The `cloudbuild.yaml` file defines the deployment process for three services:
    - **Cloud Run**: Deploys a containerized Flask app with private VPC egress enabled, restricting outbound traffic to specific IP ranges. It also configures the service to use a specific subnet and allows only internal traffic. The Cloud Run service utilizes a connection pool with a larger size (e.g., 100 connections) to handle multiple concurrent requests efficiently.
    - **Cloud Functions (Gen 1):** Deploys a Gen 1 Cloud Function with a specified service account, VPC connector, and ingress settings. Due to the nature of Cloud Functions and their scaling model, the connection pool for this service is limited to a single connection to prevent exceeding Cloud SQL connection limits.
    - **Cloud Functions (Gen 2):** Deploys a Gen 2 Cloud Function with similar configurations as the Gen 1 function, also employing a connection pool limited to one connection.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.
