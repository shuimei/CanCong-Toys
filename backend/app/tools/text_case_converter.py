from pydantic import BaseModel
from enum import Enum

class CaseType(str, Enum):
    UPPER = "upper"
    LOWER = "lower"
    TITLE = "title"
    SENTENCE = "sentence"
    CAPITALIZE = "capitalize"

class TextCaseRequest(BaseModel):
    text: str
    case_type: CaseType

class TextCaseResult(BaseModel):
    converted_text: str

def convert_text_case(text: str, case_type: CaseType) -> TextCaseResult:
    """
    转换文本大小写格式
    :param text: 输入文本
    :param case_type: 转换类型
    :return: 转换后的文本
    """
    if not text:
        return TextCaseResult(converted_text="")
    
    if case_type == CaseType.UPPER:
        converted_text = text.upper()
    elif case_type == CaseType.LOWER:
        converted_text = text.lower()
    elif case_type == CaseType.TITLE:
        converted_text = text.title()
    elif case_type == CaseType.CAPITALIZE:
        converted_text = text.capitalize()
    elif case_type == CaseType.SENTENCE:
        # 句子格式：每句话的首字母大写
        sentences = text.split('. ')
        converted_sentences = [s.capitalize() for s in sentences]
        converted_text = '. '.join(converted_sentences)
    else:
        converted_text = text
    
    return TextCaseResult(converted_text=converted_text)