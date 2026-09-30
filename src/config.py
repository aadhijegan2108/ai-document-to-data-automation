import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


DEFAULT_GEMINI_MODEL = "gemini-3.5-flash-lite"
DEFAULT_LOG_FILE_NAME = "invoice_processing.log"


@dataclass(frozen=True)
class AppConfig:
    """Application configuration and project paths."""

    project_root: Path
    input_dir: Path
    output_dir: Path
    logs_dir: Path
    data_dir: Path
    registry_path: Path

    gemini_model: str
    gemini_api_key: str | None
    log_file_name: str


def create_config() -> AppConfig:
    """Create and validate the application configuration."""

    project_root = Path(__file__).resolve().parents[1]

    input_dir = project_root / "input"
    output_dir = project_root / "output"
    logs_dir = project_root / "logs"
    data_dir = project_root / "data"

    registry_path = data_dir / "invoice_registry.json"

    configured_model = os.getenv("GEMINI_MODEL")

    if configured_model is None:
        gemini_model = DEFAULT_GEMINI_MODEL
    else:
        gemini_model = configured_model.strip()

        if not gemini_model:
            raise ValueError(
                "GEMINI_MODEL cannot be empty."
            )

    gemini_api_key = os.getenv("GEMINI_API_KEY")

    return AppConfig(
        project_root=project_root,
        input_dir=input_dir,
        output_dir=output_dir,
        logs_dir=logs_dir,
        data_dir=data_dir,
        registry_path=registry_path,
        gemini_model=gemini_model,
        gemini_api_key=gemini_api_key,
        log_file_name=DEFAULT_LOG_FILE_NAME,
    )