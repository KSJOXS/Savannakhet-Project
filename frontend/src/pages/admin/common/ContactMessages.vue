<template>
    <div class="inbox-page">

        <!-- Header -->
        <div class="page-header">
            <div>
                <h2><i class="fas fa-inbox"></i> Contact Inbox</h2>
                <p class="subtitle">Messages submitted through the Contact page.</p>
            </div>
            <div class="header-pills">
                <span class="pill pill-blue">{{ unreadCount }} Unread</span>
                <span class="pill pill-gray">{{ messages.length }} Total</span>
            </div>
        </div>

        <!-- Filter Tabs -->
        <div class="filter-bar">
            <button v-for="f in filters" :key="f.value"
                :class="['tab-btn', { active: activeFilter === f.value }]"
                @click="activeFilter = f.value">
                {{ f.label }}
                <span class="tab-count">{{ getFilterCount(f.value) }}</span>
            </button>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="loading-state">
            <i class="fas fa-spinner fa-spin"></i> Loading messages...
        </div>

        <!-- Message List -->
        <div v-else class="message-list">
            <div v-if="filteredMessages.length === 0" class="empty-inbox">
                <i class="fas fa-envelope-open-text"></i>
                <p>No messages here.</p>
            </div>

            <div
                v-for="msg in filteredMessages"
                :key="msg.id"
                :class="['message-row', { 'unread': !msg.is_read }]"
                @click="openMessage(msg)"
            >
                <!-- Unread dot -->
                <div class="unread-dot-col">
                    <span v-if="!msg.is_read" class="unread-dot"></span>
                </div>

                <!-- Sender avatar -->
                <div class="sender-avatar">{{ msg.name.charAt(0).toUpperCase() }}</div>

                <!-- Content -->
                <div class="message-content">
                    <div class="message-top">
                        <span class="sender-name">{{ msg.name }}</span>
                        <span class="message-subject">{{ msg.subject }}</span>
                    </div>
                    <div class="message-preview">{{ truncate(msg.message, 80) }}</div>
                </div>

                <!-- Meta -->
                <div class="message-meta">
                    <span class="message-date">{{ formatDate(msg.created_at) }}</span>
                    <div class="message-badges">
                        <span v-if="msg.is_replied" class="badge badge-green">Replied</span>
                        <span v-else-if="msg.is_read" class="badge badge-gray">Read</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Message Detail Modal -->
        <div v-if="selectedMsg" class="modal-overlay" @click.self="selectedMsg = null">
            <div class="modal-box">

                <div class="modal-head">
                    <div>
                        <h3>{{ selectedMsg.subject }}</h3>
                        <p class="modal-sender">
                            From: <strong>{{ selectedMsg.name }}</strong>
                            &lt;<a :href="`mailto:${selectedMsg.email}`">{{ selectedMsg.email }}</a>&gt;
                        </p>
                        <p class="modal-date">{{ formatDateFull(selectedMsg.created_at) }}</p>
                    </div>
                    <button class="close-x" @click="selectedMsg = null">&times;</button>
                </div>

                <div class="modal-message-body">
                    {{ selectedMsg.message }}
                </div>

                <!-- Status badges -->
                <div class="modal-status-row">
                    <span v-if="selectedMsg.is_replied" class="badge badge-green"><i class="fas fa-check-circle"></i> Replied</span>
                    <span v-else-if="selectedMsg.is_read" class="badge badge-blue"><i class="fas fa-envelope-open"></i> Read</span>
                    <span v-else class="badge badge-yellow"><i class="fas fa-envelope"></i> New</span>
                </div>

                <!-- Reply Section -->
                <div class="reply-section">
                    <label><i class="fas fa-reply"></i> Reply to {{ selectedMsg.name }}</label>
                    <textarea
                        v-model="replyText"
                        placeholder="Type your reply here..."
                        rows="4"
                        class="reply-textarea"
                    ></textarea>
                    <div class="reply-actions">
                        <button @click="selectedMsg = null" class="btn-ghost">Close</button>
                        <button
                            @click="sendReply"
                            class="btn-reply"
                            :disabled="!replyText.trim() || replying"
                        >
                            <i class="fas fa-paper-plane"></i>
                            {{ replying ? 'Sending...' : 'Send Reply' }}
                        </button>
                    </div>
                </div>

            </div>
        </div>

        <!-- Reply Success Toast -->
        <transition name="toast">
            <div v-if="showToast" class="toast">
                <i class="fas fa-check-circle"></i> Reply sent successfully!
            </div>
        </transition>

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

const messages = ref([])
const loading = ref(true)
const activeFilter = ref('all')
const selectedMsg = ref(null)
const replyText = ref('')
const replying = ref(false)
const showToast = ref(false)

