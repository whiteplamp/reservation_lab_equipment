from fastapi import FastAPI
from equipment.routes import router as equipment_router


app = FastAPI()


app.include_router(equipment_router)



