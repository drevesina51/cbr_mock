# CBR Mock Service

## Features
- Mock API for Central Bank of Russia rates
- Dynamic test data generation
- Supports parallel e2e testing

## Quick Start
```bash
# Install dependencies
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Run dev server
make run

# Or production
make prod
```

## API Endpoints
- `GET /scripts/XML_daily.asp` - Main endpoint
  - Parameters:
    - `date_req` - Date in DD/MM/YYYY format
    - `test_id` - Unique test identifier (optional)
    - `force_error` - Set to true to get 500 error

- `GET /healthcheck` - Service status
- `POST /reset-test-state` - Reset test data

## Testing
```bash
# Single request
make test

# Load testing (requires locust)
make load-test
```