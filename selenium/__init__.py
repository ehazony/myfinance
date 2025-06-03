"""Minimal selenium stub for tests."""

import sys

# Create submodule structure
webdriver_mod = sys.modules.setdefault(__name__ + '.webdriver', type(sys)('webdriver'))
common_mod = sys.modules.setdefault(__name__ + '.webdriver.common', type(sys)('common'))
by_mod = sys.modules.setdefault(__name__ + '.webdriver.common.by', type(sys)('by'))
support_mod = sys.modules.setdefault(__name__ + '.webdriver.support', type(sys)('support'))
ec_mod = sys.modules.setdefault(__name__ + '.webdriver.support.expected_conditions', type(sys)('expected_conditions'))
wait_mod = sys.modules.setdefault(__name__ + '.webdriver.support.wait', type(sys)('wait'))
dc_mod = sys.modules.setdefault(__name__ + '.webdriver.common.desired_capabilities', type(sys)('desired_capabilities'))

class By:
    ID = 'id'
    CLASS_NAME = 'class'
    XPATH = 'xpath'
by_mod.By = By

class WebDriverWait:
    def __init__(self, driver, timeout):
        pass
    def until(self, *args, **kwargs):
        return True
wait_mod.WebDriverWait = WebDriverWait

# Provide a dummy ExpectedConditions with attributes used
class _EC:
    def __getattr__(self, name):
        def _call(*args, **kwargs):
            return True
        return _call

ec_mod.__getattr__ = lambda name: getattr(_EC(), name)

# Ensure packages are importable
webdriver_mod.support = support_mod
webdriver_mod.common = common_mod
support_mod.expected_conditions = ec_mod
support_mod.wait = wait_mod
common_mod.by = by_mod
common_mod.desired_capabilities = dc_mod
dc_mod.DesiredCapabilities = type('DesiredCapabilities', (), {})

__all__ = ['webdriver']
