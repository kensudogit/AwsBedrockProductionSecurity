"""Cognito access-token protected FastAPI skeleton. No direct Bedrock call."""
import os
from functools import lru_cache
from typing import Annotated

import jwt
from jwt import PyJWKClient
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

app = FastAPI(title="Bedrock protected API skeleton")
bearer = HTTPBearer(auto_error=False)


@lru_cache
def settings():
    region = os.environ.get("AWS_REGION", "")
    pool = os.environ.get("COGNITO_USER_POOL_ID", "")
    client = os.environ.get("COGNITO_APP_CLIENT_ID", "")
    if not (region and pool and client):
        raise RuntimeError("Cognito configuration missing; refusing authentication")
    issuer = f"https://cognito-idp.{region}.amazonaws.com/{pool}"
    return issuer, client


@lru_cache
def jwks_client(issuer: str):
    return PyJWKClient(f"{issuer}/.well-known/jwks.json", cache_keys=True)


def verify_access_token(token: str) -> dict:
    try:
        issuer, client = settings()
        key = jwks_client(issuer).get_signing_key_from_jwt(token).key
        claims = jwt.decode(
            token, key, algorithms=["RS256"], issuer=issuer,
            options={"verify_aud": False, "require": ["exp", "iat", "iss", "sub", "token_use", "client_id"]},
            leeway=30,
        )
        if claims.get("token_use") != "access" or claims.get("client_id") != client:
            raise ValueError("invalid token type or client")
        return claims
    except (jwt.PyJWTError, ValueError, RuntimeError, OSError) as exc:
        raise HTTPException(status_code=401, detail="Invalid access token") from exc


def principal(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]) -> dict:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Authentication required")
    return verify_access_token(credentials.credentials)


def require_scope(scope: str):
    def dependency(user: Annotated[dict, Depends(principal)]) -> dict:
        if scope not in user.get("scope", "").split():
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return dependency


class PromptRequest(BaseModel):
    prompt: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/generate")
def generate(payload: PromptRequest, user: Annotated[dict, Depends(require_scope("genai/invoke"))]):
    # Replace with Bedrock call from server-side IAM role after quotas, tenant policy,
    # moderation, audit metadata, timeout and model access checks are implemented.
    return {"status": "authenticated", "subject": user["sub"], "note": "Bedrock integration not enabled in skeleton"}
