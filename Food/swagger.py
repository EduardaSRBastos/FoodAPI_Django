from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Food API",
        default_version='v1',
        description="Food API description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
