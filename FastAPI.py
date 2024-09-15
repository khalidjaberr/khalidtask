# pip install pytest
# pip install pytest-mock
# pip install httpx

# Create Car
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlalchemy.orm import Session
from app.main import app  # assuming your FastAPI app is in main.py
from app.schemas import CarCreate

client = TestClient(app)

# Test case for creating a new car
@patch('app.crud.get_db')  # Mock database session
def test_create_car(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    car_data = {"brand": "Toyota", "model": "Corolla", "year": 2022}
    response = client.post("/cars/", json=car_data)
    
    assert response.status_code == 200
    assert response.json()["brand"] == "Toyota"



# Retrieve All Cars
@patch('app.crud.get_db')
def test_get_all_cars(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.all.return_value = [
        {"id": 1, "brand": "Toyota", "model": "Corolla", "year": 2022},
        {"id": 2, "brand": "Honda", "model": "Civic", "year": 2020}
    ]
    
    response = client.get("/cars/")
    
    assert response.status_code == 200
    assert len(response.json()) == 2



# Retrieve Specific Car
@patch('app.crud.get_db')
def test_get_car(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.filter.return_value.first.return_value = {
        "id": 1, "brand": "Toyota", "model": "Corolla", "year": 2022
    }
    
    response = client.get("/cars/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["brand"] == "Toyota"


# Update Car
@patch('app.crud.get_db')
def test_update_car(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.filter.return_value.first.return_value = {
        "id": 1, "brand": "Toyota", "model": "Corolla", "year": 2022
    }
    mock_db.commit.return_value = None
    
    update_data = {"brand": "Toyota", "model": "Corolla", "year": 2023}
    response = client.put("/cars/1", json=update_data)
    
    assert response.status_code == 200
    assert response.json()["year"] == 2023




#  Delete Car
@patch('app.crud.get_db')
def test_delete_car(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.filter.return_value.first.return_value = {
        "id": 1, "brand": "Toyota", "model": "Corolla", "year": 2022
    }
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None
    
    response = client.delete("/cars/1")
    
    assert response.status_code == 204


# Add Mocking for External Dependencies
@patch('app.utils.send_email')
def test_create_car_with_email_notification(mock_send_email):
    mock_send_email.return_value = True
    
    car_data = {"brand": "Toyota", "model": "Corolla", "year": 2022}
    response = client.post("/cars/", json=car_data)
    
    assert response.status_code == 200
    mock_send_email.assert_called_once()
