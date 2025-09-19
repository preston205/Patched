from flask import Flask

app = Flask(__name__)


@app.get('/')
def home() -> str:
    return 'Hello, Flask!'


def test_home() -> None:
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert response.data == b'Hello, Flask!'
