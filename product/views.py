from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from product.models import Product
from product.permissions import IsAuthorOrIsAdmin, IsAuthor
from product.serializers import ProductListSerializer, ReviewSerializer
from review.models import Review
from review.serializers import ReviewListSerializer


class ProductFilter(filters.FilterSet):
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'created_at')


class ProductListView(ListAPIView):
    queryset = Product.objects.only('title')
    serializer_class = ProductListSerializer


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class CreateProductView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class UpdateProductView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class DeleteProductView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthorOrIsAdmin, ]
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filter.SearchFilter,
                       rest_filter.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'text']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductListSerializer
        return ProductListSerializer


class CreateReviewView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_selializer_contex(self):
        return {'request': self.request}


class UpdateReviewView(UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthor]


class DeleteReviewView(DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthor]


from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ReviewViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor]

