<template>
  <div class="tool-detail" v-if="tool">
    <el-page-header @back="goBack" :content="tool.name" class="page-header" />
    
    <div class="tool-info">
      <div class="tool-header">
        <div class="icon-wrapper">
          <el-icon size="32" color="#409eff">
            <component :is="getToolIcon(tool.id)" />
          </el-icon>
        </div>
        <div>
          <h1>{{ tool.name }}</h1>
          <p class="tool-description">{{ tool.description }}</p>
        </div>
        <el-tag type="info">{{ tool.category }}</el-tag>
      </div>
      
      <div class="tool-content">
        <!-- BMI计算器 -->
        <div v-if="tool.id === 1" class="tool-form">
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon class="card-header-icon"><component :is="scaleIcon" /></el-icon>
                <span>计算BMI</span>
              </div>
            </template>
            
            <el-form :model="bmiForm" label-width="80px" @submit.prevent="calculateBMI">
              <el-form-item label="身高">
                <el-input v-model.number="bmiForm.height" placeholder="请输入身高(cm)">
                  <template #append>cm</template>
                </el-input>
              </el-form-item>
              
              <el-form-item label="体重">
                <el-input v-model.number="bmiForm.weight" placeholder="请输入体重(kg)">
                  <template #append>kg</template>
                </el-input>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="calculateBMI" :loading="calculating">
                  计算BMI
                </el-button>
              </el-form-item>
            </el-form>
            
            <div v-if="bmiResult" class="result">
              <el-alert
                :title="`您的BMI指数是: ${bmiResult.bmi}`"
                :type="getAlertType(bmiResult.category)"
                show-icon
                :description="bmiResult.description"
                class="result-alert"
              />
            </div>
          </el-card>
        </div>
        
        <!-- 图片格式转换器 -->
        <div v-else-if="tool.id === 2" class="tool-form">
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon class="card-header-icon"><component :is="pictureIcon" /></el-icon>
                <span>图片格式转换</span>
              </div>
            </template>
            
            <el-form :model="imageForm" label-width="100px">
              <el-form-item label="源格式">
                <el-select v-model="imageForm.sourceFormat" placeholder="请选择源格式">
                  <el-option
                    v-for="format in imageFormats"
                    :key="format.name"
                    :label="format.name"
                    :value="format.name"
                  />
                </el-select>
              </el-form-item>
              
              <el-form-item label="目标格式">
                <el-select v-model="imageForm.targetFormat" placeholder="请选择目标格式">
                  <el-option
                    v-for="format in imageFormats"
                    :key="format.name"
                    :label="format.name"
                    :value="format.name"
                    :disabled="format.name === imageForm.sourceFormat"
                  />
                </el-select>
              </el-form-item>
              
              <el-form-item label="上传图片">
                <el-upload
                  class="upload-demo"
                  drag
                  action="#"
                  :auto-upload="false"
                  :on-change="handleFileChange"
                >
                  <el-icon class="el-icon--upload"><component :is="uploadFilledIcon" /></el-icon>
                  <div class="el-upload__text">
                    将文件拖到此处，或<em>点击上传</em>
                  </div>
                </el-upload>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="convertImage" :disabled="!imageFile">
                  转换图片
                </el-button>
              </el-form-item>
            </el-form>
            
            <div v-if="convertResult" class="result">
              <el-alert
                :title="convertResult.message"
                :type="convertResult.success ? 'success' : 'error'"
                show-icon
                class="result-alert"
              />
            </div>
          </el-card>
        </div>
        
        <!-- 密码生成器 -->
        <div v-else-if="tool.id === 3" class="tool-form">
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon class="card-header-icon"><component :is="keyIcon" /></el-icon>
                <span>密码生成器</span>
              </div>
            </template>
            
            <el-form :model="passwordForm" label-width="120px">
              <el-form-item label="密码长度">
                <el-slider 
                  v-model="passwordForm.length" 
                  :min="4" 
                  :max="50" 
                  show-input
                />
              </el-form-item>
              
              <el-form-item label="包含字符类型">
                <el-checkbox-group v-model="passwordForm.characterTypes">
                  <el-checkbox label="uppercase">大写字母</el-checkbox>
                  <el-checkbox label="lowercase">小写字母</el-checkbox>
                  <el-checkbox label="digits">数字</el-checkbox>
                  <el-checkbox label="symbols">符号</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="generatePassword">
                  生成密码
                </el-button>
              </el-form-item>
            </el-form>
            
            <div v-if="passwordResult" class="result">
              <el-alert
                title="生成的密码"
                type="success"
                show-icon
                class="result-alert"
              >
                <template #default>
                  <div class="password-result">
                    <div class="password-text">{{ passwordResult.generated_password }}</div>
                    <div class="password-strength">强度: {{ passwordResult.strength }}</div>
                    <el-button 
                      size="small" 
                      @click="copyToClipboard(passwordResult.generated_password)"
                      class="copy-button"
                    >
                      复制密码
                    </el-button>
                  </div>
                </template>
              </el-alert>
            </div>
          </el-card>
        </div>
        
        <!-- 文本大小写转换 -->
        <div v-else-if="tool.id === 4" class="tool-form">
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon class="card-header-icon"><component :is="documentIcon" /></el-icon>
                <span>文本大小写转换</span>
              </div>
            </template>
            
            <el-form :model="textCaseForm" label-width="100px">
              <el-form-item label="输入文本">
                <el-input
                  v-model="textCaseForm.text"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入要转换的文本"
                />
              </el-form-item>
              
              <el-form-item label="转换类型">
                <el-select v-model="textCaseForm.caseType" placeholder="请选择转换类型">
                  <el-option label="大写" value="upper" />
                  <el-option label="小写" value="lower" />
                  <el-option label="首字母大写" value="title" />
                  <el-option label="句首字母大写" value="sentence" />
                  <el-option label="首字符大写" value="capitalize" />
                </el-select>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="convertTextCase">
                  转换文本
                </el-button>
              </el-form-item>
            </el-form>
            
            <div v-if="textCaseResult" class="result">
              <el-alert
                title="转换结果"
                type="success"
                show-icon
                class="result-alert"
              >
                <template #default>
                  <div class="text-result">
                    <el-input
                      type="textarea"
                      :rows="4"
                      :value="textCaseResult.converted_text"
                      readonly
                    />
                    <el-button 
                      size="small" 
                      @click="copyToClipboard(textCaseResult.converted_text)"
                      class="copy-button"
                    >
                      复制结果
                    </el-button>
                  </div>
                </template>
              </el-alert>
            </div>
          </el-card>
        </div>
        
        <!-- 时间戳转换器 -->
        <div v-else-if="tool.id === 5" class="tool-form">
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon class="card-header-icon"><component :is="clockIcon" /></el-icon>
                <span>时间戳转换器</span>
              </div>
            </template>
            
            <el-form :model="timestampForm" label-width="120px">
              <el-form-item label="输入值">
                <el-input v-model="timestampForm.value" placeholder="请输入时间戳或日期">
                  <template #append>
                    <el-select v-model="timestampForm.type" style="width: 120px">
                      <el-option label="时间戳" value="timestamp" />
                      <el-option label="日期" value="date" />
                    </el-select>
                  </template>
                </el-input>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="convertTimestamp">
                  转换
                </el-button>
              </el-form-item>
            </el-form>
            
            <div v-if="timestampResult" class="result">
              <el-alert
                title="转换结果"
                :type="timestampResult.result.includes('错误') ? 'error' : 'success'"
                show-icon
                class="result-alert"
              >
                <template #default>
                  <div class="timestamp-result">
                    <div class="result-item">
                      <label>原始值:</label>
                      <span>{{ timestampResult.original_value }}</span>
                    </div>
                    <div class="result-item">
                      <label>转换结果:</label>
                      <span>{{ timestampResult.result }}</span>
                    </div>
                  </div>
                </template>
              </el-alert>
            </div>
          </el-card>
        </div>
        
        <!-- 单位换算器 -->
        <div v-else-if="tool.id === 6" class="tool-form">
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon class="card-header-icon"><component :is="magicStickIcon" /></el-icon>
                <span>单位换算器</span>
              </div>
            </template>
            
            <el-form :model="unitForm" label-width="100px">
              <el-form-item label="单位类型">
                <el-select 
                  v-model="unitForm.unitType" 
                  placeholder="请选择单位类型"
                  @change="onUnitTypeChange"
                >
                  <el-option label="长度" value="length" />
                  <el-option label="重量" value="weight" />
                  <el-option label="温度" value="temperature" />
                </el-select>
              </el-form-item>
              
              <el-form-item label="数值">
                <el-input-number 
                  v-model="unitForm.value" 
                  :precision="6" 
                  :step="1"
                  controls-position="right"
                />
              </el-form-item>
              
              <el-form-item label="从">
                <el-select v-model="unitForm.fromUnit" placeholder="源单位">
                  <el-option
                    v-for="unit in unitOptions"
                    :key="unit"
                    :label="unit"
                    :value="unit"
                  />
                </el-select>
              </el-form-item>
              
              <el-form-item label="到">
                <el-select v-model="unitForm.toUnit" placeholder="目标单位">
                  <el-option
                    v-for="unit in unitOptions"
                    :key="unit"
                    :label="unit"
                    :value="unit"
                  />
                </el-select>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="convertUnit">
                  换算
                </el-button>
              </el-form-item>
            </el-form>
            
            <div v-if="unitResult" class="result">
              <el-alert
                title="换算结果"
                type="success"
                show-icon
                class="result-alert"
              >
                <template #default>
                  <div class="unit-result">
                    <div class="result-item">
                      <label>换算:</label>
                      <span>{{ unitResult.from_value }} {{ unitResult.from_unit }} = {{ unitResult.result }} {{ unitResult.to_unit }}</span>
                    </div>
                  </div>
                </template>
              </el-alert>
            </div>
          </el-card>
        </div>
        
        <!-- 其他工具 -->
        <div v-else class="tool-form">
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon class="card-header-icon"><component :is="magicStickIcon" /></el-icon>
                <span>工具使用说明</span>
              </div>
            </template>
            
            <el-empty description="该工具正在开发中，敬请期待！" />
          </el-card>
        </div>
      </div>
    </div>
  </div>
  
  <div v-else-if="loading" class="loading">
    <el-skeleton animated>
      <template #template>
        <el-skeleton-item variant="h1" style="width: 50%" />
        <el-skeleton-item variant="p" style="width: 100%; margin-top: 20px;" />
        <el-skeleton-item variant="p" style="width: 80%; margin-top: 10px;" />
      </template>
    </el-skeleton>
  </div>
  
  <div v-else-if="error" class="error">
    <el-result
      icon="error"
      title="数据加载失败"
      :sub-title="error"
    >
      <template #extra>
        <el-button type="primary" @click="goBack">返回首页</el-button>
      </template>
    </el-result>
  </div>
  
  <div v-else class="error">
    <el-result
      icon="error"
      title="工具未找到"
      sub-title="抱歉，未找到您访问的工具，请检查链接是否正确"
    >
      <template #extra>
        <el-button type="primary" @click="goBack">返回首页</el-button>
      </template>
    </el-result>
  </div>
