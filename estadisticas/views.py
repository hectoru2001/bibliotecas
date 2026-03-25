from django.shortcuts import render, redirect
from .forms import LibraryVisitorStatsForm, DatosEstadisticosForm
from .models import LibraryVisitorStats, DatosEstadisticos
from django.db.models import Sum
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
import calendar

def stats_form(request):
    if request.method == 'POST':
        form = LibraryVisitorStatsForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the form data to the database
            return redirect('stats_form')  # Redirect after saving
    else:
        form = LibraryVisitorStatsForm()
    return render(request, 'stats/stats_form.html', {'form': form})

def submit_stats(request):
    return render(request, 'stats/confirmation.html')

def confirmation(request):
    return render(request, 'stats/confirmation.html')

def datos_estadisticos(request):
    if request.method == 'POST':
        form = DatosEstadisticosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datos_estadisticos')
    else:
        form = DatosEstadisticosForm()
    return render(request, 'stats/datos_estadisticos.html', {'form': form})


def monthly_log(request):
    context = {'months': range(1, 13), 'years': range(2020, 2026)}
    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        # Calculate the first and last day of the selected month
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1])
        # Query data for the selected month using 'date' field
        stats = LibraryVisitorStats.objects.filter(date__range=(first_day, last_day))
        # Aggregate sums for all fields
        aggregates = stats.aggregate(
            # Age Range: Adultos mayores de 60 años
            adults_over_60_males_sum=Sum('adults_over_60_males'),
            adults_over_60_females_sum=Sum('adults_over_60_females'),
            adults_over_60_preschool_sum=Sum('adults_over_60_preschool'),
            adults_over_60_primary_sum=Sum('adults_over_60_primary'),
            adults_over_60_secondary_sum=Sum('adults_over_60_secondary'),
            adults_over_60_preparatory_sum=Sum('adults_over_60_preparatory'),
            adults_over_60_undergraduate_sum=Sum('adults_over_60_undergraduate'),
            adults_over_60_postgraduate_sum=Sum('adults_over_60_postgraduate'),
            adults_over_60_household_sum=Sum('adults_over_60_household'),
            adults_over_60_employed_or_worker_sum=Sum('adults_over_60_employed_or_worker'),
            adults_over_60_unemployed_sum=Sum('adults_over_60_unemployed'),
            # Age Range: Adultos entre 30 y 59 años
            adults_30_to_59_males_sum=Sum('adults_30_to_59_males'),
            adults_30_to_59_females_sum=Sum('adults_30_to_59_females'),
            adults_30_to_59_preschool_sum=Sum('adults_30_to_59_preschool'),
            adults_30_to_59_primary_sum=Sum('adults_30_to_59_primary'),
            adults_30_to_59_secondary_sum=Sum('adults_30_to_59_secondary'),
            adults_30_to_59_preparatory_sum=Sum('adults_30_to_59_preparatory'),
            adults_30_to_59_undergraduate_sum=Sum('adults_30_to_59_undergraduate'),
            adults_30_to_59_postgraduate_sum=Sum('adults_30_to_59_postgraduate'),
            adults_30_to_59_household_sum=Sum('adults_30_to_59_household'),
            adults_30_to_59_employed_or_worker_sum=Sum('adults_30_to_59_employed_or_worker'),
            adults_30_to_59_students_sum=Sum('adults_30_to_59_students'),
            adults_30_to_59_unemployed_sum=Sum('adults_30_to_59_unemployed'),
            # Age Range: Adultos jóvenes entre 18 y 29 años
            young_adults_18_to_29_males_sum=Sum('young_adults_18_to_29_males'),
            young_adults_18_to_29_females_sum=Sum('young_adults_18_to_29_females'),
            young_adults_18_to_29_preschool_sum=Sum('young_adults_18_to_29_preschool'),
            young_adults_18_to_29_primary_sum=Sum('young_adults_18_to_29_primary'),
            young_adults_18_to_29_secondary_sum=Sum('young_adults_18_to_29_secondary'),
            young_adults_18_to_29_preparatory_sum=Sum('young_adults_18_to_29_preparatory'),
            young_adults_18_to_29_undergraduate_sum=Sum('young_adults_18_to_29_undergraduate'),
            young_adults_18_to_29_postgraduate_sum=Sum('young_adults_18_to_29_postgraduate'),
            young_adults_18_to_29_household_sum=Sum('young_adults_18_to_29_household'),
            young_adults_18_to_29_employed_or_worker_sum=Sum('young_adults_18_to_29_employed_or_worker'),
            young_adults_18_to_29_students_sum=Sum('young_adults_18_to_29_students'),
            young_adults_18_to_29_unemployed_sum=Sum('young_adults_18_to_29_unemployed'),
            # Age Range: Adolescentes entre 13 y 17 años
            adolescents_13_to_17_males_sum=Sum('adolescents_13_to_17_males'),
            adolescents_13_to_17_females_sum=Sum('adolescents_13_to_17_females'),
            adolescents_13_to_17_preschool_sum=Sum('adolescents_13_to_17_preschool'),
            adolescents_13_to_17_primary_sum=Sum('adolescents_13_to_17_primary'),
            adolescents_13_to_17_secondary_sum=Sum('adolescents_13_to_17_secondary'),
            adolescents_13_to_17_preparatory_sum=Sum('adolescents_13_to_17_preparatory'),
            adolescents_13_to_17_household_sum=Sum('adolescents_13_to_17_household'),
            adolescents_13_to_17_employed_or_worker_sum=Sum('adolescents_13_to_17_employed_or_worker'),
            adolescents_13_to_17_students_sum=Sum('adolescents_13_to_17_students'),
            adolescents_13_to_17_unemployed_sum=Sum('adolescents_13_to_17_unemployed'),
            # Age Range: Niños entre 0 y 12 años
            kids_0_to_12_males_sum=Sum('kids_0_to_12_males'),
            kids_0_to_12_females_sum=Sum('kids_0_to_12_females'),
            kids_0_to_12_preschool_sum=Sum('kids_0_to_12_preschool'),
            kids_0_to_12_primary_sum=Sum('kids_0_to_12_primary'),
            kids_0_to_12_household_sum=Sum('kids_0_to_12_household'),
            kids_0_to_12_students_sum=Sum('kids_0_to_12_students'),
            # Materials Used
            general_collection_sum=Sum('general_collection'),
            reference_collection_sum=Sum('reference_collection'),
            children_collection_sum=Sum('children_collection'),
            audiovisual_sum=Sum('audiovisual'),
            publications_sum=Sum('publications'),
            ludoteca_sum=Sum('ludoteca'),
            braille_sum=Sum('braille'),
            special_collection_sum=Sum('special_collection'),
            state_collection_sum=Sum('state_collection'),
            # Credentials Issued
            physical_loan_sum=Sum('physical_loan'),
            credentials_issued_males_sum=Sum('credentials_issued_males'),
            credentials_issued_females_sum=Sum('credentials_issued_females'),
            # Reading Promotion
            reading_promotion_adults_over_60_males_sum=Sum('reading_promotion_adults_over_60_males'),
            reading_promotion_adults_over_60_females_sum=Sum('reading_promotion_adults_over_60_females'),
            reading_promotion_adults_30_to_59_males_sum=Sum('reading_promotion_adults_30_to_59_males'),
            reading_promotion_adults_30_to_59_females_sum=Sum('reading_promotion_adults_30_to_59_females'),
            reading_promotion_young_adults_18_to_29_males_sum=Sum('reading_promotion_young_adults_18_to_29_males'),
            reading_promotion_young_adults_18_to_29_females_sum=Sum('reading_promotion_young_adults_18_to_29_females'),
            reading_promotion_adolescents_13_to_17_males_sum=Sum('reading_promotion_adolescents_13_to_17_males'),
            reading_promotion_adolescents_13_to_17_females_sum=Sum('reading_promotion_adolescents_13_to_17_females'),
            reading_promotion_children_0_to_12_males_sum=Sum('reading_promotion_children_0_to_12_males'),
            reading_promotion_children_0_to_12_females_sum=Sum('reading_promotion_children_0_to_12_females'),
            # Guided Visits
            guided_visits_adults_over_60_males_sum=Sum('guided_visits_adults_over_60_males'),
            guided_visits_adults_over_60_females_sum=Sum('guided_visits_adults_over_60_females'),
            guided_visits_adults_30_to_59_males_sum=Sum('guided_visits_adults_30_to_59_males'),
            guided_visits_adults_30_to_59_females_sum=Sum('guided_visits_adults_30_to_59_females'),
            guided_visits_young_adults_18_to_29_males_sum=Sum('guided_visits_young_adults_18_to_29_males'),
            guided_visits_young_adults_18_to_29_females_sum=Sum('guided_visits_young_adults_18_to_29_females'),
            guided_visits_adolescents_13_to_17_males_sum=Sum('guided_visits_adolescents_13_to_17_males'),
            guided_visits_adolescents_13_to_17_females_sum=Sum('guided_visits_adolescents_13_to_17_females'),
            guided_visits_children_0_to_12_males_sum=Sum('guided_visits_children_0_to_12_males'),
            guided_visits_children_0_to_12_females_sum=Sum('guided_visits_children_0_to_12_females'),
            # Digital Services
            digital_services_adults_over_60_males_sum=Sum('digital_services_adults_over_60_males'),
            digital_services_adults_over_60_females_sum=Sum('digital_services_adults_over_60_females'),
            digital_services_adults_30_to_59_males_sum=Sum('digital_services_adults_30_to_59_males'),
            digital_services_adults_30_to_59_females_sum=Sum('digital_services_adults_30_to_59_females'),
            digital_services_young_adults_18_to_29_males_sum=Sum('digital_services_young_adults_18_to_29_males'),
            digital_services_young_adults_18_to_29_females_sum=Sum('digital_services_young_adults_18_to_29_females'),
            digital_services_adolescents_13_to_17_males_sum=Sum('digital_services_adolescents_13_to_17_males'),
            digital_services_adolescents_13_to_17_females_sum=Sum('digital_services_adolescents_13_to_17_females'),
            digital_services_children_0_to_12_males_sum=Sum('digital_services_children_0_to_12_males'),
            digital_services_children_0_to_12_females_sum=Sum('digital_services_children_0_to_12_females'),
        )
        context.update({
            'stats': stats,
            'selected_month': month,
            'selected_year': year,
            'aggregates': aggregates
        })
    return render(request, 'stats/monthly_log.html', context)