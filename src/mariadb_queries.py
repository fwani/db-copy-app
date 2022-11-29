import logging
from typing import List

import pymysql

import log
from config import DBSettings

logger = logging.getLogger(__name__)


def get_rows(db_settings: DBSettings, sql: str):
    logger.info(f"Start to get rows. sql = [{sql}]")
    with pymysql.connect(host=db_settings.host,
                         port=db_settings.port,
                         user=db_settings.user,
                         password=db_settings.password,
                         db=db_settings.dbname
                         ) as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
            logger.info(f"Complete to get rows. sql = [{sql}]")
            return rows
        except Exception as e:
            raise


def insert_rows(db_settings: DBSettings, table_name: str, columns: List[str], rows: List[List[object]]):
    insert_try_rows = len(rows)
    logger.info(f"Start to insert table. table_name = {table_name}, insert_rows = {insert_try_rows}")
    count_target_sql = f"select count(*) from {table_name}"
    values_format = '(' + ', '.join(['%s'] * len(columns)) + ')'
    insert_sql = f"insert IGNORE into {table_name}({', '.join(columns)}) values {values_format}"
    with pymysql.connect(host=db_settings.host,
                         port=db_settings.port,
                         user=db_settings.user,
                         password=db_settings.password,
                         db=db_settings.dbname
                         ) as conn:
        try:
            with conn.cursor() as cur:
                before_count = get_rows(db_settings, count_target_sql)[0][0]
                logger.info(f"Before count of {table_name} is {before_count}, Now try insert [{insert_try_rows}] rows")
                cur.executemany(insert_sql, rows)
                conn.commit()
                after_count = get_rows(db_settings, count_target_sql)[0][0]
                logger.info(f"After count of {table_name} is {after_count},"
                            f" Ignored rows is [{insert_try_rows - (after_count - before_count)}].")
            logger.info(f"Complete to delete and insert table. table_name = {table_name}, insert_rows = {len(rows)}")
        except Exception as e:
            raise


if __name__ == "__main__":
    log.setup_custom_logger()
    _db_settings = DBSettings(
        {"host": "localhost", "port": 3306, "dbname": "test", "user": "root", "password": "fwani"})
    rows = get_rows(_db_settings, "select * from analyze_tech")
    insert_rows(_db_settings, "analyze_tech_copied", columns=['id', 'name'], rows=rows)
