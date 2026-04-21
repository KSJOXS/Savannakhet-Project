<template>
    <div class="elegant-divider">
        <div class="line left-line"></div>
        <div class="icon-box">
            <i :class="icon"></i>
        </div>
        <div class="line right-line"></div>
    </div>
</template>

<script setup>
defineProps({
    icon: {
        type: String,
        default: 'fas fa-map-marked-alt' // Good defaults: fas fa-plane, fas fa-star, fas fa-leaf, fas fa-utensils
    }
});
</script>

<style scoped>
.elegant-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 60px auto;
    width: 90%;
    max-width: 800px;
    opacity: 0.85;
}

.line {
    flex-grow: 1;
    height: 2px;
    border-radius: 5px;
}

.left-line {
    background: linear-gradient(90deg, transparent 0%, #cbd5e1 100%);
}

.right-line {
    background: linear-gradient(270deg, transparent 0%, #cbd5e1 100%);
}

.icon-box {
    margin: 0 25px;
    color: #3b82f6; /* Modern blue */
    font-size: 1.8rem;
    animation: gentleBounce 3s infinite ease-in-out;
    background: white;
    padding: 10px;
    border-radius: 50%;
    box-shadow: 0 4px 10px rgba(59, 130, 246, 0.15);
}

@keyframes gentleBounce {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-6px) scale(1.05); }
}
</style>
