import httpx
import structlog
from typing import Dict, Any, List
from core.exceptions import GraphAPIException

logger = structlog.get_logger(__name__)

class GraphService:
    def __init__(self):
        self.base_url = "https://graph.microsoft.com/v1.0"
        
    def _get_headers(self, token: str) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    async def get_message(self, token: str, message_id: str) -> Dict[str, Any]:
        """Fetch a specific email message"""
        url = f"{self.base_url}/me/messages/{message_id}"
        async with httpx.AsyncClient() as client:
            try:
                logger.info("Fetching message from Graph API", message_id=message_id)
                response = await client.get(url, headers=self._get_headers(token))
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error("Failed to fetch message", message_id=message_id, error=str(e))
                raise GraphAPIException(f"Failed to fetch message from Graph API: {str(e)}")

    async def get_thread(self, token: str, conversation_id: str) -> List[Dict[str, Any]]:
        """Fetch all messages in a conversation thread"""
        url = f"{self.base_url}/me/messages?$filter=conversationId eq '{conversation_id}'&$orderby=receivedDateTime asc"
        async with httpx.AsyncClient() as client:
            try:
                logger.info("Fetching thread from Graph API", conversation_id=conversation_id)
                response = await client.get(url, headers=self._get_headers(token))
                response.raise_for_status()
                return response.json().get("value", [])
            except httpx.HTTPError as e:
                logger.error("Failed to fetch thread", conversation_id=conversation_id, error=str(e))
                raise GraphAPIException(f"Failed to fetch thread from Graph API: {str(e)}")
                
    async def get_attachments(self, token: str, message_id: str) -> List[Dict[str, Any]]:
        """Fetch attachments for a specific message"""
        url = f"{self.base_url}/me/messages/{message_id}/attachments"
        async with httpx.AsyncClient() as client:
            try:
                logger.info("Fetching attachments from Graph API", message_id=message_id)
                response = await client.get(url, headers=self._get_headers(token))
                response.raise_for_status()
                return response.json().get("value", [])
            except httpx.HTTPError as e:
                logger.error("Failed to fetch attachments", message_id=message_id, error=str(e))
                raise GraphAPIException(f"Failed to fetch attachments from Graph API: {str(e)}")

graph_service = GraphService()
