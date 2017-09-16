import pytest
from drinks import app, db
from config import TestConfig
from flask.ext.sqlalchemy import SQLAlchemy
from drinks.models.drink import Drink


class TestDrinksApi:
    @pytest.fixture(scope='session')
    def mock_app(self):
        app.config.from_object(TestConfig)
        return app

    @pytest.fixture()
    def setup_db(self):
        print 'Setting up db'
        db.create_all()

        print 'Clearing the table for a fresh start'
        db.session.query(Drink).delete()
        db.session.commit()

        yield
        print 'Clearing the table again to end the session'
        db.session.query(Drink).delete()
        db.session.commit()


    @pytest.fixture(scope='session')
    def mock_client(self, mock_app):
        client = mock_app.test_client()
        return client

    @pytest.fixture()
    def mock_drinks(self):
        mock_drinks = [
            {
                "price": 1.51,
                "id": 2,
                "start_availability_date": "15 sep 17",
                "name": "chocolate milk"
            },
            {
                "price": 1.52,
                "id": 3,
                "start_availability_date": "15 aug 19",
                "name": "apple juice"
            },
            {
                "price": 1.52,
                "end_availability_date": "29 aug 19",
                "id": 4,
                "start_availability_date": "16 aug 18",
                "name": "apple sauce"
            }
        ]

    def test_add_drink(self, mock_client, setup_db):
        mock_drink = {
            "price": 1.51,
            "id": 2,
            "start_availability_date": "15 sep 17",
            "name": "chocolate milk"
        }

        resp = mock_client.post('/drink', query_string={
            'name': mock_drink.get('name'),
            'price': mock_drink.get('price'),
            'start_availability_date': mock_drink.get('start_availability_date'),
            'end_availability_date': mock_drink.get('end_availability_date')
        })

        stuff = db.session.query(Drink).all()

        assert resp.status_code == 200

    # def test_search(self, mock_client, mock_drinks):
    #     results = mock_client.get('/drink/search')
    #     for result in results:
    #         print result.id