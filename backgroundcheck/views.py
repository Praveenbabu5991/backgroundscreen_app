from django.shortcuts import render
from . import mails 
from io import BytesIO
from email.generator import BytesGenerator
import base64
from apiclient import errors
#import templates
from django.http import HttpResponse
import pandas as pd


# Create your views here.
def home(request):
#    return HttpResponse("hii hello")
    return render(request,'bgcheck/home.html')

def result(request):
    data=pd.DataFrame()
    company1=request.GET['c1']
    company2=request.GET['c2']
    comp_list=[company1,company2]
    from_=[]
    time_=[]
    text_=[]
    subject_=[]
    to_=[]


    
    for company in comp_list:
        service=mails.get_service()
        id=mails.search_message(service,'me','has:attachment subject:'+company+' offer')
        print(id)
        #work on pass id and check for conditons and store result
        msg_att=GetAttachments(service,'me',id[-1])
        message = service.users().messages().get(userId='me', id=id[-1]).execute()
        #print(message)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        for items in message['payload']['headers']:
            if items['name']=="From":
                from_.append(items['value'])
            if items['name']=="To":
                to_.append(items['value'])
            if items['name']=="Date":
                time_.append(items['value'])  
            if items['name']=="Subject":
                subject_.append(items['value']) 
        print("text")
        print(message['snippet'])
        text_.append(message['snippet'])
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    data['From']=from_
    data['To']=to_
    data['Time']=time_
    data['Text']=text_
    data['Subject']=subject_
    file_name = 'BackData.xlsx'
    data.to_excel(file_name)
    return render(request,'bgcheck/result.html')


def GetAttachments(service, user_id, msg_id):
    """Get and store attachment from Message with given id.

    :param service: Authorized Gmail API service instance.
    :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    :param msg_id: ID of Message containing attachment.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
            if part['filename']:
                if 'data' in part['body']:
                    data = part['body']['data']
                    print(data)
                else:
                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
                    data = att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = part['filename']

                with open(path, 'w') as f:
                    f.write(str(file_data))

    except :
        print('An error occurred: %s')