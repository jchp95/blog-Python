from django.urls import path
from .views import ChatResponseView  # Importa la vista basada en clase

urlpatterns = [
    path('chat/', ChatResponseView.as_view(), name='chat_response'),  # Usa as_view() para conectar la clase
]