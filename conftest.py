import os

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def credenciales():
    email = os.environ.get("QA_EMAIL")
    password = os.environ.get("QA_PASSWORD")
    if not email or not password:
        pytest.fail(
            "Faltan QA_EMAIL / QA_PASSWORD. Copia .env.example a .env "
            "y completa tus credenciales de prueba."
        )
    return {"email": email, "password": password}
