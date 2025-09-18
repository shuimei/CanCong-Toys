from pydantic import BaseModel
from enum import Enum
from typing import Dict, List

class UnitType(str, Enum):
    LENGTH = "length"
    WEIGHT = "weight"
    TEMPERATURE = "temperature"

class UnitConvertRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str
    unit_type: UnitType

class UnitConvertResult(BaseModel):
    result: float
    from_value: float
    from_unit: str
    to_unit: str

# 定义单位换算关系
CONVERSION_FACTORS: Dict[UnitType, Dict[str, float]] = {
    UnitType.LENGTH: {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "inch": 0.0254,
        "foot": 0.3048,
        "yard": 0.9144,
        "mile": 1609.344
    },
    UnitType.WEIGHT: {
        "mg": 0.000001,
        "g": 0.001,
        "kg": 1.0,
        "ton": 1000.0,
        "oz": 0.0283495,
        "lb": 0.453592
    },
    UnitType.TEMPERATURE: {
        "celsius": 1.0,
        "fahrenheit": 1.0,
        "kelvin": 1.0
    }
}

def convert_unit(
    value: float,
    from_unit: str,
    to_unit: str,
    unit_type: UnitType
) -> UnitConvertResult:
    """
    单位换算
    :param value: 输入值
    :param from_unit: 源单位
    :param to_unit: 目标单位
    :param unit_type: 单位类型
    :return: 换算结果
    """
    try:
        if unit_type == UnitType.TEMPERATURE:
            # 温度换算需要特殊处理
            result = _convert_temperature(value, from_unit, to_unit)
        else:
            # 其他单位换算
            factors = CONVERSION_FACTORS[unit_type]
            
            if from_unit not in factors:
                raise ValueError(f"不支持的源单位: {from_unit}")
            
            if to_unit not in factors:
                raise ValueError(f"不支持的目标单位: {to_unit}")
            
            # 转换到基准单位再转换到目标单位
            base_value = value * factors[from_unit]
            result = base_value / factors[to_unit]
        
        return UnitConvertResult(
            result=round(result, 6),
            from_value=value,
            from_unit=from_unit,
            to_unit=to_unit
        )
    except Exception as e:
        raise ValueError(f"单位换算错误: {str(e)}")

def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """
    温度单位换算
    """
    # 先转换为摄氏度
    if from_unit == "fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "kelvin":
        celsius = value - 273.15
    else:  # celsius
        celsius = value
    
    # 从摄氏度转换为目标单位
    if to_unit == "fahrenheit":
        return celsius * 9/5 + 32
    elif to_unit == "kelvin":
        return celsius + 273.15
    else:  # celsius
        return celsius

def get_supported_units(unit_type: UnitType) -> List[str]:
    """
    获取支持的单位列表
    """
    return list(CONVERSION_FACTORS[unit_type].keys())