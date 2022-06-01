from fastapi import APIRouter, HTTPException
from starlette import status

from app.api import crud
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_summary(payload: SummaryPayloadSchema):
    summary_id = await crud.post(payload)

    response_object = {
        "url": payload.url,
        "id": summary_id,
    }
    return response_object


@router.get("/{id}", response_model=SummarySchema)
async def read_summary(id: int) -> SummarySchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found")

    return summary

@router.get("/", response_model=list[SummarySchema])
async def read_all_summaries() -> list[SummarySchema]:
    return await crud.get_all()
