"Flag feature tests."""

import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
)

from ensign import BinaryFlag


@pytest.fixture
def flag(db):
    """
    Create a flag for the current feature under test, clean up when done.
    """
    return BinaryFlag.create("flag0")


@given('a feature flag named "flag0"')
def a_feature_flag_named_flag0():
    """a feature flag named "flag0"."""


@pytest.mark.spec
@scenario('flag.feature', 'Enable the feature')
def test_enable_the_feature():
    """Enable the feature."""


@given('the flag is enabled')
def the_flag_is_enabled(flag):
    """the flag is enabled."""
    flag.set()


@then('the code should run')
def the_code_should_run(flag):
    """the code should run."""
    @flag
    def testfun():
        return "executed"
    assert testfun() == "executed"


@pytest.mark.spec
@scenario('flag.feature', 'Disable the feature')
def test_disable_the_feature():
    """Disable the feature."""


@given('the flag is disabled')
def the_flag_is_disabled(flag):
    """the flag is disabled."""
    flag.unset()


@then('the code should not run')
def the_code_should_not_run(flag):
    """the code should not run."""
    @flag
    def testfun():
        return "executed"
    assert testfun() is None
