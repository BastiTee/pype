# -*- coding: utf-8 -*-
"""Pype core tests."""

from pype.core import get_from_json_or_default


class TestCore:
    """Pype miscellaneous utils tests."""

    def test_get_from_json_or_default__noneinput(self):
        """get_from_json_or_default called with none-inputs."""
        value = get_from_json_or_default(None, None, None)
        assert not value

    def test_get_from_json_or_default__noneinputwithemptybreadcrumb(self):
        """get_from_json_or_default called with empty breadcrumb."""
        value = get_from_json_or_default(None, '', None)
        assert not value

    def test_get_from_json_or_default__noneinputwithbreadcrumb(self):
        """get_from_json_or_default called with breadcrumb but empty JSON."""
        value = get_from_json_or_default(None, 'test', None)
        assert not value

    def test_get_from_json_or_default__noneinputwithbreadcrumbcustom(self):
        """get_from_json_or_default called w/ crumb, empy JSON and default."""
        value = get_from_json_or_default(None, 'test', 'custom')
        assert value == 'custom'

    def test_get_from_json_or_default__firstlevelbreadcrumb(self):
        """get_from_json_or_default to resolve a first level entry."""
        value = get_from_json_or_default({
            'test': 'response'
        }, 'test', 'custom')
        assert value == 'response'

    def test_get_from_json_or_default__secondlevelbreadcrumb(self):
        """get_from_json_or_default to resolve a second level entry."""
        value = get_from_json_or_default({
            'test': {
                'subtest': 'response'
            }
        }, 'test.subtest', 'default'
        )
        assert value == 'response'

    def test_get_from_json_or_default__secondlevelbreadcrumbmiss(self):
        """get_from_json_or_default to miss a second level entry."""
        value = get_from_json_or_default({
            'test': {
                'subtest': 'response'
            }
        }, 'test.subtestmiss', 'default'
        )
        assert value == 'default'
