from pydantic import BaseModel
from datetime import datetime
from typing import Union

class TimestampConvertRequest(BaseModel):
    value: Union[int, str]
    to_timestamp: bool = False  # True表示将日期转换为时间戳，False表示将时间戳转换为日期

class TimestampConvertResult(BaseModel):
    result: str
    original_value: Union[int, str]

def convert_timestamp(value: Union[int, str], to_timestamp: bool = False) -> TimestampConvertResult:
    """
    时间戳与日期相互转换
    :param value: 输入值（时间戳或日期字符串）
    :param to_timestamp: 转换方向
    :return: 转换结果
    """
    try:
        if to_timestamp:
            # 将日期转换为时间戳
            if isinstance(value, str):
                # 尝试解析日期字符串
                dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            else:
                raise ValueError("日期转换为时间戳时，输入值必须是日期字符串")
            
            timestamp = int(dt.timestamp())
            return TimestampConvertResult(
                result=str(timestamp),
                original_value=value
            )
        else:
            # 将时间戳转换为日期
            if isinstance(value, str):
                timestamp = int(value)
            else:
                timestamp = value
            
            dt = datetime.fromtimestamp(timestamp)
            formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")
            return TimestampConvertResult(
                result=formatted_date,
                original_value=value
            )
    except Exception as e:
        return TimestampConvertResult(
            result=f"转换错误: {str(e)}",
            original_value=value
        )