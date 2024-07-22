# # pylint: disable=R0801, R0913
# from typing import List
#
# from src.application.modules.project.dtos import (
#     ProjectCreateDTO,
#     ProjectUpdateDTO,
#     ProjectDTO,
# )
# from src.application.modules.project.repositories import IProjectRepository
# from src.application.modules.time_log.dtos import TimeLogDTO
#
#
# class ProjectService:
#     def __init__(self, repository: IProjectRepository):
#         self._repository = repository
#
#     async def create(self, request_dto: ProjectCreateDTO) -> ProjectDTO:
#         project_dto = ProjectDTO(**request_dto.model_dump(), time_logs=[], _idF=None)
#
#         return await self._repository.save(project_dto)
#
#     async def update(self, project_id: str, request_dto: ProjectUpdateDTO) -> ProjectDTO:
#         return await self._repository.update(
#             ProjectDTO(**request_dto.model_dump() | {"_id": project_id})
#         )
#
#     async def delete(self, project_id: str) -> None:
#         return await self._repository.delete(project_id)
#
#     async def get_all(self, name: str | None = None) -> List[ProjectDTO]:
#         return await self._repository.get_all(name)
#
#     async def get_by_id(self, project_id: str) -> ProjectDTO:
#         return await self._repository.get_by_id(project_id)
#
#     async def get_by_owner_id(self, owner_id: str) -> List[ProjectDTO]:
#         return await self._repository.get_by_owner_id(owner_id)
#
#     async def add_time_log(self, project_id: str, time_log: TimeLogDTO) -> ProjectDTO:
#         return await self._repository.add_time_log(project_id, time_log)
#
#     async def delete_time_log(self, project_id: str, time_log_id: str) -> ProjectDTO:
#         return await self._repository.delete_time_log(project_id, time_log_id)
#
#     async def update_time_log(self, project_id: str, time_log: TimeLogDTO) -> ProjectDTO:
#         return await self._repository.update_time_log(project_id, time_log)
