import { hasAuth } from "@/router/utils";

export const auth = {
  mounted(el, binding) {
    const { value } = binding;
    if (value) {
      !hasAuth(value) && el.parentNode?.removeChild(el);
    } else {
      throw new Error(
        "[Directive: auth]: need auths! Like v-auth=\"['btn.add','btn.edit']\""
      );
    }
  }
};
