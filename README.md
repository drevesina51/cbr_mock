# CBR Mock API Service

FastAPI mock service for Central Bank of Russia currency rates API

## Features

- Full mock implementation of CBR API endpoint
- Dynamic response generation based on request parameters
- Built-in request logging to SQLite database
- Automatic Swagger documentation
- Load testing support

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/cbr_mock.git
    cd cbr_mock
    ```

2.  Create and activate virtual environment:
    *   Linux/Mac:
        ```bash
        python -m venv venv
        source venv/bin/activate
        ```
    *   Windows:
        ```powershell
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the server
*   Development mode with auto-reload:
    ```bash
    make run
    ```
*   Production mode:
    ```bash
    make prod
    ```

### Endpoints
- Main endpoint: `GET /scripts/XML_daily.asp?date_req=DD/MM/YYYY`
- Healthcheck: `GET /healthcheck`
- Request log: `GET /requests-log`
- Reset test state: `POST /reset-test-state`

### Examples
- Successful request:
    ```bash
    curl "http://localhost:8000/scripts/XML_daily.asp?date_req=22/07/2025"
    ```
- Force error response:
    ```bash
    curl "http://localhost:8000/scripts/XML_daily.asp?date_req=22/07/2025&force_error=true"
    ```

## Testing
- Run basic tests:
    ```bash
    make test
    ```
- Run load testing (requires locust):
    ```bash
    make load-test
    ```

## Implementation Status

### ✅ Fully Implemented
- Microservice architecture (FastAPI)
- Asynchronous interaction
- Unique data generation per test
- No hardcoded responses
- No headers usage
- Makefile with commands
- Swagger documentation
- Database integration (SQLite)

### ⚠️ Not Implemented
- Proto files (gRPC interface)
- Golang version
