from django.urls import path

from .views import interviews_availability

#from .views import user_detail_view
#from .views import user_redirect_view
#from .views import user_update_view

app_name = "interviews"
urlpatterns = [
    path("<int:id>/availability", interviews_availability),
]
