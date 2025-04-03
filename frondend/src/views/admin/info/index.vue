<template>
    <div class="maincontent">
        <div class="type_select">
            <Segmented v-model="infoType" :options="infoTypeOptions" />
        </div>
        <div class="info">
            <!-- 站长信息表单 -->
            <el-form v-if="infoType == 0" ref="userInfoRef" :model="userInfo" :rules="userRules" label-width="120px"
                label-position="right">
                <el-form-item prop="avatar">
                    <el-upload class="avatar-uploader" :data="getFileData"
                        action="http://127.0.0.1:8000/api/admin/info/web/upload" :show-file-list="false"
                        :headers="headers" :on-success="handleAvatarSuccess" :before-upload="beforeUpload">
                        <img v-if="userInfo.avatar" :src="userInfo.avatar" class="avatar" />
                        <el-icon v-else class="avatar-uploader-icon">
                            <IconifyIconOffline :icon="Plus" />
                        </el-icon>
                    </el-upload>
                </el-form-item>
                <el-form-item label="昵称：" prop="nick_name">
                    <el-input v-model="userInfo.nick_name" maxlength="100" placeholder="请输入昵称" />
                </el-form-item>
                <el-form-item label="文案：" prop="title">
                    <el-input v-model="userInfo.title" maxlength="100" placeholder="请输入文案" />
                </el-form-item>
                <el-form-item label="背景：" prop="bg_img">
                    <div style="width: 100%;">
                        <el-upload ref="upload" v-model:file-list="userInfo.bg_img" list-type="picture" :headers="headers" :on-success="handleBgSuccess"
                            :before-upload="beforeUpload" :limit="1" :on-exceed="handleExceed" :data="getFileData" :on-remove="handleRemoveBg"
                            action="http://127.0.0.1:8000/api/admin/info/web/upload">
                            <div style="display: flex;">
                                <el-button :icon="useRenderIcon(Upload)">上传背景图</el-button>
                            </div>
                        </el-upload>
                    </div>
                </el-form-item>
                <el-divider content-position="center">网站链接</el-divider>
                <el-form-item label="Github：" prop="github_url">
                    <el-input v-model="userInfo.github_url" maxlength="100" placeholder="请输入github地址" />
                </el-form-item>
            </el-form>
            <!-- 网站信息表单 -->
            <el-form v-if="infoType == 1" ref="webInfoRef" :model="webInfo" :rules="webRules" label-width="120px"
                label-position="right">
                <el-form-item label="网站名称：" prop="web_name">
                    <el-input v-model="webInfo.web_name" maxlength="100" placeholder="请输入网站名称" />
                </el-form-item>
                <el-form-item label="头部通知：" prop="header_inform">
                    <el-input v-model="webInfo.header_inform" maxlength="100" placeholder="请输入头部通知" />
                </el-form-item>
                <el-form-item label="侧边栏公告：" prop="aside_inform">
                    <el-input v-model="webInfo.aside_inform" type="textarea" maxlength="500" :rows="3"
                        show-word-limit placeholder="请输入侧边栏公告" />
                </el-form-item>
                <el-divider content-position="center">网站信息</el-divider>
                <el-form-item label="备案信息：" prop="archival_inform">
                    <el-input v-model="webInfo.archival_inform" maxlength="100" placeholder="请输入备案信息" />
                </el-form-item>
                <el-form-item label="运行时间：" prop="web_time">
                    <el-date-picker v-model="webInfo.web_time" type="datetime" placeholder="运行时间" value-format="YYYY-MM-DD HH:mm:ss" />
                </el-form-item>
                <el-divider content-position="center">首页轮播图</el-divider>
                <el-form-item>
                    <div style="margin: 0 auto;" class="slideshow">
                        <el-upload v-model:file-list="slideshowList" :headers="headers"
                            :before-upload="beforeUpload" :data="getFileData" :class="{ 'hideUploadBtn': slideshowList.length >= 6 }"
                            action="http://127.0.0.1:8000/api/admin/info/web/upload" list-type="picture-card" :limit="6"
                            :on-preview="handlePictureCardPreview">
                            <el-icon>
                                <IconifyIconOffline :icon="Plus" />
                            </el-icon>
                        </el-upload>

                        <el-dialog v-model="dialogVisible">
                            <img w-full :src="dialogImageUrl" alt="预览图片" />
                        </el-dialog>
                    </div>
                </el-form-item>
            </el-form>
            <div class="footer_button">
                <el-button type="primary" @click="handleSubmit">保存</el-button>
                <el-button @click="resetInfo">重置</el-button>
            </div>
        </div>
    </div>
