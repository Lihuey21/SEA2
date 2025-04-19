import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to path
from calculator import app  # Import your Flask app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Choose A Tool" in response.data

def test_addition(client):
    response = client.post("/", data={"mode": "calculator", "num1": "5", "num2": "3", "operation": "+"})
    assert b"8.0" in response.data

def test_subtraction(client):
    response = client.post("/", data={"mode": "calculator", "num1": "10", "num2": "4", "operation": "-"})
    assert b"6.0" in response.data

def test_multiplication(client):
    response = client.post("/", data={"mode": "calculator", "num1": "3", "num2": "4", "operation": "x"})
    assert b"12.0" in response.data

def test_division(client):
    response = client.post("/", data={"mode": "calculator", "num1": "8", "num2": "2", "operation": "÷"})
    assert b"4.0" in response.data

def test_divide_by_zero(client):
    response = client.post("/", data={"mode": "calculator", "num1": "8", "num2": "0", "operation": "÷"})
    assert b"Cannot divide by zero" in response.data

def test_invalid_number_input(client):
    response = client.post("/", data={"mode": "calculator", "num1": "abc", "num2": "5", "operation": "+"})
    assert b"Please enter valid numbers." in response.data

def test_currency_conversion_usd_to_myr(client):
    response = client.post("/", data={
        "mode": "converter",
        "amount": "10",
        "source_currency": "USD",
        "target_currency": "MYR"
    })
    assert b"10.0 USD = 47.00 MYR" in response.data

def test_currency_conversion_myr_to_jpy(client):
    response = client.post("/", data={
        "mode": "converter",
        "amount": "10",
        "source_currency": "MYR",
        "target_currency": "JPY"
    })
    assert b"10.0 MYR = 234.00 JPY" in response.data

def test_invalid_currency_input(client):
    response = client.post("/", data={
        "mode": "converter",
        "amount": "abc",
        "source_currency": "USD",
        "target_currency": "MYR"
    })
    assert b"Please enter valid numbers." in response.data
