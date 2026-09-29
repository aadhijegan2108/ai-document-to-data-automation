from dataclasses import dataclass
from typing import Iterable

from processing_result import ProcessingResult, ProcessingStatus


@dataclass(frozen=True)
class BatchSummary:
    """Summary of a batch invoice-processing run."""

    total: int
    successful: int
    duplicates: int
    validation_failed: int
    processing_errors: int

    @property
    def failed(self) -> int:
        """Return the total number of failed invoices."""

        return self.validation_failed + self.processing_errors


def create_batch_summary(
    results: Iterable[ProcessingResult],
) -> BatchSummary:
    """Create a summary from invoice-processing results."""

    results_list = list(results)

    successful = sum(
        result.status == ProcessingStatus.SUCCESS
        for result in results_list
    )

    duplicates = sum(
        result.status == ProcessingStatus.DUPLICATE
        for result in results_list
    )

    validation_failed = sum(
        result.status == ProcessingStatus.VALIDATION_FAILED
        for result in results_list
    )

    processing_errors = sum(
        result.status == ProcessingStatus.PROCESSING_ERROR
        for result in results_list
    )

    return BatchSummary(
        total=len(results_list),
        successful=successful,
        duplicates=duplicates,
        validation_failed=validation_failed,
        processing_errors=processing_errors,
    )