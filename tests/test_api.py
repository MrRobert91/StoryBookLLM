import os
import sys
import types

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient

# Create a lightweight dummy module for app.story_generator before importing app
dummy_story_generator = types.ModuleType("app.story_generator")

def dummy_generate_story(theme: str, num_chapters: int, words_per_chapter: int):
    """Return a fake PDF path and success flag"""
    return "static/CuentosGenerados/test.pdf", True

dummy_story_generator.generate_story = dummy_generate_story
sys.modules["app.story_generator"] = dummy_story_generator

from app.main import app


@pytest.fixture
def client(monkeypatch):
    # Patch the generate_story function to avoid heavy external calls
    from app import story_generator
    monkeypatch.setattr(story_generator, "generate_story", dummy_generate_story)
    # Ensure the expected PDF file exists to satisfy file checks
    os.makedirs("static/CuentosGenerados", exist_ok=True)
    with open("static/CuentosGenerados/test.pdf", "w") as f:
        f.write("dummy pdf content")
    return TestClient(app)


def test_generate_story_endpoint(client):
    payload = {
        "theme": "Space Adventure",
        "num_chapters": 1,
        "words_per_chapter": 50,
    }
    response = client.post("/api/generate-story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "pdf_url" in data
    assert "message" in data
