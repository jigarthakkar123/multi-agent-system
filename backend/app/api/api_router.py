from fastapi import APIRouter
from .auth import router as auth_router
from .profile import router as profile_router
from .dataset import router as dataset_router
from .analytics import router as analytics_router
from .agents import router as agents_router
from .approvals import router as approvals_router
from .reports import router as reports_router
from .chat import router as chat_router
from .users import router as users_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(profile_router)
api_router.include_router(dataset_router)
api_router.include_router(analytics_router)
api_router.include_router(agents_router)
api_router.include_router(approvals_router)
api_router.include_router(reports_router)
api_router.include_router(chat_router)
