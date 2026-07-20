import msal
import structlog
from core.config import get_settings
from core.exceptions import AuthenticationException

logger = structlog.get_logger(__name__)

class MSALAuthService:
    def __init__(self):
        self.settings = get_settings()
        authority = f"https://login.microsoftonline.com/{self.settings.tenant_id}"
        
        self.app = msal.ConfidentialClientApplication(
            self.settings.client_id,
            authority=authority,
            client_credential=self.settings.client_secret
        )

    def exchange_sso_for_graph_token(self, sso_token: str, scopes: list = ["https://graph.microsoft.com/.default"]) -> str:
        """
        Exchange the Office Add-in SSO token for an OBO Graph API token.
        """
        try:
            logger.info("Initiating OBO flow to acquire Graph Token")
            result = self.app.acquire_token_on_behalf_of(
                user_assertion=sso_token,
                scopes=scopes
            )
            
            if "access_token" in result:
                return result["access_token"]
            else:
                error_desc = result.get("error_description", "Unknown error")
                logger.error("OBO flow failed", error=error_desc, full_result=result)
                raise AuthenticationException(f"Failed to acquire Graph token: {error_desc}")
        except Exception as e:
            logger.error("Exception during OBO flow", error=str(e))
            raise AuthenticationException("Error exchanging SSO token for Graph token")

auth_service = MSALAuthService()
