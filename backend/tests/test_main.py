import pytest
from fastapi.testclient import TestClient
import os
import tempfile
from main import app

client = TestClient(app)

def test_health_check():
    """Test API health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "endpoints" in data

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

class TestObjectsAPI:
    def test_create_object_success(self):
        """Test creating a tracked object"""
        object_data = {
            "name": "test_keys",
            "alias": "test car keys, test house keys"
        }
        
        response = client.post("/api/objects/", json=object_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "test_keys"
        assert data["alias"] == object_data["alias"]
        assert "id" in data
    
    def test_create_object_duplicate(self):
        """Test creating duplicate object fails"""
        object_data = {
            "name": "duplicate_test",
            "alias": "test duplicate object"
        }
        
        # Create first object
        client.post("/api/objects/", json=object_data)
        
        # Try to create duplicate
        response = client.post("/api/objects/", json=object_data)
        assert response.status_code == 409
    
    def test_get_objects(self):
        """Test retrieving tracked objects"""
        response = client.get("/api/objects/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)

class TestSearchAPI:
    def test_search_empty_query(self):
        """Test search with empty query fails"""
        response = client.post("/api/search/", json={"query": ""})
        assert response.status_code == 400
    
    def test_search_valid_query(self):
        """Test search with valid query"""
        # First create an object to search for
        client.post("/api/objects/", json={
            "name": "search_test_keys",
            "alias": "test keys for searching"
        })
        
        response = client.post("/api/search/", json={
            "query": "Where are my search_test_keys?"
        })
        assert response.status_code == 200
        
        data = response.json()
        assert "found" in data
        assert "message" in data or "location" in data

class TestUploadAPI:
    def test_upload_no_file(self):
        """Test upload without file fails"""
        response = client.post("/api/upload")
        assert response.status_code == 422
    
    def test_upload_invalid_file_type(self):
        """Test upload with invalid file type"""
        # Create a fake text file
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"This is not a video file")
            tmp_path = tmp.name
        
        with open(tmp_path, "rb") as f:
            response = client.post("/api/upload", files={"file": ("test.txt", f, "text/plain")})
        
        os.unlink(tmp_path)
        assert response.status_code == 400

if __name__ == "__main__":
    pytest.main([__file__])
