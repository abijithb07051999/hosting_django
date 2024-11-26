from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from calendar import month_name
from library.crud_operations import CRUDOperations
from . import models, serializer
from student.models import StudentModel
from student.serializer import StudentSerializer


class FeesView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            cid = request.headers['Class-Id']
            response = CRUDOperations.getFilteredData(model=models.FeesModel, serializer=serializer.FeesSerializer, fees_class_id = cid)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.FeesModel, serializer=serializer.FeesSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Post Method
    def post(self, request):
        fees_data={**request.data,
                'fees_class_id':request.headers['Class-Id']
                }
        response = CRUDOperations.addNewData(serializer=serializer.FeesSerializer, data=fees_data)
        if response['status']:
            class_id = response['data']['fees_class_id']
            fees_id = response['data']['id']
            date=response['data']['fees_last_date']
            student_response = CRUDOperations.getFilteredData(model=StudentModel, serializer=StudentSerializer, student_class_id =class_id)
            for students in student_response:
                data = {
                'fees_id': fees_id,
                'fees_class_id': class_id,
                'fees_student_id': students['id'],
                'fees_paid_date': date,
                'paid_status': False
                }
                status_response = CRUDOperations.addNewData(serializer=serializer.FeesStatusSerializer, data=data)
                if not status_response['status']:
                    return Response({"message": "Failed to update fees status for some students."}, status=status.HTTP_400_BAD_REQUEST)
        
            return Response({"message": "Fees status updated for all students."}, status=status.HTTP_200_OK)          
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    # ? Update Method   
    def put(self, request, id):
        response = CRUDOperations.updateExistingData(model=models.FeesModel, serializer=serializer.FeesSerializer, id=id, data=request.data)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Delete Method  
    def delete(self ,request, id):
        response = CRUDOperations.deleteExistingData(model=models.FeesModel, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        


class FeesStatusView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            cid = request.headers['Class-Id']
            fid=request.headers['Fees-Id']
            fees_response= CRUDOperations.getSpecificData(model=models.FeesModel, serializer=serializer.FeesSerializer, id=fid)
            data = {
                'fees_id':int(fid),
                'fees_reason':fees_response['data']['fees_reason'],
                'unpaid': [],
                'paid': []
            }
            class_fees= CRUDOperations.getFilteredData(model=models.FeesStatusModel, serializer=serializer.FeesStatusSerializer, fees_class_id = cid,fees_id=fid)
            for entry in class_fees:
                student_data=CRUDOperations.getSpecificData(model=StudentModel,serializer=StudentSerializer,id=entry['fees_student_id'],student_class_id=cid)
                paid=entry['paid_status']
                if paid:
                    student_entry={
                        'id':entry['id'],
                        'fees_student_id':student_data['data']['id'],
                        'student_name':student_data['data']['student_name'],
                        'student_image':student_data['data']['student_image'],
                        'paid_status': paid
                        
                    }
                    data['paid'].append(student_entry)
                else:
                    student_entry={
                        'id':entry['id'],
                        'fees_student_id':student_data['data']['id'],
                        'student_name':student_data['data']['student_name'],
                        'student_image':student_data['data']['student_image'],
                        'paid_status': paid
                        
                    }
                    data['unpaid'].append(student_entry)
            
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.FeesStatusModel, serializer=serializer.FeesStatusSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # # ? Post Method
    # def post(self, request):
    #     response = CRUDOperations.addNewData(serializer=serializer.FeesStatusSerializer, data=request.data)
    #     if response['status']:
    #         return Response(data=response['data'], status=status.HTTP_200_OK)
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
    # ? Update Method   
    def put(self, request, id):
        class_id=request.headers['Class-Id']
        if class_id is None:
            return Response({'error':"Class_id Required"},status=status.HTTP_400_BAD_REQUEST)
        fees_details={
            **request.POST.dict(),
            'fees_paid_date':datetime.today().strftime('%Y-%m-%d')
        }
        response = CRUDOperations.updateExistingData(model=models.FeesStatusModel, serializer=serializer.FeesStatusSerializer, id=id, data=fees_details)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Delete Method  
    def delete(self ,request, id):
        response = CRUDOperations.deleteExistingData(model=models.FeesStatusModel, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    