import { http } from "@/utils/http";


/** 登录 */
export const getLogin = (data) => {
  return http.request("post", "admin/auth/login", { data });
};

/** 刷新`token` */
export const refreshTokenApi = (data) => {
  return http.request("post", "admin/auth/token/refresh", { data });
};
