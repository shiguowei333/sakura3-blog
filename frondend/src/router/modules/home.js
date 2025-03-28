const { VITE_HIDE_HOME } = import.meta.env;
const Layout = () => import("@/layout/index.vue");

export default [
  {
    path: "/",
    name: "Home",
    component: Layout,
    redirect: "/welcome",
    meta: {
      icon: "ep:home-filled",
      title: "首页",
      rank: 0
    },
    children: [
      {
        path: "/welcome",
        name: "Welcome",
        component: () => import("@/views/welcome/index.vue"),
        meta: {
          title: "首页",
          showLink: VITE_HIDE_HOME === "true" ? false : true
        }
      }
    ]
  },
  {
    path: "/info",
    name: "info",
    component: () => import("@/views/admin/info/index.vue"),
    meta: {
      icon: "ep:home-filled",
      title: "基础信息",
      showLink: true
    }
  },
  {
    path: "/tag",
    name: "tag",
    component: () => import("@/views/admin/tag/index.vue"),
    meta: {
      icon: "ep:home-filled",
      title: "标签管理",
      showLink: true
    }
  },
  {
    path: "/category",
    name: "category",
    component: () => import("@/views/admin/category/index.vue"),
    meta: {
      icon: "ep:home-filled",
      title: "分类管理",
      showLink: true
    }
  },
];
