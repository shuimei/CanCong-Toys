from pydantic import BaseModel
import random
import string

class PasswordRequest(BaseModel):
    length: int = 12
    include_uppercase: bool = True
    include_lowercase: bool = True
    include_digits: bool = True
    include_symbols: bool = False

class PasswordResult(BaseModel):
    password: str
    strength: str

def generate_password(
    length: int = 12,
    include_uppercase: bool = True,
    include_lowercase: bool = True,
    include_digits: bool = True,
    include_symbols: bool = False
) -> PasswordResult:
    """
    生成安全的随机密码
    :param length: 密码长度
    :param include_uppercase: 是否包含大写字母
    :param include_lowercase: 是否包含小写字母
    :param include_digits: 是否包含数字
    :param include_symbols: 是否包含符号
    :return: 生成的密码和强度评估
    """
    if length < 1:
        length = 12
    
    # 构建字符集
    characters = ""
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # 如果没有选择任何字符类型，默认包含小写字母和数字
    if not characters:
        characters = string.ascii_lowercase + string.digits
    
    # 生成密码
    password = ''.join(random.choice(characters) for _ in range(length))
    
    # 评估密码强度
    strength = "弱"
    if length >= 8:
        strength = "中"
    if length >= 12 and include_uppercase and include_digits:
        strength = "强"
    if length >= 16 and include_symbols:
        strength = "很强"
    
    # 确保返回UTF-8编码的字符串
    return PasswordResult(password=password, strength=strength)