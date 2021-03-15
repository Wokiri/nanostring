"""nanostring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from .views import (
    home_page_view,
    about_page_view,
    cell_types_for_spatial_decon_uploader_view,
    cell_types_detail_view,
    CellTypeList,
    update_cell_type_view,
    messages_view,
)

app_name = 'pages'

urlpatterns = [
    path('', home_page_view, name='home_page'),
    path('about-us/', about_page_view, name='about_page'),
    path('file-upload/', cell_types_for_spatial_decon_uploader_view, name='upload_page'),
    path('cell-types/', cell_types_detail_view, name='cell_types_detail_page'),
    path('messages/', messages_view, name='messages_page'),
    path('<slug:prev_name>/messages/', messages_view, name='messages_page'),
    path('update-cell-type/', CellTypeList.as_view(), name='list_cell_type_page'),
    path('update-cell-type/<slug:clusterid>/', update_cell_type_view, name='update_cell_type_page'),
]
