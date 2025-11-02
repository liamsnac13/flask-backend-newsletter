import requests
response = requests.post("http://127.0.0.1:8000/newsletter", json={
    "newsletter": {
        "titre": "Test",
        "introduction": "Ceci est un test"
    }
})
print(response.status_code)
print(response.json())
