.PHONY: run test load-test clean

run:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

prod:
	uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

test:
	curl "http://localhost:8000/scripts/XML_daily.asp?date_req=$$(date +'%d/%m/%Y')"
	@echo ""
	curl "http://localhost:8000/scripts/XML_daily.asp?date_req=22/07/2025&test_id=12345"
	@echo ""
	curl "http://localhost:8000/healthcheck"
	@echo ""

load-test:
	locust -f load_test.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache
