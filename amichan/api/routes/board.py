from fastapi import APIRouter

from amichan.api.schemas.requests.thread import CreateThreadRequest
from amichan.api.schemas.responses.board import BoardsResponse
from amichan.api.schemas.responses.thread import ThreadFeedResponse, ThreadResponse
from amichan.core.dependencies import DBSession, IBoardsService, IThreadService

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
    thread_service: IThreadService,
) -> ThreadResponse:
    """
    Create new article.
    """
    thread_dto = await thread_service.create_new_thread(
        session=session,
        author_nickname=payload.thread.nickname,
        thread_to_create=payload.to_dto(),
    )
    return ThreadResponse.from_dto(dto=thread_dto)
