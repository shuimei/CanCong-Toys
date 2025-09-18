// API 配置文件

// 从环境变量获取基础URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// API 端点配置
export const API_ENDPOINTS = {
  // 工具相关
  TOOLS: `${API_BASE_URL}/api/tools`,
  TOOL_DETAIL: (id) => `${API_BASE_URL}/api/tools/${id}`,
  SEARCH_TOOLS: (query) => `${API_BASE_URL}/api/tools/search?query=${encodeURIComponent(query)}`,
  POPULAR_TOOLS: `${API_BASE_URL}/api/tools/popular`,
  RECENT_TOOLS: `${API_BASE_URL}/api/tools/recent`,
  
  // 工具功能相关
  BMI_CALCULATE: `${API_BASE_URL}/api/functions/bmi`,
  IMAGE_FORMATS: `${API_BASE_URL}/api/functions/image-formats`,
  IMAGE_CONVERT: `${API_BASE_URL}/api/functions/convert-image`,
  GENERATE_PASSWORD: `${API_BASE_URL}/api/functions/generate-password`,
  CONVERT_TEXT_CASE: `${API_BASE_URL}/api/functions/convert-text-case`,
  CONVERT_TIMESTAMP: `${API_BASE_URL}/api/functions/convert-timestamp`,
  CONVERT_UNIT: `${API_BASE_URL}/api/functions/convert-unit`,
  UNIT_TYPES: (unitType) => `${API_BASE_URL}/api/functions/unit-types/${unitType}`
}

// 添加一个辅助函数用于调试API调用
export const apiCall = async (url, options = {}) => {
  console.log('API调用:', url, options);
  
  try {
    const response = await fetch(url, options);
    console.log('API响应:', response.status, response.statusText);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('API数据:', data);
    return { success: true, data };
  } catch (error) {
    console.error('API调用失败:', error);
    return { success: false, error: error.message };
  }
};

export default {
  API_BASE_URL,
  API_ENDPOINTS,
  apiCall
}