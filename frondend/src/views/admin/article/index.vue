<template>
    <div class="maincontent">
        <!-- 筛选搜索区域 -->
        <div class="top">
            <el-form ref="searchFormRef" :inline="true" :model="searchForm" class="searchform">
                <el-form-item label="文章标题：" prop="title">
                    <el-input v-model="searchForm.title" placeholder="请输入文章标题" clearable class="!w-[180px]" />
                </el-form-item>
                <el-form-item label="文章分类：" prop="category">
                    <el-select v-model="searchForm.category" placeholder="请选择分类" class="!w-[150px]" clearable>
                        <el-option v-for="category in categoryList" :label="category.category_name"
                            :value="category.id" />
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
                <span style="font-size: 20px; font-weight: 700; height: 32px; line-height: 32px;">文章管理</span>
                <el-button type="primary" :icon="useRenderIcon(Add)" @click="$router.push({name: 'pubarticle'})"> 发布新文章 </el-button>
            </div>
            <div class="inner-table">
                <el-table :data="dataList" class="el-table" height="100%"
                    style="margin-bottom: 20px; margin: 0 1%; width: 98%;" row-key="id" lazy default-expand-all
                    :cell-style="{ 'text-align': 'center' }"
                    :header-cell-style="{ 'background-color': 'var(--el-fill-color-light)', 'text-align': 'center', 'color': 'var(--el-text-color-primary)' }">
                    <el-table-column prop="article_title" label="文章标题" />
                    <el-table-column prop="category_name" label="文章分类" />
                    <el-table-column prop="create_time" label="标签" >
                        <template #default="{ row }">
                            <el-tag v-for="tag in row.tags" type="primary" style="margin-right: 5px;">{{ tag.tag_name }}</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="user" label="作者" />
                    <el-table-column prop="create_time" label="发布时间" />
                    <el-table-column label="操作" align="center" fixed="right" min-width="100px">
                        <template #default="{ row }">
                            <div class="ellink">
                                <el-link :underline="false" type="primary" @click="$router.push({name: 'pubarticle', query: {id: row.id}})">编辑</el-link>
                                <el-link :underline="false" type="danger" @click="handleOnDel(e, row)">删除</el-link>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="pagenation">
                <el-pagination v-model:current-page="searchForm.page" v-model:page-size="searchForm.limit" :total="total" background layout="->, total, prev, pager, next, sizes" :page-sizes="[10, 20, 50, 100]" @change="getArticleData" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { ref, reactive, onMounted } from "vue";
import { getArticles, deleteArticle } from "@/api/admin/article";
import { getCategorys } from "@/api/admin/category";
import { ElMessage, ElMessageBox } from "element-plus";
import Search from "@iconify-icons/ri/search-line";
import Reset from "@iconify-icons/ri/refresh-line";
import Add from "@iconify-icons/ri/add-circle-line";
import { useRouter } from 'vue-router'


defineOptions({
    name: "ArticleList"
});

const $router = useRouter()

// 搜索区域相关
const searchFormRef = ref(null);
const searchForm = reactive({
    title: "",
    category: "",
    page: 1,
    limit: 10
});
const total = ref(0)
const page = ref(10)
const loading = ref(false);
const categoryList = ref([])

// 搜索点击事件
const onSearch = async () => {
    loading.value = true
    searchForm.page = 1
    await getArticleData()
    loading.value = false
}

// 重置点击事件
const onReset = () => {
    searchFormRef.value.resetFields()
    getArticleData()
}

// //数据展示区域
const dataList = ref([]);

const getArticleData = async () => {
    let res = await getArticles(searchForm)
    if (res.code == 2000) {
        dataList.value = res.data.records
        total.value = res.data.total
    }
    let categoryRes = await getCategorys()
    if (categoryRes.code == 2000) {
        categoryList.value = categoryRes.data.records
    }
}


// 删除文章相关
const delId = ref('')
const delName = ref('')

// 处理删除按钮点击事件逻辑
const handleOnDel = (e, row) => {
    delId.value = row.id
    delName.value = row.article_title
    ElMessageBox.confirm(
        '是否确认删除?',
        '提示',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(async () => {

            let res = await deleteArticle(delId.value)
            if (res.success) {
                getArticleData()
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
}


onMounted(() => {
    getArticleData()
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

.pagenation {
    margin: 10px 0;
    margin-right: 15px;
}
</style>