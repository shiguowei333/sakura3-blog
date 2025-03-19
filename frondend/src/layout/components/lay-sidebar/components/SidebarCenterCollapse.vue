<script setup>
import { computed } from "vue";
import { useGlobal } from "@pureadmin/utils";
import { useNav } from "@/layout/hooks/useNav";

import ArrowLeft from "@iconify-icons/ri/arrow-left-double-fill";


const props = defineProps({
  isActive: {
    default: false
  }
});


const { tooltipEffect } = useNav();

const iconClass = computed(() => {
  return ["w-[16px]", "h-[16px]"];
});

const { $storage } = useGlobal();
const themeColor = computed(() => $storage.layout?.themeColor);

const emit = defineEmits();

const toggleClick = () => {
  emit("toggleClick");
};
</script>

<template>
  <div
    v-tippy="{
      content: isActive ? '点击折叠' : '点击展开',
      theme: tooltipEffect,
      hideOnClick: 'toggle',
      placement: 'right'
    }"
    class="center-collapse"
    @click="toggleClick"
  >
    <IconifyIconOffline
      :icon="ArrowLeft"
      :class="[iconClass, themeColor === 'light' ? '' : 'text-primary']"
      :style="{ transform: isActive ? 'none' : 'rotateY(180deg)' }"
    />
  </div>
</template>

<style lang="scss" scoped>
.center-collapse {
  position: absolute;
  top: 50%;
  right: 2px;
  z-index: 1002;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 34px;
  cursor: pointer;
  background: var(--el-bg-color);
  border: 1px solid var(--pure-border-color);
  border-radius: 4px;
  transform: translate(12px, -50%);
}
</style>
