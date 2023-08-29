import json
import os
import unittest
from unittest.mock import patch, ANY

from lambda_handler import lambda_handler
from models.models import ProductToPersist, CustomerToPersist, SupplierToPersist
from utils.component_provider import ComponentProvider


@patch.dict(os.environ, {
    'DB_HOST': 'localhost',
    'DB_NAME': 'test_db',
    'DB_USER': 'test_user',
    'DB_PASSWORD': 'test_password'
})
class LambdaHandlerIntegrationTest(unittest.TestCase):

    def tearDown(self):
        ComponentProvider._persistence_service = None
        ComponentProvider._topic_router = None

    @patch('utils.component_provider.ComponentProvider.get_rds_client')
    @patch('clients.rds_client.RdsClient')
    def test_lambda_handler_integration(self, mock_rds_client, mock_get_rds_client):
        mock_get_rds_client.return_value = mock_rds_client

        mock_insert_product = mock_rds_client.insert_product
        mock_insert_product.return_value = None

        event = {
            'Records': [{
                'Sns': {
                    'Message': json.dumps({
                        'name': 'TestProduct',
                        'description': 'TestDescription',
                        'safety_stock': 10,
                        'max_stock': 50,
                        'quantity': 30
                    }),
                    'TopicArn': 'NewProductTopic'
                }
            }]
        }
        context = {}

        # Act
        result = lambda_handler(event, context)

        # Assert
        expected_product_to_persist = ProductToPersist(
            id=ANY,  # Here, you'd use ANY or some other way to deal with the dynamically generated ID
            name='TestProduct',
            description='TestDescription',
            safety_stock=10,
            max_stock=50,
            quantity=30
        )
        mock_insert_product.assert_called_with(expected_product_to_persist)

    @patch('utils.component_provider.ComponentProvider.get_rds_client')
    @patch('clients.rds_client.RdsClient')
    def test_lambda_handler_integration_new_supplier(self, mock_rds_client, mock_get_rds_client):
        mock_get_rds_client.return_value = mock_rds_client

        mock_insert_supplier = mock_rds_client.insert_supplier
        mock_insert_supplier.return_value = None

        event = {
            'Records': [{
                'Sns': {
                    'Message': json.dumps({
                        'name': 'TestSupplier',
                    }),
                    'TopicArn': 'NewSupplierTopic'
                }
            }]
        }
        context = {}

        result = lambda_handler(event, context)

        expected_supplier_to_persist = SupplierToPersist(
            id=ANY,
            name='TestSupplier'
        )
        mock_insert_supplier.assert_called_with(expected_supplier_to_persist)

    @patch('utils.component_provider.ComponentProvider.get_rds_client')
    @patch('clients.rds_client.RdsClient')
    def test_lambda_handler_integration_new_customer(self, mock_rds_client, mock_get_rds_client):
        mock_get_rds_client.return_value = mock_rds_client

        mock_insert_customer = mock_rds_client.insert_customer
        mock_insert_customer.return_value = None

        event = {
            'Records': [{
                'Sns': {
                    'Message': json.dumps({
                        'name': 'TestCustomer',
                    }),
                    'TopicArn': 'NewCustomerTopic'
                }
            }]
        }
        context = {}

        result = lambda_handler(event, context)

        expected_customer_to_persist = CustomerToPersist(
            id=ANY,
            name='TestCustomer'
        )
        mock_insert_customer.assert_called_with(expected_customer_to_persist)
