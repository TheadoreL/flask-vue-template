<template>
    <div>
      This is index view
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router'; // 导入 useRoute

export default defineComponent({
  name: 'Index',
  setup() {

    const pageInit = async () => {
      console.log("index page")
    };

    onMounted(() => {
      pageInit();
    });

    return { pageInit };
  }
});
</script>