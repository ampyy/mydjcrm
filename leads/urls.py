from django.urls import path
from . import views


urlpatterns =[
    path('all', views.LeadListView.as_view(), name ='lead_list'),
    path('<pk>', views.LeadDetailView.as_view(), name='lead_detail'),
    path('<int:pk>/update', views.LeadUpdateView.as_view(), name='lead_update'),
    path('create/', views.LeadCreateView.as_view(), name='lead_create'),
    path('<int:pk>/delete', views.LeadDeleteView.as_view(), name='lead_delete'),
    path('<int:pk>/assign_agent', views.AssignAgentView.as_view(), name='assign_agent'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>', views.CategoryDetailView.as_view(), name='category_detail'),
    path('<int:pk>/categories/update', views.CategoryUpdateView.as_view(), name='category_update'),
]