const filters = [
    { value: 'all', label: 'All' },
    { value: 'unread', label: 'Unread' },
    { value: 'read', label: 'Read' },
    { value: 'replied', label: 'Replied' },
]

const fetchMessages = async () => {
    loading.value = true
    try {
        const res = await api.get('/api/admin/messages')
        messages.value = res.data
    } catch (e) {
        console.error('Failed to fetch messages', e)
    } finally {
        loading.value = false
    }
}

const unreadCount = computed(() => messages.value.filter(m => !m.is_read).length)

const filteredMessages = computed(() => {
    switch (activeFilter.value) {
        case 'unread': return messages.value.filter(m => !m.is_read)
        case 'read': return messages.value.filter(m => m.is_read && !m.is_replied)
        case 'replied': return messages.value.filter(m => m.is_replied)
        default: return messages.value
    }
})

const getFilterCount = (val) => {
    if (val === 'all') return messages.value.length
    if (val === 'unread') return messages.value.filter(m => !m.is_read).length
    if (val === 'read') return messages.value.filter(m => m.is_read && !m.is_replied).length
    if (val === 'replied') return messages.value.filter(m => m.is_replied).length
    return 0
}

const openMessage = async (msg) => {
    selectedMsg.value = msg
    replyText.value = ''
    if (!msg.is_read) {
        try {
            await api.put(`/api/admin/messages/${msg.id}/read`)
            msg.is_read = true
        } catch (e) {
            console.error('Failed to mark as read', e)
        }
    }
}

const sendReply = async () => {
    if (!replyText.value.trim() || !selectedMsg.value) return
    replying.value = true
    try {
        const fd = new FormData()
        fd.append('reply_text', replyText.value)
        await api.post(`/api/admin/messages/${selectedMsg.value.id}/reply`, fd)
        selectedMsg.value.is_replied = true
        replyText.value = ''
        selectedMsg.value = null
        showToast.value = true
        setTimeout(() => showToast.value = false, 3000)
        await fetchMessages()
    } catch (e) {
        alert('Failed to send reply.')
    } finally {
        replying.value = false
    }
}

const truncate = (text, len) => text?.length > len ? text.substring(0, len) + '...' : text

