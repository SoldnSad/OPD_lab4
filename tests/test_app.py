import unittest
from unittest.mock import patch
from flask import Flask, render_template, request, jsonify
import requests
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../currency_converter')))
from currency_converter.app import app, get_exchange_rate


class CurrencyConverterTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.get_exchange_rate')
    def test_convert_usd_to_eur(self, mock_get_exchange_rate):
        mock_get_exchange_rate.return_value = 0.9304
        response = self.app.post('/', data=dict(
            amount='100',
            from_currency='USD',
            to_currency='EUR'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Converted Amount: 93.04', response.data)

    @patch('app.get_exchange_rate')
    def test_convert_usd_to_rub(self, mock_get_exchange_rate):
        mock_get_exchange_rate.return_value = 83.8594
        response = self.app.post('/', data=dict(
            amount='1',
            from_currency='USD',
            to_currency='RUB'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Converted Amount: 83.8594', response.data)

    def test_invalid_amount(self):
        response = self.app.post('/', data=dict(
            amount='0',
            from_currency='USD',
            to_currency='EUR'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Converted Amount: 0.0', response.data)

    @patch('app.get_exchange_rate')
    def test_api_error_handling(self, mock_get_exchange_rate):
        mock_get_exchange_rate.return_value = None
        response = self.app.post('/', data=dict(
            amount= None,
            from_currency='USD',
            to_currency='EUR'
        ))
        self.assertEqual(response.status_code, 400)


    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Currency Converter', response.data)

if __name__ == '__main__':
    unittest.main()
