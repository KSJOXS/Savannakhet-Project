<template>
    <div class="inbox-page">

        <!-- Header -->
        <div class="page-header">
            <div class="header-left">
                <div class="header-icon-wrap">
                    <i class="fas fa-inbox"></i>
                </div>
                <div>
                    <h2>Contact Inbox</h2>
                    <p class="subtitle">Messages submitted through the Contact page.</p>
                </div>
            </div>
            <div class="header-pills">
                <span class="pill pill-blue">
                    <i class="fas fa-circle-dot"></i>
                    {{ unreadCount }} Unread
                </span>
                <span class="pill pill-gray">
                    <i class="fas fa-envelope"></i>
                    {{ messages.length }} Total
                </span>
            </div>
        </div>

        <!-- Filter Tabs -->
        <div class="filter-bar">
            <button v-for="f in filters" :key="f.value"
                :class="['tab-btn', { active: activeFilter === f.value }]"
                @click="activeFilter = f.value">
                <i :class="f.icon"></i>
                {{ f.label }}
                <span class="tab-count">{{ getFilterCount(f.value) }}</span>
            </button>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <span>Loading messages...</span>
        </div>

        <!-- Message List -->
        <div v-else class="message-list">
            <div v-if="filteredMessages.length === 0" class="empty-inbox">
                <div class="empty-icon">
                    <i class="fas fa-envelope-open-text"></i>
                </div>
                <p>No messages here.</p>
                <span>All caught up! 🎉</span>
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
                <div class="sender-avatar" :style="getAvatarStyle(msg.name)">
                    {{ msg.name.charAt(0).toUpperCase() }}
                </div>

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
                        <span v-if="msg.is_replied" class="badge badge-green">
                            <i class="fas fa-check-circle"></i> Replied
                        </span>
                        <span v-else-if="msg.is_read" class="badge badge-blue">
                            <i class="fas fa-envelope-open"></i> Read
                        </span>
                        <span v-else class="badge badge-amber">
                            <i class="fas fa-circle"></i> New
                        </span>
                    </div>
                </div>

                <i class="fas fa-chevron-right row-arrow"></i>
            </div>
        </div>

        <!-- ─── Message Detail Modal ─── -->
        <transition name="modal-fade">
            <div v-if="selectedMsg" class="modal-overlay" @click.self="selectedMsg = null">
                <div class="modal-box">

                    <!-- Modal Header -->
                    <div class="modal-head">
                        <div class="modal-head-avatar" :style="getAvatarStyle(selectedMsg.name)">
                            {{ selectedMsg.name.charAt(0).toUpperCase() }}
                        </div>
                        <div class="modal-head-info">
                            <h3>{{ selectedMsg.subject }}</h3>
                            <p class="modal-sender">
                                <i class="fas fa-user-circle"></i>
                                <strong>{{ selectedMsg.name }}</strong>
                                <a :href="`mailto:${selectedMsg.email}`" class="email-chip">
                                    <i class="fas fa-envelope"></i>
                                    {{ selectedMsg.email }}
                                </a>
                            </p>
                            <p class="modal-date">
                                <i class="fas fa-clock"></i>
                                {{ formatDateFull(selectedMsg.created_at) }}
                            </p>
                        </div>
                        <div class="modal-head-actions">
                            <span v-if="selectedMsg.is_replied" class="status-chip chip-green">
                                <i class="fas fa-check-circle"></i> Replied
                            </span>
                            <span v-else-if="selectedMsg.is_read" class="status-chip chip-blue">
                                <i class="fas fa-envelope-open"></i> Read
                            </span>
                            <span v-else class="status-chip chip-amber">
                                <i class="fas fa-star"></i> New
                            </span>
                            <button class="close-x" @click="selectedMsg = null" title="Close">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Message Body -->
                    <div class="modal-message-body">
                        <div class="message-label">
                            <i class="fas fa-comment-alt"></i> Message
                        </div>
                        <div class="message-text">{{ selectedMsg.message }}</div>
                    </div>

                    <!-- Reply History (ถ้าตอบแล้ว) -->
                    <div v-if="selectedMsg.is_replied" class="reply-history">
                        <div class="rh-header">
                            <div class="rh-title">
                                <i class="fas fa-paper-plane"></i>
                                Your Reply
                            </div>
                            <span class="rh-date" v-if="selectedMsg.replied_at">
                                <i class="fas fa-clock"></i>
                                {{ formatDateFull(selectedMsg.replied_at) }}
                            </span>
                        </div>
                        <div v-if="selectedMsg.reply_text" class="rh-body">{{ selectedMsg.reply_text }}</div>
                        <div v-else class="rh-no-record">
                            <i class="fas fa-info-circle"></i>
                            Reply was sent before history tracking was enabled.
                        </div>
                    </div>

                    <!-- ปุ่ม Close เมื่อตอบแล้ว -->
                    <div v-if="selectedMsg.is_replied" class="replied-close-bar">
                        <button @click="selectedMsg = null" class="btn-close-replied">
                            <i class="fas fa-times"></i> Close
                        </button>
                    </div>

                    <!-- Reply Section (เฉพาะเมื่อยังไม่ได้ตอบ) -->
                    <div class="reply-section" v-if="!selectedMsg.is_replied">
                        <div class="reply-header">
                            <div class="reply-title">
                                <i class="fas fa-reply"></i>
                                Reply to <strong>{{ selectedMsg.name }}</strong>
                            </div>
                            <div class="reply-destination">
                                <i class="fas fa-paper-plane"></i>
                                Will be sent to: <span class="dest-email">{{ selectedMsg.email }}</span>
                            </div>
                        </div>

                        <div class="textarea-wrap" :class="{ focused: textareaFocused }">
                            <textarea
                                v-model="replyText"
                                placeholder="Type your reply here... (This will be emailed directly to the user)"
                                rows="5"
                                class="reply-textarea"
                                @focus="textareaFocused = true"
                                @blur="textareaFocused = false"
                            ></textarea>
                            <div class="char-count">{{ replyText.length }} chars</div>
                        </div>

                        <div class="reply-actions">
                            <button @click="selectedMsg = null" class="btn-ghost">
                                <i class="fas fa-times"></i> Close
                            </button>
                            <button
                                @click="sendReply"
                                class="btn-reply"
                                :disabled="!replyText.trim() || replying"
                            >
                                <span v-if="replying" class="btn-inner">
                                    <i class="fas fa-spinner fa-spin"></i> Sending...
                                </span>
                                <span v-else class="btn-inner">
                                    <i class="fas fa-paper-plane"></i> Send Email Reply
                                </span>
                            </button>
                        </div>
                    </div>

                </div>
            </div>
        </transition>

        <!-- Reply Success Toast -->
        <transition name="toast">
            <div v-if="showToast" class="toast">
                <div class="toast-icon"><i class="fas fa-check-circle"></i></div>
                <div class="toast-body">
                    <strong>Reply sent!</strong>
                    <span>Email has been delivered to {{ lastRepliedEmail }}</span>
                </div>
            </div>
        </transition>

        <!-- Error Toast -->
        <transition name="toast">
            <div v-if="showError" class="toast toast-error">
                <div class="toast-icon"><i class="fas fa-exclamation-circle"></i></div>
                <div class="toast-body">
                    <strong>Failed to send</strong>
                    <span>{{ errorMsg }}</span>
                </div>
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
const showError = ref(false)
const errorMsg = ref('')
const lastRepliedEmail = ref('')
const textareaFocused = ref(false)
const showReplyBox = ref(false)

