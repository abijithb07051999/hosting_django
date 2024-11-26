from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from library.crud_operations import CRUDOperations
from . import models, serializer
from teacher.models import TeacherModel
from teacher.serializer import TeacherSerializer
from classes.models import ClassesModel
from classes.serializer import ClassesSerializer

class SubjectView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            cid = request.headers['Class-Id']
            class_response=CRUDOperations.getSpecificData(model=ClassesModel,serializer=ClassesSerializer,id=cid)
            
            data={
                'class_id':cid,
                'class_name':class_response['data']['class_name'],
                'subjects':[]
                
            }
            response = CRUDOperations.getFilteredData(model=models.SubjectModel, serializer=serializer.SubjectSerializer, subject_class_id = cid)
            for entry in response:
                teacher_response=CRUDOperations.getSpecificData(model=TeacherModel,serializer=TeacherSerializer,id=entry['subject_teacher_id'])
                subject_entry={
                    'subject_id':entry['id'],
                    'subject_name': entry['subject_name'],
                    'teacher_id':teacher_response['data']['id'],
                    'teacher_name':teacher_response['data']['teacher_name'],
                    'teacher_image':teacher_response['data']['teacher_image']
                }
                data['subjects'].append(subject_entry)
                
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.SubjectModel, serializer=serializer.SubjectSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Post Method
    def post(self, request):
        response = CRUDOperations.addNewData(serializer=serializer.SubjectSerializer, data=request.data)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Update Method   
    def put(self, request, id):
        response = CRUDOperations.updateExistingData(model=models.SubjectModel, serializer=serializer.SubjectSerializer, id=id, data=request.data)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Delete Method  
    def delete(self ,request, id):
        response = CRUDOperations.deleteExistingData(model=models.SubjectModel, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
