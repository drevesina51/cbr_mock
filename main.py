from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
import xml.etree.ElementTree as ET
from datetime import datetime
import hashlib
import random
from typing import Optional
from sqlite3 import connect
from contextlib import closing

app = FastAPI()

CURRENCY_DATA = [
    {"ID": "R01010", "NumCode": "036", "CharCode": "AUD", "Nominal": 1, "Name": "Australian dollar"},
    {"ID": "R01020A", "NumCode": "944", "CharCode": "AZN", "Nominal": 1, "Name": "Azerbaijani manat"},
    {"ID": "R01035", "NumCode": "826", "CharCode": "GBP", "Nominal": 1, "Name": "British pound sterling"},
    {"ID": "R01060", "NumCode": "051", "CharCode": "AMD", "Nominal": 100, "Name": "Armenian dram"},
    {"ID": "R01090B", "NumCode": "933", "CharCode": "BYN", "Nominal": 1, "Name": "Belarusian ruble"},
    {"ID": "R01100", "NumCode": "975", "CharCode": "BGN", "Nominal": 1, "Name": "Bulgarian lev"},
    {"ID": "R01115", "NumCode": "986", "CharCode": "BRL", "Nominal": 1, "Name": "Brazilian real"},
    {"ID": "R01135", "NumCode": "348", "CharCode": "HUF", "Nominal": 100, "Name": "Hungarian forint"},
    {"ID": "R01200", "NumCode": "344", "CharCode": "HKD", "Nominal": 10, "Name": "Hong Kong dollar"},
    {"ID": "R01215", "NumCode": "208", "CharCode": "DKK", "Nominal": 10, "Name": "Danish krone"},
    {"ID": "R01235", "NumCode": "840", "CharCode": "USD", "Nominal": 1, "Name": "US dollar"},
    {"ID": "R01239", "NumCode": "978", "CharCode": "EUR", "Nominal": 1, "Name": "Euro"},
    {"ID": "R01270", "NumCode": "356", "CharCode": "INR", "Nominal": 100, "Name": "Indian rupee"},
    {"ID": "R01335", "NumCode": "398", "CharCode": "KZT", "Nominal": 100, "Name": "Kazakhstani tenge"},
    {"ID": "R01350", "NumCode": "124", "CharCode": "CAD", "Nominal": 1, "Name": "Canadian dollar"},
    {"ID": "R01370", "NumCode": "417", "CharCode": "KGS", "Nominal": 100, "Name": "Kyrgyzstani som"},
    {"ID": "R01375", "NumCode": "156", "CharCode": "CNY", "Nominal": 10, "Name": "Chinese yuan"},
    {"ID": "R01500", "NumCode": "498", "CharCode": "MDL", "Nominal": 10, "Name": "Moldovan leu"},
    {"ID": "R01535", "NumCode": "578", "CharCode": "NOK", "Nominal": 10, "Name": "Norwegian krone"},
    {"ID": "R01565", "NumCode": "985", "CharCode": "PLN", "Nominal": 1, "Name": "Polish zloty"},
    {"ID": "R01585F", "NumCode": "946", "CharCode": "RON", "Nominal": 10, "Name": "Romanian leu"},
    {"ID": "R01589", "NumCode": "960", "CharCode": "XDR", "Nominal": 1, "Name": "SDR (Special Drawing Rights)"},
    {"ID": "R01625", "NumCode": "702", "CharCode": "SGD", "Nominal": 1, "Name": "Singapore dollar"},
    {"ID": "R01670", "NumCode": "972", "CharCode": "TJS", "Nominal": 10, "Name": "Tajikistani somoni"},
    {"ID": "R01700J", "NumCode": "949", "CharCode": "TRY", "Nominal": 10, "Name": "Turkish lira"},
    {"ID": "R01710A", "NumCode": "934", "CharCode": "TMT", "Nominal": 1, "Name": "New Turkmenistan manat"},
    {"ID": "R01717", "NumCode": "860", "CharCode": "UZS", "Nominal": 10000, "Name": "Uzbekistani som"},
    {"ID": "R01720", "NumCode": "980", "CharCode": "UAH", "Nominal": 10, "Name": "Ukrainian hryvnia"},
    {"ID": "R01760", "NumCode": "203", "CharCode": "CZK", "Nominal": 10, "Name": "Czech koruna"},
    {"ID": "R01770", "NumCode": "752", "CharCode": "SEK", "Nominal": 10, "Name": "Swedish krona"},
    {"ID": "R01775", "NumCode": "756", "CharCode": "CHF", "Nominal": 1, "Name": "Swiss franc"},
    {"ID": "R01810", "NumCode": "710", "CharCode": "ZAR", "Nominal": 10, "Name": "South African rand"},
    {"ID": "R01815", "NumCode": "410", "CharCode": "KRW", "Nominal": 1000, "Name": "South Korean won"},
    {"ID": "R01820", "NumCode": "392", "CharCode": "JPY", "Nominal": 100, "Name": "Japanese yen"}
]

