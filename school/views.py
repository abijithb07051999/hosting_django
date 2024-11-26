from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from library.crud_operations import CRUDOperations

from category.models import CategoryModel
from category.serializer import CategorySerializer
from django.core.files.storage import FileSystemStorage
from django.http import QueryDict
from library.savefile import saveFile
from . import models, serializer
from classes.models import ClassesModel
from classes.serializer import ClassesSerializer
from teacher.models import TeacherModel
from teacher.serializer import TeacherSerializer
url = 'http://localhost:8000/media'

# ? For School Operations
class SchoolLoginView(APIView):
    def post(self,request):
        passkey=request.data.get('school_passkey')
        if models.SchoolModel.objects.filter(school_passkey=passkey).exists():
            school_response=CRUDOperations.getFilteredData(model=models.SchoolModel, serializer=serializer.SchoolSerializer, school_passkey=passkey)
            if len(school_response) != 0:
                school=school_response[0]
                if school['school_enabled']:
                    data={
                    'school_id': school['id'],
                    'school_image':school['school_image'],
                    'school_name':school['school_name'],
                    'classes':[]
                    
                    }
                    classes_response= CRUDOperations.getFilteredData(model=ClassesModel, serializer=ClassesSerializer, school_id=school['id'])
                    for entry in classes_response:
                        classes_entry={
                            'class_id':entry['id'],
                            'class_name': entry['class_name']
                        }
                        data['classes'].append(classes_entry)
                    return Response(data=data,status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(data="school not enabled",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="School Not Found",status=status.HTTP_404_NOT_FOUND)


                   
class SchoolView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            response = CRUDOperations.getAllData(model=models.SchoolModel, serializer=serializer.SchoolSerializer)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.SchoolModel, serializer=serializer.SchoolSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Post Method
    def post(self, request):
        school_details={
            **request.POST.dict(),
            'school_image':'path'
        }
        check_serializer=serializer.SchoolSerializer(data=school_details)
        if check_serializer.is_valid():
            school_details['school_image']=saveFile(path="school", file=request.FILES['school_image'])
            response = CRUDOperations.addNewData(serializer=serializer.SchoolSerializer, data=school_details)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                print("Bad Request")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Update Method   
    def put(self, request, id):
        if 'school_image' in request.POST:
            response = CRUDOperations.updateExistingData(model=models.SchoolModel, serializer=serializer.SchoolSerializer, id=id, data=request.data)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        else:
            school_details={
            **request.POST.dict(),
            'school_image':'path'
            }
            check_serializer=serializer.SchoolSerializer(data=school_details)
            if check_serializer.is_valid():
                school_details['school_image']=saveFile(path="school", file=request.FILES['school_image'])
                response = CRUDOperations.addNewData(serializer=serializer.SchoolSerializer, data=school_details)
                if response['status']:
                    return Response(data=response['data'], status=status.HTTP_200_OK)
                else:
                    print("Bad Request")
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
    # ? Delete Method  
    def delete(self ,request, id):
        response = CRUDOperations.deleteExistingData(model=models.SchoolModel, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
# ? For School Enable / Disable
class SchoolEnableDisable(APIView):
    def put(self, request, id):
        response = CRUDOperations.updateExistingData(model=models.SchoolModel, serializer=serializer.SchoolSerializer, id=id, data=request.data)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# ? For Role Operations
class RoleView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        school_id = request.headers['School-Id']
        if id is None:
            response = CRUDOperations.getFilteredData(model=models.RolesModel, serializer=serializer.RoleSerializer, school_id=school_id)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.RolesModel, serializer=serializer.RoleSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Post Method
    def post(self, request):
        school_id = request.headers['School-Id']
        data={
            'school_id':school_id,
            **request.data.dict(),
        }
        response = CRUDOperations.addNewData(serializer=serializer.RoleSerializer, data=data)
        if response['status']:
            
            return Response(data='Role Created', status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Update Method
    def put(self ,request, id):
        response = CRUDOperations.updateExistingData(model=models.RolesModel, serializer=serializer.RoleSerializer, id=id, data=request.data)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Delete Method  
    def delete(self ,request, id):
        response = CRUDOperations.deleteExistingData(model=models.RolesModel, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# ? For Permission Operations
# class PermissionView(APIView):
#      # ? Get Method
#     def get(self, request, id=None):
#         role_id = request.headers['Role-Id']
#         if id is None:
#             response = CRUDOperations.getFilteredData(model=models.PermissionModel, serializer=serializer.PermissionSerializer,role_id = role_id)
#             return Response(response, status=status.HTTP_200_OK)
#         else:
#             response = CRUDOperations.getSpecificData(model=models.PermissionModel, serializer=serializer.PermissionSerializer, id=id)
#             if response['status']:
#                 return Response(data=response['data'], status=status.HTTP_200_OK)
#             else:
#                 return Response(status=status.HTTP_400_BAD_REQUEST)
    
#     # ? Post Method
#     def post(self, request):
#         response = CRUDOperations.addNewData(serializer=serializer.PermissionSerializer, data=request.data)
#         if response['status']:
            
#             return Response(data=response['data'], status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#     # ? Update Method
#     def put(self ,request, id):
#         response = CRUDOperations.updateExistingData(model=models.PermissionModel, serializer=serializer.PermissionSerializer, id=id, data=request.data)
#         if response['status']:
#             return Response(data=response['data'], status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#     # ? Delete Method  
#     def delete(self ,request, id):
#         response = CRUDOperations.deleteExistingData(model=models.PermissionModel, id=id)
#         if response:
#             return Response(status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    # ? Login for Admin and Staffs
    def post(self, request):
        school_id=request.headers['School-Id']
        school_response=CRUDOperations.getSpecificData(model=models.SchoolModel,serializer=serializer.SchoolSerializer,id=school_id)
        if school_response['status'] and school_response['data']['school_enabled']:
            role_name=request.data.get('role_name')
            role_user=request.data.get('role_username')
            role_password=request.data.get('role_password')
            if models.RolesModel.objects.filter(role_username = role_user, role_password = role_password).exists():
                response = CRUDOperations.getFilteredData(model=models.RolesModel, serializer=serializer.RoleSerializer, role_username = role_user, role_password = role_password,role_name=role_name,school_id=school_id)
                if len(response) != 0:
                    return Response(data=response[0], status=status.HTTP_200_OK)
                else:
                    return Response(data= 'Invalid Entry',status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data="User Name Or PassWord Incorrect",status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
# class CategorySchool(APIView):
#     def get(self, request):
#         role_id = request.headers['Role-Id']
#         school_id=request.headers['School-Id']
#         school_response=CRUDOperations.getSpecificData(model=models.SchoolModel,serializer=serializer.SchoolSerializer,id=school_id)
#         if school_response['status'] and school_response['data']['school_enabled']:
#             permission_response = CRUDOperations.getFilteredData(model=models.PermissionModel, serializer=serializer.PermissionSerializer, role_id=role_id, view=False)
#             categories = []
#             for category in permission_response:
#                 category_response = CRUDOperations.getSpecificData(model=CategoryModel, serializer=CategorySerializer, id=category['category_id'])
#                 categories.append(category_response['data'])
        
#             return Response(data=categories,status=status.HTTP_200_OK)
    
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)
    
