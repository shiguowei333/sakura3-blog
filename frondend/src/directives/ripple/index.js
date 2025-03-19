import "./index.scss";
import { isObject } from "@pureadmin/utils";



function transform(el, value) {
  el.style.transform = value;
  el.style.webkitTransform = value;
}

const calculate = (
  e,
  el,
  value = {}
) => {
  const offset = el.getBoundingClientRect();

  // 获取点击位置距离 el 的垂直和水平距离
  let localX = e.clientX - offset.left;
  let localY = e.clientY - offset.top;

  let radius = 0;
  let scale = 0.3;
  // 计算点击位置到 el 顶点最远距离，即为圆的最大半径（勾股定理）
  if (el._ripple?.circle) {
    scale = 0.15;
    radius = el.clientWidth / 2;
    radius = value.center
      ? radius
      : radius + Math.sqrt((localX - radius) ** 2 + (localY - radius) ** 2) / 4;
  } else {
    radius = Math.sqrt(el.clientWidth ** 2 + el.clientHeight ** 2) / 2;
  }

  // 中心点坐标
  const centerX = `${(el.clientWidth - radius * 2) / 2}px`;
  const centerY = `${(el.clientHeight - radius * 2) / 2}px`;

  // 点击位置坐标
  const x = value.center ? centerX : `${localX - radius}px`;
  const y = value.center ? centerY : `${localY - radius}px`;

  return { radius, scale, x, y, centerX, centerY };
};

const ripples = {
  show(e, el, value = {}) {
    if (!el?._ripple?.enabled) {
      return;
    }

    // 创建 ripple 元素和 ripple 父元素
    const container = document.createElement("span");
    const animation = document.createElement("span");

    container.appendChild(animation);
    container.className = "v-ripple__container";

    if (value.class) {
      container.className += ` ${value.class}`;
    }

    const { radius, scale, x, y, centerX, centerY } = calculate(e, el, value);

    // ripple 圆大小
    const size = `${radius * 2}px`;

    animation.className = "v-ripple__animation";
    animation.style.width = size;
    animation.style.height = size;

    el.appendChild(container);

    // 获取目标元素样式表
    const computed = window.getComputedStyle(el);
    // 防止 position 被覆盖导致 ripple 位置有问题
    if (computed && computed.position === "static") {
      el.style.position = "relative";
      el.dataset.previousPosition = "static";
    }

    animation.classList.add("v-ripple__animation--enter");
    animation.classList.add("v-ripple__animation--visible");
    transform(
      animation,
      `translate(${x}, ${y}) scale3d(${scale},${scale},${scale})`
    );
    animation.dataset.activated = String(performance.now());

    setTimeout(() => {
      animation.classList.remove("v-ripple__animation--enter");
      animation.classList.add("v-ripple__animation--in");
      transform(animation, `translate(${centerX}, ${centerY}) scale3d(1,1,1)`);
    }, 0);
  },

  hide(el) {
    if (!el?._ripple?.enabled) return;

    const ripples = el.getElementsByClassName("v-ripple__animation");

    if (ripples.length === 0) return;
    const animation = ripples[ripples.length - 1];

    if (animation.dataset.isHiding) return;
    else animation.dataset.isHiding = "true";

    const diff = performance.now() - Number(animation.dataset.activated);
    const delay = Math.max(250 - diff, 0);

    setTimeout(() => {
      animation.classList.remove("v-ripple__animation--in");
      animation.classList.add("v-ripple__animation--out");

      setTimeout(() => {
        const ripples = el.getElementsByClassName("v-ripple__animation");
        if (ripples.length === 1 && el.dataset.previousPosition) {
          el.style.position = el.dataset.previousPosition;
          delete el.dataset.previousPosition;
        }

        if (animation.parentNode?.parentNode === el)
          el.removeChild(animation.parentNode);
      }, 300);
    }, delay);
  }
};

function isRippleEnabled(value) {
  return typeof value === "undefined" || !!value;
}

function rippleShow(e) {
  const value = {};
  const element = e.currentTarget;

  if (!element?._ripple || element._ripple.touched) return;

  value.center = element._ripple.centered;
  if (element._ripple.class) {
    value.class = element._ripple.class;
  }

  ripples.show(e, element, value);
}

function rippleHide(e) {
  const element = e.currentTarget;
  if (!element?._ripple) return;

  window.setTimeout(() => {
    if (element._ripple) {
      element._ripple.touched = false;
    }
  });
  ripples.hide(element);
}

function updateRipple(
  el,
  binding,
  wasEnabled
) {
  const { value, modifiers } = binding;
  const enabled = isRippleEnabled(value);
  if (!enabled) {
    ripples.hide(el);
  }

  el._ripple = el._ripple ?? {};
  el._ripple.enabled = enabled;
  el._ripple.centered = modifiers.center;
  el._ripple.circle = modifiers.circle;
  if (isObject(value) && value.class) {
    el._ripple.class = value.class;
  }

  if (enabled && !wasEnabled) {
    el.addEventListener("pointerdown", rippleShow);
    el.addEventListener("pointerup", rippleHide);
  } else if (!enabled && wasEnabled) {
    removeListeners(el);
  }
}

function removeListeners(el) {
  el.removeEventListener("pointerdown", rippleShow);
  el.removeEventListener("pointerup", rippleHide);
}

function mounted(el, binding) {
  updateRipple(el, binding, false);
}

function unmounted(el) {
  delete el._ripple;
  removeListeners(el);
}

function updated(el, binding) {
  if (binding.value === binding.oldValue) {
    return;
  }

  const wasEnabled = isRippleEnabled(binding.oldValue);
  updateRipple(el, binding, wasEnabled);
}

export const Ripple = {
  mounted,
  unmounted,
  updated
};
