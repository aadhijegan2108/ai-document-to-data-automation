from application import run_application


def main() -> None:
    """Start the invoice automation application."""

    results, summary = run_application()

    print("\n" + "=" * 60)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 60)

    print(f"Total invoices        : {summary.total}")
    print(f"Successful            : {summary.successful}")
    print(f"Duplicates            : {summary.duplicates}")
    print(f"Validation failures   : {summary.validation_failed}")
    print(f"Processing errors     : {summary.processing_errors}")
    print(f"Total failed          : {summary.failed}")

    # Display individual non-success results.
    for result in results:
        if not result.is_success:
            print(
                f"\n{result.status.value.upper()}: "
                f"{result.filename}"
            )

            print(f"Message: {result.message}")

            for error in result.errors:
                print(f"- {error}")


if __name__ == "__main__":
    main()