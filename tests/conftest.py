import pytest
from mimesis import Generic
from mimesis.enums import Locale


@pytest.fixture
def data_provider() -> Generic:
    return Generic(locale=Locale.RU)
