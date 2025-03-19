import { http } from '@/utils/http'

const url = '/system/department/'

export const getDepartmentList = (name) => http.get(url, {params: {name}} )

export const addDepartment = (data) => http.post(url, {data})

export const updateDepartment = (id, data) => http.put(`${url}${id}/`, {data})

export const deleteDepartment = (id) => http.delete(`${url}${id}/`)