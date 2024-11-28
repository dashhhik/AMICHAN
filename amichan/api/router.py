from fastapi import APIRouter

from amichan.api.routes import board, thread

router = APIRouter()

router.include_router(router=thread.router, prefix="/thread", tags=["thread"])
router.include_router(router=board.router, prefix="/board", tags=["board"])
