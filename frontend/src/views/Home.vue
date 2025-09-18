<template>
  <div class="home">
    <!-- 调试信息 -->
    <div v-if="debugInfo" class="debug-info">
      <p>API Base URL: {{ debugInfo.apiBaseUrl }}</p>
      <p>Tools Count: {{ tools.length }}</p>
      <p>Popular Tools Count: {{ popularTools.length }}</p>
      <p>Recent Tools Count: {{ recentTools.length }}</p>
    </div>
    
    <div v-if="searchQuery" class="search-results">
      <h2>搜索结果: "{{ searchQuery }}"</h2>
      <el-button @click="clearSearch" type="primary" plain size="small" class="clear-search">
        清除搜索
      </el-button>
    </div>
    
    <div v-if="!searchQuery" class="section">
      <div class="section-header">
        <h2>热门工具</h2>
        <el-link type="primary" @click="viewAllTools">查看全部</el-link>
      </div>
      <div class="tools-grid">
        <ToolCard 
          v-for="tool in popularTools" 
          :key="tool.id" 
          :tool="tool"
          @tool-click="handleToolClick"
        />
        <el-empty v-if="popularTools.length === 0 && !loading" description="暂无热门工具" />
      </div>
    </div>
    
    <div v-if="!searchQuery" class="section">
      <div class="section-header">
        <h2>最新工具</h2>
        <el-link type="primary" @click="viewAllTools">查看全部</el-link>
      </div>
      <div class="tools-grid">
        <ToolCard 
          v-for="tool in recentTools" 
          :key="tool.id" 
          :tool="tool"
          @tool-click="handleToolClick"
        />
        <el-empty v-if="recentTools.length === 0 && !loading" description="暂无最新工具" />
      </div>
    </div>
    
    <div v-if="searchQuery" class="section">
      <div class="tools-grid">
        <ToolCard 
          v-for="tool in filteredTools" 
          :key="tool.id" 
          :tool="tool"
          @tool-click="handleToolClick"
        />
        <el-empty 
          v-if="filteredTools.length === 0" 
          description="没有找到相关工具" 
        />
      </div>
    </div>
    
    <div v-if="loading" class="loading">
      <el-skeleton animated>
        <template #template>
          <div class="skeleton-grid">
            <el-skeleton-item variant="image" style="width: 100%; height: 150px;" />
            <el-skeleton-item variant="image" style="width: 100%; height: 150px;" />
            <el-skeleton-item variant="image" style="width: 100%; height: 150px;" />
          </div>
        </template>
      </el-skeleton>
    </div>
    
    <div v-if="error" class="error">
      <el-alert
        title="数据加载失败"
        :description="error"
        type="error"
        show-icon
        closable
        @close="error = null"
      />
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import ToolCard from '../components/ToolCard.vue'
import { API_ENDPOINTS, apiCall } from '../config/api.js'

export default {
  name: 'Home',
  components: {
    ToolCard
  },
  props: {
    searchQuery: {
      type: String,
      default: ''
    }
  },
  emits: ['clear-search'],
  setup(props, { emit }) {
    const router = useRouter()
    const tools = ref([])
    const popularTools = ref([])
    const recentTools = ref([])
    const loading = ref(true)
    const error = ref(null)
    const debugInfo = ref({
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    })
    
    // 获取所有工具
    const fetchTools = async () => {
      try {
        loading.value = true
        error.value = null
        
        // 获取所有工具
        const toolsResponse = await apiCall(API_ENDPOINTS.TOOLS)
        if (toolsResponse.success) {
          tools.value = toolsResponse.data
        } else {
          error.value = `获取工具列表失败: ${toolsResponse.error}`
        }
        
        // 获取热门工具
        const popularResponse = await apiCall(API_ENDPOINTS.POPULAR_TOOLS)
        if (popularResponse.success) {
          popularTools.value = popularResponse.data
        } else {
          error.value = `获取热门工具失败: ${popularResponse.error}`
        }
        
        // 获取最新工具
        const recentResponse = await apiCall(API_ENDPOINTS.RECENT_TOOLS)
        if (recentResponse.success) {
          recentTools.value = recentResponse.data
        } else {
          error.value = `获取最新工具失败: ${recentResponse.error}`
        }
      } catch (err) {
        console.error('获取工具失败:', err)
        error.value = `获取工具失败: ${err.message}`
      } finally {
        loading.value = false
      }
    }
    
    // 搜索工具
    const searchTools = async (query) => {
      if (!query) return;
      
      try {
        loading.value = true
        error.value = null
        
        const response = await apiCall(API_ENDPOINTS.SEARCH_TOOLS(query))
        if (response.success) {
          tools.value = response.data
        } else {
          error.value = `搜索工具失败: ${response.error}`
        }
      } catch (err) {
        console.error('搜索工具失败:', err)
        error.value = `搜索工具失败: ${err.message}`
      } finally {
        loading.value = false
      }
    }
    
    // 根据搜索查询过滤工具
    const filteredTools = computed(() => {
      if (!props.searchQuery) return []
      
      const query = props.searchQuery.toLowerCase()
      return tools.value.filter(tool => 
        tool.name.toLowerCase().includes(query) || 
        tool.description.toLowerCase().includes(query) ||
        tool.category.toLowerCase().includes(query)
      )
    })
    
    // 处理工具点击
    const handleToolClick = (toolId) => {
      router.push(`/tool/${toolId}`)
    }
    
    // 查看所有工具
    const viewAllTools = () => {
      // 在实际应用中可能会跳转到工具列表页面
    }
    
    // 清除搜索
    const clearSearch = () => {
      emit('clear-search')
    }
    
    // 监听搜索查询变化
    watch(() => props.searchQuery, (newQuery) => {
      if (newQuery) {
        searchTools(newQuery)
      } else {
        fetchTools()
      }
    })
    
    onMounted(() => {
      fetchTools()
    })
    
    return {
      tools,
      popularTools,
      recentTools,
      loading,
      error,
      debugInfo,
      filteredTools,
      handleToolClick,
      viewAllTools,
      clearSearch
    }
  }
}
</script>

<style scoped>
.home {
  padding: 20px 0;
}

.debug-info {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
  font-size: 14px;
}

.section {
  margin-bottom: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  color: #333;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.clear-search {
  margin-bottom: 20px;
}

.loading {
  padding: 40px 0;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.error {
  margin: 20px 0;
}

@media (max-width: 768px) {
  .tools-grid,
  .skeleton-grid {
    grid-template-columns: repeat(auto-fill, minmax(100%, 1fr));
  }
}
</style>