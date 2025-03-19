<template>
    <div class="maincontent">
        <!-- 筛选搜索区域 -->
        <div class="top">
            <el-form ref="formRef" :inline="true" :model="form" class="searchform">
                <el-form-item label="角色名称：" prop="name">
                    <el-input v-model="form.name" placeholder="请输入角色名称" clearable class="!w-[180px]" />
                </el-form-item>
                <el-form-item label="角色标识：" prop="code">
                    <el-input v-model="form.code" placeholder="请输入角色标识" clearable class="!w-[180px]" />
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
                    style="margin-bottom: 20px; margin: 0 1%; width: 98%;" row-key="id" lazy default-expand-all
                    show-overflow-tooltip
                    :header-cell-style="{ 'background-color': 'var(--el-fill-color-light)', 'color': 'var(--el-text-color-primary)' }">
                    <el-table-column prop="name" label="角色名称" />
                    <el-table-column prop="code" label="角色标识" />
                    <el-table-column prop="remark" label="备注" />
                    <el-table-column prop="create_time" label="创建时间" />
                    <el-table-column label="操作" align="center" fixed="right" min-width="100px">
                        <template #default="{ row }">
                            <div class="ellink">
                                <el-link :underline="false" type="primary" @click="handleOnEdit(e, row)">编辑</el-link>
                                <el-link :underline="false" type="primary" @click="handleOnRole(e, row)">权限</el-link>
                                <el-link :underline="false" type="danger" @click="handleOnDel(e, row)">删除</el-link>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <!-- 新增/编辑表单 -->
        <el-dialog v-model="isDialogVisible" :title="isEditMode ? '编辑角色' : '新增角色'" :width="'40%'">
            <el-form ref="roleFormRef" :model="roleData" :rules="rules" label-width="80px" label-position="right">
                <el-form-item label="角色名称" prop="name">
                    <el-input v-model="roleData.name" maxlength="20" show-word-limit placeholder="请输入角色名称" />
                </el-form-item>
                <el-form-item label="角色标识" prop="code">
                    <el-input v-model="roleData.code" maxlength="20" show-word-limit placeholder="请输入角色标识" />
                </el-form-item>
                <el-form-item label="备注" prop="remark">
                    <el-input v-model="roleData.remark" maxlength="50" type="textarea" show-word-limit
                        placeholder="请输入备注" />
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="isDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="handleSubmit">确认</el-button>
                </div>
            </template>
        </el-dialog>
        <!-- 编辑权限抽屉组件 -->
        <el-drawer v-model="isDrawerVisible" size="20%">
            <template #header>
                <h1 style="color: black;">菜单权限</h1>
            </template>
            <template #default>
                <div class="flex flex-wrap">
                    <el-checkbox v-model="isExpandAll" label="展开/折叠" />
                    <el-checkbox v-model="isSelectAll" label="全选/全不选" />
                    <el-checkbox v-model="isLinkage" label="父子联动" />
                </div>
                <div style="margin-top: 10px;">
                    <el-tree-v2 ref="treeRef" :height="700" style="max-width: 300px" :props="props" show-checkbox
                        :check-strictly="!isLinkage" :data="menuData" />
                </div>
            </template>
            <template #footer>
                <div style="flex: auto">
                    <el-button @click="isDrawerVisible = false">取消</el-button>
                    <el-button type="primary" @click="confirmClick">确认</el-button>
                </div>
            </template>
        </el-drawer>
    </div>
</template>

<script setup>
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { ref, reactive, onMounted, nextTick, watch } from "vue";
import { getRoleList, addRole, updateRole, deleteRole } from "@/api/system/role";
import { getMenuList } from "@/api/system/menu";
import { ElMessage, ElMessageBox } from "element-plus";
import { handleTree } from "@/utils/tree";
import Search from "@iconify-icons/ri/search-line";
import Reset from "@iconify-icons/ri/refresh-line";
import Add from "@iconify-icons/ri/add-circle-line"
import { getKeyList } from "@pureadmin/utils";


defineOptions({
    name: "role"
});

// 搜索区域相关
const formRef = ref(null);
const form = reactive({
    name: "",
    code: ""
});
const loading = ref(false);

// 搜索点击事件
const onSearch = async () => {
    loading.value = true
    let res = await getRoleData()
    if (res.code = 2000) {
        loading.value = false
    }
}

