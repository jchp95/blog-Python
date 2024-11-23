import json
import requests
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class ChatResponseView(View):
    def get(self, request):
        return render(request, 'chat.html')  # Renderiza la plantilla del chat

    @method_decorator(csrf_exempt)  # Deshabilitar CSRF para simplificar (no recomendado para producción)
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({'error': 'El mensaje no puede estar vacío.'}, status=400)

            response = self.handle_specific_questions(user_message)
            if response:
                return JsonResponse({'response': response})

            # Llamar a la API de Gemini para otras preguntas
            generated_response = self.call_gemini_api(user_message)
            return JsonResponse({'response': generated_response})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON no válido. Por favor, verifica tu mensaje.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Ocurrió un error inesperado. Por favor, intenta de nuevo más tarde.'}, status=500)

    def handle_specific_questions(self, message):
        """Maneja preguntas específicas y devuelve respuestas predefinidas."""
        if "el blog" in message.lower():
            return (
                "¡Hola! Somos el Team EL BLOG. En nuestro equipo, la pasión y la creatividad se unen para llevar tus ideas al siguiente nivel. "
                "Nos encanta colaborar, innovar y encontrar soluciones que realmente marquen la diferencia. "
                "¡Creemos en construir relaciones auténticas con nuestros clientes y hacer que cada proyecto sea una experiencia divertida y exitosa!"
            )
        elif "servicios" in message.lower():
            return (
                "¡Hola! Nuestro objetivo es ayudarle y tenemos una gama de servicios diseñados para hacerle la vida más fácil. "
                "Mira lo que podemos hacer por ti: Diseño creativo, Desarrollo web, Creación de contenido, Gestión de redes sociales, Consultoría y estrategia."
            )
        return None

    def call_gemini_api(self, message):
        """Llama a la API de Gemini y devuelve la respuesta generada."""
        api_key = os.getenv("GEMINI_API_KEY")  # Cargar la clave de API desde el archivo .env
        try:
            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}',
                headers={'Content-Type': 'application/json'},
                json={'contents': [{'parts': [{'text': message}]}]}
            )

            response.raise_for_status()  # Lanza un error para respuestas no exitosas
            return response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Sin respuesta')
        except requests.ConnectionError:
            return 'No se pudo conectar con el servicio. Por favor, verifica tu conexión a Internet.'
        except requests.Timeout:
            return 'La solicitud ha tardado demasiado. Por favor, intenta de nuevo más tarde.'
        except requests.RequestException as e:
            return f'Error al llamar a la API: {str(e)}'