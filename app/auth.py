from __future__ import annotations

from datetime import UTC, datetime, timedelta
from functools import wraps
from typing import Any, Callable

import jwt
from flask import current_app, g, jsonify, request

from . import repositories


def _error(message: str, status_code: int):
    return jsonify({"error": message}), status_code


def _extract_token() -> str | None:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header.removeprefix("Bearer ").strip()
    return token or None


def create_access_token(user: dict[str, Any]) -> str:
    now = datetime.now(UTC)
    expires_at = now + timedelta(hours=current_app.config["JWT_EXPIRES_IN_HOURS"])
    payload = {
        "sub": str(user["id"]),
        "email": user["email"],
        "plan": user["plan"],
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGORITHM"],
    )


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        current_app.config["JWT_SECRET_KEY"],
        algorithms=[current_app.config["JWT_ALGORITHM"]],
    )


def auth_required(view: Callable):
    @wraps(view)
    def wrapped(*args, **kwargs):
        token = _extract_token()
        if not token:
            return _error("Missing Bearer token.", 401)

        try:
            payload = decode_access_token(token)
        except jwt.ExpiredSignatureError:
            return _error("Token has expired.", 401)
        except jwt.InvalidTokenError:
            return _error("Invalid token.", 401)

        user = repositories.get_user(str(payload["sub"]))
        if not user:
            return _error("Authenticated user no longer exists.", 401)

        g.current_user = user
        g.current_user_id = str(user["id"])
        g.jwt_payload = payload
        return view(*args, **kwargs)

    return wrapped
