# Idoven code challenge

Welcome to Idoven code challenge! This is a brief guide to get you started with the API.

## Installation

To get started, follow these steps:

1. Make sure you have [Docker](https://www.docker.com/get-started) and [docker-compose](https://docs.docker.com/compose/install/) installed on your system.

2. Clone this repository to your local machine.

3. Navigate to the project directory in your terminal.

4. Run the following command to start the application and its dependencies, this will set up the required services and start the application:

   ```bash
   docker-compose up
## Usage

### Creating a User

1. Use the `/api/user` endpoint to create a user. Provide an username and password. This is an unprotected endpoint, everyone can access it - an improved mechanism should be created to handle users creation

### Authentication and Authorization

1. Use the `/api/login` endpoint to log in to the platform and obtain an authorization token.

2. Include the obtained token in the `Authorization` header for all subsequent requests to access protected routes.

### Uploading an ECG

1. Use the `/api/ecgs` endpoint to upload an electrocardiogram (ECG). Make sure to include the ECG data as required.

### Retrieving ECG Insights

1. Use the `/api/ecgs/<ecg_id>/insights` endpoint to get insights on a specific ECG. Provide the `ecg_id` in the URL to retrieve insights for that ECG.


## API Documentation

You can access the API documentation to learn more about the available endpoints, request parameters, and response formats.

### Swagger Documentation

Visit the Swagger documentation for an interactive API exploration experience. This is a great option for testing and understanding the API endpoints.

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

### ReDoc Documentation

ReDoc is another option for viewing the API documentation, providing a clean and user-friendly documentation view.

- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Make sure the application is running, and you can access the documentation URLs from your local environment. For a production environment, replace `http://localhost:8000` with the actual domain where your application is deployed.


## Authorization

Authorization in this application is implemented using JSON Web Tokens (JWT) for secure and stateless authentication. When a user successfully logs in, an access token is generated and signed with a secret key using JWT. This token is then provided to the user and must be included in the Authorization header of subsequent requests as a "Bearer" token. The server validates the token by decrypting it using the same secret key, ensuring its integrity and authenticity. The JWT contains information about the user (subject) and an expiration time to control access. This approach enhances security by eliminating the need to store user sessions on the server, and it allows for seamless, stateless authentication, making it suitable for web and API security.