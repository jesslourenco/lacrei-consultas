import re
import bleach
from django.core.exceptions import ValidationError
from email_validator import validate_email, EmailNotValidError

REGEX_CEP = re.compile(r"^\d{5}-\d{3}$")  # Format: XXXXX-XXX
STRICT_EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def email_validator(email: str) -> None:
    """Valida emails usando uma regex e email_validator."""
    if not email or not STRICT_EMAIL_REGEX.match(email):
        raise ValidationError("Formato de email inválido.")

    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        raise ValidationError("Formato de email inválido")
    
def cep_validator(cep: str) -> None:
    """Valida fromato do CEP (XXXXX-XXX)."""
    if not REGEX_CEP.match(cep):
        raise ValidationError("Formato de CEP inválido. Use XXXXX-XXX.")

def sanitize_text(text: str) -> str:
    """Sanitiza inputs de texto, removendo possiveis HTML perigosos."""
    return bleach.clean(text, tags=[], strip=True)

def sanitize_fields(instance, fields: list[str]) -> None:
    """Sanitiza varios campos de uma instancia Model."""
    for field in fields:
        value = getattr(instance, field, None)
        if value:
            setattr(instance, field, sanitize_text(value))
