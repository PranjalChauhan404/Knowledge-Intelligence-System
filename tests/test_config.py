from app.config import Config


def test_config_defaults():
    assert Config.HOST == "0.0.0.0"
    assert Config.PORT == 5000
    assert Config.DEBUG is False