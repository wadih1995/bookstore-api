from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, OrderViewSet

router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('books', BookViewSet)
router.register('orders', OrderViewSet)

urlpatterns = router.urls
