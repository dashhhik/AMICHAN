# import abc
#
# from amichan.domain.dtos.jwt import AuthTokenDTO, JWTUserDTO

#
# class IJWTTokenService(abc.ABC):
#
#     @abc.abstractmethod
#     def generate_token(self, user: UserDTO) -> AuthTokenDTO: ...
#
#     @abc.abstractmethod
#     def get_user_info_from_token(self, auth_token: AuthTokenDTO) -> JWTUserDTO: ...
