<template>
  <div class="container">
    <header>
      <button class="back" @click="router.push('/groups')">← Back</button>
      <h1>{{ group?.name }}</h1>
      <span class="currency">{{ group?.currency }}</span>
    </header>

    <div class="tabs">
      <button :class="{ active: tab === 'expenses' }" @click="tab = 'expenses'">Expenses</button>
      <button :class="{ active: tab === 'balances' }" @click="tab = 'balances'">Balances</button>
      <button :class="{ active: tab === 'members' }" @click="tab = 'members'">Members</button>
    </div>

    <!-- Expenses tab -->
    <div v-if="tab === 'expenses'">
      <div class="top-bar">
        <span class="count">{{ expenses.length }} expenses</span>
        <button @click="showExpenseModal = true">+ Add expense</button>
      </div>
      <div v-if="expenses.length === 0" class="empty">No expenses yet</div>
      <div class="list">
        <div v-for="expense in expenses" :key="expense.id" class="card">
          <div>
            <div class="card-title">{{ expense.description }}</div>
            <div class="card-sub">{{ expense.split_type }} split</div>
          </div>
          <div class="amount">${{ expense.amount }}</div>
        </div>
      </div>
    </div>

    <!-- Balances tab -->
    <div v-if="tab === 'balances'">
      <div class="section-title">Who owes what</div>
      <div v-if="transactions.length === 0" class="empty">Everyone is settled up!</div>
      <div class="list">
        <div v-for="(tx, i) in transactions" :key="i" class="card tx-card">
          <div>
            <span class="tx-from">{{ tx.from_user }}</span>
            <span class="tx-arrow"> → </span>
            <span class="tx-to">{{ tx.to_user }}</span>
          </div>
          <div class="amount">${{ tx.amount }}</div>
        </div>
      </div>
    </div>

    <!-- Members tab -->
    <div v-if="tab === 'members'">
      <div class="top-bar">
        <span class="count">{{ members.length }} members</span>
        <button @click="showMemberModal = true">+ Add member</button>
      </div>
      <div class="list">
        <div v-for="member in members" :key="member.id" class="card">
          <div class="card-title">{{ member.name }}</div>
          <div class="card-sub">{{ member.email }}</div>
        </div>
      </div>
    </div>

    <!-- Add expense modal -->
    <div v-if="showExpenseModal" class="modal-overlay" @click.self="showExpenseModal = false">
      <div class="modal">
        <h3>Add expense</h3>
        <div class="field">
          <label>Description</label>
          <input v-model="newExpense.description" placeholder="e.g. Campsite fee" />
        </div>
        <div class="field">
          <label>Amount</label>
          <input v-model="newExpense.amount" type="number" step="0.01" placeholder="0.00" />
        </div>
        <div class="field">
          <label>Split type</label>
          <select v-model="newExpense.split_type">
            <option value="equal">Equal</option>
            <option value="exact">Exact</option>
            <option value="percentage">Percentage</option>
          </select>
        </div>
        <p v-if="expenseError" class="error">{{ expenseError }}</p>
        <div class="modal-actions">
          <button class="secondary" @click="showExpenseModal = false">Cancel</button>
          <button @click="handleAddExpense" :disabled="addingExpense">
            {{ addingExpense ? 'Adding...' : 'Add' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Add member modal -->
    <div v-if="showMemberModal" class="modal-overlay" @click.self="showMemberModal = false">
      <div class="modal">
        <h3>Add member</h3>
        <div class="field">
          <label>Email</label>
          <input v-model="newMemberEmail" placeholder="friend@example.com" />
        </div>
        <p v-if="memberError" class="error">{{ memberError }}</p>
        <div class="modal-actions">
          <button class="secondary" @click="showMemberModal = false">Cancel</button>
          <button @click="handleAddMember" :disabled="addingMember">
            {{ addingMember ? 'Adding...' : 'Add' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import client from '@/api/client'

const router = useRouter()
const route = useRoute()
const groupId = route.params.id as string

const tab = ref('expenses')
const group = ref<{ name: string; currency: string } | null>(null)
const expenses = ref<any[]>([])
const transactions = ref<any[]>([])
const members = ref<any[]>([])

const showExpenseModal = ref(false)
const newExpense = ref({ description: '', amount: '', split_type: 'equal' })
const addingExpense = ref(false)
const expenseError = ref('')

const showMemberModal = ref(false)
const newMemberEmail = ref('')
const addingMember = ref(false)
const memberError = ref('')

onMounted(async () => {
  const [groupRes, expensesRes, simplifyRes] = await Promise.all([
    client.get(`/groups/${groupId}`),
    client.get(`/groups/${groupId}/expenses`),
    client.get(`/groups/${groupId}/simplify`)
  ])
  group.value = groupRes.data
  members.value = groupRes.data.members
  expenses.value = expensesRes.data
  transactions.value = simplifyRes.data.transactions
})

async function handleAddExpense() {
  if (!newExpense.value.description || !newExpense.value.amount) return
  addingExpense.value = true
  expenseError.value = ''
  try {
    const res = await client.post(`/groups/${groupId}/expenses`, {
      description: newExpense.value.description,
      amount: parseFloat(newExpense.value.amount),
      split_type: newExpense.value.split_type
    })
    expenses.value.push(res.data)
    const simplifyRes = await client.get(`/groups/${groupId}/simplify`)
    transactions.value = simplifyRes.data.transactions
    showExpenseModal.value = false
    newExpense.value = { description: '', amount: '', split_type: 'equal' }
  } catch {
    expenseError.value = 'Failed to add expense'
  } finally {
    addingExpense.value = false
  }
}

async function handleAddMember() {
  if (!newMemberEmail.value) return
  addingMember.value = true
  memberError.value = ''
  try {
    const res = await client.post(`/groups/${groupId}/members`, { email: newMemberEmail.value })
    members.value.push(res.data)
    showMemberModal.value = false
    newMemberEmail.value = ''
  } catch {
    memberError.value = 'User not found or already in group'
  } finally {
    addingMember.value = false
  }
}
</script>

<style scoped>
.container { max-width: 640px; margin: 0 auto; padding: 1.5rem; }
header { display: flex; align-items: center; gap: 12px; margin-bottom: 1.5rem; }
header h1 { font-size: 1.2rem; font-weight: 600; margin: 0; flex: 1; }
.back { background: none; border: 1px solid #ddd; border-radius: 8px; padding: 6px 12px; cursor: pointer; font-size: 0.85rem; }
.currency { font-size: 0.8rem; color: #999; background: #f5f5f0; padding: 4px 8px; border-radius: 6px; }
.tabs { display: flex; gap: 4px; margin-bottom: 1.5rem; background: #f5f5f0; padding: 4px; border-radius: 10px; }
.tabs button { flex: 1; padding: 8px; border: none; background: none; border-radius: 8px; cursor: pointer; font-size: 0.9rem; color: #666; }
.tabs button.active { background: white; color: #333; font-weight: 500; }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.count { font-size: 0.85rem; color: #999; }
.top-bar button { background: #4a9b6f; color: white; border: none; border-radius: 8px; padding: 7px 14px; cursor: pointer; font-size: 0.85rem; }
.empty { color: #999; text-align: center; padding: 3rem 0; font-size: 0.95rem; }
.list { display: flex; flex-direction: column; gap: 8px; }
.card { background: white; border: 1px solid #e5e5e0; border-radius: 10px; padding: 1rem 1.25rem; display: flex; justify-content: space-between; align-items: center; }
.card-title { font-weight: 500; font-size: 0.95rem; }
.card-sub { font-size: 0.8rem; color: #999; margin-top: 2px; }
.amount { font-weight: 600; color: #4a9b6f; font-size: 1rem; }
.section-title { font-size: 0.85rem; color: #999; margin-bottom: 1rem; }
.tx-from { font-weight: 500; color: #c0392b; }
.tx-arrow { color: #999; }
.tx-to { font-weight: 500; color: #4a9b6f; }
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