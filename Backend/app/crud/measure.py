from sqlalchemy.orm import Session

from ..schemas.measure import MeasureBaseSchema


def create_measure(db: Session, data: MeasureBaseSchema):
    pass
