import pytest

pytestmark = pytest.mark.unit


def test_main_returns_zero():
    from demo_app.main import main

    assert main() == 0
