import { http } from "@/utils/http";

const url = 'admin/category/'

/** 获取所有分类信息 */
export const getCategorys = (name) => {
    return http.get(url, {params: {name}});
};

/** 新增分类信息 */
export const addCategory = (data) => {
    return http.post(url, {data});
};

/** 更新分类信息 */
export const updateCategory = (id, data) => {
    return http.put(`${url}${id}/`, { data });
};

/** 删除分类信息 */
export const deleteCategory = (id) => {
    return http.delete(`${url}${id}/`);
};
