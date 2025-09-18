import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [vue()],
    server: {
      host: '0.0.0.0',
      port: 13002,
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:8003',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '/api')
        }
      }
    },
    define: {
      __APP_ENV__: JSON.stringify(env.VITE_APP_ENV),
    }
  }
})