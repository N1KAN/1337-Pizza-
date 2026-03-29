import pytest

import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema
from app.database.connection import SessionLocal
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
import app.api.v1.endpoints.dough.crud as dough_crud

# Konstante zur Vermeidung von Magic Numbers
DEFAULT_PIZZA_PRICE = 10

@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_pizza_type_create_read_delete(db):
    new_pizza_name = 'TestPizza'
    number_of_pizzas_before = len(pizza_type_crud.get_all_pizza_types(db))
    new_dough_name = 'Test'
    new_dough_price = 1.0
    new_dough_description = 'description'
    new_dough_stock = 10

    new_doug = DoughCreateSchema(
        name=new_dough_name,
        price=new_dough_price,
        description=new_dough_description,
        stock=new_dough_stock,
    )

    db_dough = dough_crud.create_dough(new_doug, db)
    created_dough_id = db_dough.id

    # Arrange: Neue PizzaType-Daten
    pizza_type = PizzaTypeCreateSchema(
        name=new_pizza_name,
        price=DEFAULT_PIZZA_PRICE,
        description='Test pizza description',
        dough_id=created_dough_id,
    )

    # Act: PizzaType erstellen
    db_pizza_type = pizza_type_crud.create_pizza_type(pizza_type, db)
    created_pizza_id = db_pizza_type.id

    # Assert: Eine Pizza mehr
    pizzas = pizza_type_crud.get_all_pizza_types(db)
    assert len(pizzas) == number_of_pizzas_before + 1

    # Act: PizzaType erneut lesen
    read_pizza_type = pizza_type_crud.get_pizza_type_by_id(created_pizza_id, db)

    # Assert: Korrekte Daten
    assert read_pizza_type.id == created_pizza_id
    assert read_pizza_type.name == new_pizza_name
    assert read_pizza_type.price == DEFAULT_PIZZA_PRICE

    # Act: PizzaType löschen
    pizza_type_crud.delete_pizza_type_by_id(created_pizza_id, db)

    # Assert: Anzahl wieder wie zuvor
    pizzas = pizza_type_crud.get_all_pizza_types(db)
    assert len(pizzas) == number_of_pizzas_before

    # Assert: Gelöschte Pizza nicht mehr auffindbar
    deleted_pizza = pizza_type_crud.get_pizza_type_by_id(created_pizza_id, db)
    assert deleted_pizza is None
