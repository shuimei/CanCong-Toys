from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Union, List
from ..tools.bmi_calculator import BMIRequest, BMIResult, calculate_bmi
from ..tools.image_converter import ImageConvertRequest, ImageConvertResult, get_supported_formats
from ..tools.password_generator import PasswordRequest, PasswordResult, generate_password
from ..tools.text_case_converter import TextCaseRequest, TextCaseResult, convert_text_case, CaseType
from ..tools.timestamp_converter import TimestampConvertRequest, TimestampConvertResult, convert_timestamp
from ..tools.unit_converter import UnitConvertRequest, UnitConvertResult, convert_unit, get_supported_units, UnitType

router = APIRouter(prefix="/api/functions", tags=["functions"])

class FunctionResponse(BaseModel):
    success: bool
    data: Union[BMIResult, PasswordResult, TextCaseResult, TimestampConvertResult, UnitConvertResult, list, dict, None]
    message: str = None

@router.post("/bmi", response_model=FunctionResponse)
async def bmi_calculator(request: BMIRequest):
    """BMI计算器功能"""
    try:
        result = calculate_bmi(request.weight, request.height)
        return FunctionResponse(success=True, data=result)
    except Exception as e:
        return FunctionResponse(success=False, message=str(e))

@router.get("/image-formats", response_model=FunctionResponse)
async def get_image_formats():
    """获取支持的图片格式"""
    try:
        formats = get_supported_formats()
        return FunctionResponse(success=True, data=formats)
    except Exception as e:
        return FunctionResponse(success=False, message=str(e))

@router.post("/convert-image", response_model=FunctionResponse)
async def convert_image(request: ImageConvertRequest):
    """图片格式转换功能"""
    try:
        # 实际应用中这里会处理图片转换
        # 当前只是模拟返回成功
        result = ImageConvertResult(
            success=True,
            message=f"图片已从 {request.source_format} 转换为 {request.target_format}",
            converted_image_data=request.image_data  # 实际应该返回转换后的数据
        )
        return FunctionResponse(success=True, data=result)
    except Exception as e:
        return FunctionResponse(success=False, message=str(e))

@router.post("/generate-password", response_model=FunctionResponse)
async def generate_password_endpoint(request: PasswordRequest):
    """密码生成器功能"""
    try:
        result = generate_password(
            length=request.length,
            include_uppercase=request.include_uppercase,
            include_lowercase=request.include_lowercase,
            include_digits=request.include_digits,
            include_symbols=request.include_symbols
        )
        return FunctionResponse(success=True, data=result)
    except Exception as e:
        return FunctionResponse(success=False, message=str(e))

@router.post("/convert-text-case", response_model=FunctionResponse)
async def convert_text_case_endpoint(request: TextCaseRequest):
    """文本大小写转换功能"""
    try:
        result = convert_text_case(request.text, request.case_type)
        return FunctionResponse(success=True, data=result)
    except Exception as e:
        return FunctionResponse(success=False, message=str(e))

@router.post("/convert-timestamp", response_model=FunctionResponse)
async def convert_timestamp_endpoint(request: TimestampConvertRequest):
    """时间戳转换功能"""
    try:
        result = convert_timestamp(request.value, request.to_timestamp)
        return FunctionResponse(success=True, data=result)
    except Exception as e:
        return FunctionResponse(success=False, message=str(e))

@router.post("/convert-unit", response_model=FunctionResponse)
async def convert_unit_endpoint(request: UnitConvertRequest):
    """单位换算功能"""
    try:
        result = convert_unit(request.value, request.from_unit, request.to_unit, request.unit_type)
        return FunctionResponse(success=True, data=result)
    except Exception as e:
        return FunctionResponse(success=False, message=str(e))

@router.get("/unit-types/{unit_type}", response_model=FunctionResponse)
async def get_unit_types(unit_type: UnitType):
    """获取支持的单位类型"""
    try:
        units = get_supported_units(unit_type)
        return FunctionResponse(success=True, data=units)
    except Exception as e:
        return FunctionResponse(success=False, message=str(e))