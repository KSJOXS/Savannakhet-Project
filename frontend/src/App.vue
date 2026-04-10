<template>
  <div id="app">
    <router-view />
    <Footer v-if="!isAdminRoute && !isAuthRoute" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Footer from './components/Footer.vue';

const route = useRoute();

const isAdminRoute = computed(() => {
    return route.path && route.path.startsWith('/admin');
});

const isAuthRoute = computed(() => {
    return route.path && ['/login', '/register'].includes(route.path);
});
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;600&display=swap');

body {
  margin: 0;
  font-family: 'Prompt', sans-serif;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
</style>