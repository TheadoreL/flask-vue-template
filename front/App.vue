<template>
  <div class="common-layout">
    <!-- vue-router view -->
    <router-view />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

</script>

<style scoped>

</style>