const formatDate = (dateStr) => {
    const d = new Date(dateStr)
    const now = new Date()
    const diff = now - d
    if (diff < 86400000) return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const formatDateFull = (dateStr) => {
    return new Date(dateStr).toLocaleString('en-US', {
        weekday: 'short', year: 'numeric', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
    })
}

onMounted(fetchMessages)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.inbox-page {
    font-family: 'Inter', sans-serif;
    padding: 32px 40px;
    background: #f8fafc;
    min-height: 100vh;
}

/* ─── Header ─── */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}
.page-header h2 { font-size: 1.55rem; font-weight: 700; color: #0f172a; margin: 0; display: flex; align-items: center; gap: 10px; }
.subtitle { color: #64748b; font-size: 0.92rem; margin: 4px 0 0; }

.header-pills { display: flex; gap: 8px; }
.pill { padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
.pill-blue { background: #dbeafe; color: #1d4ed8; }
.pill-gray { background: #f1f5f9; color: #475569; }

/* ─── Filter Tabs ─── */
.filter-bar {
    display: flex;
    gap: 6px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 5px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    margin-bottom: 20px;
    width: fit-content;
}
.tab-btn {
    padding: 7px 16px; border: none; border-radius: 7px; background: transparent;
    color: #64748b; font-size: 0.88rem; font-weight: 500; cursor: pointer;
    transition: 0.15s; font-family: inherit; display: flex; align-items: center; gap: 6px;
}
.tab-btn:hover { background: #f1f5f9; }
.tab-btn.active { background: #3b82f6; color: white; }
.tab-count { background: rgba(255,255,255,0.25); border-radius: 10px; padding: 1px 7px; font-size: 0.75rem; font-weight: 700; }
.tab-btn:not(.active) .tab-count { background: #f1f5f9; color: #64748b; }

/* ─── Loading ─── */
.loading-state { text-align: center; padding: 60px; color: #64748b; font-size: 1.1rem; }

/* ─── Message List ─── */
.message-list {
    background: white;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    overflow: hidden;
}

.empty-inbox {
    text-align: center; padding: 80px; color: #94a3b8;
}
.empty-inbox i { font-size: 3.5rem; margin-bottom: 16px; display: block; }

.message-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 24px;
    border-bottom: 1px solid #f1f5f9;
    cursor: pointer;
    transition: 0.15s;
}
.message-row:last-child { border-bottom: none; }
.message-row:hover { background: #f8fafc; }
.message-row.unread { background: #fafbff; }

.unread-dot-col { width: 12px; flex-shrink: 0; }
.unread-dot {
    width: 8px; height: 8px;
    background: #3b82f6;
    border-radius: 50%;
    display: block;
}

.sender-avatar {
    width: 40px; height: 40px; border-radius: 50%;
    background: #eff6ff; color: #3b82f6;
    font-weight: 700; font-size: 1rem;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}

.message-content { flex: 1; min-width: 0; }
.message-top { display: flex; align-items: baseline; gap: 10px; margin-bottom: 4px; }
.sender-name { font-weight: 700; font-size: 0.95rem; color: #0f172a; white-space: nowrap; }
.message-subject { font-weight: 500; font-size: 0.92rem; color: #334155; }
.message-row:not(.unread) .sender-name { font-weight: 500; color: #475569; }
.message-row:not(.unread) .message-subject { color: #64748b; }
.message-preview { font-size: 0.85rem; color: #94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.message-meta { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; flex-shrink: 0; }
.message-date { font-size: 0.8rem; color: #94a3b8; white-space: nowrap; }
.message-badges { display: flex; gap: 4px; }
.badge { padding: 2px 8px; border-radius: 10px; font-size: 0.72rem; font-weight: 600; display: inline-flex; align-items: center; gap: 4px; }
.badge-green { background: #dcfce7; color: #15803d; }
.badge-blue { background: #dbeafe; color: #1d4ed8; }
.badge-gray { background: #f1f5f9; color: #64748b; }
.badge-yellow { background: #fef9c3; color: #a16207; }

/* ─── Modal ─── */
.modal-overlay {
    position: fixed; inset: 0;
    background: rgba(15,23,42,0.55);
    display: flex; align-items: center; justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(4px);
}
.modal-box {
    background: white;
    border-radius: 18px;
    width: 600px;
    max-width: 95vw;
    max-height: 90vh;
    overflow-y: auto;
    padding: 32px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.2);
}

.modal-head {
    display: flex; justify-content: space-between; align-items: flex-start;
    margin-bottom: 24px; gap: 16px;
}
.modal-head h3 { font-size: 1.25rem; font-weight: 700; color: #0f172a; margin: 0 0 8px; }
.modal-sender { font-size: 0.9rem; color: #475569; margin: 4px 0; }
.modal-sender a { color: #3b82f6; text-decoration: none; }
.modal-date { font-size: 0.82rem; color: #94a3b8; margin: 0; }
.close-x { background: none; border: none; font-size: 1.6rem; cursor: pointer; color: #94a3b8; line-height: 1; flex-shrink: 0; }

.modal-message-body {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 20px;
    font-size: 0.97rem;
    color: #334155;
    line-height: 1.7;
    white-space: pre-wrap;
    margin-bottom: 20px;
}

.modal-status-row { margin-bottom: 24px; }

/* ─── Reply ─── */
.reply-section { border-top: 1px solid #f1f5f9; padding-top: 20px; }
.reply-section label { font-size: 0.88rem; font-weight: 600; color: #475569; display: block; margin-bottom: 10px; }
.reply-textarea {
    width: 100%; box-sizing: border-box;
    padding: 14px; border: 1px solid #cbd5e1; border-radius: 10px;
    font-size: 0.95rem; font-family: inherit; color: #334155;
    resize: vertical; outline: none; transition: 0.15s; background: #fafbfc;
}
.reply-textarea:focus { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59,130,246,0.1); background: white; }

.reply-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 14px; }

.btn-ghost { background: #f1f5f9; color: #475569; border: none; padding: 10px 20px; border-radius: 9px; cursor: pointer; font-family: inherit; font-weight: 500; }
.btn-reply {
    background: #3b82f6; color: white; border: none;
    padding: 10px 22px; border-radius: 9px; cursor: pointer;
    font-family: inherit; font-weight: 600; font-size: 0.92rem;
    display: flex; align-items: center; gap: 8px; transition: 0.15s;
}
.btn-reply:hover:not(:disabled) { background: #2563eb; }
.btn-reply:disabled { opacity: 0.6; cursor: not-allowed; }

/* ─── Toast ─── */
.toast {
    position: fixed; bottom: 30px; right: 30px;
    background: #0f172a; color: white;
    padding: 14px 22px; border-radius: 12px;
    font-size: 0.92rem; font-weight: 600;
    display: flex; align-items: center; gap: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    z-index: 2000;
}
.toast i { color: #22c55e; font-size: 1.1rem; }
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(20px); }
</style>
