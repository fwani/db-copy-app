import logging
from typing import List

import pymysql

import log
from config import DBSettings, DestSchema

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


def insert_rows(dest_schema: DestSchema, rows: List[List[object]]):
    insert_try_rows = len(rows)
    logger.info(f"Start to insert table. table_name = {dest_schema.table_name}, insert_rows = {insert_try_rows}")
    values_format = '(' + ', '.join(['%s'] * len(dest_schema.columns)) + ')'
    insert_sql = f"insert into {dest_schema.table_name}({', '.join(dest_schema.columns)}) values {values_format}"
    with pymysql.connect(host=dest_schema.db_info.host,
                         port=dest_schema.db_info.port,
                         user=dest_schema.db_info.user,
                         password=dest_schema.db_info.password,
                         db=dest_schema.db_info.dbname
                         ) as conn:
        try:
            with conn.cursor() as cur:
                if dest_schema.id_column is not None and len(dest_schema.id_column) > 0 and len(
                        dest_schema.ignore_id) > 0:
                    ignore_ids = [f"'{key}'" for key in dest_schema.ignore_id]
                    delete_sql = f"delete from {dest_schema.table_name} " \
                                 f"where {dest_schema.id_column} not in ({','.join(ignore_ids)})"
                    logger.info(
                        f"Delete rows where {dest_schema.id_column} not in {dest_schema.ignore_id}."
                        f" table_name = {dest_schema.table_name}")
                    cur.execute(delete_sql)
                for row in rows:
                    msg = "Insert {%-20s} ... " % str(row)
                    try:
                        cur.execute(insert_sql, row)
                        logger.info(msg + "OK")
                    except Exception as e:
                        logger.error(msg + "Fail")
            conn.commit()
            logger.info(
                f"Complete to delete and insert table."
                f" table_name = {dest_schema.table_name}, insert_rows = {len(rows)}")
        except Exception as e:
            raise


if __name__ == "__main__":
    log.setup_custom_logger()
    _db_settings = DBSettings(
        {"host": "localhost", "port": 3306, "dbname": "test", "user": "root", "password": "fwani"})
    rows = get_rows(_db_settings, "select * from analyze_tech")
    insert_rows(
        DestSchema({
            "db_info": _db_settings,
            "table_name": "analyze_tech_copied",
            "columns": ['id', 'name'],
            "id_column": 'id',
            "ignore_id": [2, 3, 4]
        }),
        rows=rows,
    )
