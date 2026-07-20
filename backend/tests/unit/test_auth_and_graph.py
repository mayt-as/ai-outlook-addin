import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from services.auth.msal_service import MSALAuthService
from services.graph.graph_client import GraphService

def test_msal_obo_flow_success():
    auth = MSALAuthService()
    auth.app.acquire_token_on_behalf_of = MagicMock(return_value={"access_token": "graph_token_123"})
    token = auth.exchange_sso_for_graph_token("sso_token_456")
    assert token == "graph_token_123"

@pytest.mark.asyncio
async def test_graph_get_message():
    graph = GraphService()
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"id": "123", "subject": "Test"}
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp
        
        result = await graph.get_message("token", "123")
        assert result["subject"] == "Test"
        mock_get.assert_called_once()
