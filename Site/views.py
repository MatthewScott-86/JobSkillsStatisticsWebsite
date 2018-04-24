# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from Site.forms import *
from Site.models import *
from Site import DisplayData
from django.views.generic import TemplateView
import datetime
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import render_to_string
import plotly.plotly as py
import plotly.graph_objs as go
import os


def glassdoor_database(request):
    data = pd.read_excel(os.path.join(settings.BASE_DIR, 'data/LPR_data-2018-01.xlsx'))
    data_html = data.to_html()
    context = {'loaded_data': data_html}
    return render(request, 'glassdoor_database.html', context)

def indeed_database(request):
    job_postings = JobPosting.objects.all()  # order by date
    return render(request, 'indeed_database.html', {'job_postings': job_postings})

def database(request):
    return render(request, 'database.html')

def landing_page(request):
    return render(request, 'index.html')


class IndeedPlot(TemplateView):
    template_name = "indeed.html"
    plotGenerator = DisplayData.PlotGenerator();
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndeedPlot, self).get_context_data(**kwargs)
        context['plot'] = self.plotGenerator.GetSkillsFromJobRegionDateCount(kwargs['job'], kwargs['city'])
        context['jobs'] = Jobs.objects.all().values_list('category', flat=True)
        cities_list = Cities.objects.all().values_list('City', 'Area')
        cities = []
        for city in cities_list:
            cities.append(city[0] + ", " + city[1])
        context['cities'] = cities
        return context

@csrf_exempt
def indeed(request):
    if request.method == 'GET' and 'job' in request.GET:
        job=request.GET['job']
        city=request.GET['city']
        g = IndeedPlot()
        context = g.get_context_data(job=job, city=city)
        return render(request, 'indeed.html', context)
    else:
        jobs = Jobs.objects.all().values_list('category', flat=True)
        cities_list = Cities.objects.all().values_list('City', 'Area')
        cities = []
        for city in cities_list:
            cities.append(city[0] + ", " + city[1])
        return render(request, 'indeed.html', {'jobs' : jobs, 'cities' : cities})

class IndeedComparePlot(TemplateView):
    plotGenerator = DisplayData.PlotGenerator();
    template_name = "indeed_compare.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndeedComparePlot, self).get_context_data(**kwargs)
        context['plot'] = self.plotGenerator.CompareJobsPlot(kwargs['job1'], kwargs['job2'])
        context['jobs'] = Jobs.objects.all().values_list('category', flat=True)
        return context

def indeed_compare(request):
    if request.method == 'GET' and 'job1' in request.GET:
        job1=request.GET['job1']
        job2=request.GET['job2']
        g = IndeedComparePlot()
        context = g.get_context_data(job1=job1, job2=job2)
        return render(request, 'indeed_compare.html', context)
    else:
        jobs = Jobs.objects.all().values_list('category', flat=True)
        return render(request, 'indeed_compare.html', {'jobs' : jobs})

class Plot(TemplateView):
    template_name = "plot.html"
    plotGenerator = DisplayData.PlotGenerator();
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot, self).get_context_data(**kwargs)
        context['plot'] = self.plotGenerator.GetSkillsFromJobRegion("data analyst", "Boston, MA")
        print(context['plot'])
        return context

class PlotGlassDoor(TemplateView):
    plotGenerator = DisplayData.PlotGenerator();
    template_name = "glassdoor.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlotGlassDoor, self).get_context_data(**kwargs)
        context['plot'] = self.plotGenerator.GlassdoorPlot1(kwargs['genstat'])
        return context

class PlotGlassDoorBox(TemplateView):
    plotGenerator = DisplayData.PlotGenerator();
    template_name = "glassdoor.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlotGlassDoorBox, self).get_context_data(**kwargs)
        context['plot6'] = self.plotGenerator.GlassdoorPlot6(kwargs['boxplot'])
        return context

class PlotGlassDoorBox2(TemplateView):
    plotGenerator = DisplayData.PlotGenerator();
    template_name = "glassdoor.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlotGlassDoorBox2, self).get_context_data(**kwargs)
        context['plot2'] = self.plotGenerator.GlassdoorPlot2(kwargs['boxplot'])
        return context

@csrf_exempt
def glassdoor(request):
    if request.method == 'GET' and 'genstat' in request.GET:
        genstat=request.GET['genstat']
        g = PlotGlassDoor()
        context = g.get_context_data(genstat=genstat)
        return render(request, 'glassdoor.html', context)
    elif request.method == 'GET' and 'boxplot' in request.GET:
        boxplot=request.GET['boxplot']
        if boxplot == 'Median Base Pay':
            g = PlotGlassDoorBox()
            context = g.get_context_data(boxplot=boxplot)
            return render(request, 'glassdoor.html', context)
        else:
            g = PlotGlassDoorBox2()
            context = g.get_context_data(boxplot=boxplot)
            return render(request, 'glassdoor.html', context)
    else:
        return render(request, 'glassdoor.html')