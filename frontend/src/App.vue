<template>
  <div class="app-container">
    <el-header class="header">
      <div class="header-content">
        <div class="logo">
          <el-icon size="30"><Tools /></el-icon>
          <h1>CanCong-Toys</h1>
        </div>
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索工具..." 
          class="search-input"
          clearable
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </el-header>
    
    <el-main class="main">
      <router-view :search-query="searchQuery" @clear-search="searchQuery = ''" />
    </el-main>
    
    <el-footer class="footer">
      <p>© 2025 CanCong-Toys - 实用小工具合集</p>
    </el-footer>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'App',
  setup() {
    const searchQuery = ref('')
    
    const handleSearch = () => {
      // 搜索功能将在子组件中处理
    }
    
    return {
      searchQuery,
      handleSearch
    }
  }
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #409eff;
}

.search-input {
  width: 300px;
}

.main {
  flex: 1;
  max-width: 1200px;
  margin: 20px auto;
  width: 100%;
  padding: 0 20px;
}

.footer {
  text-align: center;
  background-color: #f5f5f5;
  padding: 20px;
  margin-top: auto;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 15px;
  }
  
  .search-input {
    width: 100%;
  }
}
</style>