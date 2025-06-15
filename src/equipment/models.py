from peewee import AutoField, TextField, DateTimeField, IntegerField

from src.database.common import BaseModel
from src.equipment.schemas import EquipmentStatus


class Equipment(BaseModel):
    id = AutoField()
    name = TextField()
    serial = TextField()
    lab_number = IntegerField()
    student_name = TextField()
    status = TextField(default=EquipmentStatus.AVAILABLE.name)
    start_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)
