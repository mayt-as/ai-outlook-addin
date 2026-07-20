from fastapi import APIRouter, Depends, HTTPException
import structlog
from domain.dtos.requests import (
    SummaryRequest, DraftRequest, RewriteRequest, ActionItemsRequest, PriorityRequest
)
from domain.dtos.responses import (
    SummaryResponse, GeneratedTextResponse, ActionItemsResponse, PriorityResponse
)
from api.dependencies.auth import get_graph_token
from services.graph.graph_client import graph_service
from services.business.ai_service import business_ai_service

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/ai", tags=["AI Gateway"])

def _extract_text_from_message(msg: dict) -> str:
    body = msg.get("body", {})
    return body.get("content", "")

@router.post("/summary", response_model=SummaryResponse)
async def summary(req: SummaryRequest, token: str = Depends(get_graph_token)):
    logger.info("Processing summary request", message_id=req.message_id)
    msg = await graph_service.get_message(token, req.message_id)
    content = _extract_text_from_message(msg)
    
    result = await business_ai_service.generate_summary(content, req.summary_type)
    return SummaryResponse(summary=result)

@router.post("/extract-actions", response_model=ActionItemsResponse)
async def extract_actions(req: ActionItemsRequest, token: str = Depends(get_graph_token)):
    logger.info("Processing action items request", message_id=req.message_id)
    msg = await graph_service.get_message(token, req.message_id)
    content = _extract_text_from_message(msg)
    
    data = await business_ai_service.extract_action_items(content)
    return ActionItemsResponse(**data)

@router.post("/classify-priority", response_model=PriorityResponse)
async def classify_priority(req: PriorityRequest, token: str = Depends(get_graph_token)):
    logger.info("Processing priority request", message_id=req.message_id)
    msg = await graph_service.get_message(token, req.message_id)
    content = _extract_text_from_message(msg)
    
    data = await business_ai_service.classify_priority(content)
    return PriorityResponse(**data)

@router.post("/draft", response_model=GeneratedTextResponse)
async def draft(req: DraftRequest, token: str = Depends(get_graph_token)):
    logger.info("Processing draft request")
    result = await business_ai_service.generate_draft(req.instructions, req.tone)
    return GeneratedTextResponse(text=result)

@router.post("/rewrite", response_model=GeneratedTextResponse)
async def rewrite(req: RewriteRequest, token: str = Depends(get_graph_token)):
    logger.info("Processing rewrite request")
    result = await business_ai_service.rewrite_text(req.selected_text, req.tone)
    return GeneratedTextResponse(text=result)
