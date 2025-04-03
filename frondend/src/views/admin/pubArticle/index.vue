<template>
    <div class="maincontent">
        <div class="markdown">
            <!-- markdown编辑器区域 -->
            <MdEditor v-model="article.article_content" style="height: 100%;" />
        </div>
        <div class="right">
            <el-form ref="articleFormRef" :model="article" :rules="articleRules" label-width="70px"
                label-position="right">
                <el-form-item label="标题：" prop="article_title">
                    <el-input v-model="article.article_title" maxlength="100" placeholder="请输入文章标题" />
                </el-form-item>
                <el-form-item label="分类：" prop="category">
                    <el-select v-model="article.category" placeholder="请选择分类" clearable>
                        <el-option v-for="category in categoryList" :label="category.category_name"
                            :value="category.id" />
                    </el-select>
                </el-form-item>
                <el-form-item label="标签：" prop="tag_ids">
                    <el-select v-model="article.tag_ids" multiple placeholder="请选择标签">
                        <el-option v-for="tag in tagList" :key="tag.id" :label="tag.tag_name" :value="tag.id" />
                    </el-select>
                </el-form-item>
            </el-form>
            <div class="handlerbutton">
                <div>
                    <el-button type="warning" @click="save">暂存</el-button>
                    <el-button type="success" @click="publish">发布</el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>

defineOptions({
    name: 'PubArticle'
})

import { ref } from 'vue'
import { onMounted } from 'vue';
import { genFileId, ElMessage } from 'element-plus'
import { getCategorys } from '@/api/admin/category'
import { getTags } from '@/api/admin/tag'
import { MdEditor } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import { addArticle, getArticle, updateArticle } from '@/api/admin/article';
import { useRoute } from 'vue-router'

const $route = useRoute()

const articleFormRef = ref(null)
const article_id = ref('')
const article = ref({
    article_title: '',
    article_content: '',
    category: '',
    tag_ids: []
})
const categoryList = ref([])
const tagList = ref([])
const articleRules = ref({
    article_title: [{ required: true, message: '请输入文章标题', trigger: 'blur' }],
    category: [{ required: true, message: '请选择文章标题', trigger: 'change' }]
})

const save = () => {
    ElMessage({
        type: 'info',
        message: '该功能暂时无法使用'
    })
}

const publish = async() => {
    await articleFormRef.value.validate(async(valid) => {
        if(valid) {
            if(article.value.article_content == '') {
                ElMessage({
                    type: 'warning',
                    message: '博客内容为空'
                })
                return
            }
            let res = article_id.value? await updateArticle(article_id.value, article.value): await addArticle(article.value)
            if(res.code == 2000) {
                ElMessage({
                    type: 'success',
                    message: '发布成功'
                })
            }
        }
    })
}

onMounted(async () => {
    let categoryRes = await getCategorys()
    if (categoryRes.code == 2000) {
        categoryList.value = categoryRes.data.records
    }
    let tagRes = await getTags()
    if (tagRes.code == 2000) {
        tagList.value = tagRes.data.records
    }
    if($route.query.id) {
        let res = await getArticle($route.query.id)
        if(res.code == 2000) {
            article_id.value = res.data.id
            article.value.article_title = res.data.article_title
            article.value.article_content = res.data.article_content
            article.value.category = res.data.category
            article.value.tag_ids = res.data.tags.map((tag) => tag.id)
        }
    }
})
</script>

<style lang='scss' scoped>
.maincontent {
    display: flex;
    height: calc(100vh - 160px);
    background-color: var(--el-bg-color);
    padding: 20px;
    overflow: auto;

    .markdown {
        flex: 1;
        margin-right: 10px;
    }

    .right {
        width: 20%;
        padding-top: 10px;
    }

    .handlerbutton {
        display: flex;
        justify-content: center;
    }
}
</style>
