import httpx
import pytest

from fastapi import status

from auth.jwt_handler import create_access_token
from models.events import Event


@pytest.fixture(scope='module')
async def access_token():
    return create_access_token("testuser1@gmail.com")


@pytest.fixture(scope='module')
async def  mock_event():
    new_event = Event(
        creator="testuser1@gmail.com",
        title="FastAPI Book Launch",
        image="https://linktomyimage.com/image.png", 
        description="We will be discussing the contents of \
        the FastAPI book in this event.Ensure to come with \
        your own copy to win gifts!", 
        tags=["python", "fastapi", "book", "launch"], 
        location="Google Meet"
    )
    
    await Event.insert_one(new_event)
    
    yield new_event


@pytest.mark.asyncio
async def test_get_events(default_client: httpx.AsyncClient, mock_event: Event):
    response = await default_client.get("/event/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["_id"] == str(mock_event.id)


@pytest.mark.asyncio
async def test_get_event(default_client: httpx.AsyncClient, mock_event: Event):
    url = f'/event/{str(mock_event.id)}'
    response = await default_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["creator"] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)


@pytest.mark.asyncio
async def test_post_event(default_client: httpx.AsyncClient, access_token: str):
    payload = {
        "title": "FastAPI Book Launch",
        "image": "https://linktomyimage.com/image.png", 
        "description": "We will be discussing the contents \
        of the FastAPI book in this event.Ensure to come \
        with your own copy to win gifts!",
        "tags": [
            "python", 
            "fastapi", 
            "book", 
            "launch"
        ],
        "location": "Google Meet",
    }
    
    headers = {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {access_token}"
    }
    
    test_response = {
        "message": "Event created successfully"
    }
    
    response = await default_client.post('/event/new', json=payload, headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_get_events_count(default_client: httpx.AsyncClient):
    response = await default_client.get('/event/')
    
    events = response.json()
    
    assert response.status_code == status.HTTP_200_OK
    assert len(events) == 2


@pytest.mark.asyncio
async def test_update_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str):
    test_payload = {
        "title": "Updated FastAPI event"
    }
    
    headers = {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {access_token}"
    }
    
    url = f'/event/{str(mock_event.id)}'
    response = await default_client.put(url, json=test_payload, headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == test_payload['title']


@pytest.mark.asyncio
async def test_delete_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str):
    test_response = {
        "message": "Event deleted successfully."
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    url = f'/event/{mock_event.id}'
    
    response = await default_client.delete(url, headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_get_event_again(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
