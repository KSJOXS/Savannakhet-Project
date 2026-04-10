<template>
    <div class="admin-page">

        <!-- Toast Notification -->
        <transition name="toast">
            <div v-if="toast.show" :class="['toast', toast.type]">
                <i :class="toast.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
                {{ toast.message }}
            </div>
        </transition>

        <div class="header-content">
            <div class="title-section">
                <h3><i class="fas fa-tags"></i> Category Management</h3>
                <p class="subtitle">Add or remove categories for travel places in the system.</p>
            </div>
        </div>

        <div class="card add-card">
            <div class="add-cat-form">
                <div class="input-wrapper" :class="{ 'input-error': validationError }">
                    <i class="fas fa-plus-circle"></i>
                    <input
                        v-model="newCatName"
                        @keyup.enter="addCategory"
                        @input="validationError = ''"
                        placeholder="Enter new category name..."
                        :class="{ 'is-error': validationError }"
                    >
                </div>

                <div class="select-wrapper">
                    <select v-model="selectedParentType" class="type-select">
                        <option value="other">📁 Other</option>
                        <option value="nature">🏞️ Nature</option>
                        <option value="restaurant">🍴 Restaurant</option>
                        <option value="hotel">🏨 Hotel</option>
                        <option value="culture">🏛️ Culture</option>
                    </select>
                </div>

                <button @click="addCategory" class="btn-primary" :disabled="isLoading">
                    <i class="fas fa-save"></i>
                    {{ isLoading ? 'Add' : 'Add Category' }}
                </button>
            </div>
            <!-- Inline Validation Message -->
            <p v-if="validationError" class="validation-msg">
                <i class="fas fa-info-circle"></i> {{ validationError }}
            </p>
        </div>

        <div v-if="categories.length > 0" class="cat-grid">
            <div v-for="cat in categories" :key="cat.id" class="cat-card">
                <div class="cat-info">
                    <div class="icon-box">
                        <i :class="getIconForType(cat.parent_type)"></i>
                    </div>
                    <div class="cat-details">
                        <span class="cat-name">{{ cat.name }}</span>
                        <span class="parent-type-tag" :class="cat.parent_type">{{ cat.parent_type }}</span>
                    </div>
                </div>
                <button @click="deleteCategory(cat.id, cat.name)" class="btn-del" title="Delete category">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
        </div>

        <div v-else class="empty-state">
            <div class="empty-icon">
                <i class="fas fa-folder-open"></i>
            </div>
            <p>No categories yet.</p>
            <span>Add your first category using the form above.</span>
        </div>

        <!-- Delete Confirm Modal -->
        <transition name="modal">
            <div v-if="deleteModal.show" class="modal-overlay" @click.self="deleteModal.show = false">
                <div class="modal-box">
                    <div class="modal-icon">
                        <i class="fas fa-trash-alt"></i>
                    </div>
                    <h4>Delete Category</h4>
                    <p>Are you sure you want to delete <strong>"{{ deleteModal.name }}"</strong>?<br>
                    <span class="warning-text">This action cannot be undone.</span></p>
                    <div class="modal-actions">
                        <button @click="deleteModal.show = false" class="btn-cancel">Cancel</button>
                        <button @click="confirmDelete" class="btn-confirm-del" :disabled="isDeleting">
                            <i class="fas fa-trash-alt"></i>
                            {{ isDeleting ? 'Deleting...' : 'Yes, Delete' }}
                        </button>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { categoryRepository } from '@/repositories/categoryRepository'

const categories = ref([])
const newCatName = ref('')
const selectedParentType = ref('other')
const validationError = ref('')
const isLoading = ref(false)
const isDeleting = ref(false)

const toast = reactive({ show: false, message: '', type: 'success' })
const deleteModal = reactive({ show: false, id: null, name: '' })

const showToast = (message, type = 'success') => {
    toast.message = message
    toast.type = type
    toast.show = true
    setTimeout(() => { toast.show = false }, 3500)
}

const fetchCats = async () => {
    try {
        const res = await categoryRepository.getAll()
        categories.value = res.data
    } catch (error) {
        console.error('Fetch Error:', error)
    }
}

