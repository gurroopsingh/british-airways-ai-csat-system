from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_all():
    print("Testing /sentiment...")
    res = client.post("/sentiment", json={"text": "This was the worst flight ever."})
    print(res.status_code, res.json())
    
    print("Testing /predict...")
    res = client.post("/predict", json={"text": "This was the worst flight ever."})
    print(res.status_code, res.json())
    
    print("Testing /recommend...")
    res = client.post("/recommend", json={"topic_label": "Flight Delays", "sentiment": "Negative"})
    print(res.status_code, res.json())
    
    print("Testing /process_review...")
    res = client.post("/process_review", json={"text": "My flight was delayed by 3 hours and the luggage was lost."})
    print(res.status_code, res.json())

if __name__ == "__main__":
    test_all()
