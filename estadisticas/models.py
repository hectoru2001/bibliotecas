from django.db import models

class LibraryVisitorStats(models.Model):
    date = models.DateField(auto_now_add=True)  # Automatically set to the current date

    # Age Range: Adultos mayores de 60 años
    adults_over_60_males = models.PositiveIntegerField(default=0, verbose_name="Adultos mayores de 60 años - Hombres")
    adults_over_60_females = models.PositiveIntegerField(default=0, verbose_name="Adultos mayores de 60 años - Mujeres")
    adults_over_60_preschool = models.PositiveIntegerField(default=0, verbose_name=" - Preescolar")
    adults_over_60_primary = models.PositiveIntegerField(default=0, verbose_name=" - Primaria")
    adults_over_60_secondary = models.PositiveIntegerField(default=0, verbose_name=" - Secundaria")
    adults_over_60_preparatory = models.PositiveIntegerField(default=0, verbose_name=" - Preparatoria")
    adults_over_60_undergraduate = models.PositiveIntegerField(default=0, verbose_name=" - Licenciatura")
    adults_over_60_postgraduate = models.PositiveIntegerField(default=0, verbose_name=" - Posgrado")
    adults_over_60_household = models.PositiveIntegerField(default=0, verbose_name="mayores de 60 años - Hogar")
    adults_over_60_employed_or_worker = models.PositiveIntegerField(default=0, verbose_name="mayores de 60 años - Empleado / Trabajador")
    adults_over_60_students = models.PositiveIntegerField(default=0, verbose_name="Mayores de 60 años- Estudiantes")
    adults_over_60_unemployed = models.PositiveIntegerField(default=0, verbose_name="mayores de 60 años - Desocupados")

    # Age Range: Adultos entre 30 y 59 años
    adults_30_to_59_males = models.PositiveIntegerField(default=0, verbose_name="Adultos entre 30 y 59 años - Hombres")
    adults_30_to_59_females = models.PositiveIntegerField(default=0, verbose_name="Adultos entre 30 y 59 años - Mujeres")
    adults_30_to_59_preschool = models.PositiveIntegerField(default=0, verbose_name=" - Preescolar")
    adults_30_to_59_primary = models.PositiveIntegerField(default=0, verbose_name=" - Primaria")
    adults_30_to_59_secondary = models.PositiveIntegerField(default=0, verbose_name=" - Secundaria")
    adults_30_to_59_preparatory = models.PositiveIntegerField(default=0, verbose_name=" - Preparatoria")
    adults_30_to_59_undergraduate = models.PositiveIntegerField(default=0, verbose_name=" - Licenciatura")
    adults_30_to_59_postgraduate = models.PositiveIntegerField(default=0, verbose_name=" - Posgrado")
    adults_30_to_59_household = models.PositiveIntegerField(default=0, verbose_name="30 y 59 años - Hogar")
    adults_30_to_59_employed_or_worker = models.PositiveIntegerField(default=0, verbose_name="30 y 59 años- Empleado / Trabajador")
    adults_30_to_59_students = models.PositiveIntegerField(default=0, verbose_name="30 y 59 años- Estudiantes")
    adults_30_to_59_unemployed = models.PositiveIntegerField(default=0, verbose_name="30 y 59 años - Desocupados")

    # Age Range: Adultos jóvenes entre 18 y 29 años
    young_adults_18_to_29_males = models.PositiveIntegerField(default=0, verbose_name="Adultos jóvenes entre 18 y 29 años - Hombres")
    young_adults_18_to_29_females = models.PositiveIntegerField(default=0, verbose_name="Adultos jóvenes entre 18 y 29 años - Mujeres")
    young_adults_18_to_29_preschool = models.PositiveIntegerField(default=0, verbose_name=" - Preescolar")
    young_adults_18_to_29_primary = models.PositiveIntegerField(default=0, verbose_name=" - Primaria")
    young_adults_18_to_29_secondary = models.PositiveIntegerField(default=0, verbose_name="- Secundaria")
    young_adults_18_to_29_preparatory = models.PositiveIntegerField(default=0, verbose_name=" - Preparatoria")
    young_adults_18_to_29_undergraduate = models.PositiveIntegerField(default=0, verbose_name=" - Licenciatura")
    young_adults_18_to_29_postgraduate = models.PositiveIntegerField(default=0, verbose_name=" - Posgrado")
    young_adults_18_to_29_household = models.PositiveIntegerField(default=0, verbose_name=" 18 y 29 años - Hogar")
    young_adults_18_to_29_employed_or_worker = models.PositiveIntegerField(default=0, verbose_name=" 18 y 29 años - Empleado / Trabajador")
    young_adults_18_to_29_students = models.PositiveIntegerField(default=0, verbose_name=" 18 y 29 años - Estudiantes")
    young_adults_18_to_29_unemployed = models.PositiveIntegerField(default=0, verbose_name=" 18 y 29 años - Desocupados")

    # Age Range: Adolescentes entre 13 y 17 años
    adolescents_13_to_17_males = models.PositiveIntegerField(default=0, verbose_name="Adolescentes entre 13 y 17 años - Hombres")
    adolescents_13_to_17_females = models.PositiveIntegerField(default=0, verbose_name="Adolescentes entre 13 y 17 años - Mujeres")
    adolescents_13_to_17_preschool = models.PositiveIntegerField(default=0, verbose_name=" - Preescolar")
    adolescents_13_to_17_primary = models.PositiveIntegerField(default=0, verbose_name=" - Primaria")
    adolescents_13_to_17_secondary = models.PositiveIntegerField(default=0, verbose_name="- Secundaria")
    adolescents_13_to_17_preparatory = models.PositiveIntegerField(default=0, verbose_name=" - Preparatoria")
    adolescents_13_to_17_household = models.PositiveIntegerField(default=0, verbose_name=" - Hogar")
    adolescents_13_to_17_employed_or_worker = models.PositiveIntegerField(default=0, verbose_name=" 13 y 17 años - Empleado / Trabajador")
    adolescents_13_to_17_students = models.PositiveIntegerField(default=0, verbose_name=" - Estudiantes")
    adolescents_13_to_17_unemployed = models.PositiveIntegerField(default=0, verbose_name=" 13 y 17 años - Desocupados")

    #Age Range: Niños entre 0 y 12 años
    kids_0_to_12_males = models.PositiveIntegerField(default=0, verbose_name="Niños entre 0 y 12 años - Hombres")
    kids_0_to_12_females = models.PositiveIntegerField(default=0, verbose_name="Niños entre 0 y 12 años - Mujeres")
    kids_0_to_12_preschool = models.PositiveIntegerField(default=0, verbose_name="Niños entre 0 y 12 años - Preescolar")
    kids_0_to_12_primary = models.PositiveIntegerField(default=0, verbose_name="Niños entre 0 y 12 años - Primaria")
    kids_0_to_12_secondary = models.PositiveIntegerField(default=0, verbose_name="- Secundaria")
    kids_0_to_12_household = models.PositiveIntegerField(default=0, verbose_name="0 y 12 años - Hogar")
    kids_0_to_12_students = models.PositiveIntegerField(default=0, verbose_name=" 0 y 12 años - Estudiantes")

    # Materials Used
    general_collection = models.PositiveIntegerField(default=0, verbose_name="Colección General")
    reference_collection = models.PositiveIntegerField(default=0, verbose_name="Colección de Consulta")
    children_collection = models.PositiveIntegerField(default=0, verbose_name="Colección Infantil")
    audiovisual = models.PositiveIntegerField(default=0, verbose_name="Audiovisual")
    publications = models.PositiveIntegerField(default=0, verbose_name="Publicaciones periodicas")
    ludoteca = models.PositiveIntegerField(default=0, verbose_name="Ludoteca")
    braille = models.PositiveIntegerField(default=0, verbose_name="Braille")
    special_collection = models.PositiveIntegerField(default=0, verbose_name="Colección Especial")
    state_collection = models.PositiveIntegerField(default=0, verbose_name="Colección Estatal")

    # Credentials Issued (including gender breakdown for physical loans)
    physical_loan = models.PositiveIntegerField(default=0, verbose_name="Préstamo a domicilio")
    credentials_issued_males = models.PositiveIntegerField(default=0, verbose_name="Credenciales Expedidas - Hombres")
    credentials_issued_females = models.PositiveIntegerField(default=0, verbose_name="Credenciales Expedidas - Mujeres")

    # Actividades de Fomento a la Lectura
    reading_promotion_adults_over_60_males = models.PositiveIntegerField(default=0, verbose_name="Asistentes adultos mayores de 60 hombres - Adultos mayores de 60 años (Hombres)")
    reading_promotion_adults_over_60_females = models.PositiveIntegerField(default=0, verbose_name="Asistentes adultos mayores de 60 hombres - Adultos mayores de 60 años (Mujeres)")
    reading_promotion_adults_30_to_59_males = models.PositiveIntegerField(default=0, verbose_name="Asistentes adultos  - Adultos entre 30 y 59 años (Hombres)")
    reading_promotion_adults_30_to_59_females = models.PositiveIntegerField(default=0, verbose_name="Asistentes adultos  - Adultos entre 30 y 59 años (Mujeres)")
    reading_promotion_young_adults_18_to_29_males = models.PositiveIntegerField(default=0, verbose_name="Asistentes adultos  - Adultos jóvenes entre 18 y 29 años (Hombres)")
    reading_promotion_young_adults_18_to_29_females = models.PositiveIntegerField(default=0, verbose_name="Asistentes adultos  - Adultos jóvenes entre 18 y 29 años (Mujeres)")
    reading_promotion_adolescents_13_to_17_males = models.PositiveIntegerField(default=0, verbose_name="Asistentes - Adolescentes entre 13 y 17 años (Hombres)")
    reading_promotion_adolescents_13_to_17_females = models.PositiveIntegerField(default=0, verbose_name="Asistentes  - Adolescentes entre 13 y 17 años (Mujeres)")
    reading_promotion_children_0_to_12_males = models.PositiveIntegerField(default=0, verbose_name="Asistentes  - Niños entre 0 y 12 años (Hombres)")
    reading_promotion_children_0_to_12_females = models.PositiveIntegerField(default=0, verbose_name="Asistentes - Niños entre 0 y 12 años (Mujeres)")

    # Visitas Guiadas
    guided_visits_adults_over_60_males = models.PositiveIntegerField(default=0, verbose_name="Visitas Guiadas -  (Hombres)")
    guided_visits_adults_over_60_females = models.PositiveIntegerField(default=0, verbose_name="Visitas Guiadas -  (Mujeres)")
    guided_visits_adults_30_to_59_males = models.PositiveIntegerField(default=0, verbose_name="Visitas Guiadas -  (Hombres)")
    guided_visits_adults_30_to_59_females = models.PositiveIntegerField(default=0, verbose_name="Visitas Guiadas -  (Mujeres)")
    guided_visits_young_adults_18_to_29_males = models.PositiveIntegerField(default=0, verbose_name="Visitas Guiadas -  (Hombres)")
    guided_visits_young_adults_18_to_29_females = models.PositiveIntegerField(default=0, verbose_name="Visitas Guiadas -  (Mujeres)")
    guided_visits_adolescents_13_to_17_males = models.PositiveIntegerField(default=0, verbose_name="Visitas Guiadas - (Hombres)")
    guided_visits_adolescents_13_to_17_females = models.PositiveIntegerField(default=0, verbose_name="Visitas Guiadas - (Mujeres)")
    guided_visits_children_0_to_12_males = models.PositiveIntegerField(default=0, verbose_name="Visitas Guiadas -  (Hombres)")
    guided_visits_children_0_to_12_females = models.PositiveIntegerField(default=0, verbose_name="Visitas Guiadas - (Mujeres)")


    # Actividades Artísticas Culturales
    CULTURAL_ACTIVITY_CHOICES = [
        ('', '-- Seleccione una actividad --'),
        ('conciertos', 'Conciertos'),
        ('teatro', 'Teatro'),
        ('danza', 'Danza'),
        ('proyecciones_cine', 'Proyecciones de Cine'),
        ('fotografia', 'Fotografía'),
        ('pintura', 'Pintura'),
        ('exposiciones', 'Exposiciones'),
    ]
    cultural_activity_type = models.CharField(max_length=50, choices=CULTURAL_ACTIVITY_CHOICES, default='', blank=True, verbose_name="Tipo de Actividad Cultural")
    cultural_adults_over_60_males = models.PositiveIntegerField(default=0, verbose_name="Act. Cultural - Adultos mayores de 60 años (Hombres)")
    cultural_adults_over_60_females = models.PositiveIntegerField(default=0, verbose_name="Act. Cultural - Adultos mayores de 60 años (Mujeres)")
    cultural_adults_30_to_59_males = models.PositiveIntegerField(default=0, verbose_name="Act. Cultural - Adultos entre 30 y 59 años (Hombres)")
    cultural_adults_30_to_59_females = models.PositiveIntegerField(default=0, verbose_name="Act. Cultural - Adultos entre 30 y 59 años (Mujeres)")
    cultural_young_adults_18_to_29_males = models.PositiveIntegerField(default=0, verbose_name="Act. Cultural - Adultos jóvenes entre 18 y 29 años (Hombres)")
    cultural_young_adults_18_to_29_females = models.PositiveIntegerField(default=0, verbose_name="Act. Cultural - Adultos jóvenes entre 18 y 29 años (Mujeres)")
    cultural_adolescents_13_to_17_males = models.PositiveIntegerField(default=0, verbose_name="Act. Cultural - Adolescentes entre 13 y 17 años (Hombres)")
    cultural_adolescents_13_to_17_females = models.PositiveIntegerField(default=0, verbose_name="Act. Cultural - Adolescentes entre 13 y 17 años (Mujeres)")
    cultural_children_0_to_12_males = models.PositiveIntegerField(default=0, verbose_name="Act. Cultural - Niños entre 0 y 12 años (Hombres)")
    cultural_children_0_to_12_females = models.PositiveIntegerField(default=0, verbose_name="Act. Cultural - Niños entre 0 y 12 años (Mujeres)")

    # Módulo de Servicios Digitales
    digital_services_adults_over_60_males = models.PositiveIntegerField(default=0, verbose_name="Módulo de Servicios Digitales -  (Hombres)")
    digital_services_adults_over_60_females = models.PositiveIntegerField(default=0, verbose_name="Módulo de Servicios Digitales -  (Mujeres)")
    digital_services_adults_30_to_59_males = models.PositiveIntegerField(default=0, verbose_name="Módulo de Servicios Digitales -  (Hombres)")
    digital_services_adults_30_to_59_females = models.PositiveIntegerField(default=0, verbose_name="Módulo de Servicios Digitales -  (Mujeres)")
    digital_services_young_adults_18_to_29_males = models.PositiveIntegerField(default=0, verbose_name="Módulo de Servicios Digitales -  (Hombres)")
    digital_services_young_adults_18_to_29_females = models.PositiveIntegerField(default=0, verbose_name="Módulo de Servicios Digitales -  (Mujeres)")
    digital_services_adolescents_13_to_17_males = models.PositiveIntegerField(default=0, verbose_name="Módulo de Servicios Digitales -  (Hombres)")
    digital_services_adolescents_13_to_17_females = models.PositiveIntegerField(default=0, verbose_name="Módulo de Servicios Digitales -  (Mujeres)")
    digital_services_children_0_to_12_males = models.PositiveIntegerField(default=0, verbose_name="Módulo de Servicios Digitales -  (Hombres)")
    digital_services_children_0_to_12_females = models.PositiveIntegerField(default=0, verbose_name="Módulo de Servicios Digitales -  (Mujeres)")

    

    class Meta:
        verbose_name = "Estadísticas de usuarios atendidos"
        verbose_name_plural = "Estadísticas de usuarios atendidos"

    def __str__(self):
        return f"Estadísticas del {self.date}"


