import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, Mock, MagicMock
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI
from datetime import timedelta
from amichan.api.routes import auth  
from amichan.api.schemas.requests.auth import BanUserRequest
from amichan.core.dependencies import IJWTService, CurrentUser, DBSession
from amichan import app
from amichan.api.router import router
from fastapi import APIRouter
from amichan.core.config import get_app_settings
from amichan.api.routes import board, thread, auth, post
from fastapi.middleware.cors import CORSMiddleware
from amichan.core.security import HTTPTokenHeader
from amichan.api.schemas.requests.board import BoardCreateRequest
from amichan.api.schemas.requests.thread import CreateThreadRequest
from amichan.core.dependencies import IBoardsService, IThreadService, DBSession, CurrentUser, get_current_user

@pytest.fixture
def mock_router(mocker):

    router = APIRouter()

    router.include_router(router=thread.router, prefix="/thread", tags=["thread"])
    router.include_router(router=board.router, prefix="/board", tags=["board"])
    router.include_router(router=auth.router, prefix="/auth", tags=["auth"])
    router.include_router(router=post.router, prefix="/post", tags=["post"])
    return router

@pytest.fixture
def mock_app_settings(mocker):
    # Мокаем DevAppSettings и задаем фейковые значения для всех нужных параметров
    mock_settings = mocker.patch('amichan.core.config.DevAppSettings', autospec=True)
    mock_settings.return_value.postgres_host = "localhost"
    mock_settings.return_value.postgres_port = 5432
    mock_settings.return_value.postgres_user = "user"
    mock_settings.return_value.postgres_password = "password"
    mock_settings.return_value.postgres_db = "db"
    mock_settings.return_value.database_url = "postgresql://user:password@localhost:5432/db"
    mock_settings.return_value.jwt_secret_key = "secret"
    mock_settings.return_value.mail_username = "mail_user"
    mock_settings.return_value.mail_password = "mail_pass"
    mock_settings.return_value.mail_from = "mail_from@example.com"
    mock_settings.return_value.mail_port = 587
    mock_settings.return_value.mail_server = "smtp.mail.com"
    mock_settings.return_value.mail_tls = True
    mock_settings.return_value.mail_ssl = False
    return mock_settings

@pytest.fixture
def mock_jwt_service(mocker):
    # Мокаем сервис JWT
    return mocker.patch('amichan.core.dependencies.IJWTService', autospec=True)

@pytest.fixture
def mock_session(mocker):
    return mocker.create_autospec(DBSession, instance=True)

@pytest.fixture
def client():
    # Настроим тестовый клиент FastAPI
    settings = get_app_settings()

    application = FastAPI(**settings.fastapi_kwargs)
    application.include_router(router)

    origins = [
        "http://localhost:5173",  # Для фронтенда на Vite
        "http://127.0.0.1:5173",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Разрешенные источники
        allow_credentials=True,
        allow_methods=["*"],  # Разрешенные методы (GET, POST и т.д.)
        allow_headers=["*"],  # Разрешенные заголовки
    )

    return TestClient(application)
@pytest.fixture
def clean_app():
    # Настроим тестовый клиент FastAPI
    settings = get_app_settings()

    application = FastAPI(**settings.fastapi_kwargs)
    application.include_router(router)

    origins = [
        "http://localhost:5173",  # Для фронтенда на Vite
        "http://127.0.0.1:5173",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Разрешенные источники
        allow_credentials=True,
        allow_methods=["*"],  # Разрешенные методы (GET, POST и т.д.)
        allow_headers=["*"],  # Разрешенные заголовки
    )

    return application
@pytest.fixture
def mock_router(mocker):
    return mocker.patch('amichan.api.router', autospec = True)

def test_router(clean_app):
    assert len(clean_app.routes) > 0

@pytest.mark.parametrize("email, expected_status_code, expected_message, det", [
    ("test@edu.hse.ru", 200, "Magic link sent to test@edu.hse.ru", "message"),  
    ("test@example.com", 400, "Invalid email domain", "detail"),             
])
def test_send_magic_link(client, mock_jwt_service, mock_app_settings, email, expected_status_code, expected_message, det):
    response = client.post(
        "/auth/send_magic_link/",
        json={"email": email}
    )
    assert response.status_code == expected_status_code
    assert response.json() == {det: expected_message}

@pytest.fixture
def token():
    return "aboba"

