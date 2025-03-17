import requests

response = requests.post(
    "http://localhost:8000/api/generate-story",
    json={
        "theme": "Space Adventure",
        "num_chapters": 1,
        "words_per_chapter": 100
    }
)

print(response.status_code)
print(response.json())