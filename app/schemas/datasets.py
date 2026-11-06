from datetime import datetime
from pydantic import BaseModel,ConfigDict
class DatasetOut(BaseModel):
 model_config=ConfigDict(from_attributes=True)
 id:int; filename:str; row_count:int; columns:list[str]; created_at:datetime
class DatasetPreview(BaseModel):
 dataset_id:int; columns:list[str]; rows:list[dict]
class NumericSummary(BaseModel):
 dataset_id:int; numeric_columns:dict[str,dict[str,float|int|None]]
