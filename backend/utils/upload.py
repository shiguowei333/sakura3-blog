import json

from rest_framework.views import APIView
from django.conf import settings
from utils.response import DetailResponse, FailureResponse
from qiniu import Auth, put_data
import uuid


def upload_file(file_name, file_path, file_data):
    # 构建鉴权对象
    q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    # 上传空间
    bucket_name = settings.QINIU_BUCKET_NAME
    key = f'{file_path}{str(uuid.uuid4())}.{file_name.split('.')[-1]}'
    token = q.upload_token(bucket_name, key, 3600)
    res = put_data(token, key, file_data)
    return res[1]

class SlideUploadView(APIView):
    def post(self, request, *args, **kwargs):
        res = upload_file(request.data['file_name'],'web_img/',request.data['file'])
        if res.status_code == 200:
            file_info = json.loads(res.text_body)
            data = {
                'req_id': res.req_id,
                'file_name': file_info['key'].split('/')[-1],
                'file_path': file_info['key'],
                'url': res.url + file_info['key']
            }
            return DetailResponse(data, message='上传成功')
        return FailureResponse(message='上传失败')