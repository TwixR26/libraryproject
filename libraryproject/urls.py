from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include("apps.bookmodule.urls")), # أي رابط يبدأ بـ books يذهب للمكتبة
    path('users/', include("apps.usermodule.urls")), # أي رابط يبدأ بـ users يذهب للمستخدمين
]