from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.services.resume_parser import ResumeParserError, parse_resume
from app.services.resume_intelligence import ResumeAnalysisResponse, analyze_resume_text

router = APIRouter(prefix="/resume", tags=["Resume Intelligence"])


@router.post(
    "/upload",
    status_code=status.HTTP_200_OK,
    summary="Upload and extract text from a resume",
    description="Upload a PDF or DOCX resume to extract raw text and document metadata in memory.",
)
async def upload_resume(file: UploadFile = File(...)):
    """
    Accepts multipart/form-data with a 'file' parameter.
    Validates file format (.pdf, .docx), enforces file size limits, and extracts text.
    """
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No resume file was uploaded.",
        )

    try:
        # Read the file content into memory
        file_bytes = await file.read()

        # Parse and extract text using the dedicated service
        result = parse_resume(filename=file.filename, content=file_bytes)
        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except ResumeParserError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process resume: {str(exc)}",
        ) from exc
    finally:
        await file.close()


@router.post(
    "/analyze",
    response_model=ResumeAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze resume and generate structured candidate profile",
    description="Upload a PDF or DOCX resume to extract text and generate a structured profile with skills, education, experience, and projects.",
)
async def analyze_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Accepts multipart/form-data with a 'file' parameter.
    Extracts text and applies rule-based NLP extraction to produce a structured CandidateProfile.
    Persists successful results into PostgreSQL without breaking the response structure.
    """
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No resume file was uploaded.",
        )

    try:
        file_bytes = await file.read()
        parsed_result = parse_resume(filename=file.filename, content=file_bytes)
        profile = analyze_resume_text(parsed_result["text"])

        # Persist candidate and resume analysis safely
        try:
            crud.persist_resume_analysis(
                db=db,
                filename=file.filename,
                file_type=parsed_result.get("file_type"),
                extracted_text=parsed_result.get("text"),
                profile_data=profile.model_dump(),
            )
        except Exception as db_exc:
            # Persistence errors must not fail the client request
            pass

        return ResumeAnalysisResponse(
            filename=file.filename,
            file_type=parsed_result.get("file_type"),
            characters=parsed_result.get("characters"),
            pages=parsed_result.get("pages"),
            text=parsed_result.get("text"),
            profile=profile,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except ResumeParserError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze resume: {str(exc)}",
        ) from exc
    finally:
        await file.close()
