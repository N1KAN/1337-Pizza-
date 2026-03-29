import pytest


import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema, PizzaTypeToppingQuantityCreateSchema
from app.database.connection import SessionLocal
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.topping.schemas import ToppingCreateSchema
import app.api.v1.endpoints.topping.crud as topping_crud


DEFAULT_PIZZA_PRICE = 10.0
DEFAULT_TOPPING_PRICE = 1.0
DEFAULT_TOPPING_QUANTITY = 2

@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_pizza_type_crud_extended(db):
    pizza_name = 'TestPizzaExtended'
    updated_pizza_name = 'UpdatedPizzaName'
    dough = DoughCreateSchema(
        name='DoughForPizzaTypeTest',
        price=1.0,
        description='desc',
        stock=5
    )
    db_dough = dough_crud.create_dough(dough, db)

    # Arrange: Create PizzaType
    pizza_schema = PizzaTypeCreateSchema(
        name=pizza_name,
        price=DEFAULT_PIZZA_PRICE,
        description='some description',
        dough_id=db_dough.id
    )
    db_pizza = pizza_type_crud.create_pizza_type(pizza_schema, db)

    # Test: get_pizza_type_by_name
    # Act:
    same_pizza = pizza_type_crud.get_pizza_type_by_name(pizza_name, db)
    # Assert:
    assert same_pizza is not None
    assert same_pizza.id == db_pizza.id

    # Test: update_pizza_type
    #Arrange:
    updated_schema = PizzaTypeCreateSchema(
        name=updated_pizza_name,
        price=DEFAULT_PIZZA_PRICE + 1,
        description='updated description',
        dough_id=db_dough.id
    )
    #Act:
    updated_pizza = pizza_type_crud.update_pizza_type(db_pizza, updated_schema, db)
    #Assert:
    assert updated_pizza.name == updated_pizza_name
    assert updated_pizza.price == DEFAULT_PIZZA_PRICE + 1

    # Create a Topping
    #Arrange:
    topping_schema = ToppingCreateSchema(
        name='TestTopping',
        price=DEFAULT_TOPPING_PRICE,
        description='topping desc',
        stock=10
    )

    db_topping = topping_crud.create_topping(topping_schema, db)

    # Test: create_topping_quantity
    topping_quantity_schema = PizzaTypeToppingQuantityCreateSchema(
        topping_id=db_topping.id,
        quantity=2
    )
    #Act:
    topping_quantity = pizza_type_crud.create_topping_quantity(updated_pizza, topping_quantity_schema, db)
    #Assert:
    assert topping_quantity.topping_id == db_topping.id
    assert topping_quantity.quantity == DEFAULT_TOPPING_QUANTITY

    # Test: get_topping_quantity_by_id
    #Act:
    retrieved_tq = pizza_type_crud.get_topping_quantity_by_id(updated_pizza.id, db_topping.id, db)
    #Assert:
    assert retrieved_tq is not None
    assert retrieved_tq.quantity == DEFAULT_TOPPING_QUANTITY

    # Test: get_joined_topping_quantities_by_pizza_type
    #Act:
    joined_tqs = pizza_type_crud.get_joined_topping_quantities_by_pizza_type(updated_pizza.id, db)
    #Assert:
    assert len(joined_tqs) == 1
    assert joined_tqs[0].topping_id == db_topping.id

    # Clean-up
    pizza_type_crud.delete_pizza_type_by_id(updated_pizza.id, db)
    assert pizza_type_crud.get_pizza_type_by_id(updated_pizza.id, db) is None
