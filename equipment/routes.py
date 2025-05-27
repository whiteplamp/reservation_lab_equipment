from typing import List

from fastapi import APIRouter, Query

from equipment.schemas import SortEquipment, OrderBy, EquipmentObject, ReserveEquipmentRequest

router = APIRouter(
    prefix="/equipment",
    tags=['Оборудование']
)


@router.get(
    path="/",
    description="Получение списка оборудования",
    response_model=List[EquipmentObject]
)
def get_equipment(
        offset: int = 0,
        limit: int = 50,
        sort_by: SortEquipment = Query(
            SortEquipment.name,
            description="""Поля для сортировки: \n
            - name: по названию оборудования \n
            - lab_name: по названию лаборатории \n
            - status: по статусу \n
            - start_time: по времени начала бронирования \n
            - end_time: по времени окончания бронирования \n
            """
        ),
        order_by: OrderBy = Query(
            OrderBy.asc,
            description="""Сортировать по: \n
            - asс: Возрастанию \n
            - desc: Убыванию \n
            """
        ),

):
    pass


@router.post(
    path='/',
    description='Зарезервировать оборудование',
)
def reserve_equipment(
    request: ReserveEquipmentRequest
):
    pass
