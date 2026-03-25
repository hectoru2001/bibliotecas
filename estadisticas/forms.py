from django import forms
from .models import LibraryVisitorStats, DatosEstadisticos

class LibraryVisitorStatsForm(forms.ModelForm):
    class Meta:
        model = LibraryVisitorStats
        exclude = ['date']  # Exclude the 'date' field since it's auto-set
        widgets = {
            # Adultos mayores de 60 años
            'adults_over_60_males': forms.NumberInput(attrs={'min': 0}),
            'adults_over_60_females': forms.NumberInput(attrs={'min': 0}),
            'adults_over_60_preschool': forms.NumberInput(attrs={'min': 0}),
            'adults_over_60_primary': forms.NumberInput(attrs={'min': 0}),
            'adults_over_60_secondary': forms.NumberInput(attrs={'min': 0}),
            'adults_over_60_preparatory': forms.NumberInput(attrs={'min': 0}),
            'adults_over_60_undergraduate': forms.NumberInput(attrs={'min': 0}),
            'adults_over_60_postgraduate': forms.NumberInput(attrs={'min': 0}),
            'adults_over_60_household': forms.NumberInput(attrs={'min': 0}),
            'adults_over_60_employed_or_worker': forms.NumberInput(attrs={'min': 0}),
            'adults_over_60_students': forms.NumberInput(attrs={'min': 0}),
            'adults_over_60_unemployed': forms.NumberInput(attrs={'min': 0}),

            # Adultos entre 30 y 59 años
            'adults_30_to_59_males': forms.NumberInput(attrs={'min': 0}),
            'adults_30_to_59_females': forms.NumberInput(attrs={'min': 0}),
            'adults_30_to_59_preschool': forms.NumberInput(attrs={'min': 0}),
            'adults_30_to_59_primary': forms.NumberInput(attrs={'min': 0}),
            'adults_30_to_59_secondary': forms.NumberInput(attrs={'min': 0}),
            'adults_30_to_59_preparatory': forms.NumberInput(attrs={'min': 0}),
            'adults_30_to_59_undergraduate': forms.NumberInput(attrs={'min': 0}),
            'adults_30_to_59_postgraduate': forms.NumberInput(attrs={'min': 0}),
            'adults_30_to_59_household': forms.NumberInput(attrs={'min': 0}),
            'adults_30_to_59_employed_or_worker': forms.NumberInput(attrs={'min': 0}),
            'adults_30_to_59_students': forms.NumberInput(attrs={'min': 0}),
            'adults_30_to_59_unemployed': forms.NumberInput(attrs={'min': 0}),

            # Adultos jóvenes entre 18 y 29 años
            'young_adults_18_to_29_males': forms.NumberInput(attrs={'min': 0}),
            'young_adults_18_to_29_females': forms.NumberInput(attrs={'min': 0}),
            'young_adults_18_to_29_preschool': forms.NumberInput(attrs={'min': 0}),
            'young_adults_18_to_29_primary': forms.NumberInput(attrs={'min': 0}),
            'young_adults_18_to_29_secondary': forms.NumberInput(attrs={'min': 0}),
            'young_adults_18_to_29_preparatory': forms.NumberInput(attrs={'min': 0}),
            'young_adults_18_to_29_undergraduate': forms.NumberInput(attrs={'min': 0}),
            'young_adults_18_to_29_postgraduate': forms.NumberInput(attrs={'min': 0}),
            'young_adults_18_to_29_household': forms.NumberInput(attrs={'min': 0}),
            'young_adults_18_to_29_employed_or_worker': forms.NumberInput(attrs={'min': 0}),
            'young_adults_18_to_29_students': forms.NumberInput(attrs={'min': 0}),
            'young_adults_18_to_29_unemployed': forms.NumberInput(attrs={'min': 0}),

            # Adolescentes entre 13 y 17 años
            'adolescents_13_to_17_males': forms.NumberInput(attrs={'min': 0}),
            'adolescents_13_to_17_females': forms.NumberInput(attrs={'min': 0}),
            'adolescents_13_to_17_preschool': forms.NumberInput(attrs={'min': 0}),
            'adolescents_13_to_17_primary': forms.NumberInput(attrs={'min': 0}),
            'adolescents_13_to_17_secondary': forms.NumberInput(attrs={'min': 0}),
            'adolescents_13_to_17_preparatory': forms.NumberInput(attrs={'min': 0}),
            'adolescents_13_to_17_household': forms.NumberInput(attrs={'min': 0}),
            'adolescents_13_to_17_employed_or_worker': forms.NumberInput(attrs={'min': 0}),
            'adolescents_13_to_17_students': forms.NumberInput(attrs={'min': 0}),
            'adolescents_13_to_17_unemployed': forms.NumberInput(attrs={'min': 0}),

            #Niños entre 0 y 12 años
            'kids_0_to_12_males' : forms.NumberInput(attrs={'min': 0}),
            'kids_0_to_12_females' : forms.NumberInput(attrs={'min': 0}),
            'kids_0_to_12_preschool' : forms.NumberInput(attrs={'min': 0}),
            'kids_0_to_12_primary' : forms.NumberInput(attrs={'min': 0}),
            'kids_0_to_12_secondary' : forms.NumberInput(attrs={'min': 0}),
            'kids_0_to_12_household' : forms.NumberInput(attrs={'min': 0}),
            'kids_0_to_12_students' : forms.NumberInput(attrs={'min': 0}),


            # Materiales Utilizados
            'general_collection': forms.NumberInput(attrs={'min': 0}),
            'reference_collection': forms.NumberInput(attrs={'min': 0}),
            'children_collection': forms.NumberInput(attrs={'min': 0}),
            'audiovisual': forms.NumberInput(attrs={'min': 0}),
            'publications': forms.NumberInput(attrs={'min': 0}),
            'ludoteca': forms.NumberInput(attrs={'min': 0}),
            'braille': forms.NumberInput(attrs={'min': 0}),
            'special_collection': forms.NumberInput(attrs={'min': 0}),
            'state_collection': forms.NumberInput(attrs={'min': 0}),

            # Credenciales Expedidas
            'physical_loan': forms.NumberInput(attrs={'min': 0}),
            'credentials_issued_males': forms.NumberInput(attrs={'min': 0}),
            'credentials_issued_females': forms.NumberInput(attrs={'min': 0}),

            # Actividades de Fomento a la Lectura
            'reading_promotion_adults_over_60_males': forms.NumberInput(attrs={'min': 0}),
            'reading_promotion_adults_over_60_females': forms.NumberInput(attrs={'min': 0}),
            'reading_promotion_adults_30_to_59_males': forms.NumberInput(attrs={'min': 0}),
            'reading_promotion_adults_30_to_59_females': forms.NumberInput(attrs={'min': 0}),
            'reading_promotion_young_adults_18_to_29_males': forms.NumberInput(attrs={'min': 0}),
            'reading_promotion_young_adults_18_to_29_females': forms.NumberInput(attrs={'min': 0}),
            'reading_promotion_adolescents_13_to_17_males': forms.NumberInput(attrs={'min': 0}),
            'reading_promotion_adolescents_13_to_17_females': forms.NumberInput(attrs={'min': 0}),
            'reading_promotion_children_0_to_12_males': forms.NumberInput(attrs={'min': 0}),
            'reading_promotion_children_0_to_12_females': forms.NumberInput(attrs={'min': 0}),

            # Visitas Guiadas
            'guided_visits_adults_over_60_males': forms.NumberInput(attrs={'min': 0}),
            'guided_visits_adults_over_60_females': forms.NumberInput(attrs={'min': 0}),
            'guided_visits_adults_30_to_59_males': forms.NumberInput(attrs={'min': 0}),
            'guided_visits_adults_30_to_59_females': forms.NumberInput(attrs={'min': 0}),
            'guided_visits_young_adults_18_to_29_males': forms.NumberInput(attrs={'min': 0}),
            'guided_visits_young_adults_18_to_29_females': forms.NumberInput(attrs={'min': 0}),
            'guided_visits_adolescents_13_to_17_males': forms.NumberInput(attrs={'min': 0}),
            'guided_visits_adolescents_13_to_17_females': forms.NumberInput(attrs={'min': 0}),
            'guided_visits_children_0_to_12_males': forms.NumberInput(attrs={'min': 0}),
            'guided_visits_children_0_to_12_females': forms.NumberInput(attrs={'min': 0}),



            # Actividades Artísticas Culturales
            'cultural_activity_type': forms.Select(attrs={'style': 'width:100%;padding:8px;border:1px solid #ddd;border-radius:4px;font-size:14px;color:#333;'}),
            'cultural_adults_over_60_males': forms.NumberInput(attrs={'min': 0}),
            'cultural_adults_over_60_females': forms.NumberInput(attrs={'min': 0}),
            'cultural_adults_30_to_59_males': forms.NumberInput(attrs={'min': 0}),
            'cultural_adults_30_to_59_females': forms.NumberInput(attrs={'min': 0}),
            'cultural_young_adults_18_to_29_males': forms.NumberInput(attrs={'min': 0}),
            'cultural_young_adults_18_to_29_females': forms.NumberInput(attrs={'min': 0}),
            'cultural_adolescents_13_to_17_males': forms.NumberInput(attrs={'min': 0}),
            'cultural_adolescents_13_to_17_females': forms.NumberInput(attrs={'min': 0}),
            'cultural_children_0_to_12_males': forms.NumberInput(attrs={'min': 0}),
            'cultural_children_0_to_12_females': forms.NumberInput(attrs={'min': 0}),

            # Módulo de Servicios Digitales
            'digital_services_adults_over_60_males': forms.NumberInput(attrs={'min': 0}),
            'digital_services_adults_over_60_females': forms.NumberInput(attrs={'min': 0}),
            'digital_services_adults_30_to_59_males': forms.NumberInput(attrs={'min': 0}),
            'digital_services_adults_30_to_59_females': forms.NumberInput(attrs={'min': 0}),
            'digital_services_young_adults_18_to_29_males': forms.NumberInput(attrs={'min': 0}),
            'digital_services_young_adults_18_to_29_females': forms.NumberInput(attrs={'min': 0}),
            'digital_services_adolescents_13_to_17_males': forms.NumberInput(attrs={'min': 0}),
            'digital_services_adolescents_13_to_17_females': forms.NumberInput(attrs={'min': 0}),
            'digital_services_children_0_to_12_males': forms.NumberInput(attrs={'min': 0}),
            'digital_services_children_0_to_12_females': forms.NumberInput(attrs={'min': 0}),
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in cleaned_data:
            if isinstance(cleaned_data[field], int) and cleaned_data[field] < 0:
                raise forms.ValidationError(f"El campo {field} no puede ser negativo.")
        return cleaned_data


class DatosEstadisticosForm(forms.ModelForm):
    class Meta:
        model = DatosEstadisticos
        exclude = ['date']
        widgets = {
            # Libros Más Leídos
            'libros_general': forms.NumberInput(attrs={'min': 0}),
            'libros_consulta': forms.NumberInput(attrs={'min': 0}),
            'libros_infantil': forms.NumberInput(attrs={'min': 0}),

            # Colección SEP-Centenaria
            'sep_titulos_consultados': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ingrese los títulos más consultados...', 'style': 'width:100%;padding:8px;border:1px solid #ddd;border-radius:4px;font-size:14px;'}),
            'sep_total_libros_prestados': forms.NumberInput(attrs={'min': 0}),
            'sep_adults_over_60_males': forms.NumberInput(attrs={'min': 0}),
            'sep_adults_over_60_females': forms.NumberInput(attrs={'min': 0}),
            'sep_adults_30_to_59_males': forms.NumberInput(attrs={'min': 0}),
            'sep_adults_30_to_59_females': forms.NumberInput(attrs={'min': 0}),
            'sep_young_adults_18_to_29_males': forms.NumberInput(attrs={'min': 0}),
            'sep_young_adults_18_to_29_females': forms.NumberInput(attrs={'min': 0}),
            'sep_adolescents_13_to_17_males': forms.NumberInput(attrs={'min': 0}),
            'sep_adolescents_13_to_17_females': forms.NumberInput(attrs={'min': 0}),
            'sep_children_0_to_12_males': forms.NumberInput(attrs={'min': 0}),
            'sep_children_0_to_12_females': forms.NumberInput(attrs={'min': 0}),
            'sep_mochila_viajera': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),

            # Mejoramiento de la Infraestructura
            'infra_ampliacion': forms.CheckboxInput(),
            'infra_remodelacion': forms.CheckboxInput(),
            'infra_reconstruccion': forms.CheckboxInput(),
            'infra_reubicacion': forms.CheckboxInput(),
            'infra_mantenimiento_basico': forms.CheckboxInput(),
            'infra_equipamiento': forms.CheckboxInput(),
            'infra_observaciones': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escriba sus observaciones aquí...', 'style': 'width:100%;padding:8px;border:1px solid #ddd;border-radius:4px;font-size:14px;'}),
        }