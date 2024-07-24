from src.application.modules.user.dtos import UserGetDTO, UserDTO

from src.application.modules.user.dtos import UserCreateDTO
from src.application.modules.user.models import UserModel


class UserModelToDomainMapper:
    def map(self, model: UserModel) -> UserDTO:
        return UserDTO(
            id=model.id,
            fullname=model.fullname,
            email=model.email,
            password=model.password
        )


class UserDomainToModelMapper:
    def map(self, dto: UserDTO) -> UserModel:
        return UserModel(
            id=dto.id,
            fullname=dto.fullname,
            email=dto.email,
            password=dto.password
        )

class UserCreateDTOToDomainMapper:
    def map(self, dto: UserCreateDTO) -> UserDTO:
        return UserDTO(
            id=None,
            fullname=dto.fullname,
            email=dto.email,
            password=''
        )