// 重置点击事件
const onReset = () => {
    formRef.value.resetFields()
    getRoleData()
}

//数据展示区域
const dataList = ref([]);

const getRoleData = async () => {
    let res = await getRoleList(form)
    if (res.code == 2000) {
        dataList.value = res.data
        return res
    }
}



// 表单相关
const isDialogVisible = ref(false);
const isEditMode = ref(false);
const roleFormRef = ref(null)
const roleData = ref({
    id: '',
    name: '',
    code: '',
    remark: '',
    create_time: '',
    menus: []
})

// 校验规则
const rules = reactive({
    name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
    code: [{ required: true, message: '请输入角色标识', trigger: 'blur' }]
})
// 处理新增按钮点击事件逻辑
const handleOnAdd = async () => {
    isEditMode.value = false
    isDialogVisible.value = true
    await nextTick()
    roleFormRef.value.resetFields()
}
// 处理编辑按钮点击事件逻辑
const handleOnEdit = async (e, row) => {
    isEditMode.value = true
    isDialogVisible.value = true
    await nextTick()
    roleFormRef.value.resetFields()
    for (const k in row) {
        roleData.value[k] = row[k]
    }
}

// 处理提交事件
const handleSubmit = () => {
    roleFormRef.value.validate(async (valid) => {
        if (valid) {
            let data = roleData.value
            delete data.create_time
            try {
                let res = isEditMode.value ? await updateRole(data.id, data) : await addRole(data)
                if (res.code == 2000) {
                    isDialogVisible.value = false
                    formRef.value.resetFields()
                    await getRoleData()
                    ElMessage({
                        type: 'success',
                        message: isEditMode.value ? '编辑成功' : '新增成功'
                    })
                } else {
                    return false
                }
            } catch (error) {
                ElMessage({
                    type: 'error',
                    message: isEditMode.value ? '编辑失败！该角色标识已存在' : '新增失败！该角色标识已存在'
                })
            }
        }
    })
}

// 菜单权限相关
const isDrawerVisible = ref(false)
const isExpandAll = ref(false)
const isSelectAll = ref(false)
const isLinkage = ref(true)
const treeRef = ref(null)
const treeIds = ref([])
const menuData = ref([])
const props = {
    value: 'id',
    label: 'title',
    children: 'children'
}
// 处理点击出现抽屉组件
const handleOnRole = async (e, row) => {
    isDrawerVisible.value = true
    for (const k in row) {
        roleData.value[k] = row[k]
    }
    let res = await getMenuList('')
    if (res.code == 2000) {
        treeIds.value = getKeyList(res.data, "id");
        menuData.value = handleTree(res.data, 'id', 'parent')
    }
    await nextTick()
    isExpandAll.value = true
    isLinkage.value = false
    treeRef.value.setCheckedKeys(row.menus)
}

// 提交菜单权限配置
const confirmClick = async () => {
    roleData.value.menus = [...treeRef.value.getHalfCheckedKeys(), ...treeRef.value.getCheckedKeys()]
    let res = await updateRole(roleData.value.id, roleData.value)
    if (res.code == 2000) {
        isDrawerVisible.value = false
        await getRoleData()
        ElMessage({
            type: 'success',
            message: '赋权成功'
        })
    }
}

watch(isExpandAll, val => {
    val ? treeRef.value.setExpandedKeys(treeIds.value) : treeRef.value.setExpandedKeys([]);
});
watch(isSelectAll, val => {
    val ? treeRef.value.setCheckedKeys(treeIds.value) : treeRef.value.setCheckedKeys([]);
});


// 处理删除按钮点击事件逻辑
const handleOnDel = (e, row) => {

    ElMessageBox.confirm(
        `是否确认删除角色'${row.name}'?`,
        '提示',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(async () => {
            try {
                let res = await deleteRole(row.id)
                if (res.code == 2000) {
                    formRef.value.resetFields()
                    getRoleData()
                    ElMessage({
                        type: 'success',
                        message: '删除成功'
                    })
                }
            } catch (error) {
                ElMessage({
                    type: 'error',
                    message: '删除失败，该菜单下存在子菜单！'
                })
            }
        })
}

onMounted(() => {
    getRoleData()
});

</script>

<style lang="scss" scoped>
::v-deep(.el-drawer__header) {
    margin-bottom: 0;
}

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

    /* padding: 10px; */
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