class Config:
    DB_PATH = "currency.db"
    ERROR_RATE = 0.1  # 10% chance of random error
    BASE_SEED = 10000

def init_db():
    with closing(connect(Config.DB_PATH)) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_req TEXT NOT NULL,
            test_id TEXT,
            response_code INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

def log_request(date_req: str, test_id: Optional[str], response_code: int):
    with closing(connect(Config.DB_PATH)) as conn:
        conn.execute(
            "INSERT INTO requests (date_req, test_id, response_code) VALUES (?, ?, ?)",
            (date_req, test_id, response_code)
        )
        conn.commit()

def generate_currency_values(date_req: str, test_id: Optional[str] = None):
    seed = f"{date_req}_{test_id}" if test_id else date_req
    seed_hash = int(hashlib.sha256(seed.encode()).hexdigest(), 16) % Config.BASE_SEED
    
    values = {}
    for currency in CURRENCY_DATA:
        currency_seed = f"{seed_hash}_{currency['ID']}"
        currency_hash = int(hashlib.sha256(currency_seed.encode()).hexdigest(), 16)
        
        if currency["Nominal"] == 1:
            base = 30 + (hash(currency['ID']) % 70)
            value = base + (currency_hash % 100)/100
        else:
            value = (currency_hash % 1000)/10000 + 0.01
        
        values[currency["CharCode"]] = round(value, 4)
    
    return values

def generate_xml(date_req: str, test_id: Optional[str] = None):
    root = ET.Element("ValCurs", Date=date_req)
    currencies = generate_currency_values(date_req, test_id)
    
    for currency in CURRENCY_DATA:
        char_code = currency["CharCode"]
        if char_code in currencies:
            valute = ET.SubElement(root, "Valute", ID=currency["ID"])
            ET.SubElement(valute, "NumCode").text = currency["NumCode"]
            ET.SubElement(valute, "CharCode").text = char_code
            ET.SubElement(valute, "Nominal").text = str(currency["Nominal"])
            ET.SubElement(valute, "Name").text = currency["Name"]
            ET.SubElement(valute, "Value").text = str(currencies[char_code])
    
    return ET.tostring(root, encoding="utf-8").decode()

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/scripts/XML_daily.asp",
         summary="Mock CBR currency rates",
         response_description="XML with currency rates")
async def mock_cbr(
    date_req: str, 
    force_error: bool = False,
    test_id: Optional[str] = None
):

    try:
        datetime.strptime(date_req, "%d/%m/%Y")
        
        # 10% chance of random error
        if not force_error and random.random() < Config.ERROR_RATE:
            force_error = True
        
        if force_error:
            log_request(date_req, test_id, 500)
            raise HTTPException(status_code=500, detail="Internal server error")

        xml_data = generate_xml(date_req, test_id)
        log_request(date_req, test_id, 200)
        return PlainTextResponse(content=xml_data, media_type="application/xml")
    
    except ValueError:
        log_request(date_req, test_id, 400)
        raise HTTPException(status_code=400, detail="Date must be in DD/MM/YYYY format")

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "OK", "version": "1.0"}

@app.post("/reset-test-state")
async def reset_state():
    with closing(connect(Config.DB_PATH)) as conn:
        conn.execute("DELETE FROM requests")
        conn.commit()
    return {"status": "test state reset"}

@app.get("/requests-log")
async def get_requests_log():
    with closing(connect(Config.DB_PATH)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM requests ORDER BY timestamp DESC LIMIT 100")
        return {"requests": cursor.fetchall()}
