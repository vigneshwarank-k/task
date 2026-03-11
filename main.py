from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import Base, engine
from api.endpoints.agent import router as agent_router
from api.endpoints.api_endpoints import router as api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router, prefix="/agent", tags=["ChatAgent"])
app.include_router(api_router, tags=["Create product"])
