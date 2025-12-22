class BaseAppException(Exception):
    """Base exception class for all custom application exceptions."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        detail: str | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail or message
        super().__init__(self.message)
