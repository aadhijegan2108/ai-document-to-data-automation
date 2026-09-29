from batch_processor import process_batch
from batch_reporter import BatchSummary, create_batch_summary
from config import AppConfig, create_config
from logger import setup_logger
from processing_result import ProcessingResult


def run_application(
    config: AppConfig | None = None,
) -> tuple[list[ProcessingResult], BatchSummary]:
    """Run the complete invoice automation workflow."""

    if config is None:
        config = create_config()

    # Create required directories.
    config.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    config.data_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger = setup_logger(config)

    logger.info("=" * 60)
    logger.info("BATCH INVOICE PROCESSING STARTED")
    logger.info("=" * 60)

    results = process_batch(
        config,
        logger,
    )

    summary = create_batch_summary(results)

    logger.info("=" * 60)
    logger.info("BATCH INVOICE PROCESSING COMPLETED")
    logger.info(
        f"Summary | Total: {summary.total} | "
        f"Successful: {summary.successful} | "
        f"Duplicates: {summary.duplicates} | "
        f"Validation Failed: {summary.validation_failed} | "
        f"Processing Errors: {summary.processing_errors}"
    )
    logger.info("=" * 60)

    return results, summary