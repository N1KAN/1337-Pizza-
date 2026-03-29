import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

import app.api.v1.endpoints.user.crud as user_crud
from app.api.v1.endpoints.user.schemas import UserSchema, UserCreateSchema
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


@router.get('', response_model=List[UserSchema], tags=['user'])
def get_all_users(
        db: Session = Depends(get_db),
):
    logger.info('Received request to fetch all users')
    users = user_crud.get_all_users(db)
    logger.info('Found {} users'.format(len(users)))
    return users


@router.post('', response_model=UserSchema, status_code=status.HTTP_201_CREATED, tags=['user'])
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    logger.info('Received request to create a new user: {}'.format(user.username))
    new_user = user_crud.create_user(user, db)
    logger.info('User created successfully: {}'.format(new_user.username))
    return new_user


@router.put('/{user_id}', response_model=None, tags=['user'])
def update_user(
        user_id: uuid.UUID,
        changed_user: UserCreateSchema,
        db: Session = Depends(get_db),
):
    logger.info('Received request to update user with ID: {}'.format(user_id))
    user_found = user_crud.get_user_by_id(user_id, db)

    if user_found:
        user_crud.update_user(user_found, changed_user, db)
        logger.info('User {} updated successfully'.format(user_id))
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        logger.error('User {} not found'.format(user_id))
        raise HTTPException(status_code=404)


@router.get('/{user_id}', response_model=UserSchema, tags=['user'])
def get_user(user_id: uuid.UUID,
             response: Response,
             db: Session = Depends(get_db)):
    logger.info('Received request to fetch user with ID: {}'.format(user_id))
    user_found = user_crud.get_user_by_id(user_id, db)

    if not user_found:
        logger.error('User {} not found'.format(user_id))
        raise HTTPException(status_code=404, detail='Item not found')

    logger.info('User {} found'.format(user_id))
    return user_found


@router.delete('/{user_id}', response_model=None, tags=['user'])
def delete_user(
        user_id: uuid.UUID,
        db: Session = Depends(get_db),
):
    logger.info('Received request to delete user with ID: {}'.format(user_id))
    user_found = user_crud.get_user_by_id(user_id, db)

    if not user_found:
        logger.error('User {} not found'.format(user_id))
        raise HTTPException(status_code=404, detail='Item not found')

    user_crud.delete_user_by_id(user_id, db)
    logger.info('User {} deleted successfully'.format(user_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
