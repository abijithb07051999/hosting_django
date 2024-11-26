from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from library.crud_operations import CRUDOperations
from library.savefile import saveFile
from django.core.files.storage import FileSystemStorage
from django.http import QueryDict

from . import models, serializer
from classes.models import  ClassesModel
from classes.serializer import ClassesSerializer
from subject.models import SubjectModel
from subject.serializer import SubjectSerializer
url = 'http://localhost:8000/media'

class TeacherView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            sid = request.headers['School-Id']
            response = CRUDOperations.getFilteredData(model=models.TeacherModel, serializer=serializer.TeacherSerializer, teacher_school_id =sid)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.TeacherModel, serializer=serializer.TeacherSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Post Method
    def post(self, request):
        teacher_details={
            **request.POST.dict(),
            'teacher_image' : 'image'
        }
        check_serializer=serializer.TeacherSerializer(data=teacher_details)
        if check_serializer.is_valid():
            teacher_details['teacher_image']=saveFile(path="teacher",file=request.FILES['teacher_image'])
            response=CRUDOperations.addNewData(serializer=serializer.TeacherSerializer,data=teacher_details)
            if response['status']:
                return Response(data=response['data'],status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
       
        
    # ? Update Method   
    def put(self, request, id):
        if 'teacher_image' in request.POST:
            response = CRUDOperations.updateExistingData(model=models.TeacherModel, serializer=serializer.TeacherSerializer, id=id, data=request.data)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST) 
        else:
            teacher_details={
            **request.POST.dict(),
            'teacher_image' : 'image'
            }
            check_serializer=serializer.TeacherSerializer(data=teacher_details,partial=True)
            if check_serializer.is_valid():
                teacher_details['teacher_image']=saveFile(path="teacher",file=request.FILES['teacher_image'])
                response=CRUDOperations.updateExistingData(model=models.TeacherModel, serializer=serializer.TeacherSerializer, id=id, data=teacher_details)
                if response['status']:
                    return Response(data=response['data'],status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Delete Method  
    def delete(self ,request, id):
        class_response=CRUDOperations.getFilteredData(model=ClassesModel,serializer=ClassesSerializer,teacher_id=id)
        subject_response=CRUDOperations.getFilteredData(model=SubjectModel,serializer=SubjectSerializer,subject_teacher_id=id)
        if len(class_response)==0 and len(subject_response)==0:
            
            response = CRUDOperations.deleteExistingData(model=models.TeacherModel, id=id)
            if response:
                return Response(data="success",status=status.HTTP_200_OK)
            else:
                return Response(data="Failed",status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(data={
                'class': class_response,
                'subject':subject_response
            },status=status.HTTP_400_BAD_REQUEST)
            


class ClassBasedTeachersView(APIView):
    def get(self,request):
        class_id=request.headers['Class-Id']
        teachers_response=CRUDOperations.getFilteredData(model=ClassesModel,serializer=ClassesSerializer,id=class_id)