class DatosEstadisticos(models.Model):
    date = models.DateField(auto_now_add=True)

    # ---- Sección 1: Libros Más Leídos ----
    libros_general = models.PositiveIntegerField(default=0, verbose_name="General")
    libros_consulta = models.PositiveIntegerField(default=0, verbose_name="Consulta")
    libros_infantil = models.PositiveIntegerField(default=0, verbose_name="Infantil")

    # ---- Sección 2: Colección SEP-Centenaria "Mochila Viajera" ----
    sep_titulos_consultados = models.TextField(blank=True, default='', verbose_name="Títulos más consultados en préstamo de colección")
    sep_total_libros_prestados = models.PositiveIntegerField(default=0, verbose_name="Total de libros prestados")

    sep_adults_over_60_males = models.PositiveIntegerField(default=0, verbose_name="SEP - Adultos mayores de 60 años (Hombres)")
    sep_adults_over_60_females = models.PositiveIntegerField(default=0, verbose_name="SEP - Adultos mayores de 60 años (Mujeres)")
    sep_adults_30_to_59_males = models.PositiveIntegerField(default=0, verbose_name="SEP - Adultos entre 30 y 59 años (Hombres)")
    sep_adults_30_to_59_females = models.PositiveIntegerField(default=0, verbose_name="SEP - Adultos entre 30 y 59 años (Mujeres)")
    sep_young_adults_18_to_29_males = models.PositiveIntegerField(default=0, verbose_name="SEP - Adultos jóvenes entre 18 y 29 años (Hombres)")
    sep_young_adults_18_to_29_females = models.PositiveIntegerField(default=0, verbose_name="SEP - Adultos jóvenes entre 18 y 29 años (Mujeres)")
    sep_adolescents_13_to_17_males = models.PositiveIntegerField(default=0, verbose_name="SEP - Adolescentes entre 13 y 17 años (Hombres)")
    sep_adolescents_13_to_17_females = models.PositiveIntegerField(default=0, verbose_name="SEP - Adolescentes entre 13 y 17 años (Mujeres)")
    sep_children_0_to_12_males = models.PositiveIntegerField(default=0, verbose_name="SEP - Niños entre 0 y 12 años (Hombres)")
    sep_children_0_to_12_females = models.PositiveIntegerField(default=0, verbose_name="SEP - Niños entre 0 y 12 años (Mujeres)")

    sep_mochila_viajera = models.BooleanField(default=False, verbose_name="La biblioteca ha realizado la actividad Mochila Viajera")

    # ---- Sección 3: Mejoramiento de la Infraestructura ----
    infra_ampliacion = models.BooleanField(default=False, verbose_name="Ampliación")
    infra_remodelacion = models.BooleanField(default=False, verbose_name="Remodelación")
    infra_reconstruccion = models.BooleanField(default=False, verbose_name="Reconstrucción")
    infra_reubicacion = models.BooleanField(default=False, verbose_name="Reubicación")
    infra_mantenimiento_basico = models.BooleanField(default=False, verbose_name="Mantenimiento Básico")
    infra_equipamiento = models.BooleanField(default=False, verbose_name="Equipamiento")
    infra_observaciones = models.TextField(blank=True, default='', verbose_name="Observaciones")

    class Meta:
        verbose_name = "Datos Estadísticos"
        verbose_name_plural = "Datos Estadísticos"

    def __str__(self):
        return f"Datos Estadísticos del {self.date}"
