from django.test import TestCase

# Create your tests here.
def test_create_task(client):
    response = client.post('/api/v1/task/create/', {
        "title": "Test",
        "description": "Demo",
        "target_min": 1,
        "target_max": 5
    })
    assert response.status_code == 201
