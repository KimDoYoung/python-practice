import asyncio
import pytest
from typing import Dict, Any
from backend.app.domains.system.eventdays_model import EventDays
from backend.app.domains.system.eventdays_service import EventDaysService
from beanie import PydanticObjectId, init_beanie

from mongodb import MongoDb
from backend.app.domains.system.eventdays_model import EveryDays

# from backend.app.core.dependency import get_eventdays_service

@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def event_days_service(db_client):
    return EventDaysService(db_client=db_client)

@pytest.mark.asyncio
async def test_create_event(event_loop, event_days_service: EventDaysService):
    service = await event_days_service
    event_data = {
        "locdate": "2024-05-20",
        "dateKind": "01",
        "dateName": "Test Event",
        "isHoliday": "N",
        "name": "Event Name",
        "date": "2024-05-20",
        "description": "Event Description"
    }
    event = await service.create(event_data)
    assert event.name == "Event Name1"
    assert event.date == "2024-05-20"
    assert event.description == "Event Description"
    assert event.locdate == "2024-05-20"
    assert event.dateKind == "01"
    assert event.dateName == "Test Event"
    assert event.isHoliday == "N"