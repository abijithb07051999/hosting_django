from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from library.crud_operations import CRUDOperations
from datetime import datetime
from calendar import month_name
from collections import defaultdict
from . import models, serializer
from subject.models import SubjectModel
from subject.serializer import SubjectSerializer

class PortionView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            cid = request.headers['Class-Id']
            class_portions = CRUDOperations.getFilteredData(model=models.PortionModel,serializer=serializer.PortionSerializer,class_id=cid)[::-1]
            data = []
            portions_by_date = defaultdict(lambda: defaultdict(list))
            
            for entry in class_portions:
                date = entry['date']
                subject_id = entry['subject_id']
                
                subjects_data = CRUDOperations.getSpecificData(
                    model=SubjectModel,
                    serializer=SubjectSerializer,
                    id=subject_id
                )
                subject_name = subjects_data['data']['subject_name']
                portions_by_date[date][subject_name].append({'id':entry['id'],'portion':entry['portion']})
            for date, subjects in portions_by_date.items():
                portions = [
                    {
                        'subject': subject,
                        'portions': portions  
                    }
                    for subject, portions in subjects.items()
                ]
                data.append({'date': date, 'portion': portions})
            
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.PortionModel, serializer=serializer.PortionSerializer, id=id)
            
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Post Method
    def post(self, request):
        print(request.POST)
        portions={
            **request.data.dict(),
            
            'weekday': datetime.strptime(request.data.get('date'), '%Y-%m-%d').strftime("%A")
            }
        response = CRUDOperations.addNewData(serializer=serializer.PortionSerializer, data=portions)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Update Method   
    def put(self, request, id):
        portions={
            **request.data.dict(),
            
            }
        if 'date' in request.data:
            portions['weekday']= datetime.strptime(request.data.get('date'), '%Y-%m-%d').strftime("%A")
        response = CRUDOperations.updateExistingData(model=models.PortionModel, serializer=serializer.PortionSerializer, id=id, data=portions)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Delete Method  
    def delete(self ,request, id):
        response = CRUDOperations.deleteExistingData(model=models.PortionModel, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
