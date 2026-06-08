import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/overview':      { target: 'http://localhost:8000', changeOrigin: true },
      '/players':       { target: 'http://localhost:8000', changeOrigin: true },
      '/drives':        { target: 'http://localhost:8000', changeOrigin: true },
      '/pick-and-roll': { target: 'http://localhost:8000', changeOrigin: true },
      '/shot-quality':  { target: 'http://localhost:8000', changeOrigin: true },
      '/lineups':       { target: 'http://localhost:8000', changeOrigin: true },
    },
  },
})
