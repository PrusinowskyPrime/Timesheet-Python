from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from src.application.modules.common.responses import ErrorResponse
from src.application.modules.project.dtos import (
    ProjectCreateDTO,
    ProjectUpdateDTO,
    ProjectDTO,
)
from src.application.modules.project.services import (
    ProjectService,
)
from src.dependencies.project_factories import get_project_service

router = APIRouter(prefix="/api/v1/projects", tags=["APIv1 Project"])


@router.post(
    "/",
    response_model=ProjectDTO,
    responses={
        201: {"model": ProjectDTO},
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    request: ProjectCreateDTO,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    return await project_service.create(ProjectCreateDTO(**request.model_dump()))


@router.put(
    "/{project_id}",
    response_model=ProjectDTO,
    responses={
        200: {"model": ProjectDTO},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
)
async def update_project(
    project_id: int,
    request: ProjectUpdateDTO,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    return await project_service.update(project_id=project_id, request_dto=request)


@router.delete(
    "/{project_id}",
    responses={204: {"model": None}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: int,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    return await project_service.delete(project_id)


# @router.get(
#     "/owned/",
#     response_model=List[ProjectDTO],
#     responses={
#         200: {"model": List[ProjectDTO]},
#         401: {"model": ErrorResponse},
#     },
#     status_code=status.HTTP_200_OK,
# )
# async def get_by_owner_id_projects(
#     current_user: Annotated[CurrentUserDTO, Depends(get_current_user)],
#     project_service: Annotated[ProjectService, Depends(get_project_service)],
# ):
#     return await project_service.get_by_owner_id(current_user.id)


@router.get(
    "/",
    response_model=List[ProjectDTO],
    responses={200: {"model": List[ProjectDTO]}},
    status_code=status.HTTP_200_OK,
)
async def get_all_projects(
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    return await project_service.get_all()


@router.get(
    "/{project_id}",
    response_model=ProjectDTO,
    responses={200: {"model": ProjectDTO}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
)
async def get_by_id(
    project_id: int,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    return await project_service.get_by_id(project_id)
