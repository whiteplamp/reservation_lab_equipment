import json
from pathlib import Path

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.equipment.models import Equipment
from src.equipment.routes import router as equipment_router
from src.equipment.schemas import EquipmentStatus

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(equipment_router)



def create_tables():
    Equipment.create_table()


@app.on_event("startup")
async def startup_event():
    create_tables()
    mock_file = Path("mock/mock.json")

    if not mock_file.exists():
        print(f"Mock file not found at {mock_file}")
        return

    try:
        with open(mock_file, "r", encoding="utf-8") as f:
            equipment_data = json.load(f)

            # Удаляем все существующие записи
            Equipment.delete().execute()

            # Создаем новые записи
            for item in equipment_data:
                # Преобразуем строковый статус в Enum
                status = EquipmentStatus(item["status"])

                Equipment.create(
                    id=item["id"],
                    name=item["name"],
                    serial=item["serial"],
                    lab_number=item["lab_number"],
                    student_name=item["student_name"],
                    status=status.name,
                    start_time=item["start_time"],
                    end_time=item["end_time"]
                )

            print(f"Successfully loaded {len(equipment_data)} equipment items")

    except Exception as e:
        print(f"Error loading mock data: {str(e)}")



