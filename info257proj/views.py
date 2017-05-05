from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Avg
from .forms import TimeSeriesForm
from .forms import SearchTypeForm
from .forms import NodeSummaryQueryForm
from .forms import SPointSummaryQueryForm
from django.http import HttpResponseRedirect

from info257proj.models import AnalysisData
from info257proj.models import NodeLocations
from info257proj.models import SpointData
from info257proj.models import BowenTest
from info257proj.models import SpointLmp
from info257proj.models import HourlyLmp

def test_page(request):
	html = "<html><body> Hi, this is the test page! </body></html>" 
	return HttpResponse(html)

def download(request):
	if request.method == 'POST':
		replaced = request.POST['data'].replace("'","")
		replaced = replaced.replace("[","")
		replaced = replaced.replace("]]","")
		replaced = replaced.replace("],","\n")	
		replaced = replaced.replace(" ","")
		replaced = replaced.rstrip()
		#replaced = replaced.replace("\n","!")
		#print(replaced)
		#print(request.POST['data'])
		f = open('output.csv','w+')
		f.write(replaced)
		f.close()
		html = "<html><body> Downloaded result as CSV </body></html>" 
		return HttpResponse(html)
	else:
		html = "<html><body> Nothing set up yet for this query</body></html>" 
		return HttpResponse(html)

def search_type(request):
	if request.method == 'POST':
		if request.POST.get("Time Series"):
			return HttpResponseRedirect('/search_time_series/')
		elif request.POST.get("Node Summary Queries"):
			return HttpResponseRedirect('/search_node_summary_queries/')
		elif request.POST.get("SPoint Summary Queries"):
			return HttpResponseRedirect('/search_spoint_summary_queries/')
		else:
			html = "<html><body> Nothing set up yet for this query</body></html>" 
			return HttpResponse(html)

	else:
		form = SearchTypeForm()

	return render(request,'search_type.html', {'form':form})

def search_time_series(request):
	if request.method == 'POST':
		form = TimeSeriesForm(request.POST)
		if form.is_valid():
			results = make_time_series_query(form.cleaned_data)
			return render(request,'results.html',{'data':results})
	
	else:
		form = TimeSeriesForm()

	return render(request,'home.html', {'form': form, 'path':'/search_time_series/'})

#CURRENTLY USING A SMALLER TABLE TO SPEED QUERIES 
def make_time_series_query(data):

	results = [['Bus Name', 'Delivery Date']]
	

	nodes = BowenTest.objects.filter(busname=data['node'])
	distinct_dates = nodes.order_by().values_list('deliverydate').distinct()
	#print("distinct dates: ", len(list(distinct_dates)))

	if data['SPoint'] != '':
		spoint = SpointLmp.objects.filter(spoint=data['SPoint'])
		#print("Length: ", len(spoint))
	if data['freq'] == 'Daily':
		results[0].append('Average LMP')
		if data['SPoint'] != '':
			results[0].append('SPoint')
			results[0].append('Average SPoint_LMP')
		averages = nodes.values('deliverydate').annotate(average=Avg('lmp'))
		for a in averages:
			temp=[data['node']]
			temp.append(a['deliverydate'])
			temp.append(a['average'])
			

			
			temp_point = spoint.filter(date=a['deliverydate'])
			spoint_averages = temp_point.values('date').annotate(average=Avg('spoint_lmp'))
			for s in spoint_averages:
				temp.append(data['SPoint'])
				temp.append(s['average'])
			results.append(temp)
	else:
		results[0].append('Hourly Ending')
		results[0].append('LMP')
		for n in nodes:
			temp = [getattr(n,'busname')]
			deliv_date = getattr(n,'deliverydate')
			
			hr_ending = getattr(n,'hourending')

			temp.append(deliv_date)
			temp.append(hr_ending)
			temp.append(getattr(n,'lmp'))

			if data['SPoint'] != '':
				temp_point = spoint.filter(date=deliv_date,hourending=hr_ending)
				#print("length:", len(temp))
				#print("Delivdate: ", deliv_date, " Hour ending: ", hr_ending)
				for s in temp_point:
					temp.append(getattr(s,'spoint'))
					temp.append(getattr(s,'spoint_lmp'))

			results.append(temp)
		if data['SPoint'] != '':		
			results[0].append('SPoint')
			results[0].append('SPoint_LMP')
	
	return results


def search_node_summary_queries(request):
	if request.method == 'POST':
		form = NodeSummaryQueryForm(request.POST)
		if form.is_valid():
			results = make_node_summary_query(form.cleaned_data)
			return render(request,'results.html',{'data':results})

	else:
		form = NodeSummaryQueryForm()
	return render(request,'home.html', {'form': form, 'path': '/search_node_summary_queries/'})

def make_node_summary_query(data):
	nodes = data['node'].split(',')
	nodes = [n.lstrip() for n in nodes]
	analysis_data_values = data['analysis_data_values']
	node_locations_values = data['node_locations_values']

	results = [['node']+analysis_data_values+node_locations_values]
	for node in nodes:
		temp = [node]
		node_analysis_data = list(AnalysisData.objects.filter(node=node))
		node_loc = list(NodeLocations.objects.filter(node=node))
		if len(node_analysis_data) > 0:
			node_analysis_data = node_analysis_data[0]
			for a in analysis_data_values:
				temp.append(getattr(node_analysis_data,a))
		if len(node_loc) > 0:
			node_loc = node_loc[0]
			for l in node_locations_values:
				temp.append(getattr(node_loc,l))
		results.append(temp)


	return results

def search_spoint_summary_queries(request):
	if request.method == 'POST':
		form = SPointSummaryQueryForm(request.POST)
		if form.is_valid():
			results = make_spoint_summary_query(form.cleaned_data)
			return render(request,'results.html',{'data':results})
	
	else:
		form = SPointSummaryQueryForm()

	return render(request,'home.html', {'form': form, 'path': '/search_spoint_summary_queries/' })


def make_spoint_summary_query(data):
	if data['data_type'] == 'Yearly':
		results = [['node','revenue','production','yield_field','year']]
		for n in data['node']:
			for point in SpointData.objects.filter(node=n):
				temp = [getattr(point,'node'),getattr(point,'revenue'),getattr(point,'production'),getattr(point,'yield_field'),getattr(point,'year')]
				results.append(temp)
		return results
	else:

		spoint_attributes = ['revenue','production','yield_field']

		results = [['node','revenue','production','yield_field']]
		nodes = data['node']#.split(',')
		for n in nodes:
			temp = [n]
			node_spoints = SpointData.objects.filter(node=n)

			temp.append(node_spoints.aggregate(Avg('revenue'))['revenue__avg'])
			temp.append(node_spoints.aggregate(Avg('production'))['production__avg'])
			temp.append(node_spoints.aggregate(Avg('yield_field'))['yield_field__avg'])

			results.append(temp)

	return results


