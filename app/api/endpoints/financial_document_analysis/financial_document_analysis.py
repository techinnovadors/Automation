from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
import logging
import json

from app.agents.pdf_extractor import PDFExtractorAgent
from app.agents.pdf_extractor.prompt import PDF_EXTRACTOR_PROMPT
from app.agents.pdf_extractor.models import FinancialAnalysisSchema

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/financial_document_analysis", response_model=FinancialAnalysisSchema
)
async def financial_document_analysis(
    file: UploadFile = File(...), is_rich_text: bool = False
):
    user_id = str(uuid4())
    session_id = str(uuid4())
    try:

        pdf_extractor = PDFExtractorAgent(prompt=PDF_EXTRACTOR_PROMPT)

        content = await pdf_extractor.call_agent(
            file=file, user_id=user_id, session_id=session_id, is_rich_text=is_rich_text
        )

        if isinstance(content, dict):
            return content
        elif isinstance(content, FinancialAnalysisSchema):
            logger.info("-" * 60)
            logger.info(f"Content is a FinancialAnalysisSchema")
            logger.info("-" * 60)
            return content
        else:
            logger.exception(f"Error calling agent: {content}")
            raise HTTPException(status_code=500, detail="Error calling agent")
    except Exception as e:
        logger.exception(f"Error calling agent: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
