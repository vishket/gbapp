#!/usr/bin/env python

import os
import unittest

# Local import
from gbapp import app

basedir = os.path.abspath(os.path.dirname(__file__))


class TestGBApp(unittest.TestCase):
    """
    Tests for Guidebook sample app
    """
    def test_parse_schema_legit(self):
        """
        Test if input file exists
        Expect query string and None
        :return:
        """
        legit_input_file = basedir + '/test.csv'
        query, err = app.parse_schema(legit_input_file)
        assert query == "id INT, name VARCHAR, age INT"

    def test_parse_schema_error(self):
        """
        Test if input file does not exist
        Expect to return None type and error since input file is missing
        :return:
        """
        fake_input_file = basedir + "/fake.csv"
        query, err = app.parse_schema(fake_input_file)
        assert err is not None
