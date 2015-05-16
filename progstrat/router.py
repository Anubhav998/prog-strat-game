from rest_framework_extensions.routers import NestedRouterMixin
from rest_framework.routers import DefaultRouter

from resources import views as resource_views


class SimpleRouterWithNesting(NestedRouterMixin, DefaultRouter):
    pass


router = SimpleRouterWithNesting()


router.register('resources', resource_views.ResourceViewSet)