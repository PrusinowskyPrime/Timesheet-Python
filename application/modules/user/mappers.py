from app.application.modules.user.dtos import UserGetDTO, UserDTO


class UserDTOToGetMapper:
    def map(self, dto: UserDTO) -> UserGetDTO:
        return UserGetDTO(**dto.model_dump())
