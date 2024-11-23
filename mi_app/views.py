from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, News, Comment, Reply, CustomUser_CreationForm, Image, TermsAndConditions, Services, Contact, BannerHome, About, Carousel,CarouselCursos, Cursos
from .forms import TermsAndConditionsForm, ServicesForm, ContactForm, ContactMessageForm
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import logging
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
from django.utils import translation

from django.conf import settings  # Importa settings para acceder a LANGUAGE_SESSION_KEY
from django.utils.translation import gettext as _


# Configura el logger
logger = logging.getLogger(__name__)

def index(request):
    current_language = translation.get_language()  # Obtén el idioma actual
    return render(request, 'index.html', {
        'LANGUAGE_CODE': current_language,  # Asegúrate de pasar el idioma actual
        'request': request,  # Asegúrate de pasar el objeto de solicitud si lo necesitas
    })


def home(request):
    current_language = translation.get_language()
    banner_home = BannerHome.objects.first()
    articles = Article.objects.all()
    news = News.objects.all()
    items = Carousel.objects.all()
    items_cursos = CarouselCursos.objects.all()
    images = Image.objects.all()
    comments = Comment.objects.all()  # Fetch all comments

     # Determinar si se debe mostrar el banner de cookies
    show_cookie_banner = request.COOKIES.get('cookie_consent') is None
    return render(request, 'home.html', {
        
        'articles': articles,
        'news': news,
        'carousel_items': items,
        'carousel_cursos': items_cursos,
        'comments': comments,  # Pass comments to the template
        'images': images,
        'show_cookie_banner': show_cookie_banner,  # Pasar la variable al contexto
        'LANGUAGE_CODE': current_language,
        'banner_home': banner_home,
    })


 #######################   REGISTER  ##########################################
def register(request):
    if request.method == 'POST':
        form = CustomUser_CreationForm(request.POST)
        # Verifica si el formulario es válido y si el checkbox está marcado
        if form.is_valid() and 'terms' in request.POST:
            user = form.save()
            logger.info(f'Nuevo usuario registrado: {user.username}')  # Registra el nombre de usuario
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Error en el registro. Por favor, corrige los errores o acepta los términos y condiciones.')
    else:
        form = CustomUser_CreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


