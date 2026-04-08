import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import client from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<{ id: string; email: string; name: string } | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function register(email: string, name: string, password: string) {
    const response = await client.post('/auth/register', { email, name, password })
    user.value = response.data
  }

  async function login(email: string, password: string) {
    const response = await client.post('/auth/login', { email, password })
    token.value = response.data.access_token
    localStorage.setItem('token', token.value!)
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  return { token, user, isAuthenticated, register, login, logout }
})
