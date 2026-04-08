<template>
  <div class="container">
    <header>
      <h1>SplitTrail</h1>
      <button class="logout" @click="handleLogout">Logout</button>
    </header>

    <div class="content">
      <div class="top-bar">
        <h2>Your trips</h2>
        <button @click="showModal = true">+ New trip</button>
      </div>

      <div v-if="loading" class="empty">Loading...</div>
      <div v-else-if="groups.length === 0" class="empty">No trips yet. Create your first one!</div>

      <div class="groups-list">
        <div
          v-for="group in groups"
          :key="group.id"
          class="group-card"
          @click="router.push(`/groups/${group.id}`)"
        >
          <div class="group-name">{{ group.name }}</div>
          <div class="group-currency">{{ group.currency }}</div>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <h3>New trip</h3>
        <div class="field">
          <label>Trip name</label>
          <input v-model="newName" placeholder="e.g. Yosemite 2025" />
        </div>
        <div class="field">
          <label>Currency</label>
          <select v-model="newCurrency">
            <option>USD</option>
            <option>EUR</option>
            <option>GBP</option>
          </select>
        </div>
        <p v-if="createError" class="error">{{ createError }}</p>
        <div class="modal-actions">
          <button class="secondary" @click="showModal = false">Cancel</button>
          <button @click="handleCreate" :disabled="creating">
            {{ creating ? 'Creating...' : 'Create' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import client from '@/api/client'

const router = useRouter()
const auth = useAuthStore()

const groups = ref<Array<{ id: string; name: string; currency: string }>>([])
const loading = ref(true)
const showModal = ref(false)
const newName = ref('')
const newCurrency = ref('USD')
const creating = ref(false)
const createError = ref('')

onMounted(async () => {
  try {
    const res = await client.get('/groups')
    groups.value = res.data
  } finally {
    loading.value = false
  }
})

async function handleCreate() {
  if (!newName.value.trim()) return
  creating.value = true
  createError.value = ''
  try {
    const res = await client.post('/groups', { name: newName.value, currency: newCurrency.value })
    groups.value.push(res.data)
    showModal.value = false
    newName.value = ''
  } catch {
    createError.value = 'Failed to create trip'
  } finally {
    creating.value = false
  }
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.container { max-width: 640px; margin: 0 auto; padding: 1.5rem; }
header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
header h1 { font-size: 1.25rem; font-weight: 600; margin: 0; }
.logout { background: none; border: 1px solid #ddd; border-radius: 8px; padding: 6px 12px; cursor: pointer; font-size: 0.85rem; color: #666; }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.top-bar h2 { margin: 0; font-size: 1.1rem; }
.top-bar button { background: #4a9b6f; color: white; border: none; border-radius: 8px; padding: 8px 14px; cursor: pointer; font-size: 0.9rem; }
.empty { color: #999; text-align: center; padding: 3rem 0; font-size: 0.95rem; }
.groups-list { display: flex; flex-direction: column; gap: 10px; }
.group-card { background: white; border: 1px solid #e5e5e0; border-radius: 10px; padding: 1rem 1.25rem; cursor: pointer; display: flex; justify-content: space-between; align-items: center; transition: border-color 0.15s; }
.group-card:hover { border-color: #4a9b6f; }
.group-name { font-weight: 500; }
.group-currency { font-size: 0.8rem; color: #999; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; }
.modal { background: white; border-radius: 12px; padding: 1.5rem; width: 100%; max-width: 360px; }
.modal h3 { margin: 0 0 1.25rem; font-size: 1rem; }
.field { margin-bottom: 1rem; }
.field label { display: block; font-size: 0.85rem; font-weight: 500; margin-bottom: 4px; }
.field input, .field select { width: 100%; padding: 9px 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 0.9rem; box-sizing: border-box; }
.modal-actions { display: flex; gap: 8px; margin-top: 1.25rem; }
.modal-actions button { flex: 1; padding: 10px; border: none; border-radius: 8px; cursor: pointer; font-size: 0.9rem; font-weight: 500; }
.modal-actions button:not(.secondary) { background: #4a9b6f; color: white; }
.modal-actions button.secondary { background: #f5f5f0; color: #333; }
.error { color: #c0392b; font-size: 0.85rem; margin: 0.5rem 0; }
</style>