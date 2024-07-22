# from typing import Annotated, List
#
# from fastapi import APIRouter, Depends, status
#
# from src.application.dependencies.auth.permissions import get_current_user
# from src.application.dependencies.project_factories import get_project_service
# from src.application.modules.auth.dtos import CurrentUserDTO
# from src.application.modules.common.responses import ErrorResponse
# from src.application.modules.project.dtos import (
#     ProjectCreateDTO,
#     ProjectUpdateDTO, ProjectDTO,
# )
# from src.application.modules.project.requests import (
#     ProjectCreateRequest,
#     ProjectUpdateRequest,
# )
# from src.application.modules.project.responses import (
#     ProjectBaseResponse,
# )
# from src.application.modules.project.services import (
#     ProjectService,
# )
# from src.application.modules.time_log.dtos import TimeLogDTO
#
# router = APIRouter(prefix="/api/v1/projects", tags=["APIv1 Project"])
#
#
# @router.post(
#     "/",
#     response_model=ProjectBaseResponse,
#     responses={
#         201: {"model": ProjectBaseResponse},
#         404: {"model": ErrorResponse},
#         401: {"model": ErrorResponse},
#     },
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_project(
#     current_user: Annotated[CurrentUserDTO, Depends(get_current_user)],
#     request: ProjectCreateRequest,
#     project_service: Annotated[ProjectService, Depends(get_project_service)],
# ):
#     return await project_service.create(
#         ProjectCreateDTO(**request.model_dump() | {"owner_id": current_user.id})
#     )
#
#
# @router.put(
#     "/{project_id}",
#     response_model=ProjectBaseResponse,
#     responses={
#         200: {"model": ProjectBaseResponse},
#         404: {"model": ErrorResponse},
#     },
#     status_code=status.HTTP_200_OK,
# )
# async def update_project(
#     project_id: str,
#     request: ProjectUpdateRequest,
#     project_service: Annotated[ProjectService, Depends(get_project_service)],
# ):
#     return await project_service.update(
#         project_id=project_id,
#         request_dto=ProjectUpdateDTO(**request.model_dump())
#     )
#
#
# @router.delete(
#     "/{project_id}",
#     responses={204: {"model": None}, 404: {"model": ErrorResponse}},
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_project(
#     project_id: str,
#     project_service: Annotated[ProjectService, Depends(get_project_service)],
# ):
#     return await project_service.delete(project_id)
#
#
# @router.get(
#     "/owned/",
#     response_model=List[ProjectBaseResponse],
#     responses={
#         200: {"model": List[ProjectBaseResponse]},
#         401: {"model": ErrorResponse},
#     },
#     status_code=status.HTTP_200_OK,
# )
# async def get_by_owner_id_projects(
#     current_user: Annotated[CurrentUserDTO, Depends(get_current_user)],
#     project_service: Annotated[ProjectService, Depends(get_project_service)],
# ):
#     return await project_service.get_by_owner_id(current_user.id)
#
#
# @router.get(
#     "/",
#     response_model=List[ProjectDTO],
#     responses={200: {"model": List[ProjectDTO]}},
#     status_code=status.HTTP_200_OK,
# )
# async def get_all_projects(
#     project_service: Annotated[ProjectService, Depends(get_project_service)],
#     name: str | None = None,
# ):
#     return await project_service.get_all(name)
#
#
# @router.get(
#     "/{project_id}",
#     response_model=ProjectBaseResponse,
#     responses={200: {"model": ProjectBaseResponse}, 404: {"model": ErrorResponse}},
#     status_code=status.HTTP_200_OK,
# )
# async def get_by_id(
#     project_id: str,
#     project_service: Annotated[ProjectService, Depends(get_project_service)],
# ):
#     return await project_service.get_by_id(project_id)
#
# @router.post(
#     "/{project_id}/time_logs",
#     response_model=ProjectBaseResponse,
#     responses={
#         200: {"model": ProjectBaseResponse},
#         404: {"model": ErrorResponse},
#     },
#     status_code=status.HTTP_200_OK,
# )
# async def add_time_log(
#     project_id: str,
#     time_log: TimeLogDTO,
#     project_service: Annotated[ProjectService, Depends(get_project_service)],
# ):
#     return await project_service.add_time_log(project_id, time_log)
#
#
# @router.delete(
#     "/{project_id}/time_logs/{time_log_id}",
#     response_model=ProjectBaseResponse,
#     responses={
#         200: {"model": ProjectBaseResponse},
#         404: {"model": ErrorResponse},
#     },
#     status_code=status.HTTP_200_OK,
# )
# async def delete_time_log(
#     project_id: str,
#     time_log_id: str,
#     project_service: Annotated[ProjectService, Depends(get_project_service)],
# ):
#     return await project_service.delete_time_log(project_id, time_log_id)
#
#
# @router.put(
#     "/{project_id}/time_logs/{time_log_id}",
#     response_model=ProjectBaseResponse,
#     responses={
#         200: {"model": ProjectBaseResponse},
#         404: {"model": ErrorResponse},
#     },
#     status_code=status.HTTP_200_OK,
# )
# async def update_time_log(
#     project_id: str,
#     time_log: TimeLogDTO,
#     project_service: Annotated[ProjectService, Depends(get_project_service)],
# ):
#     return await project_service.update_time_log(project_id, time_log)