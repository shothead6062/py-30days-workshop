from pytest import MonkeyPatch

from demo_app.settings import AppSettings


def test_settings_from_env(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("APP_HOST", "0.0.0.0")
    monkeypatch.setenv("APP_PORT", "9000")
    monkeypatch.setenv("APP_DEBUG", "true")

    s = AppSettings()
    assert s.host == "0.0.0.0"
    assert s.port == 9000
    assert s.debug is True
