from datetime import datetime

import pytest

from cheapgpt.app import create_app
from cheapgpt.llm.client import FakeLLMClient
from cheapgpt.support.ticket_service import TicketService

FIXED_NOW = datetime(2024, 1, 1, 12, 0, 0)


@pytest.fixture
def fake_llm():
    return FakeLLMClient()


@pytest.fixture
def fixed_clock():
    return lambda: FIXED_NOW


@pytest.fixture
def ticket_service(fixed_clock):
    return TicketService(clock=fixed_clock)


@pytest.fixture
def client():
    app = create_app(llm=FakeLLMClient())
    app.testing = True
    return app.test_client()
