import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Allow Python to import modules from the src folder.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from config import AppConfig, create_config


class TestConfig(unittest.TestCase):

    def test_create_config_returns_app_config(self):
        config = create_config()

        self.assertIsInstance(config, AppConfig)

    def test_project_root_is_correct(self):
        config = create_config()

        self.assertEqual(
            config.project_root,
            project_root,
        )

    def test_directory_paths_are_correct(self):
        config = create_config()

        self.assertEqual(
            config.input_dir,
            project_root / "input",
        )

        self.assertEqual(
            config.output_dir,
            project_root / "output",
        )

        self.assertEqual(
            config.logs_dir,
            project_root / "logs",
        )

        self.assertEqual(
            config.data_dir,
            project_root / "data",
        )

    def test_registry_path_is_correct(self):
        config = create_config()

        self.assertEqual(
            config.registry_path,
            project_root / "data" / "invoice_registry.json",
        )

    def test_gemini_model_is_configured(self):
        config = create_config()

        self.assertEqual(
            config.gemini_model,
            "gemini-3.5-flash-lite",
        )

    def test_gemini_api_key_is_loaded(self):
        with patch.dict(
            os.environ,
            {"GEMINI_API_KEY": "test-api-key"},
            clear=False,
        ):
            config = create_config()

        self.assertEqual(
            config.gemini_api_key,
            "test-api-key",
        )

    def test_log_file_name_is_configured(self):
        config = create_config()

        self.assertEqual(
            config.log_file_name,
            "invoice_processing.log",
        )

    def test_empty_gemini_model_is_rejected(self):
        with patch.dict(
            os.environ,
            {"GEMINI_MODEL": ""},
            clear=False,
        ):
            with self.assertRaises(
                ValueError
            ) as context:
                create_config()

        self.assertEqual(
            str(context.exception),
            "GEMINI_MODEL cannot be empty.",
        )
if __name__ == "__main__":
    unittest.main()