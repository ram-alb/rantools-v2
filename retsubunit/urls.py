from django.urls import path

from retsubunit.views import RetSubUnitView

urlpatterns = [
    path("", RetSubUnitView.as_view(), name="retsubunit_index"),
]
