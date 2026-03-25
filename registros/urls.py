from django.urls import path
from .views import (
    RegistroPaso1, 
    RegistroPaso2, 
    registro_paso3, 
    RegistroCompletado, 
    RegistroPaso1Prellenar, 
    BuscarPreRegistros
)

urlpatterns = [
    path('paso1/prellenar/<int:pre_registro_id>/', RegistroPaso1Prellenar.as_view(), name='registro_paso1_prellenar'),
    
    path('buscar-pre-registros/', BuscarPreRegistros.as_view(), name='buscar_pre_registros'),
    
    path('registro/paso1/', RegistroPaso1.as_view(), name='registro_paso1'),
    path('registro/paso2/', RegistroPaso2.as_view(), name='registro_paso2'),
    path('registro/paso3/', registro_paso3, name='registro_paso3'),
    path('registro/completado/', RegistroCompletado.as_view(), name='registro_completado'),
]