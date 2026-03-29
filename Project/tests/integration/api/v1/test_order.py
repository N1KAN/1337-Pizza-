import pytest
from decimal import Decimal

import app.api.v1.endpoints.user.crud as user_crud
import app.api.v1.endpoints.order.crud as order_crud
import app.api.v1.endpoints.dough.crud as dough_crud
import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud

from app.api.v1.endpoints.user.schemas import UserCreateSchema
from app.api.v1.endpoints.order.schemas import OrderCreateSchema, AddressCreateSchema
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema


from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_order_create_read_delete(db):
    # Arrange: Create a user
    user = UserCreateSchema(username='test_order_user')
    db_user = user_crud.create_user(user, db)

    # Arrange: Create a dough
    dough = dough_crud.create_dough(
        dough_crud.DoughCreateSchema(
            name='TestDoughOrder',
            price=Decimal('1.5'),
            description='Test dough',
            stock=100
        ),
        db
    )

    # Arrange: Create a PizzaType for later test (required for valid order handling)
    pizza_type = PizzaTypeCreateSchema(
        name='TestPizzaOrder',
        price=Decimal('7.50'),
        description='Test Pizza',
        dough_id=dough.id
    )
    db_pizza_type = pizza_type_crud.create_pizza_type(pizza_type, db)

    # Arrange: Define address
    address = AddressCreateSchema(
        street='Test Street',
        post_code='12345',
        house_number=42,
        country='Testland',
        town='Testville',
        first_name='Order',
        last_name='Tester'
    )

    # Act: Create order
    order_schema = OrderCreateSchema(address=address, user_id=db_user.id)
    created_order = order_crud.create_order(order_schema, db)

    # Assert: Order was created and has an ID
    assert created_order.id is not None

    # Act: Read back order
    read_order = order_crud.get_order_by_id(created_order.id, db)
    assert read_order is not None
    assert read_order.user_id == db_user.id

    # Act: Delete order
    order_crud.delete_order_by_id(created_order.id, db)

    # Assert: Order no longer exists
    assert order_crud.get_order_by_id(created_order.id, db) is None

    # Cleanup: Delete created user, dough and pizza_type
    user_crud.delete_user_by_id(db_user.id, db)
    pizza_type_crud.delete_pizza_type_by_id(db_pizza_type.id, db)
    dough_crud.delete_dough_by_id(dough.id, db)
