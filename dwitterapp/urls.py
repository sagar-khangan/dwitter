from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

router.register(r'dweets', views.DweetsViewSet)
router.register(r'dweeters', views.DweeterViewSet)
router.register(r'dweeters-auth', views.DweeterCreateViewSet)
router.register(r'dweetcomment', views.DweetCommentViewSet)

urlpatterns = router.urls
