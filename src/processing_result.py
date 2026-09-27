from dataclasses import dataclass, field
from enum import Enum


class ProcessingStatus(Enum):
    """Possible outcomes for invoice processing."""

    SUCCESS = "success"
    DUPLICATE = "duplicate"
    VALIDATION_FAILED = "validation_failed"
    PROCESSING_ERROR = "processing_error"


@dataclass
class ProcessingResult:
    """Standard result returned after processing one invoice."""

    filename: str
    status: ProcessingStatus
    message: str = ""
    errors: list[str] = field(default_factory=list)

    @property
    def is_success(self) -> bool:
        """Return True when the invoice was processed successfully."""

        return self.status == ProcessingStatus.SUCCESS