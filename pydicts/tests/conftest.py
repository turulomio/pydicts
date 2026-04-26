import pytest
from unittest.mock import MagicMock

@pytest.fixture(autouse=True)
def force_english_locale(monkeypatch):
    """
    Forces gettext to use the original strings (English) by mocking the _ function
    in modules that use it.
    """
    # Create a mock _ function that simply returns its input
    mock_gettext_func = MagicMock(side_effect=lambda s: s)

    # List of modules that use gettext's _ function
    modules_to_patch = [
        "pydicts.lod",
        "pydicts.lod_ymv",
        "pydicts.lol",
        "pydicts.dod",
        "pydicts.casts",
    ]

    for module_name in modules_to_patch:
        # Patch the _ variable in each module
        monkeypatch.setattr(module_name + "._", mock_gettext_func)
