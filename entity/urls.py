from django.urls import path, include

from firm import views as fviews
from branch import views as bviews
from service import views as sviews
from function import views as ftviews
from rank import views as rviews
from employee import views as eviews
from location import views as lviews

from common.router import OptionalSlashRouter

router = OptionalSlashRouter()
router.register(r'firm', fviews.FirmViewSet, basename='firm')
router.register(r'branch', bviews.BranchViewSet, basename='branch')
router.register(r'service', sviews.ServiceViewSet, basename='service')
router.register(r'function', ftviews.FunctionViewSet, basename='function')
router.register(r'rank', rviews.RankViewSet, basename='rank')
router.register(r'employee', eviews.EmployeeViewSet, basename='employee')
router.register(r'country', lviews.CountryViewSet, basename='country')
router.register(r'region', lviews.RegionViewSet, basename='region')

urlpatterns = [
    path('', include(router.urls)),
]
