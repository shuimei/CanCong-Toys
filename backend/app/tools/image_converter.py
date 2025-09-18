from pydantic import BaseModel
from typing import List

class ImageConvertRequest(BaseModel):
    # 这里只定义数据模型，实际转换需要前端处理
    source_format: str
    target_format: str
    image_data: str  # base64编码的图片数据

class ImageConvertResult(BaseModel):
    success: bool
    message: str
    converted_image_data: str = None

class ImageFormatInfo(BaseModel):
    name: str
    description: str

def get_supported_formats() -> List[ImageFormatInfo]:
    """
    获取支持的图片格式
    """
    formats = [
        ImageFormatInfo(name="JPEG", description="常见的图片格式，支持压缩"),
        ImageFormatInfo(name="PNG", description="支持透明背景的无损图片格式"),
        ImageFormatInfo(name="GIF", description="支持动画的图片格式"),
        ImageFormatInfo(name="BMP", description="Windows位图格式"),
        ImageFormatInfo(name="WEBP", description="Google开发的现代图片格式，压缩率高"),
    ]
    return formats