from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from uuid import uuid4
import logging
import json

from fastapi.responses import JSONResponse

from app.agents.pdf_extractor import PDFExtractorAgent
from app.agents.pdf_extractor.prompt import PDF_EXTRACTOR_PROMPT
from app.agents.pdf_extractor.models import FinancialAnalysisSchema
from app.services.generate_report import generate_pdf

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/financial_document_analysis", response_model=FinancialAnalysisSchema)
async def financial_document_analysis(
    file: UploadFile = File(...), is_rich_text: bool = Form(default=False)
):
    user_id = str(uuid4())
    session_id = str(uuid4())
    try:

        pdf_extractor = PDFExtractorAgent(prompt=PDF_EXTRACTOR_PROMPT)

        content = await pdf_extractor.call_agent(
            file=file, user_id=user_id, session_id=session_id, is_rich_text=is_rich_text
        )

        if isinstance(content, dict):
            generate_pdf(content, file.filename)
            return content
        elif isinstance(content, FinancialAnalysisSchema):
            logger.info("-" * 60)
            logger.info(f"Content is a FinancialAnalysisSchema")
            logger.info("-" * 60)
            generate_pdf(content.model_dump(), file.filename)
            return content
        else:
            logger.exception(f"Error calling agent: {content}")
            raise HTTPException(status_code=500, detail="Error calling agent")
    except Exception as e:
        logger.exception(f"Error calling agent: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/get_schema")
async def get_schema():
    return JSONResponse(content=FinancialAnalysisSchema.model_json_schema())
