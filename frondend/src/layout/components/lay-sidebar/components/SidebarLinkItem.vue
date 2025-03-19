<script setup>
import { computed } from "vue";
import { isUrl } from "@pureadmin/utils";

const props = defineProps({
  to: {
    type: Object
  }
});

const isExternalLink = computed(() => isUrl(props.to.name));
const getLinkProps = (item) => {
  if (isExternalLink.value) {
    return {
      href: item.name,
      target: "_blank",
      rel: "noopener"
    };
  }
  return {
    to: item
  };
};
</script>

<template>
  <component
    :is="isExternalLink ? 'a' : 'router-link'"
    v-bind="getLinkProps(to)"
  >
    <slot />
  </component>
</template>
