import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open, MagicMock
import json
from main import app, load_data, search_data, paginate_data

# Setup test client
client = TestClient(app)

# Sample test data
MOCK_DATA = {
    "salesReps": [
        {
            "id": 1,
            "name": "John Doe",
            "role": "Senior Sales Rep",
            "region": "North America",
            "skills": ["Negotiation", "CRM Software", "Product Knowledge"],
            "deals": [
                {"client": "ABC Corp", "value": 75000, "status": "Closed Won"},
                {"client": "XYZ Inc", "value": 50000, "status": "In Progress"}
            ],
            "clients": [
                {"name": "ABC Corp", "industry": "Technology", "contact": "john@abccorp.com"},
                {"name": "XYZ Inc", "industry": "Healthcare", "contact": "jane@xyzinc.com"}
            ]
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "role": "Sales Manager",
            "region": "Europe",
            "skills": ["Team Leadership", "Strategic Planning", "CRM Software"],
            "deals": [
                {"client": "Euro Tech", "value": 120000, "status": "Closed Won"},
                {"client": "Med Solutions", "value": 85000, "status": "Closed Lost"}
            ],
            "clients": [
                {"name": "Euro Tech", "industry": "Technology", "contact": "contact@eurotech.com"},
                {"name": "Med Solutions", "industry": "Healthcare", "contact": "info@medsolutions.com"}
            ]
        }
    ]
}

# Mock the load_data function to return test data
@pytest.fixture(autouse=True)
def mock_load_data():
    with patch("main.load_data", return_value=MOCK_DATA):
        yield

# Test load_data function
def test_load_data():
    with patch("builtins.open", mock_open(read_data=json.dumps(MOCK_DATA))) as mock_file:
        data = load_data()
        mock_file.assert_called_once_with("../dummyData.json", "r")
        assert data == MOCK_DATA

# Test load_data function with exception
def test_load_data_exception():
    with patch("builtins.open", side_effect=Exception("File not found")):
        with pytest.raises(Exception):
            load_data()

# Test search_data function
def test_search_data():
    # Test search by name
    results = search_data(MOCK_DATA["salesReps"], "john")
    assert len(results) == 1
    assert results[0]["name"] == "John Doe"
    
    # Test search by role
    results = search_data(MOCK_DATA["salesReps"], "manager")
    assert len(results) == 1
    assert results[0]["name"] == "Jane Smith"
    
    # Test search by region
    results = search_data(MOCK_DATA["salesReps"], "europe")
    assert len(results) == 1
    assert results[0]["region"] == "Europe"
    
    # Test search by skill
    results = search_data(MOCK_DATA["salesReps"], "crm")
    assert len(results) == 2
    
    # Test empty search
    results = search_data(MOCK_DATA["salesReps"], "")
    assert len(results) == 2

# Test paginate_data function
def test_paginate_data():
    data = [{"id": i} for i in range(1, 21)]  # Create 20 items
    
    # Test first page
    result = paginate_data(data, 1, 10)
    assert len(result["data"]) == 10
    assert result["meta"]["page"] == 1
    assert result["meta"]["total_pages"] == 2
    assert result["meta"]["has_next"] == True
    assert result["meta"]["has_prev"] == False
    
    # Test second page
    result = paginate_data(data, 2, 10)
    assert len(result["data"]) == 10
    assert result["meta"]["page"] == 2
    assert result["meta"]["has_next"] == False
    assert result["meta"]["has_prev"] == True
    
    # Test with smaller page size
    result = paginate_data(data, 1, 5)
    assert len(result["data"]) == 5
    assert result["meta"]["total_pages"] == 4

# Test GET /api/data endpoint
def test_get_data_no_filters():
    response = client.get("/api/data")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["meta"]["total_items"] == 2

# Test GET /api/data with name filter
def test_get_data_with_name_filter():
    response = client.get("/api/data?name=John")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "John Doe"

# Test GET /api/data with role filter
def test_get_data_with_role_filter():
    response = client.get("/api/data?role=Manager")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "Jane Smith"

# Test GET /api/data with region filter
def test_get_data_with_region_filter():
    response = client.get("/api/data?region=Europe")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["region"] == "Europe"

# Test GET /api/data with skills filter
def test_get_data_with_skills_filter():
    response = client.get("/api/data?skills=Leadership")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert "Team Leadership" in data["data"][0]["skills"]

# Test GET /api/data with multiple filters
def test_get_data_with_multiple_filters():
    response = client.get("/api/data?role=Manager&region=Europe")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "Jane Smith"

# Test GET /api/data with pagination
def test_get_data_with_pagination():
    response = client.get("/api/data?page=1&page_size=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["meta"]["page"] == 1
    assert data["meta"]["page_size"] == 1
    assert data["meta"]["total_items"] == 2
    assert data["meta"]["total_pages"] == 2

# Test POST /api/ai endpoint
@patch("google.generativeai.GenerativeModel")
def test_ai_endpoint(mock_genai):
    # Mock the GenerativeModel class and its methods
    mock_model = MagicMock()
    mock_chat = MagicMock()
    mock_response = MagicMock()
    
    mock_response.text = "Analysis of sales data: John Doe has 2 deals with a total value of $125,000."
    mock_chat.send_message.return_value = mock_response
    mock_model.start_chat.return_value = mock_chat
    mock_genai.return_value = mock_model
    
    # Test the endpoint with a question
    request_data = {
        "question": "Who is the top performing sales rep?"
    }
    
    response = client.post("/api/ai", json=request_data)
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "Analysis of sales data" in response.json()["answer"]
    
    # Verify the correct model was used
    mock_genai.assert_called_once()
    # Verify chat was started
    mock_model.start_chat.assert_called_once()
    # Verify message was sent (contains both context and question)
    mock_chat.send_message.assert_called_once()
    sent_msg = mock_chat.send_message.call_args[0][0]
    assert "Who is the top performing sales rep?" in sent_msg

# Test POST /api/ai with custom data
@patch("google.generativeai.GenerativeModel")
def test_ai_endpoint_with_custom_data(mock_genai):
    # Mock the GenerativeModel class and its methods
    mock_model = MagicMock()
    mock_chat = MagicMock()
    mock_response = MagicMock()
    
    mock_response.text = "Custom data analysis result."
    mock_chat.send_message.return_value = mock_response
    mock_model.start_chat.return_value = mock_chat
    mock_genai.return_value = mock_model
    
    # Test the endpoint with custom data
    request_data = {
        "question": "Analyze this custom data",
        "data": {
            "salesReps": [
                {
                    "name": "Custom Rep",
                    "deals": [{"value": 100000, "status": "Closed Won"}]
                }
            ]
        }
    }
    
    response = client.post("/api/ai", json=request_data)
    assert response.status_code == 200
    assert "answer" in response.json()
    
    # Verify custom data was included in the message
    sent_msg = mock_chat.send_message.call_args[0][0]
    assert "Custom Rep" in sent_msg

# Test error handling for AI endpoint - FIXED TEST
@patch("google.generativeai.GenerativeModel", side_effect=Exception("API Error"))
def test_ai_endpoint_error(mock_genai):
    request_data = {
        "question": "Who is the top performing sales rep?"
    }
    
    response = client.post("/api/ai", json=request_data)
    # Kita sekarang memeriksa status kode 200 karena fungsi menangani kesalahan dengan baik
    assert response.status_code == 200
    
    # Kita memeriksa bahwa pesan error dikembalikan dalam respons
    response_data = response.json()
    assert "answer" in response_data
    assert "AI service is currently unavailable" in response_data["answer"]