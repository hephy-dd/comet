import pytest

from .helpers import MockResource


@pytest.fixture
def resource():
    return MockResource()
