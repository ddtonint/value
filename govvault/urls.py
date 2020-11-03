from django.urls import path

from . import views

app_name = 'govvault'
urlpatterns = [
    path('', views.index, name='index'),
    path('gv-total-holders/', views.gv_total_holders, name='gv-total-holders'),
    path('top-gvholders/', views.top_gvholders, name='top-gvholders'),
    path('value-flow/', views.value_flow, name='value-flow'),
    path('vaults-performance/', views.vaults_performance, name='vaults-performance'),
    path('seedpool-holders/', views.seedpool_holders, name='seedpool-holders'),
]