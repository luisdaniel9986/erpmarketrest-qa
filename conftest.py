import os

import pytest
from dotenv import load_dotenv

load_dotenv()


def _credenciales_de(prefijo):
    email = os.environ.get(f"QA_{prefijo}_EMAIL") if prefijo else os.environ.get("QA_EMAIL")
    password = os.environ.get(f"QA_{prefijo}_PASSWORD") if prefijo else os.environ.get("QA_PASSWORD")
    if not email or not password:
        var = f"QA_{prefijo}_EMAIL / QA_{prefijo}_PASSWORD" if prefijo else "QA_EMAIL / QA_PASSWORD"
        pytest.fail(
            f"Faltan {var}. Copia .env.example a .env "
            "y completa tus credenciales de prueba."
        )
    return {"email": email, "password": password}


@pytest.fixture
def credenciales():
    """Usuario admin — el que usa la mayoría de los tests."""
    return _credenciales_de(None)


@pytest.fixture
def credenciales_cajero():
    return _credenciales_de("CAJERO")


@pytest.fixture
def credenciales_vendedor():
    return _credenciales_de("VENDEDOR")


@pytest.fixture
def credenciales_mesero():
    return _credenciales_de("MESERO")
