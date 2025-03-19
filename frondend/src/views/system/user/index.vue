<template>
    <div class="maincontent">
        <!-- 筛选搜索区域 -->
        <div class="top">
            <el-form ref="formRef" :inline="true" :model="form" class="searchform">
                <el-form-item label="用户名：" prop="username">
                    <el-input v-model="form.username" placeholder="请输入用户名" clearable class="!w-[180px]" />
                </el-form-item>
                <el-form-item label="手机号：" prop="telephone">
                    <el-input v-model="form.telephone" placeholder="请输入手机号" clearable class="!w-[180px]" />
                </el-form-item>
                <el-form-item label="用户状态：" prop="is_active">
                    <el-select v-model="form.is_active" placeholder="请选择" clearable class="!w-[180px]">
                        <el-option value="1" label="已启用" />
                        <el-option value="0" label="已禁用" />
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" :icon="useRenderIcon(Search)" :loading="loading" @click="onSearch"> 搜索
                    </el-button>
                    <el-button :icon="useRenderIcon(Reset)" @click="onReset"> 重置 </el-button>
                </el-form-item>
            </el-form>
        </div>
        <!-- 表格数据区域 -->
        <div ref="tableContainer" class="table">
            <div class="title">
                <span style="font-size: 20px; font-weight: 700; height: 32px; line-height: 32px;">角色管理</span>
                <el-button type="primary" :icon="useRenderIcon(Add)" @click="handleOnAdd"> 新增 </el-button>
            </div>
            <div class="inner-table">
                <el-table :data="dataList" class="el-table" height="100%"
                    style="margin-bottom: 20px; margin: 0 1%; width: 98%;" row-key="id"
                    :header-cell-style="{ 'background-color': 'var(--el-fill-color-light)', 'color': 'var(--el-text-color-primary)' }">
                    <el-table-column prop="username" label="用户名" />
                    <el-table-column prop="name" label="用户姓名" />
                    <el-table-column prop="telephone" label="手机号码" />
                    <el-table-column prop="email" label="邮箱" />
                    <el-table-column prop="department" label="所属部门" />
                    <el-table-column prop="is_active" label="状态" width="200">
                        <template #default="{ row }">
                            <el-switch @change="changeStatus(e, row)" v-model="row.is_active" active-text="启用"
                                inactive-text="禁用" inline-prompt size="large"
                                style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" />
                        </template>
                    </el-table-column>
                    <el-table-column prop="create_time" label="创建时间" />
                    <el-table-column label="操作" align="center" fixed="right" min-width="100px">
                        <template #default="{ row }">
                            <div class="ellink">
                                <el-link :underline="false" type="primary" @click="handleOnEdit(e, row)">编辑</el-link>
                                <el-link :underline="false" type="danger" @click="handleOnDel(e, row)">删除</el-link>
                                <el-link :underline="false" type="primary" @click="resetPwd(e, row.id)">重置密码</el-link>
                                <el-link :underline="false" type="primary" @click="handleOnRole(e, row)">分配角色</el-link>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <!-- 新增/编辑表单 -->
        <el-dialog v-model="isDialogVisible" :title="isEditMode ? '编辑用户' : '新增用户'" :width="'40%'">
            <el-form ref="userFormRef" :model="userData" :rules="rules" label-width="80px" label-position="right">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="用户名" prop="username">
                            <el-input v-model="userData.username" maxlength="20" show-word-limit placeholder="请输入用户名" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="用户姓名" prop="name">
                            <el-input v-model="userData.name" maxlength="20" show-word-limit placeholder="请输入用户姓名" />
                        </el-form-item>
                    </el-col>
                    <el-col v-if="!isEditMode" :span="12">
                        <el-form-item label="密码" prop="password">
                            <el-input type="password" v-model="userData.password" placeholder="请输入密码" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="手机号" prop="telephone">
                            <el-input v-model="userData.telephone" maxlength="11" show-word-limit
                                placeholder="请输入手机号" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="邮箱" prop="email">
                            <el-input v-model="userData.email" maxlength="20" show-word-limit placeholder="请输入邮箱地址" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="所属部门" prop="department">
                            <el-cascader v-model="userData.department" :options="deptList" :width="100"
                                :props="{ value: 'id', label: 'name', children: 'children', checkStrictly: true }"
                                clearable filterable :show-all-levels="false" placeholder="请选择所属部门" />
                        </el-form-item>
                    </el-col>
                    <el-col v-if="!isEditMode" :span="12">
                        <el-form-item label="用户状态" prop="is_active">
                            <el-switch v-model="userData.is_active" active-text="启用" inactive-text="禁用" inline-prompt
                                style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" />
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="isDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="handleSubmit">确认</el-button>
                </div>
            </template>
        </el-dialog>
        <!-- 分配用户角色表单 -->
        <el-dialog v-model="isRoleVisible" title='角色分配' :width="'20%'">
            <el-form ref="roleFormRef" :model="userData" label-width="60px" label-position="right">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="userData.username" disabled placeholder="请输入用户名" />
                </el-form-item>
                <el-form-item label="角色" prop="roles">
                    <el-select v-model="userData.roles" multiple placeholder="请先配置用户角色" style="width: 240px">
                        <el-option v-for="item in roleList" :key="item.id" :label="item.name" :value="item.id" />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="isRoleVisible = false">取消</el-button>
                    <el-button type="primary" @click="submitRole">确认</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { ref, reactive, onMounted, nextTick } from "vue";
