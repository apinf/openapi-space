from pkg_resources import resource_filename

from rest_framework.authtoken import views as authviews

from django.conf.urls import url, include
from django.contrib import admin

from lepo.router import Router
from lepo.validate import validate_router

from space.server import views

router = Router.from_file(resource_filename(__name__, '../swagger.yaml'))
router.add_handlers(views)
validate_router(router)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^api/v1/', include(router.get_urls(), 'api')),
    url(r'^api-token-auth/', authviews.obtain_auth_token),
]
