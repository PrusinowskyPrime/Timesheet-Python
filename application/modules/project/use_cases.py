from typing import List

from app.application.modules.project.dtos import ProjectCreateDTO, ProjectWithOwnerDTO, ProjectUpdateDTO, ProjectDTO
from app.application.modules.project.mappers import ProjectDTOToWithOwnerMapper
from app.application.modules.user.mappers import UserDTOToGetMapper
from app.application.modules.user.use_cases import UserGetByIdUseCase
from app.application.modules.common.exceptions import ObjectDoesNotExist
from app.application.modules.project.repositories import IProjectRepository


class ProjectCreateUseCase:
    def __init__(self, repository: IProjectRepository):
        self._repository = repository

    async def execute(self, request_dto: ProjectCreateDTO) -> ProjectDTO:
        project_dto = ProjectDTO(**request_dto.model_dump(), records=[], _id=None)
        return await self._repository.save(project_dto)


class ProjectGetAllUseCase:
    def __init__(self, repository: IProjectRepository):
        self._repository = repository

    async def execute(self, name: str | None = None) -> List[ProjectDTO]:
        return await self._repository.get_all(name)


class ProjectGetByIdUseCase:
    def __init__(self, repository: IProjectRepository):
        self._repository = repository

    async def execute(self, project_id: str) -> ProjectDTO:
        project = await self._repository.get_by_id(project_id=project_id)

        if project is None:
            raise ObjectDoesNotExist

        return project


class ProjectDeleteUseCase:
    def __init__(
        self, repository: IProjectRepository, get_by_id_use_case: ProjectGetByIdUseCase
    ):
        self._repository = repository
        self._get_by_id_use_case = get_by_id_use_case

    async def execute(self, project_id: str) -> None:
        await self._get_by_id_use_case.execute(project_id)

        return await self._repository.delete(project_id=project_id)


class ProjectGetByOwnerIdUseCase:
    def __init__(self, repository: IProjectRepository):
        self._repository = repository

    async def execute(self, owner_id: str) -> List[ProjectDTO]:
        return await self._repository.get_by_owner_id(owner_id)


class ProjectLoadOwnerUseCase:
    def __init__(
        self,
        project_dto_to_with_owner_mapper: ProjectDTOToWithOwnerMapper,
        user_dto_to_get_mapper: UserDTOToGetMapper,
        user_get_by_id_use_case: UserGetByIdUseCase,
    ):
        self._project_dto_to_with_owner_mapper = project_dto_to_with_owner_mapper
        self._user_dto_to_get_mapper = user_dto_to_get_mapper
        self._user_get_by_id_use_case = user_get_by_id_use_case

    async def execute(self, project: ProjectDTO) -> ProjectWithOwnerDTO:
        user = await self._user_get_by_id_use_case.execute(project.owner_id)

        mapped_project = self._project_dto_to_with_owner_mapper.map(project)
        mapped_project.owner = self._user_dto_to_get_mapper.map(user)

        return mapped_project


class ProjectUpdateUseCase:
    def __init__(
        self, repository: IProjectRepository, get_by_id_use_case: ProjectGetByIdUseCase
    ):
        self._repository = repository
        self._get_by_id_use_case = get_by_id_use_case

    async def execute(
        self, request_dto: ProjectUpdateDTO, project_id: str
    ) -> ProjectDTO:
        project_dto = await self._get_by_id_use_case.execute(project_id)
        for key, value in request_dto.model_dump().items():
            setattr(project_dto, key, value)

        return await self._repository.update(project_dto)
