from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from time_sheet.src.application.modules.record.dto.record import (
    RecordCreateDTO,
    RecordUpdateDTO,
)
from time_sheet.src.application.modules.record.services.record_service import RecordService
from time_sheet.src.core.modules.auth.dto.auth import CurrentUserDTO
from time_sheet.src.infrastructure.dependencies.auth.permissions import get_current_user
from time_sheet.src.infrastructure.dependencies.record.factories import (
    get_record_service,
)
from time_sheet.src.infrastructure.ports.api.v1.common.responses import ErrorResponse
from time_sheet.src.infrastructure.ports.api.v1.record.requests import (
    RecordCreateRequest,
    RecordUpdateRequest,
)
from time_sheet.src.infrastructure.ports.api.v1.record.responses import RecordBaseResponse

router = APIRouter(prefix="/api/v1/records", tags=["APIv1 Record"])


@router.post(
    "/",
    response_model=RecordBaseResponse,
    responses={
        201: {"model": RecordBaseResponse},
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_record(
    current_user: Annotated[CurrentUserDTO, Depends(get_current_user)],
    request: RecordCreateRequest,
    record_service: Annotated[RecordService, Depends(get_record_service)],
):
    return await record_service.create(
        RecordCreateDTO(**request.model_dump() | {"owner_id": current_user.id})
    )


@router.put(
    "/{record_id}",
    response_model=RecordBaseResponse,
    responses={200: {"model": RecordBaseResponse}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
)
async def update_record(
    record_id: str,
    request: RecordUpdateRequest,
    record_service: Annotated[RecordService, Depends(get_record_service)],
):
    return await record_service.update(
        record_id=record_id, request_dto=RecordUpdateDTO(**request.model_dump())
    )


@router.delete(
    "/{record_id}",
    responses={204: {"model": None}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_record(
    record_id: str,
    record_service: Annotated[RecordService, Depends(get_record_service)],
):
    return await record_service.delete(record_id)


@router.get(
    "/",
    response_model=List[RecordBaseResponse],
    responses={200: {"model": List[RecordBaseResponse]}},
    status_code=status.HTTP_200_OK,
)
async def get_all_records(
    record_service: Annotated[RecordService, Depends(get_record_service)],
):
    return await record_service.get_all()


@router.get(
    "/owned/",
    response_model=List[RecordBaseResponse],
    responses={
        200: {"model": List[RecordBaseResponse]},
        401: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
)
async def get_by_owner_id_records(
    current_user: Annotated[CurrentUserDTO, Depends(get_current_user)],
    record_service: Annotated[RecordService, Depends(get_record_service)],
):
    return await record_service.get_by_owner_id(current_user.id)


@router.get(
    "/{record_id}",
    response_model=RecordBaseResponse,
    responses={200: {"model": RecordBaseResponse}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
)
async def get_by_id(
    record_id: str,
    record_service: Annotated[RecordService, Depends(get_record_service)],
):
    return await record_service.get_by_id(record_id)
