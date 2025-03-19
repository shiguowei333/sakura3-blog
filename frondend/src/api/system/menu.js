import { http } from '@/utils/http'

const url = '/system/menu/'

export const getMenuList = (name) => http.get(url, {params: {name}} )

export const addMenu = (data) => http.post(url, {data})

export const updateMenu = (id, data) => http.put(`${url}${id}/`, {data})

export const deleteMenu = (id) => http.delete(`${url}${id}/`)