</template>

<script setup>

defineOptions({
    name: 'Info'
})

import { ref } from 'vue'
import Segmented from "@/components/ReSegmented";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { getToken } from "@/utils/auth";
import Plus from '@iconify-icons/ep/plus'
import Upload from '@iconify-icons/ep/upload'
import { onMounted } from 'vue';
import { genFileId, ElMessage } from 'element-plus'
import { getUserInfo, updateUserInfo, getWebInfo, updateWebInfo} from '@/api/admin/info'


const infoType = ref(0)
const infoTypeOptions = [
    { label: '站长信息', value: 0 },
    { label: '网站信息', value: 1 }
]
// 上传图片请求头
const headers = {
    'Authorization': `Bearer ${getToken().accessToken}`,
}

const getFileData = (file) => {
    return { file_name: file.name }
}

const beforeUpload = (file) => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/webp'
    if (!isJpgOrPng)
        message.error('文件格式必须是jpg或png或webp')

    const isLt5M = file.size / 1024 / 1024 < 5
    if (!isLt5M)
        message.error('图片必须小于 5MB')

    return isJpgOrPng && isLt5M
}

// 个人信息部分
const userRules = ref([])
const userInfoRef = ref(null)
const userInfo = ref({
    nick_name: '',
    avatar: '',
    title: '',
    bg_img: [],
    github_url: ''
})

const upload = ref(null)
const handleExceed = (files) => {
    upload.value.clearFiles()
    const file = files[0]
    file.uid = genFileId()
    upload.value.handleStart(file)
}

const handleAvatarSuccess = (res) => {
  userInfo.value.avatar = res.data.file_path
}

const handleBgSuccess = (res) => {
  userInfo.value.bg_img = [{
    name: res.data.file_name,
    url: res.data.file_path
  }]
}

const handleRemoveBg = () => {
  userInfo.value.bg_img = []
}


// 网站信息部分
const webRules = ref([])
const webInfoRef = ref(null)
const webInfo = ref({
    web_name: '',
    header_inform: '',
    aside_inform: '',
    web_time: '',
    slideshow: [],
    archival_inform: ''
})
const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const slideshowList = ref([])

const handlePictureCardPreview = (uploadFile) => {
    dialogImageUrl.value = uploadFile.url
    dialogVisible.value = true
}



const handleSubmit = async() => {
  if(infoType.value) {
    webInfo.value.slideshow = slideshowList.value.map(element => {
      if(element.response) {
        return element.response.data.url
      }
      return element.url
    })
  }
  let data = infoType.value?webInfo.value:userInfo.value
  let res = infoType.value?await updateWebInfo(data):await updateUserInfo(data)
  if(res.code == 2000) {
    ElMessage({
      type: 'success',
      message: '修改成功'
    })
    infoType.value?getWeb():getUser()
  }
}

const resetInfo = async() => {
  infoType.value?getWeb():getUser()
}

const getUser = async() => {
  let userRes = await getUserInfo()
  userInfo.value = userRes.data
}

const getWeb = async() => {
  let webRes = await getWebInfo()
  webInfo.value = webRes.data
  slideshowList.value = webInfo.value.slideshow.map(element => {
    return {
      url: element
    }
  })
}

onMounted(async() => {
    getUser()
    getWeb()
})
</script>

<style lang='scss' scoped>
.maincontent {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 160px);
    background-color: var(--el-bg-color);
    padding: 20px;
    overflow: auto;

    .info {
        margin: 50px auto 0 auto;
        width: 50%;

        .footer_button {
            display: flex;
            justify-content: center;
        }
    }
}

::v-deep(.bg_img) {
    width: 100%;
}

::v-deep(.avatar-uploader) {
    margin: 0 auto;
}

::v-deep(.avatar-uploader .avatar) {
    width: 100px;
    height: 100px;
    display: block;
}

::v-deep(.avatar-uploader .el-upload) {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

::v-deep(.avatar-uploader .el-upload:hover) {
    border-color: var(--el-color-primary);
}

::v-deep(.el-icon.avatar-uploader-icon) {
    font-size: 28px;
    color: #8c939d;
    width: 100px;
    height: 100px;
    text-align: center;
}

::v-deep(.el-form-item__content) {
    margin-left: 0 !important;
}

::v-deep(.slideshow .el-upload-list__item), ::v-deep(.el-upload--picture-card) {
    width: 120px;
    height: 120px;
}

::v-deep(.hideUploadBtn .el-upload--picture-card) {
  display: none;
}
</style>
