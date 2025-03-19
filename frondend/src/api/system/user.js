import { http } from '@/utils/http'

const url = '/system/user/'

export const getUserList = ({page, limit, username, telephone, is_active}) => http.get(url, {params: {page, limit, username, telephone, is_active}})

export const addUser = (data) => http.post(url, {data})

export const updateUser = (id, data) => http.put(`${url}${id}/`, {data})

export const deleteUser = (id) => http.delete(`${url}${id}/`)

export const resetPassword = (id) => http.post(`${url}reset/`, {data: {id}})