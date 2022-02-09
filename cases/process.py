from datetime import date
import threading
from simple_salesforce import Salesforce 
from decouple import Config, RepositoryEnv
from django.utils import timezone
import threading
from .models import Case
from cases.variables import *

def process_case(case_list,processed):

    #set up new_case varriable and log into salesforce
    sf = Salesforce(password=sf_passwd, username=sf_user, security_token=sf_token)
    


    for case in case_list:
        new_case = None

    #verify that the case number is valid and formatted correctly for salesforce
        if case.isnumeric() != True:
            return False
        if len(case) < 6:
            case = case.zfill(6)


        case_number = case

        query= sf.query_all_iter(
            "SELECT Order_ID__c, RMA_Type__c, Outgoing_Parts_Number__c, Tracking_Number_2__c, Case_Created_By__c, Repairs_Performed__c, Origin, Parts_Needed__c, Ship_With_Return_Label__c FROM Case WHERE caseNumber = '{}'".format(case)
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
            return False

        sf.Case.upsert(
            f"case_number/{case_number}", {'Tracking_Number_Sent__c': 'Yes'}
        )
        new_case.save()
        return True

