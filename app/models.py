from datetime import datetime,timezone
from sqlalchemy import String,Integer,DateTime,JSON
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base
class Dataset(Base):
 __tablename__="datasets"
 id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
 filename:Mapped[str]=mapped_column(String(255))
 row_count:Mapped[int]=mapped_column(Integer)
 columns:Mapped[list]=mapped_column(JSON)
 records:Mapped[list]=mapped_column(JSON)
 created_at:Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
