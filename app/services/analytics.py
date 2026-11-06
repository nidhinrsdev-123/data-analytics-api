from io import BytesIO
import pandas as pd
from fastapi import HTTPException,UploadFile
from app.core.config import MAX_UPLOAD_BYTES
async def parse_csv(upload:UploadFile):
 if not upload.filename or not upload.filename.lower().endswith(".csv"): raise HTTPException(status_code=415,detail="Only CSV files are supported.")
 content=await upload.read(MAX_UPLOAD_BYTES+1)
 if len(content)>MAX_UPLOAD_BYTES: raise HTTPException(status_code=413,detail="Upload exceeds configured size limit.")
 if not content: raise HTTPException(status_code=400,detail="Uploaded file is empty.")
 try: frame=pd.read_csv(BytesIO(content))
 except Exception as exc: raise HTTPException(status_code=400,detail=f"Could not parse CSV: {exc}") from exc
 if frame.empty: raise HTTPException(status_code=400,detail="CSV must contain at least one data row.")
 if any(not str(c).strip() for c in frame.columns): raise HTTPException(status_code=400,detail="Column names must not be blank.")
 if frame.columns.duplicated().any(): raise HTTPException(status_code=400,detail="Duplicate column names are not allowed.")
 frame=frame.astype(object).where(pd.notna(frame),None)
 records=frame.to_dict(orient="records")
 clean=[{str(k):(v.item() if hasattr(v,"item") else v) for k,v in row.items()} for row in records]
 return frame,clean
def summarize(records):
 frame=pd.DataFrame(records); numeric=frame.select_dtypes(include="number"); result={}
 for column in numeric.columns:
  values=numeric[column].dropna()
  stats={"count":values.count(),"mean":values.mean(),"std":values.std(),"min":values.min(),"25%":values.quantile(.25),"50%":values.quantile(.5),"75%":values.quantile(.75),"max":values.max()}
  result[str(column)]={k:(None if pd.isna(v) else float(v)) for k,v in stats.items()}
 return result
