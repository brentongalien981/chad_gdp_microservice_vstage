import pytest
from flask import Flask, jsonify
import sys
import os

# Add the parent directory of the test file to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from app import create_app
from app.error_handlers import register_error_handlers


@pytest.fixture
def app():
    app = create_app()
    register_error_handlers(app)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_handle_general_exception(client):
    @client.application.route("/raise-exception")
    def raise_exception():
        raise Exception("Test exception")

    response = client.get("/raise-exception")
    assert response.status_code == 500
    json_data = response.get_json()
    assert json_data["error"] == "General Internal Server Error"
    assert "Test exception" in json_data["message"]


def test_handle_specific_exception(client):
    class CustomException(Exception):
        pass

    @client.application.route("/raise-custom-exception")
    def raise_custom_exception():
        raise CustomException("Custom exception occurred")

    response = client.get("/raise-custom-exception")
    assert response.status_code == 500
    json_data = response.get_json()
    assert json_data["error"] == "General Internal Server Error"
    assert "Custom exception occurred" in json_data["message"]