</template>

<script>
import { ref, reactive, onMounted, defineAsyncComponent } from 'vue'
import { useRouter } from 'vue-router'
import { API_ENDPOINTS, apiCall } from '../config/api.js'

export default {
  name: 'ToolDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  setup(props) {
    const router = useRouter()
    const tool = ref(null)
    const loading = ref(true)
    const error = ref(null)
    const calculating = ref(false)
    const bmiResult = ref(null)
    const imageFormats = ref([])
    const imageFile = ref(null)
    const convertResult = ref(null)
    const passwordResult = ref(null)
    const textCaseResult = ref(null)
    const timestampResult = ref(null)
    const unitResult = ref(null)
    const unitOptions = ref([])
    
    // 异步加载图标组件
    const scaleIcon = defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.Scale))
    const pictureIcon = defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.Picture))
    const keyIcon = defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.Key))
    const documentIcon = defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.Document))
    const clockIcon = defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.Clock))
    const magicStickIcon = defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.MagicStick))
    const uploadFilledIcon = defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.UploadFilled))
    
    // 根据工具ID获取对应图标
    const getToolIcon = (toolId) => {
      switch (toolId) {
        case 1: // BMI计算器
          return scaleIcon
        case 2: // 图片格式转换器
          return pictureIcon
        case 3: // 密码生成器
          return keyIcon
        case 4: // 文本大小写转换
          return documentIcon
        case 5: // 时间戳转换器
          return clockIcon
        case 6: // 单位换算器
          return magicStickIcon
        default:
          return magicStickIcon
      }
    }
    
    const bmiForm = reactive({
      height: '',
      weight: ''
    })
    
    const imageForm = reactive({
      sourceFormat: '',
      targetFormat: ''
    })
    
    const passwordForm = reactive({
      length: 12,
      characterTypes: ['uppercase', 'lowercase', 'digits']
    })
    
    const textCaseForm = reactive({
      text: '',
      caseType: 'upper'
    })
    
    const timestampForm = reactive({
      value: '',
      type: 'timestamp' // 'timestamp' 或 'date'
    })
    
    const unitForm = reactive({
      value: 0,
      fromUnit: '',
      toUnit: '',
      unitType: 'length'
    })
    
    // 获取工具详情
    const fetchTool = async () => {
      try {
        loading.value = true
        error.value = null
        
        const response = await apiCall(API_ENDPOINTS.TOOL_DETAIL(props.id))
        if (response.success) {
          tool.value = response.data
        } else {
          error.value = response.error
        }
      } catch (err) {
        console.error('获取工具详情失败:', err)
        error.value = err.message
      } finally {
        loading.value = false
      }
    }
    
    // 获取图片格式
    const fetchImageFormats = async () => {
      try {
        const response = await apiCall(API_ENDPOINTS.IMAGE_FORMATS)
        if (response.success) {
          imageFormats.value = response.data
        }
      } catch (error) {
        console.error('获取图片格式失败:', error)
      }
    }
    
    // 获取单位类型
    const fetchUnitTypes = async (unitType) => {
      try {
        const response = await apiCall(API_ENDPOINTS.UNIT_TYPES(unitType))
        if (response.success) {
          unitOptions.value = response.data
          if (response.data.length > 0) {
            unitForm.fromUnit = response.data[0]
            unitForm.toUnit = response.data[1] || response.data[0]
          }
        }
      } catch (error) {
        console.error('获取单位类型失败:', error)
      }
    }
    
    // 计算BMI
    const calculateBMI = async () => {
      if (!bmiForm.height || !bmiForm.weight) {
        alert('请输入完整的身高和体重信息')
        return
      }
      
      calculating.value = true
      try {
        const response = await apiCall(API_ENDPOINTS.BMI_CALCULATE, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            weight: bmiForm.weight,
            height: bmiForm.height
          })
        })
        
        if (response.success) {
          bmiResult.value = response.data
        } else {
          alert('计算失败: ' + response.error)
        }
      } catch (error) {
        console.error('计算BMI失败:', error)
        alert('计算失败，请稍后重试')
      } finally {
        calculating.value = false
      }
    }
    
    // 根据BMI类别获取提示类型
    const getAlertType = (category) => {
      switch (category) {
        case '偏瘦': return 'warning'
        case '正常': return 'success'
        case '偏重': return 'warning'
        case '肥胖': return 'error'
        default: return 'info'
      }
    }
    
    // 处理文件上传
    const handleFileChange = (file) => {
      imageFile.value = file.raw
    }
    
    // 转换图片
    const convertImage = async () => {
      if (!imageForm.sourceFormat || !imageForm.targetFormat) {
        alert('请选择源格式和目标格式')
        return
      }
      
      if (!imageFile.value) {
        alert('请上传图片文件')
        return
      }
      
      try {
        // 在实际应用中，这里会处理图片转换
        const response = await apiCall(API_ENDPOINTS.IMAGE_CONVERT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            source_format: imageForm.sourceFormat,
            target_format: imageForm.targetFormat,
            image_data: '' // 实际应该传递图片数据
          })
        })
        
        if (response.success) {
          convertResult.value = response.data
        } else {
          alert('转换失败: ' + response.error)
        }
      } catch (error) {
        console.error('转换图片失败:', error)
        alert('转换失败，请稍后重试')
      }
    }
    
    // 生成密码
    const generatePassword = async () => {
      try {
        const response = await apiCall(API_ENDPOINTS.GENERATE_PASSWORD, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            length: passwordForm.length,
            include_uppercase: passwordForm.characterTypes.includes('uppercase'),
            include_lowercase: passwordForm.characterTypes.includes('lowercase'),
            include_digits: passwordForm.characterTypes.includes('digits'),
            include_symbols: passwordForm.characterTypes.includes('symbols')
          })
        })
        
        if (response.success) {
          passwordResult.value = response.data
        } else {
          alert('生成失败: ' + response.error)
        }
      } catch (error) {
        console.error('生成密码失败:', error)
        alert('生成失败，请稍后重试')
      }
    }
    
    // 文本大小写转换
    const convertTextCase = async () => {
      if (!textCaseForm.text) {
        alert('请输入要转换的文本')
        return
      }
      
      try {
        const response = await apiCall(API_ENDPOINTS.CONVERT_TEXT_CASE, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            text: textCaseForm.text,
            case_type: textCaseForm.caseType
          })
        })
        
        if (response.success) {
          textCaseResult.value = response.data
        } else {
          alert('转换失败: ' + response.error)
        }
      } catch (error) {
        console.error('转换文本失败:', error)
        alert('转换失败，请稍后重试')
      }
    }
    
    // 时间戳转换
    const convertTimestamp = async () => {
      if (!timestampForm.value) {
        alert('请输入要转换的值')
        return
      }
      
      try {
        const response = await apiCall(API_ENDPOINTS.CONVERT_TIMESTAMP, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            value: timestampForm.value,
            to_timestamp: timestampForm.type === 'date'
          })
        })
        
        if (response.success) {
          timestampResult.value = response.data
        } else {
          alert('转换失败: ' + response.error)
        }
      } catch (error) {
        console.error('转换时间戳失败:', error)
        alert('转换失败，请稍后重试')
      }
    }
    
    // 单位换算
    const convertUnit = async () => {
      if (!unitForm.value && unitForm.value !== 0) {
        alert('请输入要换算的数值')
        return
      }
      
      if (!unitForm.fromUnit || !unitForm.toUnit) {
        alert('请选择源单位和目标单位')
        return
      }
      
      try {
        const response = await apiCall(API_ENDPOINTS.CONVERT_UNIT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            value: unitForm.value,
            from_unit: unitForm.fromUnit,
            to_unit: unitForm.toUnit,
            unit_type: unitForm.unitType
          })
        })
        
        if (response.success) {
          unitResult.value = response.data
        } else {
          alert('换算失败: ' + response.error)
        }
      } catch (error) {
        console.error('单位换算失败:', error)
        alert('换算失败，请稍后重试')
      }
    }
    
    // 单位类型改变时获取对应单位
    const onUnitTypeChange = (unitType) => {
      fetchUnitTypes(unitType)
    }
    
    // 复制到剪贴板
    const copyToClipboard = (text) => {
      navigator.clipboard.writeText(text).then(() => {
        alert('已复制到剪贴板')
      }).catch(err => {
        console.error('复制失败:', err)
        alert('复制失败')
      })
    }
    
    // 返回上一页
    const goBack = () => {
      router.go(-1)
    }
    
    onMounted(() => {
      fetchTool()
      const toolId = parseInt(props.id)
      if (toolId === 2) {
        fetchImageFormats()
      } else if (toolId === 6) {
        fetchUnitTypes('length')
      }
    })
    
    return {
      tool,
      loading,
      error,
      scaleIcon,
      pictureIcon,
      keyIcon,
      documentIcon,
      clockIcon,
      magicStickIcon,
      uploadFilledIcon,
      getToolIcon,
      bmiForm,
      calculating,
      bmiResult,
      imageForm,
      imageFormats,
      imageFile,
      convertResult,
      passwordForm,
      passwordResult,
      textCaseForm,
      textCaseResult,
      timestampForm,
      timestampResult,
      unitForm,
      unitResult,
      unitOptions,
      calculateBMI,
      getAlertType,
      handleFileChange,
      convertImage,
      generatePassword,
      convertTextCase,
      convertTimestamp,
      convertUnit,
      onUnitTypeChange,
      copyToClipboard,
      goBack
    }
  }
}
</script>

<style scoped>
.tool-detail {
  padding: 20px 0;
}

.page-header {
  margin-bottom: 20px;
}

.tool-header {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.tool-header h1 {
  margin: 0 0 5px 0;
  color: #333;
}

.tool-description {
  margin: 0;
  color: #666;
}

.tool-form {
  max-width: 1160px;
}

.card-header {
  font-weight: bold;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header-icon {
  font-size: 1.2rem;
}

.result {
  margin-top: 20px;
}

.result-alert {
  border-radius: 8px;
}

.upload-demo {
  width: 100%;
}

.loading,
.error {
  padding: 40px 0;
}

.password-result,
.text-result,
.timestamp-result,
.unit-result {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.password-text {
  font-family: monospace;
  font-size: 1.2rem;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 4px;
  word-break: break-all;
}

.password-strength {
  font-weight: bold;
}

.copy-button {
  align-self: flex-start;
}

.result-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.result-item label {
  font-weight: bold;
}

.result-item span {
  word-break: break-all;
}
</style>