const addCategory = async () => {
    const name = newCatName.value.trim()

    // Validation: show inline error if empty
    if (!name) {
        validationError.value = 'Please enter a category name before adding.'
        return
    }

    isLoading.value = true
    try {
        await categoryRepository.create({ 
            name,
            parent_type: selectedParentType.value 
        })
        newCatName.value = ''
        validationError.value = ''
        await fetchCats()
        showToast(`Category "${name}" added successfully!`, 'success')
    } catch (error) {
        showToast('Failed to add category. Please try again.', 'error')
    } finally {
        isLoading.value = false
    }
}

const getIconForType = (type) => {
    const icons = {
        nature: 'fas fa-tree',
        restaurant: 'fas fa-utensils',
        hotel: 'fas fa-bed',
        culture: 'fas fa-landmark',
        other: 'fas fa-folder'
    }
    return icons[type] || 'fas fa-folder'
}

const deleteCategory = (id, name) => {
    deleteModal.id = id
    deleteModal.name = name
    deleteModal.show = true
}

const confirmDelete = async () => {
    isDeleting.value = true
    try {
        await categoryRepository.delete(deleteModal.id)
        await fetchCats()
        showToast(`Category "${deleteModal.name}" has been deleted.`, 'success')
        deleteModal.show = false
    } catch (error) {
        const status = error?.response?.status
        if (status === 500 || status === 409) {
            showToast('Cannot delete — this category has places assigned to it.', 'error')
        } else {
            showToast('Failed to delete category. Please try again.', 'error')
        }
        deleteModal.show = false
    } finally {
        isDeleting.value = false
    }
}

onMounted(fetchCats)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');

.admin-page {
    font-family: 'Kanit', sans-serif;
    color: #334155;
    padding: 30px 40px;
    max-width: 1200px;
    margin: 0;
    min-height: 100vh;
    background-color: #fcfcfc;
}

/* Toast */
.toast {
    position: fixed;
    top: 24px;
    right: 24px;
    z-index: 9999;
    padding: 14px 22px;
    border-radius: 12px;
    font-size: 0.95rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    animation: slideIn 0.3s ease;
}
.toast.success { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
.toast.error   { background: #fff1f2; color: #9f1239; border: 1px solid #fecdd3; }

.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateX(20px); }

/* Header */
.header-content {
    margin-bottom: 30px;
    border-left: 5px solid #3b82f6;
    padding-left: 20px;
}
.title-section h3 {
    font-size: 1.6rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 12px;
}
.subtitle {
    color: #94a3b8;
    font-size: 0.95rem;
    margin-top: 4px;
}

/* Card Form */
.card.add-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    border: 1px solid #f1f5f9;
    margin-bottom: 35px;
}
.add-cat-form {
    display: flex;
    gap: 12px;
}
.input-wrapper {
    position: relative;
    flex: 1;
}
.input-wrapper i {
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
    transition: 0.2s;
}
.input-wrapper.input-error i { color: #f43f5e; }

.input-wrapper input {
    width: 100%;
    padding: 12px 12px 12px 48px;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    font-size: 0.95rem;
    font-family: 'Kanit', sans-serif;
    transition: 0.2s;
    background: #f8fafc;
    box-sizing: border-box;
}
.input-wrapper input:focus {
    background: white;
    border-color: #3b82f6;
    outline: none;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.05);
}
.input-wrapper input.is-error {
    border-color: #f43f5e;
    background: #fff1f2;
}
.input-wrapper input.is-error:focus {
    border-color: #f43f5e;
    box-shadow: 0 0 0 4px rgba(244, 63, 94, 0.08);
}

/* Validation Message */
.validation-msg {
    margin: 10px 0 0 4px;
    font-size: 0.88rem;
    color: #f43f5e;
    display: flex;
    align-items: center;
    gap: 6px;
    animation: fadeIn 0.2s ease;
}

@keyframes fadeIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }

