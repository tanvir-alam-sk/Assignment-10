# llmApp/tests/test_runner.py

from django.test.runner import DiscoverRunner

class NoDbTestRunner(DiscoverRunner):
    """A custom test runner to prevent Django from setting up a test database."""
    
    def setup_databases(self, **kwargs):
        """Override database creation"""
        pass

    def teardown_databases(self, old_config, **kwargs):
        """Override database teardown"""
        pass
