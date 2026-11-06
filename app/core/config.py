import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL","sqlite:///./analytics.db")
MAX_UPLOAD_BYTES=int(os.getenv("MAX_UPLOAD_BYTES","5000000"))
