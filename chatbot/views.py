from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from .utils import GrokChatbot, haversine_distance
from bibliotecas.models import Biblioteca
from libros.models import Libro
from datetime import datetime
import pytz
import json
import os 
from django.conf import settings

@xframe_options_exempt  # Permite que esta vista se cargue en un iframe
def chatbot_view(request):
    chatbot = GrokChatbot()
    resultados = None
    mensaje_usuario = ""
    respuesta_grok = None
    estado_conversacion = request.session.get('estado_conversacion', '')

    tz = pytz.timezone('America/Mexico_City')
    current_time = datetime.now(tz).strftime("%I:%M %p")

    # Load bibliotecas.json
    json_path = os.path.join(settings.STATICFILES_DIRS[0], 'json', 'bibliotecas.json')
    with open(json_path, 'r', encoding='utf-8') as file:
        bibliotecas_data = json.load(file)

    if request.method == "POST":
        mensaje_usuario = request.POST.get("mensaje", "").strip()
        if mensaje_usuario:
            respuesta_grok = chatbot.get_response(mensaje_usuario)
            mensaje_lower = mensaje_usuario.lower()

            # IntenciÃ³n: Buscar biblioteca mÃ¡s cercana
            if "biblioteca cerca" in mensaje_lower or mensaje_lower == "encontrar biblioteca cercana":
                # For testing, use a hardcoded user location (e.g., Ciudad JuÃ¡rez coordinates)
                user_lat = 31.7383  # Example latitude (replace with actual user input or geolocation)
                user_lon = -106.4870  # Example longitude

                # Calculate distances to all libraries
                nearest_library = None
                min_distance = float('inf')

                for biblioteca in bibliotecas_data:
                    distance = haversine_distance(
                        user_lat, user_lon,
                        biblioteca['latitud'], biblioteca['longitud']
                    )
                    if distance < min_distance:
                        min_distance = distance
                        nearest_library = biblioteca

                if nearest_library:
                    respuesta_grok = (
                        f"La biblioteca mÃ¡s cercana es '{nearest_library['nombre']}' "
                        f"ubicada en {nearest_library['direccion']}. "
                        f"Distancia aproximada: {min_distance:.2f} km."
                    )
                    resultados = [nearest_library]  # Pass as a list for template rendering
                else:
                    respuesta_grok = "No encontrÃ© bibliotecas disponibles."

            # Resto de las intenciones existentes
            else:
                # Enviar el mensaje a Grok
                respuesta_grok = chatbot.get_response(mensaje_usuario)
                # IntenciÃ³n 1: Buscar un libro por tÃ­tulo
                if "libro" in mensaje_lower and any(keyword in mensaje_lower for keyword in ["quiero", "busco", "tienes"]):
                    palabras = mensaje_lower.split()
                    posible_titulo = " ".join(palabras[palabras.index("libro") + 1:] if "libro" in palabras else palabras)
                    resultados = Libro.objects.filter(titulo__icontains=posible_titulo)
                    if resultados.exists():
                        respuesta_grok = f"He encontrado {resultados.count()} libro(s) que coinciden con '{posible_titulo}':"
                    else:
                        respuesta_grok = f"No encontrÃ© ningÃºn libro con el tÃ­tulo '{posible_titulo}'."
                # IntenciÃ³n 2: Buscar libros por categorÃ­a
                elif any(categoria.lower() in mensaje_lower for categoria in [choice[0] for choice in Libro.categoria.choices]):
                    categoria_buscada = next((cat for cat in [choice[0] for choice in Libro.categoria.choices] if cat in mensaje_lower), None)
                    resultados = Libro.objects.filter(categoria=categoria_buscada, disponible=True)
                    if resultados.exists():
                        respuesta_grok = f"He encontrado {resultados.count()} libro(s) en la categorÃ­a '{categoria_buscada}':"
                    else:
                        respuesta_grok = f"No encontrÃ© libros disponibles en la categorÃ­a '{categoria_buscada}'."
                # IntenciÃ³n 3: Buscar libros por autor 
                elif "libros de" in mensaje_lower:
                    posible_autor = mensaje_lower.split("libros de")[-1].strip()
                    resultados = Libro.objects.filter(autor__icontains=posible_autor, disponible=True)
                    if resultados.exists():
                        respuesta_grok = f"He encontrado {resultados.count()} libro(s) de '{posible_autor}':"
                    else:
                        respuesta_grok = f"No encontrÃ© libros disponibles de '{posible_autor}'."

                # IntenciÃ³n 5: Verificar disponibilidad
                elif "estÃ¡ disponible" in mensaje_lower:
                    posible_titulo = mensaje_lower.split("estÃ¡ disponible")[-1].strip()
                    libro = Libro.objects.filter(titulo__icontains=posible_titulo).first()
                    if libro:
                        if libro.disponible:
                            respuesta_grok = f"SÃ­, el libro '{libro.titulo}' estÃ¡ disponible en {libro.biblioteca.nombre}, ubicado en {libro.ubicacion}."
                        else:
                            respuesta_grok = f"Lo siento, el libro '{libro.titulo}' no estÃ¡ disponible. Estado: {libro.get_estado_display()}."
                    else:
                        respuesta_grok = f"No encontrÃ© ningÃºn libro con el tÃ­tulo '{posible_titulo}'."


                else:
                    if respuesta_grok == "No pude procesar tu solicitud.":
                        respuesta_grok = "Lo siento, no entendÃ­ tu solicitud. Puedes pedirme cosas como 'buscar un libro', 'libros de un autor', 'si un libro estÃ¡ disponible', o buscar por ISBN."

    return render(request, "chatbot/chatbot.html", {
        "resultados": resultados,
        "mensaje_usuario": mensaje_usuario,
        "respuesta_grok": respuesta_grok,
        "current_time": current_time,
    })