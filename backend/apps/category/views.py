from utils.pagination import CustomPagination
from utils.viewset import CustomViewSet
from .models import Category
from .serializers import CategorySerializer


# Create your views here.

class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            return self.queryset.filter(category_name__icontains=name)
        else:
            return self.queryset