import { handleTree, getParentPath } from "@/utils/tree";
import { getUserList, addUser, updateUser, deleteUser, resetPassword } from "@/api/system/user";
import { getDepartmentList } from "@/api/system/department";
import { ElMessage, ElMessageBox } from "element-plus";
import Search from "@iconify-icons/ri/search-line";
import Reset from "@iconify-icons/ri/refresh-line";
import Add from "@iconify-icons/ri/add-circle-line"
import { getRoleList } from "@/api/system/role";


defineOptions({
    name: "user"
});

// 查询参数相关
const formRef = ref(null);
const form = reactive({
    username: "",
    telephone: "",
    is_active: '',
    page: 1,
    limit: 10
});
const loading = ref(false);

// 搜索点击事件
const onSearch = async () => {
    loading.value = true
    let res = await getUserData()
    if (res.code = 2000) {
        loading.value = false
    }
}

// 重置点击事件
const onReset = () => {
    formRef.value.resetFields()
    getUserData()
}

//数据展示区域
const dataList = ref([]);

const getUserData = async () => {
    let res = await getUserList(form)
    if (res.code == 2000) {
        dataList.value = res.data.records
        return res
    }
}


// 变更用户状态
const changeStatus = async (e, row) => {
    let res = await updateUser(row.id, row)
    if (res.code == 2000) {
        if (row.is_active) {
            ElMessage({
                type: 'success',
                message: '启用成功'
            })
        } else {
            ElMessage({
                type: 'success',
                message: '禁用成功'
            })
        }
    }
}

const resetPwd = async (e, id) => {
    let res = await resetPassword(id)
    if (res.code == 2000) {
        ElMessage({
            type: 'success',
            message: res.message
        })
    }
}

