# # pylint: disable=C0301
# from typing import Annotated
#
# from src.application.modules.user.use_cases import UserGetByEmailOrUsernameUseCase, UserGetByIdUseCase
# from fastapi import Depends
#
# from src.application.dependencies.auth.creators import (
#     get_password_hash_service,
#     get_password_verify_service,
#     get_token_service,
# )
# from src.application.dependencies.user_factories import (
#     get_user_repository,
#     get_user_get_by_id_use_case,
#     get_user_by_email_or_username_use_case,
# )
# from src.application.modules.auth.services import LoginService, PasswordHashService, PasswordVerifyService, \
#     PasswordChangeService, TokenService
# from src.application.modules.user.repositories import IUserRepository
#
#
# def get_password_change_service(
#     get_by_id_use_case: Annotated[
#         UserGetByIdUseCase, Depends(get_user_get_by_id_use_case)
#     ],
#     user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
#     hash_service: Annotated[PasswordHashService, Depends(get_password_hash_service)],
#     verify_service: Annotated[
#         PasswordVerifyService, Depends(get_password_verify_service)
#     ],
# ) -> PasswordChangeService:
#     return PasswordChangeService(
#         user_repository=user_repository,
#         get_by_id_use_case=get_by_id_use_case,
#         hash_service=hash_service,
#         verify_service=verify_service,
#     )
#
#
# def get_login_service(
#     verify_service: Annotated[
#         PasswordVerifyService, Depends(get_password_verify_service)
#     ],
#     token_service: Annotated[TokenService, Depends(get_token_service)],
#     user_get_by_email_or_username_use_case: Annotated[
#         UserGetByEmailOrUsernameUseCase, Depends(get_user_by_email_or_username_use_case)
#     ],
# ) -> LoginService:
#     return LoginService(
#         verify_service=verify_service,
#         token_service=token_service,
#         user_get_by_email_or_username_use_case=user_get_by_email_or_username_use_case,
#     )
