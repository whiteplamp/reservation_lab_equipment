from typing import List

from fastapi import APIRouter, Query, HTTPException
from peewee import fn, DoesNotExist
from starlette import status

from src.equipment.models import Equipment
from src.equipment.schemas import SortEquipment, OrderBy, EquipmentObject, ReserveEquipmentRequest, EquipmentStatus

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
    # Определяем поле для сортировки
    sort_field = {
        SortEquipment.name: Equipment.name,
        SortEquipment.lab_number: Equipment.lab_number,
        SortEquipment.status: Equipment.status,
        SortEquipment.start_time: Equipment.start_time,
        SortEquipment.end_time: Equipment.end_time,
    }
    # Получаем оборудование с учетом пагинации и сортировки
    if order_by == OrderBy.asc:
        equipment_query = (
            Equipment.select()
            .order_by(sort_field.get(sort_by))
            .offset(offset)
            .limit(limit)
        )
    else:
        equipment_query = (
            Equipment.select()
            .order_by(sort_field.get(sort_by).desc())
            .offset(offset)
            .limit(limit)
        )

    # Преобразуем результаты в список EquipmentObject
    return [
        EquipmentObject(
            id=eq.id,
            name=eq.name,
            serial=eq.serial,
            lab_number=eq.lab_number,
            student_name=eq.student_name,
            status=EquipmentStatus(eq.status),
            start_time=eq.start_time,
            end_time=eq.end_time
        )
        for eq in equipment_query
    ]


@router.post(
    path='/',
    description='Зарезервировать оборудование',
)
def reserve_equipment(
    request: ReserveEquipmentRequest
):
    # Проверяем, что время окончания больше времени начала
    if request.end_time <= request.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be greater than start time"
        )

    # Проверяем, что оборудование существует и доступно
    try:
        equipment = Equipment.get_by_id(request.id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )

    # Проверяем доступность оборудования
    if equipment.status != EquipmentStatus.AVAILABLE.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Equipment is not available for reservation"
        )

    # Проверяем, что оборудование не забронировано на это время
    conflicting_reservations = Equipment.select().where(
        (Equipment.id == request.id) &
        (
                ((Equipment.start_time <= request.start_time) & (Equipment.end_time > request.start_time)) |
                ((Equipment.start_time < request.end_time) & (Equipment.end_time >= request.end_time)) |
                ((Equipment.start_time >= request.start_time) & (Equipment.end_time <= request.end_time))
        )
    ).exists()

    if conflicting_reservations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Equipment is already reserved for this time period"
        )

    # Обновляем запись оборудования
    equipment.status = EquipmentStatus.BOOKED.name
    equipment.student_name = request.student_name
    equipment.start_time = request.start_time
    equipment.end_time = request.end_time
    equipment.save()

    # Возвращаем обновленное оборудование
    return EquipmentObject(
        id=equipment.id,
        name=equipment.name,
        serial=equipment.serial,
        lab_number=equipment.lab_number,
        student_name=equipment.student_name,
        status=EquipmentStatus(equipment.status),
        start_time=equipment.start_time,
        end_time=equipment.end_time
    )
