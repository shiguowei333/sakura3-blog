import { http } from "@/utils/http";

const url = 'admin/tag/'

/** 获取所有标签信息 */
export const getTags = (name = '') => {
    return http.get(url, {params: {name}});
};

/** 新增标签信息 */
export const addTag = (data) => {
    return http.post(url, {data});
};

/** 更新标签信息 */
export const updateTag = (id, data) => {
    return http.put(`${url}${id}/`, { data });
};

/** 删除标签信息 */
export const deleteTag = (id) => {
    return http.delete(`${url}${id}/`);
};
