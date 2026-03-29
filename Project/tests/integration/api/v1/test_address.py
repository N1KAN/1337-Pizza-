import pytest

import app.api.v1.endpoints.order.address.crud as address_crud
from app.api.v1.endpoints.order.address.schemas import AddressCreateSchema
from app.database.connection import SessionLocal



@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# The unified test
def test_address_create_read_update_delete(db):
    # Arrange
    initial_count = len(address_crud.get_all_addresses(db))

    new_address = AddressCreateSchema(
        street='Schoeffers',
        post_code='12345',
        house_number=1,
        country='DE',
        town='Darmstadt',
        first_name='John',
        last_name='Smith',
    )



    # Act: Create
    db_address = address_crud.create_address(new_address, db)
    created_id = db_address.id

    # Assert: Address count increased
    addresses = address_crud.get_all_addresses(db)
    assert len(addresses) == initial_count + 1

    # Act: Read by ID
    read_address = address_crud.get_address_by_id(created_id, db)
    assert read_address is not None
    assert read_address.street == new_address.street
    assert read_address.post_code == new_address.post_code
    assert read_address.house_number == new_address.house_number
    assert read_address.country == new_address.country
    assert read_address.town == new_address.town
    assert read_address.first_name == new_address.first_name
    assert read_address.last_name == new_address.last_name

    # Arrange: Updated data
    updated_data = AddressCreateSchema(
        street='Mainzerweg',
        post_code='42000',
        house_number=13,
        country='DE',
        town='Fankfurt',
        first_name='Paul',
        last_name='Thompson',
    )

    # Act: Update
    updated_address = address_crud.update_address(read_address, updated_data, db)
    assert updated_address.street == updated_data.street
    assert updated_address.post_code == updated_data.post_code

    # Act: Delete
    address_crud.delete_address_by_id(created_id, db)

    # Assert: Address is deleted
    assert address_crud.get_address_by_id(created_id, db) is None
    assert len(address_crud.get_all_addresses(db)) == initial_count