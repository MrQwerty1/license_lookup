from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from .auth import views as auth_views
from .scraping import views as scraping_views

dropdowns = [
]

schema_view = get_swagger_view(title='Lookup API: Web', urlconf='api.v0.urls', url='/api/v0/')

urlpatterns = [

    # path('docs/', schema_view, name='swagger'),

    # region Auth
    # endregion

    # region Dropdowns
    # path('dropdowns/', include(dropdowns)),
    # endregion

    path('license/', scraping_views.LicenseLookupView.as_view())

]
