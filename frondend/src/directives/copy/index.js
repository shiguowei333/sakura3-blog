import { message } from "@/utils/message";
import { useEventListener } from "@vueuse/core";
import { copyTextToClipboard } from "@pureadmin/utils";


/** 文本复制指令（默认双击复制） */
export const copy = {
  mounted(el, binding) {
    const { value } = binding;
    if (value) {
      el.copyValue = value;
      const arg = binding.arg ?? "dblclick";
      // Register using addEventListener on mounted, and removeEventListener automatically on unmounted
      useEventListener(el, arg, () => {
        const success = copyTextToClipboard(el.copyValue);
        success
          ? message("复制成功", { type: "success" })
          : message("复制失败", { type: "error" });
      });
    } else {
      throw new Error(
        '[Directive: copy]: need value! Like v-copy="modelValue"'
      );
    }
  },
  updated(el, binding) {
    el.copyValue = binding.value;
  }
};
