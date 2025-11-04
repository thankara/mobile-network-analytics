from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mobile_network_analytics.api.routers.kpi_router import kpi_router

app = FastAPI(title="Mobile Network Analytics API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(kpi_router)
