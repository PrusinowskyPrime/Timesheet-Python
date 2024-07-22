# from typing import Annotated
#
# from fastapi import Depends
#
# from src.application.dependencies.auth.creators import get_token_service
# from src.application.modules.auth.dtos import CurrentUserDTO
# from src.application.modules.auth.services import TokenService
# from src.settings.oauth2 import oauth2_scheme
#
#
# def get_current_user(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     token_service: Annotated[TokenService, Depends(get_token_service)],
# ) -> CurrentUserDTO:
#     return token_service.decode(token)
