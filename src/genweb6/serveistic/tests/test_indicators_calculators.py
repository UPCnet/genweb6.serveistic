# -*- coding: utf-8 -*-

from mock import Mock
from mock import patch

from genweb6.serveistic.indicators.calculators import SessionsSourceServei

import unittest


class TestIndicatorsCalculators(unittest.TestCase):
    def setUp(self):
        pass

    # Test build_filters
    @patch('genweb6.serveistic.indicators.calculators.getToolByName')
    def test_bf_should_return_empty_re_if_no_services(self, mock_getToolByName):
        calculator = SessionsSourceServei('mock_context')
        with patch('genweb6.serveistic.data_access.servei.ServeiDataReporter.list_by_review_state',
                   side_effect=([], )):
            source_re = calculator._build_filters()
            self.assertEqual('ga:source=~^$', source_re)

    @patch('genweb6.serveistic.indicators.calculators.getToolByName')
    def test_bf_should_return_services_re_if_services(self, mock_getToolByName):
        calculator = SessionsSourceServei('mock_context')
        with patch('genweb6.serveistic.data_access.servei.ServeiDataReporter.list_by_review_state',
                   side_effect=([
                       Mock(website_url='http://domain1.com/a/b/c.html'),
                       Mock(website_url='http://domain2.com/a/b/c.html'),
                            ], )):
            source_re = calculator._build_filters()
            self.assertEqual(
                'ga:source=~^domain1\\.com$,ga:source=~^domain2\\.com$',
                source_re)

    @patch('genweb6.serveistic.indicators.calculators.getToolByName')
    def test_bf_should_return_services_re_if_services_with_url_none(self, mock_getToolByName):
        calculator = SessionsSourceServei('mock_context')
        with patch('genweb6.serveistic.data_access.servei.ServeiDataReporter.list_by_review_state',
                   side_effect=([
                       Mock(website_url='http://domain1.com/a/b/c.html'),
                       Mock(website_url=None),
                       Mock(website_url='http://domain2.com/a/b/c.html'),
                            ], )):
            source_re = calculator._build_filters()
            self.assertEqual(
                'ga:source=~^domain1\\.com$,ga:source=~^domain2\\.com$',
                source_re)

    @patch('genweb6.serveistic.indicators.calculators.getToolByName')
    def test_bf_should_return_services_re_if_services_with_url_empty(self, mock_getToolByName):
        calculator = SessionsSourceServei('mock_context')
        with patch('genweb6.serveistic.data_access.servei.ServeiDataReporter.list_by_review_state',
                   side_effect=([
                       Mock(website_url='http://domain1.com/a/b/c.html'),
                       Mock(website_url=''),
                       Mock(website_url='http://domain2.com/a/b/c.html'),
                            ], )):
            source_re = calculator._build_filters()
            self.assertEqual(
                'ga:source=~^domain1\\.com$,ga:source=~^domain2\\.com$',
                source_re)

    # Test extract_url_domain_re
    def test_eud_should_remove_protocol(self):
        calculator = SessionsSourceServei('mock_context')
        domain = calculator._extract_url_domain_re('http://domain.com')
        self.assertEqual('domain\\.com', domain)
        domain = calculator._extract_url_domain_re('ftp://domain.com')
        self.assertEqual('domain\\.com', domain)

    def test_eud_should_remove_path_after_domain(self):
        calculator = SessionsSourceServei('mock_context')
        domain = calculator._extract_url_domain_re('domain.com/1/3/4.html')
        self.assertEqual('domain\\.com', domain)

    def test_eud_should_remove_backslash_after_domain(self):
        calculator = SessionsSourceServei('mock_context')
        domain = calculator._extract_url_domain_re('domain.com/')
        self.assertEqual('domain\\.com', domain)

    def test_eud_should_remove_protocol_and_path(self):
        calculator = SessionsSourceServei('mock_context')
        domain = calculator._extract_url_domain_re(
            'http://domain.com/1/two/3.html')
        self.assertEqual('domain\\.com', domain)