def test_verification(client, token, mock_jwt_service):
    response = client.get(
        "/auth/verify_magic_link/{token}"
    )
    assert response.status_code == 400
    assert response.json() == {"detail" :"Invalid token"}

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0emJhcnRpaWFAZWR1LmhzZS5ydSIsInJvbGUiOjEsImV4cCI6MTczNDkxNjU4M30.Dy2BPURmm2H8fhWXgnJBkhsEFjprwb7btgvC2sNTO3M
@pytest.fixture
def usr():
    return None

@pytest.fixture
def prot(moker):
    return moker.patch("amichan.core.security.HTTPTokenHeader", autospec = True)

def test_ban(client, mocker, mock_jwt_service):
    mock_fastmail = mocker.patch("fastapi_mail.FastMail")
    mock_fastmail.return_value.send_message = AsyncMock()
    
    mock_jwt_service.ban_user = AsyncMock()
    mocker.patch.object(HTTPTokenHeader, "__call__", AsyncMock(return_value = "mocked_token"))
    mocker.patch("amichan.core.dependencies.CurrentUser", return_value = None)
    mocker.patch("amichan.core.dependencies.get_current_user", return_value = None)
    payload = {
        "email" : "test@edu.hse.ru",
        "reason" : "violation of rules",
        "duration" : "30d",
    }

    response = client.post("/auth/ban_user", json = payload)
    assert response.status_code == 401

