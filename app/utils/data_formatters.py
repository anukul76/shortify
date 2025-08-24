from typing import Any, List, Dict


class DataFormatter:
    @staticmethod
    def query_result_list(data: Any) -> List:
        return [dict(x._mapping) for x in data]

    @staticmethod
    def query_result_dict(data: Any) -> Dict:
        return dict(data._mapping)
