from fastapi import APIRouter

from amichan.api.routes import board, thread, auth, post

router = APIRouter()

router.include_router(router=thread.router, prefix="/thread", tags=["thread"])
router.include_router(router=board.router, prefix="/board", tags=["board"])
router.include_router(router=auth.router, prefix="/auth", tags=["auth"])
router.include_router(router=post.router, prefix="/post", tags=["post"])
