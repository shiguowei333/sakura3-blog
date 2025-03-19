<template>
  <div class="maincontent">
    <!-- 筛选搜索区域 -->
    <div class="top">
      <el-form ref="formRef" :inline="true" :model="form" class="searchform">
        <el-form-item label="菜单名称：" prop="name">
          <el-input v-model="form.name" placeholder="请输入菜单名称" clearable class="!w-[180px]" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="useRenderIcon(Search)" :loading="loading" @click="onSearch"> 搜索 </el-button>
          <el-button :icon="useRenderIcon(Reset)" @click="onReset"> 重置 </el-button>
        </el-form-item>
      </el-form>
    </div>
    <!-- 表格数据区域 -->
    <div ref="tableContainer" class="table">
      <div class="title">
        <span style="font-size: 20px; font-weight: 700; height: 32px; line-height: 32px;">菜单管理</span>
        <el-button type="primary" :icon="useRenderIcon(Add)" @click="handleOnAdd"> 新增 </el-button>
      </div>
      <div class="inner-table">
        <el-table :data="dataList" class="el-table" height="100%" style="margin-bottom: 20px; margin: 0 1%; width: 98%;"
          row-key="id" lazy default-expand-all
          :header-cell-style="{ 'background-color': 'var(--el-fill-color-light)', 'color': 'var(--el-text-color-primary)' }">
          <el-table-column label="菜单名称" style="">
            <template #default="{ row }">
              <IconifyIconOnline style="display: inline-block; vertical-align: middle;" :icon="row.icon" />&nbsp;{{
              row.title }}
            </template>
          </el-table-column>
          <el-table-column prop="menu_type" label="菜单类型">
            <template #default="{ row }">
              <el-tag :type="menuType(row.menu_type)[0]" effect="plain">{{ menuType(row.menu_type)[1] }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="route_name" label="路由名称" />
          <el-table-column prop="route_path" label="路由路径" />
          <el-table-column prop="rank" label="排序" />
          <el-table-column label="操作" align="center" fixed="right" min-width="100px">
            <template #default="{ row }">
              <div class="ellink">
                <el-link :underline="false" type="primary" @click="handleOnAdd(e, row.id)">新增</el-link>
                <el-link :underline="false" type="primary" @click="handleOnEdit(e, row)">编辑</el-link>
                <el-link :underline="false" type="danger" @click="handleOnDel(e, row)">删除</el-link>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <!-- 新增/编辑表单 -->
    <el-dialog v-model="isDialogVisible" :title="isEditMode ? '编辑菜单' : '新增菜单'" :width="'50%'" @close="clearIcon">
      <el-form ref="menuFormRef" :model="menuData" :rules="rules" label-width="100px" label-position="right">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="菜单类型">
              <el-radio-group v-model="menuData.menu_type">
                <el-radio-button :value="0" label="菜单"></el-radio-button>
                <el-radio-button :value="1" label="iframe"></el-radio-button>
                <el-radio-button :value="2" label="外链"></el-radio-button>
                <el-radio-button :value="3" label="按钮"></el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span=12>
            <el-form-item label="上级菜单">
              <el-cascader style="width: 100%;" v-model="menuData.parent" :options="dataList"
                :props="{ value: 'id', label: 'title', children: 'children', checkStrictly: true }" clearable filterable
                :show-all-levels="false" placeholder="请选择上级菜单" />
            </el-form-item>
          </el-col>
          <el-col :span=12>
            <el-form-item label="菜单名称" prop="title">
              <el-input v-model="menuData.title" placeholder="请输入菜单名称" />
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type != 3" :span="12">
            <el-form-item label="路由名称" prop="route_name">
              <el-input v-model="menuData.route_name" placeholder="请输入路由名称" />
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type != 3" :span="12">
            <el-form-item label="路由路径" prop="route_path">
              <el-input v-model="menuData.route_path" placeholder="请输入路由路径" />
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type != 3" :span="12">
            <el-form-item label="菜单图标">
              <IconSelect ref="iconSelect" v-model="menuData.icon" class="w-full" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="菜单排序" prop="rank">
              <el-input-number style="width: 100%;" v-model="menuData.rank" :min="1" :max="999" :value-on-clear="99"
                controls-position="right" />
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type == 3" :span="12">
            <el-form-item label="权限标识" prop="code">
              <el-input v-model="menuData.code" placeholder="请输入权限标识" />
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type == 0" :span="12">
            <el-form-item label="组件路径" prop="component">
              <el-input v-model="menuData.component" placeholder="请输入组件路径" />
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type == 0" :span="24">
            <el-form-item label="路由重定向" prop="redirect">
              <el-input v-model="menuData.redirect" placeholder="请输入默认跳转地址" />
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type == 0 || menuData.menu_type == 1" :span="12">
            <el-form-item label="进场动画" prop="enterTransition">
              <ReAnimateSelector v-model="menuData.enterTransition" placeholder="请选择页面进场加载动画" />
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type == 0 || menuData.menu_type == 1" :span="12">
            <el-form-item label="离场动画" prop="leaveTransition">
              <ReAnimateSelector v-model="menuData.leaveTransition" placeholder="请选择页面离场加载动画" />
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type == 1" :span="24">
            <el-form-item label="链接地址" prop="frameSrc">
              <el-input v-model="menuData.frameSrc" maxlength="20" show-word-limit placeholder="请输入iframe链接地址" />
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type == 1" :span="12">
            <el-form-item label="加载动画">
              <el-radio-group v-model="menuData.frameLoading">
                <el-radio-button label="开启" :value="true"></el-radio-button>
                <el-radio-button label="关闭" :value="false"></el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type != 3" :span="12">
            <el-form-item label="菜单">
              <el-radio-group v-model="menuData.showLink">
                <el-radio-button label="显示" :value="true"></el-radio-button>
                <el-radio-button label="隐藏" :value="false"></el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type != 3" :span="12">
            <el-form-item label="父级菜单">
              <el-radio-group v-model="menuData.showParent">
                <el-radio-button label="显示" :value="true"></el-radio-button>
                <el-radio-button label="隐藏" :value="false"></el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type == 0 || menuData.menu_type == 1" :span="12">
            <el-form-item label="缓存页面">
              <el-radio-group v-model="menuData.keepAlive">
                <el-radio-button label="缓存" :value="true"></el-radio-button>
                <el-radio-button label="不缓存" :value="false"></el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type == 0 || menuData.menu_type == 1" :span="12">
            <el-form-item label="标签页">
              <el-radio-group v-model="menuData.hiddenTag">
                <el-radio-button label="允许" :value="false"></el-radio-button>
                <el-radio-button label="禁止" :value="true"></el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col v-if="menuData.menu_type == 0 || menuData.menu_type == 1" :span="12">
            <el-form-item label="固定标签页">
              <el-radio-group v-model="menuData.fixedTag">
                <el-radio-button label="固定" :value="true"></el-radio-button>
                <el-radio-button label="不固定" :value="false"></el-radio-button>
              </el-radio-group>
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
  </div>
</template>

<script setup>
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { ref, reactive, onMounted, nextTick } from "vue";
import { IconSelect } from "@/components/ReIcon";
import ReAnimateSelector from "@/components/ReAnimateSelector";
import { handleTree, getParentPath } from "@/utils/tree";
import { getMenuList, addMenu, updateMenu, deleteMenu } from "@/api/system/menu";
import { ElMessage, ElMessageBox } from "element-plus";
import Search from "@iconify-icons/ri/search-line";
import Reset from "@iconify-icons/ri/refresh-line";
import Add from "@iconify-icons/ri/add-circle-line"


defineOptions({
  name: "menuManager"
});

// 搜索区域相关
const formRef = ref(null);
const form = reactive({
  name: ""
});
const loading = ref(false);

// 搜索点击事件
const onSearch = async () => {
  loading.value = true
  let res = await getMenuData()
  if (res.code = 2000) {
    loading.value = false
  }
}

// 重置点击事件
const onReset = () => {
  formRef.value.resetFields()
  getMenuData()
}

//数据展示区域
const dataList = ref([]);

const getMenuData = async () => {
  let res = await getMenuList(form.name)
  if (res.code == 2000) {
    dataList.value = handleTree(res.data, 'id', 'parent')
    return res
  }
}
// 字典值转换函数
const menuType = (menu_type) => {
  switch (menu_type) {
    case 0:
      return ['primary', '菜单']
    case 1:
      return ['success', 'iframe']
    case 2:
      return ['warning', '外链']
    case 3:
      return ['danger', '按钮']
    default:
      return ['', '']
  }
}



// 表单相关
const isDialogVisible = ref(false);
const isEditMode = ref(false);
const menuFormRef = ref(null)
const menuData = ref({
  id: '',
  route_name: '',
  route_path: '',
  menu_type: 0,
  component: '',
  code: '',
  title: '',
  icon: '',
  rank: 99,
  showLink: true,
  showParent: false,
  keepAlive: false,
  frameSrc: '',
  frameLoading: true,
  hiddenTag: false,
  fixedTag: false,
  enterTransition: '',
  leaveTransition: '',
  parent: '',
  redirect: ''
})

// 校验规则
const rules = reactive({
  title: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
  route_name: [{ required: true, message: '请输入路由名称', trigger: 'blur' }],
  route_path: [{ required: true, message: '请输入路由路径', trigger: 'blur' }],
  code: [{ required: true, message: '请输入权限标识', trigger: 'blur' }]
})
// 处理新增按钮点击事件逻辑
const handleOnAdd = async (e, id) => {
  isEditMode.value = false
  isDialogVisible.value = true
  await nextTick()
  initForm()
  // 需要获取该节点和祖先节点全路径
  menuData.value.parent = getParentPath(dataList.value, id)
}
// 处理编辑按钮点击事件逻辑
const handleOnEdit = async (e, row) => {
  isEditMode.value = true
  isDialogVisible.value = true
  await nextTick()
  initForm()
  for (const k in row) {
    menuData.value[k] = row[k]
  }
  // 需要获取祖先节点全路径
  menuData.value.parent = getParentPath(dataList.value, row.parent)
}

// 处理提交事件
const handleSubmit = () => {
  menuFormRef.value.validate(async (valid) => {
    if (valid) {
      let data = menuData.value
      if (menuData.value.parent) {
        data.parent = data.parent[data.parent.length - 1]
      }
      switch (data.menu_type) {
        case 0:
          data.code = ''
          data.frameSrc = ''
          break;
        case 1:
          data.code = ''
          data.component = ''
          data.redirect = ''
          break;
        case 2:
          data.code = ''
          data.component = ''
          data.redirect = ''
          data.enterTransition = ''
          data.leaveTransition = ''
          data.frameSrc = ''
          break;
        case 3:
          data.route_name = ''
          data.route_path = ''
          data.icon = ''
          data.component = ''
          data.redirect = ''
          data.enterTransition = ''
          data.leaveTransition = ''
          data.frameSrc = ''
          break;
        default:
          break;
      }
      let res = isEditMode.value ? await updateMenu(data.id, data) : await addMenu(data)
      if (res.code == 2000) {
        isDialogVisible.value = false
        formRef.value.resetFields()
        getMenuData()
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

const initForm = () => {
  menuData.value.id = '',
    menuData.value.route_name = '',
    menuData.value.route_path = '',
    menuData.value.menu_type = 0,
    menuData.value.component = '',
    menuData.value.code = '',
    menuData.value.title = '',
    menuData.value.icon = '',
    menuData.value.rank = 99,
    menuData.value.showLink = true,
    menuData.value.showParent = false,
    menuData.value.keepAlive = false,
    menuData.value.frameSrc = '',
    menuData.value.frameLoading = true,
    menuData.value.hiddenTag = false,
    menuData.value.fixedTag = false,
    menuData.value.enterTransition = '',
    menuData.value.leaveTransition = '',
    menuData.value.parent = '',
    menuData.value.redirect = ''
}

const iconSelect = ref(null)
// 清空图标
const clearIcon = () => {
  iconSelect.value.onClear()
}

// 处理删除按钮点击事件逻辑
const handleOnDel = (e, row) => {

  ElMessageBox.confirm(
    `是否确认删除'${row.title}'?`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async () => {
      try {
        let res = await deleteMenu(row.id)
        if (res.code == 2000) {
          formRef.value.resetFields()
          getMenuData()
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
  getMenuData()
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