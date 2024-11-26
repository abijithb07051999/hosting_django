from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from library.crud_operations import CRUDOperations
from datetime import datetime
from calendar import month_name
from collections import defaultdict
from . import models, serializer

class RemainderView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            cid = request.headers['Class-Id']
            data=[]
            remainder_by_date={}
            remainder_response=CRUDOperations.getFilteredData(model=models.RemainderModels, serializer=serializer.RemainderSerializer, class_id=cid)
            for remain in remainder_response:
                date=remain['date']
                if date not in remainder_by_date:
                    remainder_by_date[date]=[]
                remainder_entry={
                    'id':remain['id'],
                    'remainder': remain['remainder']
                    }
                remainder_by_date[date].append(remainder_entry) 
            for date, remainder in remainder_by_date.items():
                data.append({'date': date, 'remainder': remainder})
            return Response(data=data, status=status.HTTP_200_OK)
            
        else:
            response = CRUDOperations.getSpecificData(model=models.RemainderModels, serializer=serializer.RemainderSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Post Method
    def post(self, request):
        remainder={
            **request.data.dict(),
            
            'weekday': datetime.strptime(request.data.get('date'), '%Y-%m-%d').strftime("%A")
            }
        response = CRUDOperations.addNewData(serializer=serializer.RemainderSerializer, data=remainder)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(data=response.errors,status=status.HTTP_400_BAD_REQUEST)
        
    # ? Update Method   
    def put(self, request, id):
        remainder={
            **request.data.dict(),
            
            }
        if 'date' in request.data:
            remainder['weekday']= datetime.strptime(request.data.get('date'), '%Y-%m-%d').strftime("%A")
        response = CRUDOperations.updateExistingData(model=models.RemainderModels, serializer=serializer.RemainderSerializer, id=id, data=remainder)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Delete Method  
    def delete(self ,request, id):
        response = CRUDOperations.deleteExistingData(model=models.RemainderModels, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
