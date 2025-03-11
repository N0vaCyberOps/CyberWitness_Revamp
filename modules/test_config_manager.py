from utils.config_manager import ConfigManager
import pytest

def test_config_manager_load():
    config = ConfigManager("test_config.json").get_config("test_key")
    assert config == "test_value"

def test_config_manager_validation():
    config = ConfigManager("test_config.json")
    with pytest.raises(ValueError):
        config.validate_config()

# Utwórz plik test_config.json w głównym folderze projektu z zawartością:
# {"test_key": "test_value"}