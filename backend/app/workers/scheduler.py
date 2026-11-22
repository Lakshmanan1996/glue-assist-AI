import time
import logging
import schedule

from backend.app.workers.document_sync import scan_documents


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_document_scan():

    logging.info("Starting scheduled document scan")

    try:

        result = scan_documents()

        logging.info("New documents: %s", len(result["new"]))
        logging.info("Modified documents: %s", len(result["modified"]))
        logging.info("Unchanged documents: %s", len(result["unchanged"]))
        logging.info("Deleted documents: %s", len(result["deleted"]))

    except Exception:

        logging.exception("Document scan failed")


schedule.every(5).minutes.do(run_document_scan)


if __name__ == "__main__":

    logging.info("Glue Assist document scheduler started")

    run_document_scan()

    while True:

        schedule.run_pending()

        time.sleep(1)
