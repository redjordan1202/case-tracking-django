from threading import Thread
from django.shortcuts import render, get_object_or_404
from django.urls.conf import path
from django.http import HttpResponse, Http404, HttpResponseRedirect, request
from django.views import generic
from django.db.models import Q
from .models import Case
from decouple import config
from django.urls import reverse
import threading
from cases.variables import *
from simple_salesforce import Salesforce 
from django.utils import timezone


#Views
def IndexView(request):
    qs = Case.objects.all().order_by('case_number')
    search = request.GET.get('search')

    if search != '' and search is not None:
        qs = qs.filter(
            Q(case_number__icontains=search) | 
            Q(order_number__icontains=search) |
            Q(tracking_number__icontains=search)
            )
    
    context ={
        'cases': qs
    }
    return render(request, 'cases/cases.html', context)



class DetailsView(generic.DetailView):
    model = Case
    template_name = 'cases/details.html'


def ProcessView(request):
    return render(request, 'cases/process.html')

def GenerateView(request):
    
    CasesToProcess.reset_lists()

    sucessful_cases = []
    failed_cases = []

    data = request.POST.get('cases-process')
    case_list = data.split()
    
    process = request.POST.get('process')
    if process == 'True':
        processed = False
    if process == 'False':
        processed = True


    process_case(case_list, processed)
        
    for case in CasesToProcess.processed_cases:
        c = Case.objects.get(case_number = case)
        sucessful_cases.append(c)

    for case in CasesToProcess.failed_cases:
        failed_cases.append(case)

    context={
        'processed_cases':sucessful_cases,
        'failed_cases':failed_cases,
    }

    return render(request,'cases/generate.html',context)

def UnsentView(request):
    qs = Case.objects.all().filter(case_processed=False).order_by('case_number')
    context = {
        'cases': qs,
    }
    return render(request, 'cases/unsent.html', context)

def UpdateView(request, pk):
    case = get_object_or_404(Case, case_number=pk)
    case.case_processed = True
    case.save()

    return HttpResponseRedirect(reverse('cases:details', args=(case.case_number,)))


#None-View Classes

class CasesToProcess():
    case_list = []
    failed_cases = []
    processed_cases=[]

    def reset_lists():
        case_list = []
        failed_cases = []
        processed_cases=[]











#Non-View functions

def process_case(case_list,processed):

    #set up new_case varriable and log into salesforce
    sf = Salesforce(password=sf_passwd, username=sf_user, security_token=sf_token)

    for case in case_list:
        new_case = None
        case_number = case
    #verify that the case number is valid and formatted correctly for salesforce
        if case_number.isnumeric() != True:
            CasesToProcess.failed_cases.append(case_number)
            continue
        if len(case_number) < 6:
            case_number = case_number.zfill(6)



        query= sf.query_all_iter(
            "SELECT Order_ID__c, RMA_Type__c, Outgoing_Parts_Number__c, Tracking_Number_2__c, Case_Created_By__c, Repairs_Performed__c, Origin, Parts_Needed__c, Ship_With_Return_Label__c FROM Case WHERE caseNumber = '{}'".format(case_number)
        )
        for i in query:

            order_number = i.get('Order_ID__c')

        #gather case info
            rma_type = i.get('RMA_Type__c')
            case_creator = i.get('Case_Created_By__c')
            repair_notes = i.get('Repairs_Performed__c')
            if repair_notes == None:
                repair_notes = 'None'
            case_origin = i.get('Origin')
            part = i.get('Parts_Needed__c')
            if part == None:
                part = 'None'
            if i.get('Ship_With_Return_Label__c') == 'Yes':
                return_label = True
            if i.get('Ship_With_Return_Label__c') == 'No':
                return_label = False

            #finding out the tracking carrier
            if i.get('Tracking_Number_2__c') != None:
                tracking_number = i.get('Tracking_Number_2__c')
            else:
                tracking_number = i.get('Outgoing_Parts_Number__c')
            
            try: 
                tracking_length = len(tracking_number) 
                tracking_carrier = ''
            except:
                tracking_carrier = 'Check Tracking'

            if tracking_carrier != 'Check Tracking':
                if tracking_length != 18 or 22 or 12:
                        tracking_carrier = 'Other'
                if tracking_length == 18:
                        tracking_carrier = 'UPS'
                if tracking_length == 22:
                        tracking_carrier = 'USPS'   
                if tracking_length == 12:
                        tracking_carrier = 'Fedex'

        if case_origin != 'Amazon Messages':
            status = 'CA'

        if tracking_carrier == 'Other':
            status = 'CT'

        else:
            status = 'TS'


        if rma_type == 'Part':
            if return_label == False:
                tracking_message = part_msg % ( 
                    part,
                    tracking_carrier,
                    tracking_number             )
            else:
                tracking_message = part_with_label_msg % (  
                    part,
                    tracking_carrier,
                    tracking_number             )

        if rma_type == 'Repair':
            tracking_message = repair_msg % (   
                tracking_carrier,
                tracking_number,
                repair_notes
            )

        if rma_type == 'Replace':
            tracking_message = replace_msg % (  
                tracking_carrier,
                tracking_number         )


        date = timezone.now().date() 

        try:
            new_case = Case.objects.create(
                case_number = case_number,
                date = date,
                order_number = order_number,
                rma_type = rma_type,
                part = part,
                return_label = return_label,
                tracking_number = tracking_number,
                carrier = tracking_carrier,
                status = status,
                case_creator = case_creator,
                case_origin = case_origin,
                repair_notes = repair_notes,
                message = tracking_message, 
                case_processed = processed
                )
        except:
            CasesToProcess.failed_cases.append(case_number)
            continue

        sf.Case.upsert(
            f"caseNumber/{case_number}", {'Tracking_Number_Sent__c': 'Yes'}
        )
        new_case.save()
        CasesToProcess.processed_cases.append(case_number)
        continue
