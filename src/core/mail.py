import resend

from core.settings import get_settings


def _get_resend_api_key() -> str:
    """Obtém a API key do Resend do ambiente ou das configurações."""

    settings = get_settings()
    if settings.RESEND_API_KEY:
        return settings.RESEND_API_KEY.get_secret_value()

    raise ValueError(
        "RESEND_API_KEY não está configurada. "
        "Defina a variável de ambiente RESEND_API_KEY ou adicione no arquivo .env"
    )


def _init_resend():
    """Inicializa a API key do Resend."""
    try:
        resend.api_key = _get_resend_api_key()
    except ValueError:
        # Não falha na importação, apenas quando tentar enviar
        pass


def send_signup_success_email(to: str, user_name: str):
    settings = get_settings()

    if not settings.RESEND_TEMPLATE_SIGNUP_SUCCESS:
        raise ValueError("RESEND_TEMPLATE_SIGNUP_SUCCESS não configurado")

    return send_email(
        to=to,
        template_id=settings.RESEND_TEMPLATE_SIGNUP_SUCCESS,
        template_variables={
            "USER_NAME": user_name,
        },
    )


def send_email(
    to: str,
    subject: str | None = None,
    from_email: str | None = None,
    template_id: str | None = None,
    template_variables: dict | None = None,
) -> resend.Emails.SendResponse:
    if not resend.api_key:
        resend.api_key = _get_resend_api_key()

    settings = get_settings()
    params: resend.Emails.SendParams = {
        "from": from_email or settings.RESEND_FROM_EMAIL,
        "to": to,
    }

    if template_id:
        params["template"] = {
            "id": template_id,
            "variables": template_variables or {},
        }
        if subject:
            params["subject"] = subject

    return resend.Emails.send(params)


_init_resend()
