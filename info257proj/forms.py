from django import forms
from .models import AnalysisData
from .models import NodeLocations
from .models import SpointData
from .models import HourlyLmp

#test = HourlyLmp.objects.count()
#print(test)
#test = AnalysisData.objects.filter(node='temp').count()
#print(test)

#######     Node Summary Query Options    ########
DISTINCT_NODES = list(AnalysisData.objects.order_by().values_list('node').distinct())
DISTINCT_NODES = tuple([(n[0],n[0]) for n in DISTINCT_NODES])

ANALYSIS_DATA = [a.name for a in AnalysisData._meta.get_fields()]
if 'node' in ANALYSIS_DATA:
	ANALYSIS_DATA.remove('node')


NODE_LOCATIONS = [n.name for n in NodeLocations._meta.get_fields()]
if 'node' in NODE_LOCATIONS:
	NODE_LOCATIONS.remove('node')
if 'optional' in NODE_LOCATIONS:
	NODE_LOCATIONS.remove('optional')

ANALYSIS_DATA = tuple([(n,n) for n in ANALYSIS_DATA])
NODE_LOCATIONS = tuple([(n,n) for n in NODE_LOCATIONS])
#NODE_SUMMARY_VALUES = NODE_LOCATIONS + ANALYSIS_DATA
#NODE_SUMMARY_VALUES = tuple([(n,n) for n in NODE_SUMMARY_VALUES])
#######################################################


############# Time Series Options##################
FREQUENCY = (
	('Daily', 'Daily'),
	('Hourly', 'Hourly'),
)
############################################


######################    SPoint Summary Queries Options   ################

SPOINT = list(SpointData.objects.order_by().values_list('node').distinct())
#SPOINT2 = list(SpointData.objects.order_by().values_list('node'))
#print(len(SPOINT))
#print(len(SPOINT2))
SPOINT = tuple([(s[0],s[0]) for s in SPOINT])

DATA_TYPE = (
	('Yearly', 'Yearly'),
	('Annual Average', 'Annual Average'),
)

######################################################################

class SearchTypeForm(forms.Form):
	search_type = forms.CharField(label = 'Search Type', max_length=100)

class TimeSeriesForm(forms.Form):
	node = forms.CharField(label = 'Node', max_length=100)
	SPoint = forms.CharField(label = 'SPointLMP', max_length=100, required=False)
	freq = forms.ChoiceField(choices=FREQUENCY, initial='Hourly')

class NodeSummaryQueryForm(forms.Form):
	node = forms.CharField(label = 'Node Names (Separate values with commmas)', max_length=400)
	analysis_data_values = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=ANALYSIS_DATA,required=True)
	node_locations_values = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=NODE_LOCATIONS,required=False)

class SPointSummaryQueryForm(forms.Form):
	node = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=SPOINT)
	data_type = forms.ChoiceField(choices=DATA_TYPE,initial='Yearly')


