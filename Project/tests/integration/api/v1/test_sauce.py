import pytest
import app.api.v1.endpoints.sauces.crud as sauce_crud
from app.api.v1.endpoints.sauces.schemas import SauceCreateSchema, SauceSpicienessEnum
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_sauce_create_read_delete(db): # NoSonar
    new_sauce_name = 'Test'
    new_sauce_price = 1.0
    new_sauce_description = 'description'
    new_sauce_stock = 10
    new_sauce_spicieness = SauceSpicienessEnum('mild')
    number_of_sauces_before = len(sauce_crud.get_all_sauces(db))

    # Arrange: Instantiate a new user object
    sauce = SauceCreateSchema(name=new_sauce_name, price=new_sauce_price, description=new_sauce_description,
                              stock=new_sauce_stock, spicieness=new_sauce_spicieness)

    # Act: Add user to database
    db_sauce = sauce_crud.create_sauce(sauce, db)
    created_sauce_id = db_sauce.id

    # Assert: One more user in database
    sauces = sauce_crud.get_all_sauces(db)
    assert len(sauces) == number_of_sauces_before + 1

    # Act: Re-read user from database
    read_sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)

    # Assert: Correct user was stored in database
    assert read_sauce.id == created_sauce_id
    assert read_sauce.name == new_sauce_name

    # Act: Update beverage in database
    new_sauce_price = 4.99
    new_sauce_description = SauceSpicienessEnum('unhealthy')
    update_sauce = SauceCreateSchema(name=new_sauce_name, price=new_sauce_price,
    description=new_sauce_description, stock=new_sauce_stock, spicieness=new_sauce_spicieness)
    sauce_crud.update_sauce(read_sauce, update_sauce, db)

    # Act: Re-read beverage by name
    updated_sauce = sauce_crud.get_sauce_by_name(new_sauce_name, db)

    # Assert: New price in db
    assert new_sauce_price.__eq__(updated_sauce.price)
    assert new_sauce_spicieness.__eq__(updated_sauce.spicieness)

    # Act: Delete user
    sauce_crud.delete_sauce_by_id(created_sauce_id, db)

    # Assert: Correct number of users in database after deletion
    sauces = sauce_crud.get_all_sauces(db)
    assert len(sauces) == number_of_sauces_before

    # Assert: Correct user was deleted from database
    deleted_sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)
    assert deleted_sauce is None
