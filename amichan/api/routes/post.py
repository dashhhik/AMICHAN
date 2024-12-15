from fastapi import APIRouter

from amichan.api.schemas.requests.post import PostCreateRequest
from amichan.api.schemas.responses.post import PostResponse
from fastapi.responses import RedirectResponse
from amichan.api.schemas.responses.thread import ThreadFeedResponse, ThreadResponse
from amichan.core.dependencies import (
    DBSession,
    IPostService,
    CurrentUser,
)

router = APIRouter()


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
        post_id: int,
        session: DBSession,
        post_service: IPostService,
) -> PostResponse:
    """
    Get post by id.
    """
    post_dto = await post_service.get_post_by_id(
        session=session, post_id=post_id
    )
    return PostResponse.from_dto(dto=post_dto)


@router.post("/{thread_id}/posts", response_model=PostResponse)
async def create_post(
        thread_id: int,
        payload: PostCreateRequest,
        session: DBSession,
        current_user: CurrentUser,
        post_service: IPostService,
) -> PostResponse:
    """
    Create new post.
    """
    if current_user is None:
        RedirectResponse(url="/auth/login")
    post_dto = await post_service.create_new_post(
        session=session,
        thread_id=thread_id,
        post_create_dto=payload,
    )
    return PostResponse.from_dto(dto=post_dto)
