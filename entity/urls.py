from django.urls import path, include

from firm import views as fviews
from branch import views as bviews

from common.router import OptionalSlashRouter

router = OptionalSlashRouter()
router.register(r'firm', fviews.FirmViewSet, basename='firm')
router.register(r'branch', bviews.BranchViewSet, basename='branch')

urlpatterns = [
    path('', include(router.urls)),
]
