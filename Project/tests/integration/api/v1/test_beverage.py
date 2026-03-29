import pytest
from decimal import Decimal

import app.api.v1.endpoints.beverage.crud as beverage_crud
from app.api.v1.endpoints.beverage.schemas import BeverageCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_beverage_create_read_update_delete(db):
    # Arrange: Define new beverage data
    new_beverage_name: str = 'Cola'
    new_description: str = 'Viel Zucker'
    new_price = Decimal('2.99')
    new_stock: int = 109

    number_of_beverages_before = len(beverage_crud.get_all_beverages(db))

    beverage = BeverageCreateSchema(
        name=new_beverage_name,
        description=new_description,
        price=new_price,
        stock=new_stock
    )

    # Act: Create beverage
    db_beverage = beverage_crud.create_beverage(beverage, db)
    created_beverage_id = db_beverage.id
    created_beverage_name = db_beverage.name

    # Assert: Beverage count increased
    beverages = beverage_crud.get_all_beverages(db)
    assert len(beverages) == number_of_beverages_before + 1

    # Act: Read beverage by ID and name
    read_beverage = beverage_crud.get_beverage_by_id(created_beverage_id, db)
    read_beverage_by_name = beverage_crud.get_beverage_by_name(created_beverage_name, db)

    # Assert: Correct data was stored
    assert read_beverage.id == created_beverage_id
    assert read_beverage.name == new_beverage_name
    assert read_beverage_by_name.name == new_beverage_name
    assert read_beverage.description == new_description
    assert read_beverage.price == new_price
    assert read_beverage.stock == new_stock

    # Arrange: Updated beverage data
    update_beverage_name: str = 'Cola Zero'
    update_description: str = 'Zu wenig Zucker'
    update_price = Decimal('3.99')
    update_stock: int = 99

    update_beverage = BeverageCreateSchema(
        name=update_beverage_name,
        price=update_price,
        description=update_description,
        stock=update_stock
    )

    # Act: Update beverage
    beverage_crud.update_beverage(read_beverage, update_beverage, db)

    # Act: Delete beverage
    beverage_crud.delete_beverage_by_id(created_beverage_id, db)

    # Assert: Beverage is deleted and count is correct
    beverages = beverage_crud.get_all_beverages(db)
    assert len(beverages) == number_of_beverages_before

    deleted_beverage = beverage_crud.get_beverage_by_id(created_beverage_id, db)
    assert deleted_beverage is None
