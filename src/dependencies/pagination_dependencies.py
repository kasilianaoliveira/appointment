from fastapi_pagination import Params


def get_pagination_params(
    page: int = 1,
    size: int = 20,
) -> Params:
    """
    Dependency function to get pagination parameters with default size of 20.

    Args:
        page: Page number (default: 1)
        size: Page size (default: 20)

    Returns:
        Params object with page and size
    """
    return Params(page=page, size=size)