################################ LOG IN ######################################################################

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Asegúrate de tener esta plantilla

    def form_valid(self, form):
        # Llama al método padre para procesar el formulario
        response = super().form_valid(form)
        # Agrega un mensaje de éxito
        messages.success(self.request, "Has iniciado sesión con éxito.")
        return response

    def form_invalid(self, form):
        # Agrega un mensaje de error
        messages.error(self.request, "Usuario o contraseña incorrectos.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'  # Asegúrate de que esta ruta sea correcta
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html' 

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'  # Asegúrate de que esta ruta sea correcta
    success_url = reverse_lazy('password_reset_complete')  # Redirigir a la vista de completado

from django.views.generic import TemplateView

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

###################  COMENTARIOS  ##############################################################
@csrf_protect
@login_required
def submit_comment(request):
    # Verifica si el usuario está autenticado
    if request.method == 'POST':
        comment_content = request.POST.get('comment')
        Comment.objects.create(user=request.user, content=comment_content)
        
        # Agregar un mensaje de éxito
        messages.success(request, "Tu comentario ha sido enviado con éxito.")
        return redirect('home')
    else:
        return redirect('home')

def like_comment(request, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        comment.likes += 1
        comment.save()
        return JsonResponse({'likes': comment.likes})

def dislike_comment(request, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        comment.dislikes += 1
        comment.save()
        return JsonResponse({'dislikes': comment.dislikes})

@csrf_protect
@login_required
def submit_reply(request):
    # Verifica si el usuario está autenticado
    if request.method == 'POST':
        content = request.POST.get('reply')
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        reply = Reply.objects.create(user=request.user, content=content, comment=comment)
        reply.save()
        return redirect('home')  # Cambia 'home' por el nombre de la vista que desees redirigir
    else:
        return redirect('home')

#################################################################################################

def articles_details(request, id):
    articles = Article.objects.all()  # Obtiene todos los artículos
    images = Image.objects.all()
    return render(request, 'articles_details.html', {
        'articles': articles,
        'images': images
        })

def news_details(request, id):
    news = News.objects.all()
    images = Image.objects.all() 
    return render(request, 'news_details.html', {
        'news': news,
        'images': images
        })

from django.shortcuts import render


def about(request):
    images = Image.objects.all() 
    about_content = About.objects.first()  # Asumiendo que solo hay un registro
    context = {
        'about_content': about_content,
        'team_description': about_content.team_description,
        'team_image': about_content.team_image.url if about_content.team_image else None, 
        'what_you_can_find': about_content.what_you_can_find.split(','),  # Convierte a lista
        'why_we_do_it': about_content.why_we_do_it,
        'core_values': [
            about_content.core_value_1,
            about_content.core_value_2,
            about_content.core_value_3,
            about_content.core_value_4,
            about_content.core_value_5,
        ], 
        'contact_email': about_content.contact_email,
        'facebook_url': about_content.facebook_url,
        'whatsapp_url': about_content.whatsapp_url,
        'footer_message': about_content.footer_message,
        'images': images
    }

    return render(request, 'about.html', context)

def services(request):
    images = Image.objects.all()
    services = Services.objects.all()  # Obtener todos los servicios de la base de datos
    if request.method == 'POST':
        form = ServicesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services')  # Cambia esto al nombre de la vista que muestra los servicios
    else:
        form = ServicesForm()
    return render(request, 'services.html', {
        'form': form,
        'images': images,
        'services':  services
        })


def contact(request): 
    images = Image.objects.all()
    contact = Contact.objects.all()
    
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tienes un nuevo mensaje de contacto.') 
    else:
        form = ContactMessageForm()
      
    return render(request, 'contact.html', {
        'form': form,
        'images': images,
        'contact': contact,
        
    }) 

def terms_and_conditions_view(request):
    images = Image.objects.all()
    terms = TermsAndConditions.objects.first()  # Obtener el primer objeto
    if request.method == 'POST':
        form = TermsAndConditionsForm(request.POST, instance=terms)
        if form.is_valid():
            form.save()
            return redirect('terms_and_conditions')  # Redirigir a la misma vista
    else:
        form = TermsAndConditionsForm(instance=terms)

    return render(request, 'terms_and_conditions.html', {
        'form': form,
        'terms': terms,
        'images': images
         })

def cursos(request):
    cursos_list = Cursos.objects.all()  # Puedes aplicar filtros si es necesario

    # Pasar los objetos a la plantilla
    context = {
        'cursos': cursos_list  # 'cursos' será la variable que usarás en la plantilla
    }
    return render(request, 'cursos.html', context)

########################## CAMBIO DE IDIOMA  ##############################

# Define LANGUAGE_SESSION_KEY manualmente
LANGUAGE_SESSION_KEY = 'django_language'

# Define LANGUAGE_SESSION_KEY si no está disponible
def switch_language(request):
    lang_code = request.GET.get('lang', 'en')
    translation.activate(lang_code)
    request.session[LANGUAGE_SESSION_KEY] = lang_code  # Usa la constante directamente
    
    # Ahora obtén el idioma actual después de activarlo
    current_language = translation.get_language()
    
    print("Session content:", request.session)
    print(f"Language switched to: {lang_code}")  # Para depuración
    print("Current language:", current_language)  # Esto ahora mostrará el idioma correcto
    print(f"Current language in home view: {current_language}")

    return redirect(request.META.get('HTTP_REFERER', '/'))

################################ BUSCADOR ###########################################
from django.core.paginator import Paginator
from haystack.query import SearchQuerySet
from django.shortcuts import render
import re

def search(request):
    query = request.GET.get('q', '')
    results = []
    error_message = None

    try:
        if query:
            results = SearchQuerySet().filter(content=query) | SearchQuerySet().filter(title=query)
            print(f"Resultados iniciales: {len(results)}")  # Verifica cuántos resultados se obtienen
            terms = query.split()
            for term in terms:
                results = results | SearchQuerySet().filter(content=term) | SearchQuerySet().filter(title=term)
                print(f"Resultados después de filtrar por términos: {len(results)}")  # Verifica el número de resultados después de filtrar

            # Resaltar términos en los resultados
            for result in results:
                print(f"Título: {result.title}, Contenido: {result.content}")
                title = result.title if result.title else ""
                content = result.content if result.content else ""
                result.highlighted_title = highlight_terms(title, terms)
                result.highlighted_content = highlight_terms(content, terms)

        # Paginación
        paginator = Paginator(results, 10)  # 10 resultados por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except Exception as e:
        error_message = f"Ocurrió un error durante la búsqueda: {str(e)}"
        page_obj = []  # Asegúrate de que page_obj sea una lista vacía en caso de error

    return render(request, 'search_results.html', {'results': page_obj, 'query': query, 'error_message': error_message})
    
def highlight_terms(text, terms):
    """Resalta los términos en el texto dado."""
    if text is None:  # Verifica si el texto es None
        return ""
    if not terms:
        return text
    escaped_terms = [re.escape(term) for term in terms]
    pattern = re.compile('|'.join(escaped_terms), re.IGNORECASE)
    return pattern.sub(lambda match: f'<span class="highlight">{match.group(0)}</span>', text)
################## MANEJO DE ERRORES #####################################################

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)

#################################chat IA###########################################

