from pathlib import Path

from fastapi_cli import cli

from src.core.settings import get_settings

if __name__ == "__main__":
    settings = get_settings()

    cli.run(
        Path("src/app.py"),
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        proxy_headers=True,
    )
