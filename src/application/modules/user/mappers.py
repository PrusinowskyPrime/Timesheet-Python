from src.application.modules.user.dtos import UserGetDTO, UserDTO

from application.modules.user.dtos import UserCreateDTO
from application.modules.user.models import UserModel


class UserModelToDomainMapper:
    def map(self, model: UserModel) -> UserDTO:
        return UserDTO(
            id=model.id,
            fullname=model.id,
            email=model.email,
            password=model.password
        )


class UserDomainToModelMapper:
    def map(self, dto: UserDTO) -> UserModel:
        return UserModel(
            id=dto.id,
            fullname=dto.id,
            email=dto.email,
            password=dto.password
        )

class UserCreateDTOToDomainMapper:
    def map(self, dto: UserCreateDTO) -> UserDTO:
        return UserDTO(
            id=0,
            fullname=dto.fullname,
            email=dto.email,
            password=''
        )
