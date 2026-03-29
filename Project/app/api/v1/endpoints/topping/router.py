import uuid
from typing import List
import logging

from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import app.api.v1.endpoints.topping.crud as topping_crud
from app.api.v1.endpoints.topping.schemas import ToppingSchema, ToppingCreateSchema, ToppingListItemSchema
from app.database.connection import SessionLocal

router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('', response_model=List[ToppingListItemSchema], tags=['topping'])
def get_all_toppings(db: Session = Depends(get_db)):
    logger.info('Request to get all toppings')
    toppings = topping_crud.get_all_toppings(db)
    logger.info(f'Returned {len(toppings)} toppings')
    return toppings


@router.post('', response_model=ToppingSchema, status_code=status.HTTP_201_CREATED, tags=['topping'])
def create_topping(topping: ToppingCreateSchema,
                   request: Request,
                   db: Session = Depends(get_db),
                   ):
    logger.info(f'Attempting to create topping: {topping.name}')
    topping_found = topping_crud.get_topping_by_name(topping.name, db)

    if topping_found:
        url = request.url_for('get_topping', topping_id=topping_found.id)
        logger.warning(f'Topping already exists. Redirecting to existing topping with ID: {topping_found.id}')
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    new_topping = topping_crud.create_topping(topping, db)
    logger.info(f'Created new topping: {new_topping.name}')
    return new_topping


@router.put('/{topping_id}', response_model=ToppingSchema, tags=['topping'])
def update_topping(
        topping_id: uuid.UUID,
        changed_topping: ToppingCreateSchema,
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
):
    logger.info(f'Updating topping with ID: {topping_id}')
    topping_found = topping_crud.get_topping_by_id(topping_id, db)
    updated_topping = None

    if topping_found:
        if topping_found.name == changed_topping.name:
            logger.info(f'Updating topping with unchanged name: {topping_found.name}')
            topping_crud.update_topping(topping_found, changed_topping, db)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            topping_name_found = topping_crud.get_topping_by_name(changed_topping.name, db)
            if topping_name_found:
                url = request.url_for('get_topping', topping_id=topping_name_found.id)
                logger.warning(f'Topping with new name already exists. Redirecting to ID: {topping_name_found.id}')
                return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
            else:
                updated_topping = topping_crud.create_topping(changed_topping, db)
                logger.info(f'Created new topping while updating: {updated_topping.name}')
                response.status_code = status.HTTP_201_CREATED
    else:
        logger.error(f'Topping with ID {topping_id} not found')
        raise HTTPException(status_code=404)

    return updated_topping


@router.get('/{topping_id}', response_model=ToppingSchema, tags=['topping'])
def get_topping(topping_id: uuid.UUID,
                response: Response,
                db: Session = Depends(get_db),
                ):
    logger.info(f'Fetching topping with ID: {topping_id}')
    topping = topping_crud.get_topping_by_id(topping_id, db)

    if not topping:
        logger.warning(f'Topping with ID {topping_id} not found')
        raise HTTPException(status_code=404)

    return topping


@router.delete('/{topping_id}', response_model=None, tags=['topping'])
def delete_topping(topping_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info(f'Attempting to delete topping with ID: {topping_id}')
    topping = topping_crud.get_topping_by_id(topping_id, db)

    if not topping:
        logger.warning(f'Topping with ID {topping_id} not found for deletion')
        raise HTTPException(status_code=404, detail='Item not found')

    topping_crud.delete_topping_by_id(topping_id, db)
    logger.info(f'Topping with ID {topping_id} deleted successfully')
    return Response(status_code=status.HTTP_204_NO_CONTENT)