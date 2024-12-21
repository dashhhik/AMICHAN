from fastapi import APIRouter, HTTPException

from amichan.api.schemas.responses.thread import ThreadResponse, ThreadPostsResponse
from amichan.core.dependencies import DBSession, IThreadService, CurrentUser
from amichan.core.exceptions import ThreadNotFoundException

router = APIRouter()


@router.get("/{thread_id}", response_model=ThreadPostsResponse)
async def get_thread(
    thread_id: int,
    session: DBSession,
    thread_service: IThreadService,
) -> ThreadPostsResponse:
    """
    Get thread by id.
    """
    try:
        thread_dto = await thread_service.get_thread_by_id(
            session=session, thread_id=thread_id
        )
        return ThreadPostsResponse.from_dto(dto=thread_dto)
    except ThreadNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{thread_id}")
async def delete_thread(
    current_user: CurrentUser,
    thread_id: int,
    session: DBSession,
    thread_service: IThreadService,
) -> None:
    """
    Delete thread by id.
    """
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if current_user.role_id == 4:
        raise HTTPException(status_code=403, detail="Forbidden")
    await thread_service.delete_thread(session=session, thread_id=thread_id)