// 表单相关
const isDialogVisible = ref(false);
const isEditMode = ref(false);
const userFormRef = ref()
const userData = ref({
    id: '',
    username: '',
    name: '',
    password: '',
    telephone: '',
    email: '',
    department: '',
    is_active: true,
    roles: []
})
const deptList = ref([])
// 校验规则
const rules = reactive({
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    name: [{ required: true, message: '请输入用户姓名', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
    telephone: [{ required: true, message: '请输入密码', trigger: 'blur' }]
})
// 处理新增按钮点击事件逻辑
const handleOnAdd = async (e, id) => {
    isEditMode.value = false
    isDialogVisible.value = true
    let res = await getDepartmentList()
    deptList.value = handleTree(res.data, 'id', 'parent')
    await nextTick()
    userFormRef.value.resetFields()
}
// 处理编辑按钮点击事件逻辑
const handleOnEdit = async (e, row) => {
    isEditMode.value = true
    isDialogVisible.value = true
    let res = await getDepartmentList()
    deptList.value = handleTree(res.data, 'id', 'parent')
    await nextTick()
    userFormRef.value.resetFields()
    userData.value.id = row.id
    userData.value.username = row.username
    userData.value.name = row.name
    userData.value.telephone = row.telephone
    userData.value.email = row.email
    userData.value.is_active = row.is_active
    userData.value.roles = row.roles
    userData.value.department = getParentPath(deptList.value, row.department)
}


// 处理提交事件
const handleSubmit = () => {
    userFormRef.value.validate(async (valid) => {
        if (valid) {
            if (userData.value.department) {
                userData.value.department = userData.value.department[userData.value.department.length - 1]
            }
            let res = isEditMode.value ? await updateUser(userData.value.id, userData.value) : await addUser(userData.value)
            if (res.code == 2000) {
                isDialogVisible.value = false
                formRef.value.resetFields()
                getUserData()
                ElMessage({
                    type: 'success',
                    message: isEditMode.value ? '编辑成功' : '新增成功'
                })
            } else {
                return false
            }
        }
    })
}

// 删除用户相关
const delUserId = ref('')
const delUserName = ref('')

// 处理删除按钮点击事件逻辑
const handleOnDel = (e, row) => {
    delUserId.value = row.id
    delUserName.value = row.name
    ElMessageBox.confirm(
        `是否确认删除用户'${row.name}'?`,
        '提示',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    ).then(async () => {
        try {
            let res = await deleteUser(delUserId.value)
            if (res.code == 2000) {
                formRef.value.resetFields()
                getUserData()
                ElMessage({
                    type: 'success',
                    message: '删除成功'
                })
            }
        } catch (error) {
            ElMessage({
                type: 'error',
                message: '删除失败'
            })
        }
    })
}

// 分配角色相关
const isRoleVisible = ref(false)
const roleList = ref([])
const handleOnRole = async (e, row) => {
    isRoleVisible.value = true
    userData.value = row
    let res = await getRoleList('')
    roleList.value = res.data
}
// 处理提交分配角色表单
const submitRole = async () => {
    let res = await updateUser(userData.value.id, userData.value)
    if (res.code == 2000) {
        isRoleVisible.value = false
        getUserData()
        ElMessage({
            type: 'success',
            message: '赋权成功'
        })
    } else {
        return false
    }
}

onMounted(() => {
    getUserData()
});

</script>

<style lang="scss" scoped>
::v-deep(.el-table .cell) {
    overflow: hidden; // 溢出隐藏
    text-overflow: ellipsis; // 溢出用省略号显示
    white-space: nowrap; // 规定段落中的文本不进行换行
}

.main-content {
    margin: 24px 24px 0 !important;
}

.maincontent {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 141px);
}

.searchform {
    background-color: var(--el-bg-color);

    .el-form-item {
        margin: 15px 20px;
    }
}

.title {
    margin: 10px;
    padding: 10px;
    display: flex;
    justify-content: space-between;
}

.table {
    display: flex;
    flex-direction: column;
    flex: 1;
    margin-top: 10px;
    background-color: var(--el-bg-color);

    /* 解决element表格在flex布局下无法自适应窗口宽度缩小的问题 */
    .inner-table {
        flex: 1;
        position: relative;

        .el-table {
            position: absolute;
        }
    }
}

.ellink {
    display: flex;
    gap: 10px;
    justify-content: center;
}

.dialog-footer {
    text-align: right;
}
</style>