from django.urls import path

from .views import (
    resource_list,
    dashboard,
    resource_detail,
    upload_resource,
    bookmark_resource,
    remove_bookmark,
    delete_resource,
    bookmark_list,
    ask_doubt,
    reply_doubt,
    resolve_doubt,
    track_download
)

urlpatterns = [

    path("dashboard/", dashboard, name="dashboard"),
    path("", resource_list, name="resource_list"),

    path("upload/", upload_resource, name="resource_upload"),

    path("bookmarks/", bookmark_list, name="bookmark_list"),
    path("bookmark/<str:rid>/", bookmark_resource, name="bookmark_resource"),
    path("remove-bookmark/<str:rid>/", remove_bookmark, name="remove_bookmark"),
    path("delete/<str:rid>/", delete_resource, name="delete_resource"),

    path("doubts/", ask_doubt, name="ask_doubt"),
    path("reply/<str:did>/", reply_doubt, name="reply_doubt"),
    path("resolve/<str:did>/", resolve_doubt, name="resolve_doubt"),
    path("download/<str:rid>/", track_download, name="track_download"),

    path("<str:rid>/", resource_detail, name="resource_detail"),
]