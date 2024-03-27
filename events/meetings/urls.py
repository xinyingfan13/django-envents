from django.urls import path
from .views import (MeetingAPIView, ProfileAPIView, MeetingDetail, ProfileDetail, MeetingCreateAPIView,
                    MeetingProfileListAPIView, TimetableCreate, CreateUserView, ProfileCreateAPIView, TimetableUpdate,
                    UserInfoByToken, UserAddMeetingAPIView, UserRemoveMeetingAPIView, TagsAPIView, PlaceAPIView,
                    ChatAPIView, ChatCreateAPIView, MessageCreateAPIView, ChatMessageAPIView, MessagesAPIView,
                    ProfileChatAddAPIView, ProfileChatRemoveAPIView, MeetingChatAddAPIView, VotingAPIView,
                    VotingCreateAPIView, VotingDestroyAPIView, FieldCreateAPIView, FieldAddVoteAPIView,
                    FieldRemoveVoteAPIView, FieldDestroyAPIView, FieldRetrieveAPIView, RecommendedMeetingsForTags)

urlpatterns = [

    path('meeting/<int:pk>/voting/create/', VotingCreateAPIView.as_view()),
    path('meeting/voting/<int:pk>/delete/', VotingDestroyAPIView.as_view()),
    path('field/<int:pk>/remove_vote/', FieldRemoveVoteAPIView.as_view()),
    path('field/<int:pk>/add_vote/', FieldAddVoteAPIView.as_view()),
    path('field/<int:pk>/', FieldRetrieveAPIView.as_view()),  # new
    path('voting/<int:pk>/add_field/', FieldCreateAPIView.as_view()),
    path('voting/destroy_field/<int:pk>/', FieldDestroyAPIView.as_view()),
    path('votings/', VotingAPIView.as_view()),

    path('messages/', MessagesAPIView.as_view()),
    path('chat/<int:pk>/create_message/', MessageCreateAPIView.as_view()),
    path('chat/<int:pk>/', ChatMessageAPIView.as_view()),
    path('chat_create/', ChatCreateAPIView.as_view()),
    path('chat_list/', ChatAPIView.as_view()),

    path('places_list/', PlaceAPIView.as_view()),

    path('tags_list/', TagsAPIView.as_view()),

    path('user/recommended_meetings/', RecommendedMeetingsForTags.as_view()),
    path('user/<int:pk>/remove_chat/', ProfileChatRemoveAPIView.as_view()),
    path('user/<int:pk>/add_chat/', ProfileChatAddAPIView.as_view()),
    path('user/<int:pk>/remove_meeting/', UserRemoveMeetingAPIView.as_view()),
    path('user/<int:pk>/add_meeting/', UserAddMeetingAPIView.as_view()),
    path('user_by_token/', UserInfoByToken.as_view()),  # user_by_token/
    path('user_register/', CreateUserView.as_view()),
    path('user_create/', ProfileCreateAPIView.as_view()),
    path('users/<int:pk>/', ProfileDetail.as_view()),
    path('users/', ProfileAPIView.as_view()),

    path('timetable_update/<int:pk>/', TimetableUpdate.as_view()),
    path('timetable_create/', TimetableCreate.as_view()),

    path('meeting/<int:pk>/add_chat/', MeetingChatAddAPIView.as_view()),
    path('meeting/prifils/<int:pk>/', MeetingProfileListAPIView.as_view()),
    path('meeting/<int:pk>/', MeetingDetail.as_view()),
    path('meeting_create/', MeetingCreateAPIView.as_view()),
    path('meeting/', MeetingAPIView.as_view()),
]
