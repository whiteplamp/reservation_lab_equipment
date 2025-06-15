from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EquipmentStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    SERVICE = "SERVICE"
    BOOKED = "BOOKED"


class EquipmentObject(BaseModel):
    id: int
    name: str
    serial: str
    lab_number: int
    student_name: str
    status: EquipmentStatus
    start_time: Optional[datetime]
    end_time: Optional[datetime]


class SortEquipment(str, Enum):
    name = 'name'
    lab_number = 'lab_number'
    status = 'status'
    start_time = 'start_time'
    end_time = 'end_time'


class OrderBy(str, Enum):
    asc = 'asc'
    desc = 'desc'


class ReserveEquipmentRequest(BaseModel):
    id: int
    student_name: str
    start_time: datetime
    end_time: datetime