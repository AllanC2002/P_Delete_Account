# Project: User Account Management Service

This service provides functionality for managing user accounts, specifically focusing on account deletion. It is built using Python with the Flask framework and interacts with MySQL databases.

## Table of Contents

- [Project Overview](#project-overview)
- [Folder Structure](#folder-structure)
- [Backend Design Pattern](#backend-design-pattern)
- [Communication Architecture](#communication-architecture)
- [API Endpoints](#api-endpoints)
  - [DELETE /delete-account](#delete-delete-account)
- [Setup and Running](#setup-and-running)
  - [Prerequisites](#prerequisites)
  - [Dependencies](#dependencies)
  - [Environment Variables](#environment-variables)
  - [Running the Application](#running-the-application)
  - [Running with Docker](#running-with-docker)

## Project Overview

This application is a microservice responsible for handling the logical deletion of user accounts. When a deletion request is processed, the user's status is marked as inactive in the primary accounts database, and their associated profile in a separate user profile database is also marked as inactive. This approach preserves user data for potential recovery or auditing purposes while effectively removing the user from active status.

The service uses JSON Web Tokens (JWT) for authenticating requests.

## Folder Structure

The project is organized into the following main directories and files:

-   **`main.py`**: The main entry point for the Flask application. It defines API routes and handles incoming requests.
-   **`conections/`**: Contains modules for establishing and managing database connections.
    -   `mysql.py`: Handles connections to MySQL databases using SQLAlchemy, configured for two separate database instances (accounts and user profiles).
-   **`models/`**: Defines the data structures (ORM models) using SQLAlchemy.
    -   `models.py`: Contains class definitions for `User`, `Profile`, `Type`, and `Preference` tables.
-   **`services/`**: Contains the business logic of the application.
    -   `functions.py`: Implements functions like `delete_user`, which orchestrates the logical deletion process across databases.
-   **`tests/`**: Includes test scripts for the application.
    -   `route_test.py`: An example integration test for the `/delete-account` endpoint.
    -   `test_delete_account.py`: Likely contains more unit/integration tests for the delete functionality.
-   **`.github/workflows/`**: Contains CI/CD pipeline configurations for GitHub Actions.
    -   `docker-publish.yml`: Workflow for building and publishing Docker images.
-   **`dockerfile`**: Instructions for building a Docker image of the application.
-   **`requirements.txt`**: Lists the Python dependencies required for the project.
-   **`.env` (example, not committed)**: Would contain environment variables for configuration (database credentials, JWT secret key).
-   **`.gitignore`**: Specifies files and directories to be ignored by Git.

## Backend Design Pattern

The application employs a **Layered Architecture**:

1.  **Presentation Layer (Routes/Views)**: Implemented in `main.py` using Flask. This layer is responsible for handling HTTP requests, parsing input, and returning HTTP responses. It delegates business operations to the service layer.
2.  **Service Layer (Business Logic)**: Located in `services/functions.py`. This layer contains the core application logic, such as the process for deleting a user. It coordinates interactions between the presentation layer and the data access layer.
3.  **Data Access Layer**: Composed of modules in `conections/` (for database connection management) and `models/` (for SQLAlchemy ORM definitions). This layer abstracts the database interactions and provides a clean interface for the service layer to access and manipulate data.

This pattern promotes separation of concerns, making the application more modular, testable, and maintainable.

## Communication Architecture

-   **API Style**: The service exposes a **RESTful API** over HTTP.
-   **Authentication**: Requests to protected endpoints are authenticated using **JSON Web Tokens (JWT)**. The JWT must be included in the `Authorization` header as a `Bearer` token.
-   **Internal Communication**: Within the application, layers communicate via direct Python function calls.
-   **Database Communication**: The application interacts with MySQL databases using SQLAlchemy as an ORM. It connects to two distinct database instances: one for core account information and another for user profile details.

## API Endpoints

### DELETE /delete-account

-   **Method**: `DELETE`
-   **Description**: Logically deletes the user account associated with the authenticated user. The user's status is set to inactive in both the accounts and user profile databases.
-   **Authentication**: JWT Bearer Token required. The token payload must contain a `user_id` claim.
    -   Header: `Authorization: Bearer <your_jwt_token>`
-   **Request Body**: None.
-   **Responses**:
    -   **`200 OK`**:
        ```json
        {
            "message": "User <user_id> successfully deleted logically"
        }
        ```
    -   **`401 Unauthorized`**:
        -   Token missing or invalid format: `{"error": "Token missing or invalid"}`
        -   Invalid token data (e.g., `user_id` missing): `{"error": "Invalid token data"}`
        -   Token expired: `{"error": "Token expired"}`
        -   Other token validation errors: `{"error": "Invalid token"}`
    -   **`404 Not Found`**:
        -   User not found or already inactive: `{"error": "User not found or already inactive"}`

### Environment Variables

The application requires certain environment variables to be set for database connections and JWT configuration. Create a `.env` file in the root directory with the following variables (replace placeholders with actual values):

```env
# JWT Secret Key
SECRET_KEY="your_very_secret_jwt_key"

# Accounts Database Connection
DBA_HOSTIP="your_accounts_db_host"
DBA_PORT="your_accounts_db_port" # e.g., 3306
DBA_USER="your_accounts_db_user"
DBA_PASSWORD="your_accounts_db_password"
DBA_NAME="your_accounts_db_name"

# User Profile Database Connection
DBU_HOSTIP="your_userprofile_db_host"
DBU_PORT="your_userprofile_db_port" # e.g., 3306
DBU_USER="your_userprofile_db_user"
DBU_PASSWORD="your_userprofile_db_password"
DBU_NAME="your_userprofile_db_name"
```

**Note**: Ensure the `.env` file is added to your `.gitignore` to prevent committing sensitive credentials.
