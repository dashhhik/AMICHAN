from fastapi import APIRouter, HTTPException

from amichan.api.schemas.requests.board import BoardCreateRequest
from amichan.api.schemas.requests.thread import CreateThreadRequest
from amichan.api.schemas.responses.board import BoardsResponse
from fastapi.responses import RedirectResponse
from amichan.api.schemas.responses.thread import ThreadFeedResponse, ThreadResponse
from amichan.core.dependencies import (
    DBSession,
    IBoardsService,
    IThreadService,
    CurrentUser,
)

router = APIRouter()


@router.get("/", response_model=BoardsResponse)
async def get_boards(
    session: DBSession,
    boards_service: IBoardsService,
) -> BoardsResponse:
    """
    Get board by id.
    """
    board_dto = await boards_service.get_boards(
        session=session,
    )
    return BoardsResponse.from_dto(dto=board_dto)


@router.get("/{board_id}/threads", response_model=ThreadFeedResponse)
async def get_board_threads(
    board_id: int,
    session: DBSession,
    thread_service: IThreadService,
) -> ThreadFeedResponse:
    """
    Get threads for a board.
    """
    thread_dto = await thread_service.get_threads(
        session=session,
        board_id=board_id,
    )
    return ThreadFeedResponse.from_dto(dto=thread_dto)


@router.post("/{board_id}/threads", response_model=ThreadResponse)
async def create_thread(
    payload: CreateThreadRequest,
    session: DBSession,
    current_user: CurrentUser,
    thread_service: IThreadService,
) -> ThreadResponse:
    """
    Create new article.
    """
    if current_user is None:
        RedirectResponse(url="/auth/login")
    thread_dto = await thread_service.create_new_thread(
        session=session,
        author_nickname=payload.thread.nickname,
        thread_to_create=payload.to_dto(),
    )
    return ThreadResponse.from_dto(dto=thread_dto)


@router.delete("/{thread_id}")
async def delete_thread(
    current_user: CurrentUser,
    thread_id: int,
    session: DBSession,
    thread_service: IThreadService,
) -> None:
    """
    Delete a thread.
    """
    if current_user is None:
        RedirectResponse(url="/auth/login")
    if current_user.role_id == 4:
        HTTPException(status_code=403, detail="Forbidden")
    await thread_service.delete_thread(
        session=session,
        thread_id=thread_id,
    )
    return None


@router.post("/")
async def create_board(
    current_user: CurrentUser,
    session: DBSession,
    boards_service: IBoardsService,
    payload: BoardCreateRequest,
):
    """
    Create a new board.
    """
    if current_user is None:
        RedirectResponse(url="/auth/login")
    if current_user.role_id == 4:
        HTTPException(status_code=403, detail="Forbidden")
    await boards_service.create_new_board(
        session=session,
        board_name=payload.board.name,
        board_description=payload.board.description,
    )
    return {"message": "Board created"}


@router.delete("/{board_id}")
async def delete_board(
    current_user: CurrentUser,
    board_id: int,
    session: DBSession,
    boards_service: IBoardsService,
) -> None:
    """
    Delete a board.
    """
    if current_user is None:
        RedirectResponse(url="/auth/login")
    if current_user.role_id == 4:
        HTTPException(status_code=403, detail="Forbidden")
    await boards_service.delete_board(
        session=session,
        board_id=board_id,
    )
    return None
