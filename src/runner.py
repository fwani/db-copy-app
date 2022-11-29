import argparse
import logging

import log
import mariadb_queries
from config import load

logger = logging.getLogger(__name__)


def run_all(path):
    cases = load(path)
    logger.info(f"Run all cases. cases count = {len(cases)}")
    for case in cases:
        try:
            rows = mariadb_queries.get_rows(
                case.source.db_info,
                case.source.sql
            )
            mariadb_queries.delete_and_insert_rows(
                case.dest.db_info,
                table_name=case.dest.table_name,
                columns=case.dest.columns,
                rows=rows
            )
            logger.info(f"This case is work successfully. case = {case}")
        except Exception as e:
            logger.exception(e)
            logger.error(f"This case is not work successfully. case = {case}")


def run(_args):
    if _args.mode == "all":
        run_all(_args.conf)
    else:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mode", dest="mode", default="all")
    parser.add_argument("-c", "--conf", dest="conf", required=True)
    args = parser.parse_args()
    log.setup_custom_logger()
    run(args)
