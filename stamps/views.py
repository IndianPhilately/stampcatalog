from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Stamp, Year
from django.db.models.functions import ExtractYear
import random

def year_list(request):
    years = Year.objects.all().order_by('-year')
    all_stamps = list(Stamp.objects.all())
    random_stamps = random.sample(all_stamps, 5) if len(all_stamps) >= 5 else all_stamps
    return render(request, "stamps/year_list.html", {
        "years": years,
        "random_stamps": random_stamps,})

def year_detail(request, year):
    stamps = Stamp.objects.filter(issue_date__year=year)
    years = Year.objects.all().order_by('-year')  # add this line
    return render(request, 'stamps/year_detail.html', {'year': year, 'stamps': stamps, 'years': years,})

def stamp_detail(request, pk):
    stamp = get_object_or_404(Stamp, pk=pk)
    years = (Stamp.objects
             .annotate(year=ExtractYear('issue_date'))
             .values_list('year', flat=True)
             .distinct()
             .order_by('-year'))

    # Get the 3 most recent stamps before this one
    previous_stamps = (
        Stamp.objects.filter(issue_date__lt=stamp.issue_date)
        .order_by('-issue_date')[:3]
    )

    # Next 3 stamps
    next_stamps = (
        Stamp.objects.filter(issue_date__gt=stamp.issue_date)
        .order_by('issue_date')[:3]
    )

    # Related 3 stamps (same theme, excluding current)
    related_stamps = Stamp.objects.none()
    if stamp.keywords:
        keywords = [kw.strip() for kw in stamp.keywords.split(",") if kw.strip()]
        q_objects = Q()
        for kw in keywords:
            q_objects |= Q(keywords__icontains=kw)
        related_stamps = (Stamp.objects.filter(q_objects)
                          .exclude(pk=stamp.pk)
                          .order_by('-issue_date')[:3])

    return render(request, 'stamps/stamp_detail.html', {
        'stamp': stamp,
        'years': years,  # now a list of integers like [2025, 2024, 1947]
        'previous_stamps': previous_stamps,
        'next_stamps': next_stamps,
        'related_stamps': related_stamps,
    })


def stamp_search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Stamp.objects.filter(
            Q(name__icontains=query) |
            Q(theme__icontains=query) |
            Q(description__icontains=query) |
            Q(denomination__icontains=query) |
            Q(issue_date__year__icontains=query)
        )
    return render(request, 'stamps/stamp_search.html', {'query': query, 'results': results})