/* Buttons */
.btn-primary {
    background: #3b82f6;
    color: white;
    border: none;
    padding: 0 24px;
    border-radius: 10px;
    font-weight: 500;
    font-family: 'Kanit', sans-serif;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
}
.btn-primary:hover:not(:disabled) { background: #2563eb; transform: translateY(-1px); }
.btn-primary:disabled { background: #93c5fd; cursor: not-allowed; }

/* Cat Grid */
.cat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 16px;
}
.cat-card {
    background: white;
    padding: 16px 20px;
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid #f1f5f9;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    transition: 0.3s;
}
.cat-card:hover {
    transform: translateY(-3px);
    border-color: #3b82f6;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
}
.cat-info { display: flex; align-items: center; gap: 12px; }
.icon-box {
    width: 40px; height: 40px;
    background: #f1f5f9;
    color: #64748b;
    display: flex; align-items: center; justify-content: center;
    border-radius: 8px;
    font-size: 1.1rem;
}
.cat-details {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.cat-name { font-weight: 600; color: #1e293b; font-size: 1rem; }
.parent-type-tag {
    font-size: 0.7rem;
    padding: 1px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    font-weight: 700;
    width: fit-content;
}
.parent-type-tag.nature { background: #dcfce7; color: #166534; }
.parent-type-tag.restaurant { background: #fef9c3; color: #854d0e; }
.parent-type-tag.hotel { background: #dbeafe; color: #1e40af; }
.parent-type-tag.culture { background: #f3e8ff; color: #6b21a8; }
.parent-type-tag.other { background: #f1f5f9; color: #475569; }

.select-wrapper {
    width: 200px;
}
.type-select {
    width: 100%;
    padding: 12px;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    background: #f8fafc;
    font-family: 'Kanit', sans-serif;
    cursor: pointer;
}
.type-select:focus {
    border-color: #3b82f6;
    background: white;
}

.btn-del {
    color: #cbd5e1;
    background: transparent;
    border: none;
    width: 34px; height: 34px;
    border-radius: 6px;
    cursor: pointer;
    transition: 0.2s;
    font-size: 0.9rem;
}
.btn-del:hover { color: #f43f5e; background: #fff1f2; }

/* Empty State */
.empty-state {
    text-align: center;
    padding: 80px 20px;
    background: #f8fafc;
    border: 2px dashed #e2e8f0;
    border-radius: 16px;
    color: #94a3b8;
}

/* Modal */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(4px);
}
.modal-box {
    background: white;
    border-radius: 20px;
    padding: 40px;
    max-width: 420px;
    width: 90%;
    text-align: center;
    box-shadow: 0 25px 60px rgba(0,0,0,0.15);
}
.modal-icon {
    width: 64px; height: 64px;
    background: #fff1f2;
    color: #f43f5e;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem;
    margin: 0 auto 20px;
}
.modal-box h4 { font-size: 1.3rem; color: #1e293b; margin: 0 0 12px; }
.modal-box p { color: #64748b; line-height: 1.6; margin: 0 0 28px; }
.warning-text { font-size: 0.85rem; color: #f43f5e; }
.modal-actions { display: flex; gap: 12px; justify-content: center; }
.btn-cancel {
    padding: 10px 28px; border-radius: 10px;
    border: 1.5px solid #e2e8f0;
    background: white; color: #64748b;
    font-weight: 500; font-family: 'Kanit', sans-serif;
    cursor: pointer; transition: 0.2s;
}
.btn-cancel:hover { background: #f8fafc; }
.btn-confirm-del {
    padding: 10px 28px; border-radius: 10px;
    border: none;
    background: #f43f5e; color: white;
    font-weight: 500; font-family: 'Kanit', sans-serif;
    cursor: pointer; transition: 0.2s;
    display: flex; align-items: center; gap: 8px;
}
.btn-confirm-del:hover:not(:disabled) { background: #e11d48; transform: translateY(-1px); }
.btn-confirm-del:disabled { background: #fda4af; cursor: not-allowed; }

.modal-enter-active, .modal-leave-active { transition: all 0.25s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .modal-box, .modal-leave-to .modal-box { transform: scale(0.9); }

@media (max-width: 640px) {
    .admin-page { padding: 20px; }
    .add-cat-form { flex-direction: column; }
    .btn-primary { height: 45px; justify-content: center; }
}
</style>
