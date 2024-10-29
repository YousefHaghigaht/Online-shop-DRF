from django.urls import path,include
from . import views

app_name = 'products'

bucket_urls = [
    path('objects/', views.BucketListObjectsView.as_view(), name='bucket_objects'),
    path('delete_object/<str:key>/', views.BucketDeleteObjectView.as_view(), name='delete_object'),
    path('dl_object/<str:key>/', views.BucketDownloadObjectView.as_view(), name='download_object'),
]

urlpatterns = [
    path('detail/<int:post_id>/<slug:post_slug>/',views.ProductDetailView.as_view(),name='detail'),
    path('bucket/',include(bucket_urls)),
]

