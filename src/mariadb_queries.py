import logging
from typing import List

import pymysql

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
            logger.info(f"Complete to get rows. sql = [{sql}], rows = {len(rows)}")
            return rows
        except Exception as e:
            raise


def delete_and_insert_rows(db_settings: DBSettings, table_name: str, columns: List[str], rows: List[List[object]]):
    logger.info(f"Start to delete and insert table. table_name = {table_name}, insert_rows = {len(rows)}")
    delete_sql = f"delete from {table_name}"
    values_format = '(' + ', '.join(['%s'] * len(columns)) + ')'
    insert_sql = f"insert into {table_name}({', '.join(columns)}) values {values_format}"
    with pymysql.connect(host=db_settings.host,
                         port=db_settings.port,
                         user=db_settings.user,
                         password=db_settings.password,
                         db=db_settings.dbname
                         ) as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(delete_sql)
                cur.executemany(insert_sql, rows)
            conn.commit()
            logger.info(f"Complete to delete and insert table. table_name = {table_name}, insert_rows = {len(rows)}")
        except Exception as e:
            raise


if __name__ == "__main__":
    _db_settings = DBSettings(
        {"host": "localhost", "port": 3306, "dbname": "test", "user": "root", "password": "fwani"})
    rows = get_rows(_db_settings, "select * from analyze_tech")
    delete_and_insert_rows(_db_settings,
                           "analyze_tech_copied", columns=['id', 'name'],
                           rows=rows)
