from fastapi import APIRouter,Depends,File,HTTPException,UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.models import Dataset
from app.schemas.datasets import DatasetOut,DatasetPreview,NumericSummary
from app.services.analytics import parse_csv,summarize
router=APIRouter(prefix="/api/v1/datasets",tags=["datasets"])
@router.post("",response_model=DatasetOut,status_code=201)
async def upload_dataset(file:UploadFile=File(...),db:Session=Depends(get_db)):
 frame,records=await parse_csv(file)
 dataset=Dataset(filename=file.filename,row_count=len(frame),columns=[str(c) for c in frame.columns],records=records)
 db.add(dataset); db.commit(); db.refresh(dataset); return dataset
@router.get("",response_model=list[DatasetOut])
def list_datasets(db:Session=Depends(get_db)): return db.scalars(select(Dataset).order_by(Dataset.created_at.desc())).all()
def find_dataset(dataset_id:int,db:Session):
 obj=db.get(Dataset,dataset_id)
 if obj is None: raise HTTPException(status_code=404,detail="Dataset not found.")
 return obj
@router.get("/{dataset_id}",response_model=DatasetOut)
def get_dataset(dataset_id:int,db:Session=Depends(get_db)): return find_dataset(dataset_id,db)
@router.get("/{dataset_id}/preview",response_model=DatasetPreview)
def preview_dataset(dataset_id:int,limit:int=10,db:Session=Depends(get_db)):
 if limit<1 or limit>100: raise HTTPException(status_code=422,detail="limit must be between 1 and 100.")
 d=find_dataset(dataset_id,db); return {"dataset_id":d.id,"columns":d.columns,"rows":d.records[:limit]}
@router.get("/{dataset_id}/summary",response_model=NumericSummary)
def dataset_summary(dataset_id:int,db:Session=Depends(get_db)):
 d=find_dataset(dataset_id,db); return {"dataset_id":d.id,"numeric_columns":summarize(d.records)}
