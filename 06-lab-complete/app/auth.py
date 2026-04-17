from fastapi import Header, HTTPException, status
from app.config import settings


def verify_bearer_token(authorization: str | None = Header(default=None)) -> str:
    """
    Xác thực Bearer token đơn giản.
    Header dạng:
    Authorization: Bearer your_token
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header."
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization format."
        )

    token = authorization.replace("Bearer ", "", 1).strip()

    if token != settings.API_BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )

    return token