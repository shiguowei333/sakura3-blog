import { hasPerms } from "@/utils/auth";

export const perms = {
  mounted(el, binding) {
    const { value } = binding;
    if (value) {
      !hasPerms(value) && el.parentNode?.removeChild(el);
    } else {
      throw new Error(
        "[Directive: perms]: need perms! Like v-perms=\"['btn.add','btn.edit']\""
      );
    }
  }
};
