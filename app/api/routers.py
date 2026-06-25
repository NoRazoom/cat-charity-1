from fastapi import APIRouter

from app.api.endpoints import donation_router, project_router


main_router = APIRouter()

main_router.include_router(
    donation_router, prefix='/donation', tags=['donations']
)

main_router.include_router(
    project_router, prefix='/charity_project', tags=['charity_projects']
)