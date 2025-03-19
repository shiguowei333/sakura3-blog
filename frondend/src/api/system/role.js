import { http } from '@/utils/http'

const url = '/system/role/'

export const getRoleList = ({name, code}) => http.get(url, {params: {name, code}})

export const addRole = (data) => http.post(url, {data})

export const updateRole = (id, data) => http.put(`${url}${id}/`, {data})

export const deleteRole = (id) => http.delete(`${url}${id}/`)