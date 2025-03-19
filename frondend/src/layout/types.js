const { VITE_HIDE_HOME } = import.meta.env;

export const routerArrays =
  VITE_HIDE_HOME === "false"
    ? [
        {
          path: "/welcome",
          meta: {
            title: "首页",
            icon: "ep:home-filled"
          }
        }
      ]
    : [];


