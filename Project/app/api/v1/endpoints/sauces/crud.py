import uuid
import logging
from sqlalchemy.orm import Session

from app.api.v1.endpoints.sauces.schemas import SauceCreateSchema
from app.database.models import Sauce


def create_sauce(schema: SauceCreateSchema, db: Session):
    entity = Sauce(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info(
        'Sauce created: name={}, price={}, stock={}, description={}, spicieness={}'.format(
            entity.name, entity.price, entity.stock, entity.description, entity.spicieness
        )
    )
    return entity


def get_sauce_by_id(sauce_id: uuid.UUID, db: Session):
    entity = db.query(Sauce).filter(Sauce.id == sauce_id).first()
    return entity


def get_sauce_by_name(sauce_name: str, db: Session):
    entity = db.query(Sauce).filter(Sauce.name == sauce_name).first()
    return entity


def get_all_sauces(db: Session):
    return db.query(Sauce).all()


def update_sauce(sauce: Sauce, changed_sauce: SauceCreateSchema, db: Session):
    for key, value in changed_sauce.dict().items():
        setattr(sauce, key, value)

    db.commit()
    logging.info(
        'Sauce updated: name={}, price={}, stock={}, description={} spicieness={}'.format(
             changed_sauce.name, changed_sauce.price, changed_sauce.stock,
            changed_sauce.description, changed_sauce.spicieness
        )
    )
    db.refresh(sauce)
    return sauce


def delete_sauce_by_id(sauce_id: uuid.UUID, db: Session):
    entity = get_sauce_by_id(sauce_id, db)
    if entity:
        db.delete(entity)
        db.commit()
