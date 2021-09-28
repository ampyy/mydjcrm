from django.urls import path
from .views import *


urlpatterns= [
    path('', AgentListView.as_view(), name='agent_list'),
    path('create', AgentCreateView.as_view(), name='agent_create'),
    path('/<int:pk>', AgentDetailView.as_view(), name='agent_detail'),
    path('update/<int:pk>', AgentUpdateView.as_view(), name='agent_update'),
    path('delete/<int:pk>', AgentDeleteView.as_view(), name='agent_delete'),
]

