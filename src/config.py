import logging
import os
from typing import Dict, List

import yaml


class BaseSchema:
    def __getitem__(self, val):
        return self.__dict__[val]

    def __repr__(self):
        return '{%s}' % (
            ', '.join(f'{k} : {repr(v)}' for (k, v) in self.__dict__.items())
        )


class LoopSchema(BaseSchema):
    def __init__(self, obj: Dict):
        for k, v in obj.items():
            if isinstance(v, dict):
                setattr(self, k, LoopSchema(v))
            else:
                setattr(self, k, v)


class DBSettings(LoopSchema):
    host: str
    port: int
    dbname: str
    user: str
    password: str


class SourceSchema(LoopSchema):
    sql: str
    db_info: DBSettings


class DestSchema(LoopSchema):
    table_name: str
    columns: List
    db_info: DBSettings
    id_column: str = None
    ignore_id: List = []


class CaseSchema(BaseSchema):
    source: SourceSchema
    dest: DestSchema

    def __init__(self, case: Dict):
        self.source = SourceSchema(case['source'])
        self.dest = DestSchema(case['dest'])


logger = logging.getLogger(__name__)


def load(path=None):
    logger.info(f"Start load config file. path = {path}")
    if path is None:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../config.yml")
    with open(path, 'r') as f:
        data = yaml.load(f, yaml.Loader)

    cases = []
    for case in data['case']:
        cases.append(CaseSchema(case))
    logger.info(f"Complete load config file. cases is [{cases}]")
    return cases


if __name__ == "__main__":
    data = load("../config.yml")
    print(data)
