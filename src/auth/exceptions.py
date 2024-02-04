from fastapi import HTTPException, status



class InvalidCredentials(HTTPException):

    def __init__(
            self,
            status_code: int = status.HTTP_401_UNAUTHORIZED, 
            detail: str = 'Invalid username or password'
        ) -> None:
        super().__init__(status_code, detail)


class InactiveUser(HTTPException):

    def __init__(
            self,
            status_code: int = status.HTTP_403_FORBIDDEN, 
            detail: str = 'Inactive user'
        ) -> None:
        super().__init__(status_code, detail)


class InvalidToken(HTTPException):

    def __init__(
            self,
            status_code: int = status.HTTP_403_FORBIDDEN, 
            detail: str = 'Invalid token error'
        ) -> None:
        super().__init__(status_code, detail)