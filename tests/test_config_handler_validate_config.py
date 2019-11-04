# -*- coding: utf-8 -*-
"""pype.config_handler.validate_config."""

import copy

from pype.config_handler import PypeConfigHandler
from pype.exceptions import PypeException

from pytest import raises

from tests import VALID_CONFIG


class TestPypeConfigHandlerResolveConfigFile:  # noqa: D101

    def test_noneinput_raisetypeerror(self):  # noqa: D102
        config = PypeConfigHandler()
        with raises(PypeException):
            config.validate_config(None)

    def test_emptyinput_raisetypeerror(self):  # noqa: D102
        config = PypeConfigHandler()
        with raises(PypeException):
            config.validate_config({})

    def test_validfulljson(self):  # noqa: D102
        config = PypeConfigHandler()
        assert config.validate_config(VALID_CONFIG)

    def test_validfulljsonwithextensions(self):  # noqa: D102
        config = PypeConfigHandler()
        input_config = copy.deepcopy(VALID_CONFIG)
        input_config['additional_property'] = {}
        assert config.validate_config(input_config)

    def test_missingaliasesattribute(self):  # noqa: D102
        config = PypeConfigHandler()
        input_config = {
            'plugins': []
        }
        with raises(PypeException):
            config.validate_config(input_config)

    def test_misconfiguredplugin(self):  # noqa: D102
        config = PypeConfigHandler()
        input_config = copy.deepcopy(VALID_CONFIG)
        input_config['plugins'].append({
            'name': 'new_plugin'
        })
        with raises(PypeException):
            config.validate_config(input_config)

    def test_configuredplugin(self):  # noqa: D102
        config = PypeConfigHandler()
        input_config = copy.deepcopy(VALID_CONFIG)
        input_config['plugins'].append({
            'name': 'new_plugin',
            'path': '/some/path',
            'users': []
        })
        assert config.validate_config(input_config)

    def test_misconfigureduserinplugin(self):  # noqa: D102
        config = PypeConfigHandler()
        input_config = copy.deepcopy(VALID_CONFIG)
        input_config['plugins'].append({
            'name': 'new_plugin',
            'path': '/some/path',
            'users': [42]
        })
        with raises(PypeException):
            config.validate_config(input_config)

    def test_configuredalias(self):  # noqa: D102
        config = PypeConfigHandler()
        input_config = copy.deepcopy(VALID_CONFIG)
        input_config['aliases'].append({
            'alias': 'al',
            'command': 'pype test'
        })
        assert config.validate_config(input_config)

    def test_misconfiguredalias(self):  # noqa: D102
        config = PypeConfigHandler()
        input_config = copy.deepcopy(VALID_CONFIG)
        input_config['aliases'].append({
            'aliass': 'al',
            'commando': 'pype test'
        })
        with raises(PypeException):
            config.validate_config(input_config)