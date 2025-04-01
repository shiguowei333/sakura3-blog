import { http } from "@/utils/http";

const url = 'admin/article/'

/** 获取所有文章信息 */
export const getArticles = (data) => {
    return http.get(url, {params: data});
};

/** 获取文章详细信息 */
export const getArticle = (id) => {
    return http.get(`${url}${id}/`);
};

/** 新增分类信息 */
export const addArticle = (data) => {
    return http.post(url, {data});
};

/** 更新分类信息 */
export const updateArticle = (id, data) => {
    return http.put(`${url}${id}/`, { data });
};

/** 删除分类信息 */
export const deleteArticle = (id) => {
    return http.delete(`${url}${id}/`);
};