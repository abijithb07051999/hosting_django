from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from library.crud_operations import CRUDOperations
from django.core.files.storage import FileSystemStorage
from django.http import QueryDict
from library.savefile import saveFile
from . import models, serializer
url = 'http://localhost:8000/media'

class StudentView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            sid = request.headers['School-Id']
            cid = request.headers['Class-Id']
            response = CRUDOperations.getFilteredData(model=models.StudentModel, serializer=serializer.StudentSerializer, student_school_id =sid, student_class_id = cid)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.StudentModel, serializer=serializer.StudentSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Post Method
    def post(self, request):
        student_details = {
            **request.POST.dict(),
            'student_image' : 'path',
        }
        if 'guardian_1_image' not in request.FILES:
            student_details['guardian_1_image'] = "http://localhost:8000/placeholder/avatar-01.jpg"
        else:
            student_details['guardian_1_image']="path"
            
        if 'guardian_2_name' in request.POST:
            if 'guardian_2_image' not in request.FILES:
                student_details['guardian_2_image'] = "http://localhost:8000/placeholder/avatar-01.jpg"
            else:
                student_details['guardian_2_image']="path"
        else:
            student_details['guardian_2_image']="http://localhost:8000/placeholder/avatar-01.jpg"       
                    
        serialize_detail = serializer.StudentSerializer(data=student_details)
        if serialize_detail.is_valid():
            student_details['student_image'] = saveFile(path='student/student',file=request.FILES['student_image'])
            if student_details['guardian_1_image'] == "path":
                student_details['guardian_1_image'] =saveFile(path='student/guardian',file=request.FILES['guardian_1_image'])
            if student_details['guardian_2_image'] == "path":
                student_details['guardian_2_image'] =saveFile(path='student/guardian',file=request.FILES['guardian_2_image'])
            
            print(student_details)
            response = CRUDOperations.addNewData(serializer=serializer.StudentSerializer, data=student_details)
            if response['status']:  
                return Response(data=response['data'], status=status.HTTP_200_OK)
            
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Serializer Failure")
            return Response(status=status.HTTP_400_BAD_REQUEST)   
        
        
    # ? Update Method   
    def put(self, request, id):
        student_image = False
        guardian_1_image = False
        guardian_2_image = False
        print(request.POST)
        print(request.FILES)
        student_details = {
            **request.POST.dict()
        }
        if 'student_image' in request.POST and 'guardian_1_image' in request.POST and 'guardian_2_image' in request.POST:
            
            response = CRUDOperations.updateExistingData(model=models.StudentModel, serializer=serializer.StudentSerializer, id=id, data=request.data)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if 'student_image' in request.FILES:
                student_details['student_image'] = 'path'
                student_image = True
            if 'guardian_1_image' in request.FILES:
                student_details['guardian_1_image'] = 'path'
                guardian_1_image = True
            if 'guardian_2_image' in request.FILES:
                student_details['guardian_2_image'] = 'path'
                guardian_2_image = True
            
            serialize_detail = serializer.StudentSerializer(data=student_details)
            if serialize_detail.is_valid():
                if student_image:
                    student_details['student_image'] = saveFile(path='student/student',file=request.FILES['student_image'])
                if guardian_1_image:
                    student_details['guardian_1_image'] =saveFile(path='student/guardian',file=request.FILES['guardian_1_image'])
                if guardian_2_image:
                    student_details['guardian_2_image'] =saveFile(path='student/guardian',file=request.FILES['guardian_2_image'])
                response = CRUDOperations.updateExistingData(model=models.StudentModel, serializer=serializer.StudentSerializer, id=id, data=student_details)
                if response['status']:  
                    return Response(data=response['data'], status=status.HTTP_200_OK)
                
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                print("Serializer Failure")
                return Response(status=status.HTTP_400_BAD_REQUEST)    
            
    # ? Delete Method  
    def delete(self ,request, id):
        response = CRUDOperations.deleteExistingData(model=models.StudentModel, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

