// 改成纯静态路由菜单这个接口没什么用了，但是很多地方导入了这里，删了之后很多地方都要重新修改，就先留着了
import { http } from "@/utils/http";


export const getAsyncRoutes = () => {
  return http.request("get", "auth/asyncroutes");
};
