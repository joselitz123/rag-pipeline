import os
import unittest
from unittest.mock import patch
import importlib

class TestConfig(unittest.TestCase):

    def setUp(self):
        # Ensure a clean slate for each test by resetting modules
        if 'config' in globals():
            importlib.reload(globals()['config'])

    @patch.dict(os.environ, {"AZURE_TARGET_URI": "https://my-project.cognitiveservices.azure.com/openai/deployments/gpt-5-nano/chat/completions?api-version=2024-05-01-preview"})
    def test_azure_uri_parsing(self):
        import config
        importlib.reload(config)
        self.assertEqual(config.config.PROJECT_ENDPOINT, "https://my-project.cognitiveservices.azure.com")
        self.assertEqual(config.config.AZURE_DEPLOYMENT_NAME, "gpt-5-nano")
        self.assertEqual(config.config.API_VERSION, "2024-05-01-preview")

    @patch.dict(os.environ, {
        "PROJECT_ENDPOINT": "https://my-endpoint.com",
        "AZURE_DEPLOYMENT_NAME": "my-deployment",
        "API_VERSION": "2024-01-01",
        "AZURE_TARGET_URI": ""
    })
    def test_manual_config(self):
        import config
        importlib.reload(config)
        self.assertEqual(config.config.PROJECT_ENDPOINT, "https://my-endpoint.com")
        self.assertEqual(config.config.AZURE_DEPLOYMENT_NAME, "my-deployment")
        self.assertEqual(config.config.API_VERSION, "2024-01-01")

if __name__ == '__main__':
    unittest.main()
