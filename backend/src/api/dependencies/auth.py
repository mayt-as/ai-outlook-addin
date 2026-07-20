from fastapi import Request, Security
from fastapi.security import OAuth2PasswordBearer
from core.exceptions import AuthenticationException
from services.auth.msal_service import auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_graph_token(request: Request, sso_token: str = Security(oauth2_scheme)) -> str:
    """
    Dependency that extracts the SSO token from the Authorization header 
    and exchanges it for a Microsoft Graph access token.
    """
    if not sso_token:
        raise AuthenticationException("Missing SSO token in Authorization header")
    return auth_service.exchange_sso_for_graph_token(sso_token)
