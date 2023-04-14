# -*- coding: utf-8 -*-

"""Unit tests for the Web Service client."""

from mock import MagicMock
from mock import patch
from requests.exceptions import ConnectionError

from genweb6.serveistic.ws_client.problems import Client
from genweb6.serveistic.ws_client.problems import ClientException
from genweb6.serveistic.ws_client.problems import Problem

import base64
import datetime
import json
import unittest


class TestWSClient(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            endpoint='http://endpoint',
            login_username='test-username',
            login_password='test-password')

    def test_get_headers(self):
        # All header params are given
        client = Client(
            endpoint='#',
            login_username='username',
            login_password='password',
            content_type='application/xml')
        headers = client._get_headers()
        self.assertEqual(headers, {
            'Content-type': 'application/xml',
            'login.username': 'username',
            'login.password': 'password',
            'Authorization': "Basic {0}".format(
                base64.b64encode("username:password"))})

        # Only mandatory params are given
        client = Client(
            endpoint='#',
            login_username='username',
            login_password='password')
        headers = client._get_headers()
        self.assertEqual(headers, {
            'Content-type': 'application/json',
            'login.username': 'username',
            'login.password': 'password',
            'Authorization': "Basic {0}".format(
                base64.b64encode("username:password"))})

        # login.username and login.password are None
        client = Client(
            endpoint='#',
            login_username=None,
            login_password=None)
        headers = client._get_headers()
        self.assertEqual(headers, {
            'Content-type': 'application/json',
            'login.username': '',
            'login.password': '',
            'Authorization': "Basic {0}".format(base64.b64encode(':'))})

    def test_parse_response_result_empty(self):
        response = json.loads('{}')
        try:
            self.client._parse_response_result(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "'resultat' is not present in the response",
                cexception.message)

    def test_parse_response_result_with_undefined_exception(self):
        response = json.loads('''
            {
                "resultat": "ERROR"
            }''')
        try:
            self.client._parse_response_result(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "Error code UNDEFINED: Undefined",
                cexception.message)

    def test_parse_response_result_with_defined_exception(self):
        response = json.loads('''
            {
                "resultat": "ERROR",
                "resultatMissatge": "This is the message"
            }''')
        try:
            self.client._parse_response_result(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "Error code UNDEFINED: This is the message",
                cexception.message)

        response = json.loads('''
            {
                "resultat": "ERROR",
                "codiError": "5"
            }''')
        try:
            self.client._parse_response_result(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "Error code 5: Undefined",
                cexception.message)

        response = json.loads('''
            {
                "resultat": "ERROR",
                "codiError": "5",
                "resultatMissatge": "This is the message"
            }''')
        try:
            self.client._parse_response_result(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "Error code 5: This is the message",
                cexception.message)

    def test_parse_response_list_problems_empty(self):
        response = json.loads('''
            {
                "resultat": "SUCCESS",
                "resultatMissatge": "This is the message"
            }''')
        try:
            self.client._parse_response_list_problems(response)
            self.fail("ClientException should have been raised")
        except ClientException as cexception:
            self.assertEqual(
                "'llistaProblemes' is not present in the response",
                cexception.message)

    def test_parse_response_list_problems_not_empty(self):
        response = json.loads('''
{
   "llistaProblemes":
   [
       {
          "assumpte": "Gestió por VPN de gateway para servei atenció",
          "productNom": "e-Connect",
          "requirementId": "481897",
          "creatPerId": "11235",
          "productId": "33283",
          "statusId": "PROBLEMA_OBERT",
          "visiblePortalServeisTIC": "Y",
          "descripcioProblema": "No es posible acceder a través de la vpn",
          "creatPerNom": "Jose Antonio",
          "creatPerCognom": "Tebar Garcia",
          "dataCreacio": "2014-01-22 14:33:47.362",
          "dataLimitResolucioString": "2014-02-12 11:13:07.152",
          "idEmpresa": "1123",
          "urlProblema": "/problemes/control/problemaDetallDadesGenerals"
       },
       {}
   ],
   "resultat": "SUCCESS",
   "resultatMissatge": "Llista problemes retornada"
}
''')
        results = self.client._parse_response_list_problems(response)
        self.assertEqual(len(results), 2)
        self.assertEqual(
            results[0],
            Problem(
                topic=u"Gestió por VPN de gateway para servei atenció",
                description=u"No es posible acceder a través de la vpn",
                url=u"/problemes/control/problemaDetallDadesGenerals",
                date_creation=datetime.datetime(
                    2014, 01, 22, 14, 33, 47, 362000),
                date_fix=datetime.datetime(
                    2014, 02, 12, 11, 13, 07, 152000)))

        self.assertEqual(
            results[1],
            Problem(
                topic=u'',
                description=u'',
                url=u'',
                date_creation=u'',
                date_fix=u''))

    def test_parse_response_list_problems_wrong_format(self):
        response = json.loads('''
{
   "llistaProblemes":
   [
       {
          "assumpte": "Gestió por VPN de gateway para servei atenció",
          "descripcioProblema": "No es posible acceder a través de la vpn",
          "dataCreacio": "2014/01/22 14:33:47.362",
          "urlProblema": "/problemes/control/problemaDetallDadesGenerals"
       }
   ],
   "resultat": "SUCCESS",
   "resultatMissatge": "Llista problemes retornada"
}
''')
        results = self.client._parse_response_list_problems(response)
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0],
            Problem(
                topic=u"Gestió por VPN de gateway para servei atenció",
                description=u"No es posible acceder a través de la vpn",
                url=u"/problemes/control/problemaDetallDadesGenerals",
                date_creation=u'',
                date_fix=u''))

    def test_list_problems(self):
        # Parameter product_id empty
        try:
            self.client.list_problems("  \n   \t  ")
            self.fail("ClientException should have been raised")
        except ClientException as exception:
            self.assertEqual("Parameter 'product_id' cannot be empty",
                             exception.message)
        try:
            self.client.list_problems(None)
            self.fail("ClientException should have been raised")
        except ClientException as exception:
            self.assertEqual("Parameter 'product_id' cannot be empty",
                             exception.message)

        # Connection error
        with patch('genweb6.serveistic.ws_client.problems.requests.get',
                   side_effect=ConnectionError):
            try:
                self.client.list_problems(1)
                self.fail("ClientException should have been raised")
            except ClientException as exception:
                self.assertEqual("The connection with '{0}' could not be "
                                 "established".format(self.client.endpoint),
                                 exception.message)
        # Response status is not OK
        response_mock = MagicMock(status_code=500)
        with patch('genweb6.serveistic.ws_client.problems.requests.get',
                   side_effect=(response_mock,)):
            try:
                self.client.list_problems(1)
                self.fail("ClientException should have been raised")
            except ClientException as exception:
                self.assertEqual("Status code is not OK (500)",
                                 exception.message)

        # resultat is present
        response_mock = MagicMock(status_code=200)
        with patch('genweb6.serveistic.ws_client.problems.requests.get',
                   side_effect=(response_mock,)), patch(
                'genweb6.serveistic.ws_client.problems.Client._parse_response_list_problems',
                side_effect=([],)):
            self.assertEqual([], self.client.list_problems(1))

    def test_list_problems_with_count_parameter(self):
        response_mock = MagicMock(status_code=200)
        with patch('genweb6.serveistic.ws_client.problems.requests.get',
                   side_effect=(response_mock for _ in range(5))), patch(
                'genweb6.serveistic.ws_client.problems.Client._parse_response_list_problems',
                side_effect=([1, 2, 3, 4, 5, 6, 7, 8] for _ in range(5))):

            self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8],
                             self.client.list_problems(1))
            self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8],
                             self.client.list_problems(1, None))
            self.assertEqual([],
                             self.client.list_problems(1, 0))
            self.assertEqual([1, 2, 3, 4, 5],
                             self.client.list_problems(1, 5))
            self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8],
                             self.client.list_problems(1, 10))
