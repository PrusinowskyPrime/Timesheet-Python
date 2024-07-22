from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from src.application.dependencies.user_factories import (
    get_user_service,
)
from src.application.modules.common.responses import ErrorResponse
from src.application.modules.user.dtos import (
    UserCreateDTO,
    UserUpdateDTO,
)
from src.application.modules.user.requests import (
    UserCreateRequest,
    UserUpdateRequest,
)
from src.application.modules.user.services import UserService

from src.application.modules.user.dtos import UserGetDTO

router = APIRouter(prefix="/api/v1/users", tags=["APIv1 User"])


@router.post(
    "/",
    response_model=UserGetDTO,
    responses={201: {"model": UserGetDTO}, 409: {"model": ErrorResponse}},
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: UserCreateRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create(
        UserCreateDTO(**request.model_dump(exclude={"password_confirmation"}))
    )


@router.put(
    "/{user_id}",
    response_model=UserGetDTO,
    responses={200: {"model": UserGetDTO}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: str,
    request: UserUpdateRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.update(
        user_id=user_id, request_dto=UserUpdateDTO(**request.model_dump())
    )


@router.delete(
    "/{user_id}",
    responses={204: {"model": None}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.delete(user_id)


@router.get(
    "/",
    response_model=List[UserGetDTO],
    responses={200: {"model": List[UserGetDTO]}},
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_all()


@router.get(
    "/{user_id}",
    response_model=UserGetDTO,
    responses={200: {"model": UserGetDTO}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
)
async def get_by_id(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_by_id(user_id)
