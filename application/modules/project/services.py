# pylint: disable=R0801, R0913
from typing import List

from app.application.modules.project.dtos import (
    ProjectCreateDTO,
    ProjectUpdateDTO,
    ProjectWithOwnerDTO,
)
from app.application.modules.project.use_cases import ProjectCreateUseCase, ProjectDeleteUseCase, ProjectGetAllUseCase, \
    ProjectGetByIdUseCase, ProjectGetByOwnerIdUseCase, ProjectLoadOwnerUseCase, ProjectUpdateUseCase


class ProjectService:
    def __init__(
        self,
        create_use_case: ProjectCreateUseCase,
        delete_use_case: ProjectDeleteUseCase,
        update_use_case: ProjectUpdateUseCase,
        get_all_use_case: ProjectGetAllUseCase,
        get_by_id_use_case: ProjectGetByIdUseCase,
        get_by_owner_id: ProjectGetByOwnerIdUseCase,
        load_owner_use_case: ProjectLoadOwnerUseCase,
    ):
        self._create_use_case = create_use_case
        self._delete_use_case = delete_use_case
        self._update_use_case = update_use_case
        self._get_all_use_case = get_all_use_case
        self._get_by_id_use_case = get_by_id_use_case
        self._get_by_owner_id = get_by_owner_id
        self._load_owner_use_case = load_owner_use_case

    async def create(self, request_dto: ProjectCreateDTO) -> ProjectWithOwnerDTO:
        project = await self._create_use_case.execute(request_dto)

        return await self._load_owner_use_case.execute(project)

    async def update(
        self, project_id: str, request_dto: ProjectUpdateDTO
    ) -> ProjectWithOwnerDTO:
        project = await self._update_use_case.execute(
            request_dto=request_dto, project_id=project_id
        )

        return await self._load_owner_use_case.execute(project)

    async def delete(self, project_id: str) -> None:
        return await self._delete_use_case.execute(project_id)

    async def get_all(self, name: str | None = None) -> List[ProjectWithOwnerDTO]:
        projects = await self._get_all_use_case.execute(name)

        return [
            await self._load_owner_use_case.execute(project) for project in projects
        ]

    async def get_by_id(self, project_id: str) -> ProjectWithOwnerDTO:
        project = await self._get_by_id_use_case.execute(project_id)

        return await self._load_owner_use_case.execute(project)

    async def get_by_owner_id(self, owner_id: str) -> List[ProjectWithOwnerDTO]:
        projects = await self._get_by_owner_id.execute(owner_id)

        return [
            await self._load_owner_use_case.execute(project) for project in projects
        ]
