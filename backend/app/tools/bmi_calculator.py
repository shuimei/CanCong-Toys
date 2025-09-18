from pydantic import BaseModel

class BMIRequest(BaseModel):
    weight: float  # 体重(kg)
    height: float  # 身高(cm)

class BMIResult(BaseModel):
    bmi: float
    category: str
    description: str

def calculate_bmi(weight: float, height: float) -> BMIResult:
    """
    计算BMI指数
    :param weight: 体重(kg)
    :param height: 身高(cm)
    :return: BMI结果
    """
    # 将厘米转换为米
    height_m = height / 100
    
    # 计算BMI
    bmi = weight / (height_m ** 2)
    
    # 判断BMI类别
    if bmi < 18.5:
        category = "偏瘦"
        description = "您的体重偏轻，建议适当增加营养摄入"
    elif 18.5 <= bmi < 24:
        category = "正常"
        description = "您的体重正常，请保持健康的生活方式"
    elif 24 <= bmi < 28:
        category = "偏重"
        description = "您的体重偏重，建议适当控制饮食并加强锻炼"
    else:
        category = "肥胖"
        description = "您的体重超标，建议咨询医生并制定减重计划"
    
    return BMIResult(
        bmi=round(bmi, 2),
        category=category,
        description=description
    )