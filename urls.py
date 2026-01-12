from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # BloodConnect app URLs
    path('', include('bloodconnect_project.urls')),  # Root URLs go to bloodconnect

    # Optional: if you have more apps, include them here
    # path('another-app/', include('another_app.urls')),
]
