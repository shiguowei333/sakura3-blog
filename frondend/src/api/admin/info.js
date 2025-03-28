import { http } from "@/utils/http";

const url = 'admin/info/'

/** 获取站长信息 */
export const getUserInfo = () => {
    return http.get(url + 'user');
};

/** 更新站长信息 */
export const updateUserInfo = (data) => {
    return http.post(url + 'user', { data });
};

/** 获取网站信息 */
export const getWebInfo = () => {
    return http.get(url + 'web');
};

/** 更新网站信息 */
export const updateWebInfo = (data) => {
    return http.post(url + 'web', { data });
};
