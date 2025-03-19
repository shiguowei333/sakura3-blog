<script setup>
import MenuFold from "@iconify-icons/ri/menu-fold-fill";
import MenuUnfold from "@iconify-icons/ri/menu-unfold-fill";


const props = defineProps({
  isActive: {
    default: false
  }
});

const emit = defineEmits();

const toggleClick = () => {
  emit("toggleClick");
};
</script>

<template>
  <div
    class="px-3 mr-1 navbar-bg-hover"
    :title="isActive ? '点击折叠' : '点击展开'"
    @click="toggleClick"
  >
    <IconifyIconOffline
      :icon="isActive ? MenuFold : MenuUnfold"
      class="inline-block align-middle hover:text-primary dark:hover:!text-white"
    />
  </div>
</template>
