<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>SplitTrail</h1>
        <p>Split costs with your trail crew</p>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="field">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="you@example.com" required />
        </div>
        <div class="field">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="••••••••" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign in' }}
        </button>
      </form>

      <p class="switch">
        No account? <RouterLink to="/register">Register</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.push('/groups')
  } catch {
    error.value = 'Invalid email or password'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f0;
}
.auth-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 380px;
  border: 1px solid #e5e5e0;
}
.auth-header {
  text-align: center;
  margin-bottom: 1.5rem;
}
.auth-header h1 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 4px;
}
.auth-header p {
  color: #888;
  font-size: 0.9rem;
  margin: 0;
}
.field {
  margin-bottom: 1rem;
}
.field label {
  display: block;
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 4px;
  color: #333;
}
.field input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.15s;
}
.field input:focus {
  border-color: #4a9b6f;
}
button {
  width: 100%;
  padding: 11px;
  background: #4a9b6f;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  margin-top: 0.5rem;
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.error {
  color: #c0392b;
  font-size: 0.85rem;
  margin: 0.5rem 0;
}
.switch {
  text-align: center;
  margin-top: 1.25rem;
  font-size: 0.85rem;
  color: #888;
}
.switch a {
  color: #4a9b6f;
  text-decoration: none;
  font-weight: 500;
}
</style>