const filters = [
    { value: 'all',     label: 'All',     icon: 'fas fa-inbox' },
    { value: 'unread',  label: 'Unread',  icon: 'fas fa-circle-dot' },
    { value: 'read',    label: 'Read',    icon: 'fas fa-envelope-open' },
    { value: 'replied', label: 'Replied', icon: 'fas fa-check-circle' },
]

// Avatar colors palette
const avatarColors = [
    ['#dbeafe','#1d4ed8'], ['#fce7f3','#be185d'], ['#dcfce7','#15803d'],
    ['#fef3c7','#b45309'], ['#ede9fe','#7c3aed'], ['#fee2e2','#b91c1c'],
    ['#d1fae5','#047857'], ['#e0f2fe','#0369a1'],
]
const getAvatarStyle = (name) => {
    const idx = name.charCodeAt(0) % avatarColors.length
    const [bg, color] = avatarColors[idx]
    return { background: bg, color }
}

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
    showReplyBox.value = false   // ซ่อน reply box ทุกครั้งที่เปิด message ใหม่
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
    const targetEmail = selectedMsg.value.email
    try {
        const fd = new FormData()
        fd.append('reply_text', replyText.value)
        await api.post(`/api/admin/messages/${selectedMsg.value.id}/reply`, fd)
        selectedMsg.value.is_replied = true
        lastRepliedEmail.value = targetEmail
        replyText.value = ''
        showReplyBox.value = false
        selectedMsg.value = null
        showToast.value = true
        setTimeout(() => showToast.value = false, 4000)
        await fetchMessages()
    } catch (e) {
        errorMsg.value = e.response?.data?.detail || 'Please check your SMTP settings in .env'
        showError.value = true
        setTimeout(() => showError.value = false, 5000)
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { box-sizing: border-box; }

.inbox-page {
    font-family: 'Inter', sans-serif;
    padding: 32px 40px;
    background: #f0f4f8;
    min-height: 100vh;
}

/* ─── Header ─── */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
}
.header-left { display: flex; align-items: center; gap: 16px; }
.header-icon-wrap {
    width: 48px; height: 48px; border-radius: 14px;
    background: linear-gradient(135deg, #1e40af, #3b82f6);
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 1.2rem;
    box-shadow: 0 4px 12px rgba(59,130,246,0.35);
}
.page-header h2 {
    font-size: 1.6rem; font-weight: 800; color: #0f172a; margin: 0;
}
.subtitle { color: #64748b; font-size: 0.88rem; margin: 3px 0 0; }

.header-pills { display: flex; gap: 10px; }
.pill {
    padding: 8px 16px; border-radius: 24px; font-size: 0.83rem; font-weight: 600;
    display: flex; align-items: center; gap: 7px;
}
.pill-blue { background: #dbeafe; color: #1d4ed8; }
.pill-gray { background: #e2e8f0; color: #475569; }

/* ─── Filter Tabs ─── */
.filter-bar {
    display: flex; gap: 4px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 6px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 22px;
    width: fit-content;
}
.tab-btn {
    padding: 8px 18px; border: none; border-radius: 10px; background: transparent;
    color: #64748b; font-size: 0.875rem; font-weight: 500; cursor: pointer;
    transition: all 0.18s; font-family: inherit;
    display: flex; align-items: center; gap: 7px;
}
.tab-btn i { font-size: 0.8rem; }
.tab-btn:hover { background: #f1f5f9; color: #1e293b; }
.tab-btn.active {
    background: linear-gradient(135deg, #1e40af, #3b82f6);
    color: white;
    box-shadow: 0 4px 12px rgba(59,130,246,0.3);
}
.tab-count {
    background: rgba(255,255,255,0.25); border-radius: 12px;
    padding: 1px 8px; font-size: 0.72rem; font-weight: 700;
}
.tab-btn:not(.active) .tab-count { background: #f1f5f9; color: #64748b; }

/* ─── Loading ─── */
.loading-state {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding: 80px; color: #64748b; gap: 16px;
}
.loading-spinner {
    width: 36px; height: 36px; border: 3px solid #e2e8f0;
    border-top-color: #3b82f6; border-radius: 50%;
    animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ─── Message List ─── */
.message-list {
    background: white;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
    overflow: hidden;
}

.empty-inbox {
    text-align: center; padding: 80px 40px; color: #94a3b8;
}
.empty-icon {
    width: 80px; height: 80px; border-radius: 50%; background: #f1f5f9;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 20px; font-size: 2rem; color: #cbd5e1;
}
.empty-inbox p { font-size: 1rem; font-weight: 600; color: #475569; margin: 0 0 4px; }
.empty-inbox span { font-size: 0.85rem; color: #94a3b8; }

.message-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 24px;
    border-bottom: 1px solid #f1f5f9;
    cursor: pointer;
    transition: all 0.15s;
    position: relative;
}
.message-row:last-child { border-bottom: none; }
.message-row:hover { background: #f8fafc; transform: translateX(2px); }
.message-row.unread { background: linear-gradient(90deg, #eff6ff 0%, #fafbff 100%); }
.message-row.unread::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0;
    width: 3px; background: #3b82f6; border-radius: 0 2px 2px 0;
}

.unread-dot-col { width: 12px; flex-shrink: 0; }
.unread-dot {
    width: 9px; height: 9px;
    background: #3b82f6;
    border-radius: 50%;
    display: block;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.2);
    animation: pulse 2s ease infinite;
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 3px rgba(59,130,246,0.2); }
    50% { box-shadow: 0 0 0 6px rgba(59,130,246,0.05); }
}

.sender-avatar {
    width: 42px; height: 42px; border-radius: 50%;
    font-weight: 800; font-size: 1rem;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}

.message-content { flex: 1; min-width: 0; }
.message-top { display: flex; align-items: baseline; gap: 10px; margin-bottom: 4px; }
.sender-name { font-weight: 700; font-size: 0.93rem; color: #0f172a; white-space: nowrap; }
.message-subject { font-weight: 500; font-size: 0.9rem; color: #334155; }
.message-row:not(.unread) .sender-name { font-weight: 500; color: #475569; }
.message-row:not(.unread) .message-subject { color: #94a3b8; }
.message-preview { font-size: 0.82rem; color: #94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.message-meta { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; flex-shrink: 0; }
.message-date { font-size: 0.78rem; color: #94a3b8; white-space: nowrap; }
.message-badges { display: flex; gap: 4px; }
.badge {
    padding: 3px 10px; border-radius: 12px; font-size: 0.72rem;
    font-weight: 600; display: inline-flex; align-items: center; gap: 4px;
}
.badge-green { background: #dcfce7; color: #15803d; }
.badge-blue { background: #dbeafe; color: #1d4ed8; }
.badge-gray { background: #f1f5f9; color: #64748b; }
.badge-amber { background: #fef3c7; color: #b45309; }

.row-arrow { color: #cbd5e1; font-size: 0.75rem; flex-shrink: 0; margin-left: 4px; }

/* ─── Modal ─── */
.modal-overlay {
    position: fixed; inset: 0;
    background: rgba(15,23,42,0.6);
    display: flex; align-items: center; justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(6px);
    padding: 20px;
}
.modal-box {
    background: white;
    border-radius: 22px;
    width: 760px;
    max-width: 100%;
    max-height: 92vh;
    overflow-y: auto;
    box-shadow: 0 32px 80px rgba(0,0,0,0.25);
    border: 1px solid rgba(255,255,255,0.8);
}

/* Modal Header */
.modal-head {
    display: flex; align-items: flex-start; gap: 16px;
    padding: 28px 28px 20px;
    border-bottom: 1px solid #f1f5f9;
    background: linear-gradient(135deg, #f8faff 0%, #fff 100%);
    border-radius: 22px 22px 0 0;
}
.modal-head-avatar {
    width: 52px; height: 52px; border-radius: 16px;
    font-weight: 800; font-size: 1.3rem;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.modal-head-info { flex: 1; min-width: 0; }
.modal-head-info h3 {
    font-size: 1.2rem; font-weight: 800; color: #0f172a; margin: 0 0 8px;
    line-height: 1.3;
}
.modal-sender {
    font-size: 0.87rem; color: #475569; margin: 0 0 6px;
    display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
}
.modal-sender i { color: #94a3b8; }
.email-chip {
    display: inline-flex; align-items: center; gap: 5px;
    background: #eff6ff; color: #1d4ed8; padding: 3px 10px;
    border-radius: 20px; text-decoration: none; font-size: 0.82rem; font-weight: 600;
    transition: 0.15s;
}
.email-chip:hover { background: #dbeafe; }
.modal-date {
    font-size: 0.8rem; color: #94a3b8; margin: 0;
    display: flex; align-items: center; gap: 6px;
}
.modal-date i { color: #cbd5e1; }

.modal-head-actions {
    display: flex; align-items: center; gap: 10px; flex-shrink: 0;
}
.status-chip {
    padding: 5px 12px; border-radius: 20px; font-size: 0.77rem; font-weight: 700;
    display: inline-flex; align-items: center; gap: 5px;
}
.chip-green { background: #dcfce7; color: #15803d; }
.chip-blue { background: #dbeafe; color: #1d4ed8; }
.chip-amber { background: #fef3c7; color: #b45309; }
.close-x {
    width: 34px; height: 34px; border-radius: 10px;
    background: #f1f5f9; border: none; cursor: pointer;
    color: #64748b; font-size: 0.9rem;
    display: flex; align-items: center; justify-content: center;
    transition: 0.15s;
}
.close-x:hover { background: #fee2e2; color: #ef4444; }

/* Message Body */
.modal-message-body {
    padding: 24px 28px;
    border-bottom: 1px solid #f1f5f9;
}
.message-label {
    font-size: 0.78rem; font-weight: 700; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.8px;
    margin-bottom: 12px; display: flex; align-items: center; gap: 6px;
}
.message-text {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    font-size: 0.95rem;
    color: #334155;
    line-height: 1.8;
    white-space: pre-wrap;
    border-left: 4px solid #e2e8f0;
}

/* Reply Section */
.reply-section { padding: 24px 28px 28px; }

.reply-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 14px; flex-wrap: wrap; gap: 8px;
}
.reply-title {
    font-size: 0.95rem; font-weight: 700; color: #1e293b;
    display: flex; align-items: center; gap: 8px;
}
.reply-title i { color: #3b82f6; }
.reply-destination {
    font-size: 0.8rem; color: #64748b;
    display: flex; align-items: center; gap: 6px;
    background: #f0fdf4; padding: 5px 12px; border-radius: 20px;
    border: 1px solid #bbf7d0;
}
.reply-destination i { color: #22c55e; }
.dest-email { color: #15803d; font-weight: 700; }

.textarea-wrap {
    border: 2px solid #e2e8f0; border-radius: 14px;
    overflow: hidden; transition: 0.2s; background: #fafbfc;
    position: relative;
}
.textarea-wrap.focused { border-color: #3b82f6; box-shadow: 0 0 0 4px rgba(59,130,246,0.1); background: white; }
.reply-textarea {
    width: 100%; padding: 16px;
    border: none; outline: none;
    font-size: 0.95rem; font-family: inherit; color: #334155;
    resize: vertical; background: transparent; display: block;
    min-height: 120px;
}
.char-count {
    text-align: right; padding: 6px 14px;
    font-size: 0.75rem; color: #cbd5e1; font-weight: 500;
    border-top: 1px solid #f1f5f9;
}

.reply-actions {
    display: flex; justify-content: flex-end; gap: 10px; margin-top: 16px;
}
.btn-ghost {
    background: #f1f5f9; color: #475569; border: none;
    padding: 11px 22px; border-radius: 11px; cursor: pointer;
    font-family: inherit; font-weight: 600; font-size: 0.88rem;
    display: flex; align-items: center; gap: 7px;
    transition: 0.15s;
}
.btn-ghost:hover { background: #e2e8f0; }
.btn-reply {
    background: linear-gradient(135deg, #1e40af, #3b82f6);
    color: white; border: none;
    padding: 11px 26px; border-radius: 11px; cursor: pointer;
    font-family: inherit; font-weight: 700; font-size: 0.9rem;
    transition: all 0.2s;
    box-shadow: 0 4px 14px rgba(59,130,246,0.4);
}
.btn-reply:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(59,130,246,0.45);
}
.btn-reply:disabled { opacity: 0.55; cursor: not-allowed; transform: none; box-shadow: none; }
.btn-inner { display: flex; align-items: center; gap: 8px; }

/* ─── Toast ─── */
.toast {
    position: fixed; bottom: 30px; right: 30px;
    background: #0f172a; color: white;
    padding: 16px 22px; border-radius: 16px;
    display: flex; align-items: center; gap: 14px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.3);
    z-index: 2000; max-width: 340px;
}
.toast-error { background: #7f1d1d; }
.toast-icon { font-size: 1.4rem; }
.toast .toast-icon { color: #22c55e; }
.toast-error .toast-icon { color: #fca5a5; }
.toast-body { display: flex; flex-direction: column; gap: 2px; }
.toast-body strong { font-size: 0.9rem; }
.toast-body span { font-size: 0.78rem; color: rgba(255,255,255,0.65); }

.toast-enter-active, .toast-leave-active { transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1); }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(16px) scale(0.95); }

/* Modal transition */
.modal-fade-enter-active, .modal-fade-leave-active { transition: all 0.25s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.modal-fade-enter-from .modal-box, .modal-fade-leave-to .modal-box { transform: translateY(20px) scale(0.97); }

/* ─── Reply History ─── */
.reply-history {
    margin: 0 28px 0;
    padding: 20px;
    background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
    border: 1px solid #bbf7d0;
    border-radius: 14px;
    border-left: 4px solid #22c55e;
}
.rh-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 12px;
}
.rh-title {
    font-size: 0.85rem; font-weight: 700; color: #15803d;
    display: flex; align-items: center; gap: 6px;
}
.rh-title i { color: #22c55e; }
.rh-date { font-size: 0.75rem; color: #6b7280; }
.rh-body {
    font-size: 0.93rem; color: #1e293b; line-height: 1.75;
    white-space: pre-wrap; margin-bottom: 14px;
    background: white; padding: 14px 16px;
    border-radius: 10px; border: 1px solid #d1fae5;
}
.btn-send-another {
    background: white; border: 1.5px solid #22c55e;
    color: #15803d; padding: 7px 16px; border-radius: 9px;
    font-family: inherit; font-size: 0.82rem; font-weight: 700;
    cursor: pointer; display: inline-flex; align-items: center; gap: 6px;
    transition: 0.15s;
}
.btn-send-another:hover { background: #dcfce7; }
.rh-no-record {
    font-size: 0.82rem; color: #6b7280; font-style: italic;
    display: flex; align-items: center; gap: 6px;
    margin-top: 10px; padding: 10px 14px;
    background: #f9fafb; border-radius: 8px; border: 1px dashed #d1d5db;
}

/* ─── Replied Close Bar ─── */
.replied-close-bar {
    padding: 16px 28px 24px;
    display: flex; justify-content: flex-end;
}
.btn-close-replied {
    background: #f1f5f9; color: #475569; border: none;
    padding: 10px 24px; border-radius: 11px; cursor: pointer;
    font-family: inherit; font-weight: 600; font-size: 0.9rem;
    display: flex; align-items: center; gap: 8px;
    transition: 0.15s;
}
.btn-close-replied:hover { background: #e2e8f0; color: #1e293b; }


</style>
