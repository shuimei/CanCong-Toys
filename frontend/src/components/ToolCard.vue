<template>
  <div class="tool-card" @click="handleClick">
    <div class="card-content">
      <div class="icon-wrapper">
        <el-icon size="24" color="#409eff">
          <component :is="toolIcon" />
        </el-icon>
      </div>
      <h3 class="tool-name">{{ tool.name }}</h3>
      <p class="tool-description">{{ tool.description }}</p>
      <div class="tool-category">
        <el-tag size="small" type="info">{{ tool.category }}</el-tag>
      </div>
      <div class="tool-stats">
        <span class="usage-count">
          <el-icon><user /></el-icon>
          {{ tool.usage_count }} 次使用
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { User } from '@element-plus/icons-vue'
import { defineAsyncComponent, computed } from 'vue'

export default {
  name: 'ToolCard',
  components: {
    User
  },
  props: {
    tool: {
      type: Object,
      required: true
    }
  },
  emits: ['tool-click'],
  setup(props, { emit }) {
    // 根据工具ID获取对应图标
    const toolIcon = computed(() => {
      switch (props.tool.id) {
        case 1: // BMI计算器
          return defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.Scale))
        case 2: // 图片格式转换器
          return defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.Picture))
        case 3: // 密码生成器
          return defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.Key))
        case 4: // 文本大小写转换
          return defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.Document))
        case 5: // 时间戳转换器
          return defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.Clock))
        case 6: // 单位换算器
          return defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.MagicStick))
        default:
          return defineAsyncComponent(() => import('@element-plus/icons-vue').then(m => m.MagicStick))
      }
    })
    
    const handleClick = () => {
      emit('tool-click', props.tool.id)
    }
    
    return {
      toolIcon,
      handleClick
    }
  }
}
</script>

<style scoped>
.tool-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.tool-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.card-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.icon-wrapper {
  width: 50px;
  height: 50px;
  background-color: #ecf5ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.tool-name {
  margin: 0 0 10px 0;
  font-size: 1.2rem;
  color: #333;
  flex: 1;
}

.tool-description {
  margin: 0 0 15px 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  flex: 2;
}

.tool-category {
  margin-bottom: 15px;
}

.tool-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.usage-count {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #999;
  font-size: 0.85rem;
}
</style>