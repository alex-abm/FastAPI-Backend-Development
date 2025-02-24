from fastapi import APIRouter, HTTPException, Query
from typing import List
from .models import Joiner, Event
from .file_storage import EventFileManager
from .event_analyzer import EventAnalyzer

router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
    events = EventFileManager.read_events_from_file()
    return events


async def get_events_by_filter(
    date: str = Query(None),
    organizer: str = Query(None),
    status: str = Query(None),
    event_type: str = Query(None)
):
    
    events = EventFileManager.read_events_from_file()

    filtered_events = events
    if date:
        filtered_events = [event for event in filtered_events if event.date == date]
    if organizer:
        filtered_events = [event for event in filtered_events if event.organizer.name == organizer]
    if status:
        filtered_events = [event for event in filtered_events if event.status == status]
    if event_type:
        filtered_events = [event for event in filtered_events if event.type == event_type]

    return filtered_events

@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    events = EventFileManager.read_events_from_file()
    for event in events:
        if event.get('id') == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event not found")


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    events = EventFileManager.read_events_from_file()
    events.append(event.dict())
    EventFileManager.write_events_to_file(events)
    return event


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    events = EventFileManager.read_events_from_file()
    for idx, stored_event in enumerate(events):
        if stored_event.get('id') == event_id:
            events[idx] = event.dict()
            EventFileManager.write_events_to_file(events)
            return event
        raise HTTPException(status_code=404, detail="Event not found")


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    events = EventFileManager.read_events_from_file()
    for idx, event in enumerate(events):
        if event.get('id') == event_id:
            del events[idx]
            EventFileManager.write_events_to_file(events)
            return {"message": "Event deleted successfully"}
    raise HTTPException(status_code=404, detail="Event not found")


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    events = EventFileManager.read_events_from_file()

    joiners_multiple_meetings = EventAnalyzer.get_joiners_multiple_meetings_method(events)

    if not joiners_multiple_meetings:
        return {"message": "No joiners are found attending at least 2 meetings"}

    return {"joiners_multiple_meetings": joiners_multiple_meetings}
