<template>
    <div class="maincontent">
        <!-- 筛选搜索区域 -->
        <div class="top">
            <el-form ref="searchFormRef" :inline="true" :model="searchForm" class="searchform">
                <el-form-item label="标签名称：" prop="name">
                    <el-input v-model="searchForm.name" placeholder="请输入标签名称" clearable class="!w-[180px]" />
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
                <span style="font-size: 20px; font-weight: 700; height: 32px; line-height: 32px;">标签管理</span>
                <el-button type="primary" :icon="useRenderIcon(Add)" @click="handleOnAdd"> 新增 </el-button>
            </div>
            <div class="inner-table">
                <el-table :data="dataList" class="el-table" height="100%"
                    style="margin-bottom: 20px; margin: 0 1%; width: 98%;" row-key="id" lazy default-expand-all
                    :cell-style="{ 'text-align': 'center' }"
                    :header-cell-style="{ 'background-color': 'var(--el-fill-color-light)', 'text-align': 'center', 'color': 'var(--el-text-color-primary)' }">
                    <el-table-column prop="tag_name" label="标签名称" />
                    <el-table-column prop="amount" label="文章数量" />
                    <el-table-column prop="create_time" label="创建时间" />
                    <el-table-column prop="update_time" label="更新时间" />
                    <el-table-column label="操作" align="center" fixed="right" min-width="100px">
                        <template #default="{ row }">
                            <div class="ellink">
                                <el-link :underline="false" type="primary" @click="handleOnEdit(e, row)">编辑</el-link>
                                <el-link :underline="false" type="danger" @click="handleOnDel(e, row)">删除</el-link>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <!-- 新增/编辑表单 -->
        <el-dialog v-model="isDialogVisible" :title="isEditMode ? '编辑标签' : '新增标签'" :width="'20%'"
            @close="handleCloseDialog">
            <el-form ref="tagFormRef" :model="tagData" :rules="rules" label-width="80px" label-position="right">
                <el-form-item label="标签名称" prop="tag_name">
                    <el-input v-model="tagData.tag_name" maxlength="20" show-word-limit placeholder="请输入标签名称" />
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="isDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="handleSubmit">确认</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { ref, reactive, onMounted } from "vue";
import { getTags, addTag, updateTag, deleteTag } from "@/api/admin/tag";
import { ElMessage, ElMessageBox } from "element-plus";
import Search from "@iconify-icons/ri/search-line";
import Reset from "@iconify-icons/ri/refresh-line";
import Add from "@iconify-icons/ri/add-circle-line"


defineOptions({
    name: "tag"
});

// 搜索区域相关
const searchFormRef = ref(null);
const searchForm = reactive({
    name: ""
});
const loading = ref(false);

// 搜索点击事件
const onSearch = async () => {
    loading.value = true
    await getTagData()
    loading.value = false
}

// 重置点击事件
const onReset = () => {
    searchFormRef.value.resetFields()
    getTagData()
}

//数据展示区域
const dataList = ref([]);

const getTagData = async () => {
    let res = await getTags(searchForm.name)
    if (res.code == 2000) {
        dataList.value = res.data.records
    }
}



// 表单相关
const isDialogVisible = ref(false);
const isEditMode = ref(false);
const tagFormRef = ref(null)
const tagData = ref({
    id: '',
    tag_name: ''
})
// 校验规则
const rules = reactive({
    tag_name: [{ required: true, message: '请输入部门名称', trigger: 'blur' }]
})
// 处理新增按钮点击事件逻辑
const handleOnAdd = async () => {
    isDialogVisible.value = true
    isEditMode.value = false
}
// 处理编辑按钮点击事件逻辑
const handleOnEdit = async (e, row) => {
    isDialogVisible.value = true
    isEditMode.value = true
    tagData.value.id = row.id
    tagData.value.tag_name = row.tag_name
}
// 处理关闭dialog页面清空表单数据
const handleCloseDialog = () => {
    tagData.value.id = ""
    tagData.value.tag_name = ""
}


// 处理提交事件
const handleSubmit = () => {
    tagFormRef.value.validate(async (valid) => {
        if (valid) {
            let res = isEditMode.value ? await updateTag(tagData.value.id, tagData.value) : await addTag(tagData.value)
            if (res.success) {
                isDialogVisible.value = false
                getTagData()
                ElMessage({
                    type: 'success',
                    message: isEditMode.value ? '编辑成功' : '新增成功'
                })
            } else {
                ElMessage({
                    type: 'error',
                    message: res.message
                })
            }
        }
    })
}

// 删除标签相关
const delId = ref('')
const delName = ref('')

// 处理删除按钮点击事件逻辑
const handleOnDel = (e, row) => {
    delId.value = row.id
    delName.value = row.tag_name
    ElMessageBox.confirm(
        `是否确认删除'${delName.value}'?`,
        '提示',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(async () => {

            let res = await deleteTag(delId.value)
            if (res.success) {
                getTagData()
                ElMessage({
                    type: 'success',
                    message: '删除成功'
                })

            } else {
                ElMessage({
                    type: 'error',
                    message: res.message
                })
            }
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '取消删除',
            })
        })
}


onMounted(() => {
    getTagData()
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