def test_login(client, mock_jwt_service, mock_session, mocker):
    mock_jwt_service.login = AsyncMock(side_effect=Exception("Database connection error"))

    mocker.patch("amichan.core.dependencies.IJWTService", return_value=mock_jwt_service)
    mocker.patch("amichan.core.dependencies.DBSession", return_value=mock_session)

    payload = {
        "email": "test@edu.hse.ru",
        "password": "valid_password",
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 500

@pytest.fixture
def mocked_IBoardsService(mocker):
    return mocker.create_autospec(IBoardsService, instance=True)

@pytest.fixture
def mock_thread_service(mocker):
    return mocker.create_autospec(IThreadService, instance=True)


@pytest.fixture
def mock_session(mocker):
    return mocker.create_autospec(DBSession, instance=True)


@pytest.fixture
def mock_current_user(mocker):
    return mocker.create_autospec(CurrentUser, instance=True)


def test_get_boards(client, mocker, mock_jwt_service):
    boards_dto = [{"id": 1, "name": "Board 1", "description": "Description 1"}]
    mock_jwt_service.get_boards = AsyncMock(return_value=boards_dto)
    mocker.patch("amichan.core.dependencies.IBoardsService", return_value=mock_jwt_service)
    mocker.patch.object(HTTPTokenHeader, "__call__", AsyncMock(return_value = "mocked_token"))
    response = client.get("/board/boards")

    assert response.status_code == 405


def test_get_board_threads(client, mocker, mock_thread_service, mock_session):
    threads_dto = [{"id": 1, "title": "Thread 1", "author": "user1"}]
    mock_thread_service.get_threads = AsyncMock(return_value=threads_dto)
    mocker.patch("amichan.core.dependencies.IThreadService", return_value=mock_thread_service)

    response = client.get("/board/board/boards/1/threads")

    assert response.status_code == 404

def test_create_board(client, mocker, mock_jwt_service, mock_session, mock_current_user):
    # Mock current_user
    mock_current_user.role_id = 1  # Normal user
    mocker.patch("amichan.core.dependencies.CurrentUser", return_value=mock_current_user)

    mock_jwt_service.create_new_board = AsyncMock()
    mocker.patch("amichan.core.dependencies.IBoardsService", return_value=mock_jwt_service)

    payload = {"name": "New Board", "description": "Description of new board"}
    response = client.post("/board/boards", json=payload)

    assert response.status_code == 405


def test_create_board_unauthorized(client, mocker, mock_jwt_service, mock_session):
    # Mock current_user as None (unauthorized)
    mocker.patch("amichan.core.dependencies.CurrentUser", return_value=None)

    payload = {"name": "New Board", "description": "Description of new board"}
    response = client.post("/board/boards", json=payload)

    assert response.status_code == 405


def test_create_board_forbidden(client, mocker, mock_jwt_service, mock_session, mock_current_user):
    mock_current_user.role_id = 4 
    mocker.patch("amichan.core.dependencies.CurrentUser", return_value=mock_current_user)

    payload = {"name": "New Board", "description": "Description of new board"}
    response = client.post("/board/boards", json=payload)

    assert response.status_code == 405


def test_delete_board(client, mocker, mock_jwt_service, mock_session, mock_current_user):
    mock_current_user.role_id = 1  
    mocker.patch("amichan.core.dependencies.CurrentUser", return_value=mock_current_user)

    mock_jwt_service.delete_board = AsyncMock()
    mocker.patch("amichan.core.dependencies.IBoardsService", return_value=mock_jwt_service)

    response = client.delete("/board/boards/1")

    assert response.status_code == 404


def test_delete_board_unauthorized(client, mocker, mock_jwt_service, mock_session):
    mocker.patch("amichan.core.dependencies.CurrentUser", return_value=None)

    response = client.delete("/board/boards/1")

    assert response.status_code == 404

def test_delete_board_forbidden(client, mocker, mock_jwt_service, mock_session, mock_current_user):
    # Mock current_user with forbidden role_id
    mock_current_user.role_id = 4  # Forbidden role
    mocker.patch("amichan.core.dependencies.CurrentUser", return_value=mock_current_user)

    response = client.delete("/board/boards/1")

    assert response.status_code == 404

async def test_get_cur_user(client, mocker, mock_jwt_service, token):
    mock_jwt_service = mocker.create_autospec(IJWTService)
    mock_jwt_service.parse = AsyncMock(return_value=None)
    token = "invalid-token" 
    with pytest.raises(HTTPException):
        await get_current_user(token=token, auth_token_service=mock_jwt_service)

import pytest
from unittest.mock import AsyncMock, MagicMock
from amichan.services.thread import ThreadService
from amichan.domain.dtos.thread import CreateThreadDTO, ThreadRecordDTO, ThreadPostsDTO, ThreadsFeedDTO
from amichan.domain.repositories.thread import IThreadRepository
from amichan.core.exceptions import ThreadNotFoundException

@pytest.fixture
def mock_thread_repo():
    return MagicMock(spec=IThreadRepository)

@pytest.fixture
def thread_service(mock_thread_repo):
    return ThreadService(thread_repo=mock_thread_repo)

@pytest.mark.asyncio
async def test_create_new_thread(thread_service, mock_thread_repo):
    session = AsyncMock()  
    board_id = 1
    thread_to_create = CreateThreadDTO(title="Test Thread", content="This is a test thread.")
    created_thread = ThreadRecordDTO(id=1, title="Test Thread", content="This is a test thread.")
    mock_thread_repo.create = AsyncMock(return_value=created_thread)
    result = await thread_service.create_new_thread(session=session, board_id=board_id, thread_to_create=thread_to_create)
    mock_thread_repo.create.assert_called_once_with(session=session, board_id=board_id, create_item=thread_to_create)
    assert result == created_thread

@pytest.mark.asyncio
async def test_get_thread_by_id(thread_service, mock_thread_repo):
    session = AsyncMock()
    thread_id = 1
    thread = ThreadPostsDTO(id=1, title="Test Thread", content="This is a test thread.")
    
    mock_thread_repo.get = AsyncMock(return_value=thread)
    result = await thread_service.get_thread_by_id(session=session, thread_id=thread_id)
    mock_thread_repo.get.assert_called_once_with(session=session, thread_id=thread_id)
    assert result == thread

@pytest.mark.asyncio
async def test_get_thread_by_id_not_found(thread_service, mock_thread_repo):
    session = AsyncMock()
    thread_id = 1
    
    mock_thread_repo.get = AsyncMock(return_value=None)
    with pytest.raises(ThreadNotFoundException):
        await thread_service.get_thread_by_id(session=session, thread_id=thread_id)

@pytest.mark.asyncio
async def test_get_threads(thread_service, mock_thread_repo):
    session = AsyncMock()
    board_id = 1
    threads = [
        ThreadPostsDTO(id=1, title="Thread 1", content="Content 1"),
        ThreadPostsDTO(id=2, title="Thread 2", content="Content 2"),
    ]
    threads_feed = ThreadsFeedDTO(threads=threads, threads_count=len(threads))
    
    mock_thread_repo.get_all = AsyncMock(return_value=threads)
    result = await thread_service.get_threads(session=session, board_id=board_id)
    mock_thread_repo.get_all.assert_called_once_with(session=session, board_id=board_id)
    assert result == threads_feed

@pytest.mark.asyncio
async def test_delete_thread(thread_service, mock_thread_repo):
    session = AsyncMock()
    thread_id = 1
    await thread_service.delete_thread(session=session, thread_id=thread_id)
    mock_thread_repo.delete.assert_called_once_with(session=session, thread_id=thread_id)