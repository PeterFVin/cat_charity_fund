from datetime import datetime

from app.models.base_model import Base_Project_Donation


def func_donation(
        target: Base_Project_Donation,
        sources: list[Base_Project_Donation]) -> list[Base_Project_Donation]:
    modified_objects = []
    if target.invested_amount is None:
        target.invested_amount = 0
    for source in sources:
        if target.fully_invested:
            break
        rest_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        modified_objects.append(source)
        for operation in [target, source]:
            operation.invested_amount += rest_amount
            operation.fully_invested = (
                operation.invested_amount == operation.full_amount
            )
            if operation.fully_invested:
                operation.close_date = datetime.now()

    return modified_objects