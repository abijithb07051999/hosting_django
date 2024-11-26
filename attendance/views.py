from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from library.crud_operations import CRUDOperations
import json
from datetime import datetime
from calendar import month_name
import school.models
import school.serializer
from . import models, serializer
from student.models import StudentModel
from student.serializer import StudentSerializer
from collections import defaultdict

class AttendaceView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            c_id=request.headers['Class-Id']
            data=[]
            class_attendance = CRUDOperations.getFilteredData(model=models.AttendanceModel, serializer=serializer.AttendanceSerializer,class_id=c_id)
            attendance_by_month = defaultdict(lambda: defaultdict(list))
            for entry in class_attendance:
                
                month = entry['month']
                date = entry['date']
                student_id = entry['student_id']          
                student_data=CRUDOperations.getSpecificData(model=StudentModel, serializer=StudentSerializer,id=student_id)
                student_name = student_data['data']['student_name']
                student_image = student_data['data']['student_image']
                attendance_by_month[month][date].append({
                    'id': entry['id'],
                    'student_id': student_id,
                    'student_name': student_name,
                    'student_image': student_image,
                    'attendance_status': entry['attendance_status']
                })
            data = [
            {
                'month': month,
                'attendance': [
                    {
                        'date': date,
                        'students': students
                    }
                    for date, students in dates.items()
                ]
            }
            for month, dates in attendance_by_month.items()
        ]
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.AttendanceModel, serializer=serializer.AttendanceSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
     
    # ? Post Method
    def post(self, request):
        response = CRUDOperations.addNewData(serializer=serializer.AttendanceSerializer, data=request.data)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Update Method   
    def put(self, request, id):
        response = CRUDOperations.updateExistingData(model=models.AttendanceModel, serializer=serializer.AttendanceSerializer, id=id, data=request.data)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Delete Method  
    def delete(self ,request, id):
        response = CRUDOperations.deleteExistingData(model=models.AttendanceModel, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class AllStudentsAttendanceView(APIView):
    # ? Post Class based students Attendance updation
    def post(self, request):
        print(request.data)
        class_id = request.headers.get('Class-Id')
        date = request.data.get("date")
        weekday = datetime.strptime(date, '%Y-%m-%d').strftime("%A")
        month = datetime.strptime(date, '%Y-%m-%d').strftime("%B")
        attendance_list=request.data.get('attendance_list')
        if not class_id or not attendance_list:
            return Response({"message": "Class ID and attendance list are required."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = []
            for record in attendance_list:
                student_id = record.get("student_id")
                attendance_status = record.get("attendance_status")  
                
                if student_id is None or attendance_status is None:
                    errors.append({"student_id": student_id, "message": "Invalid data"})
                    continue

                attendance_data = {
                    'class_id': class_id,
                    'date': date,
                    'weekday': weekday,
                    'student_id': student_id,
                    'month': month,
                    'attendance_status': attendance_status  
                }
                
                if models.AttendanceModel.objects.filter(student_id=student_id, class_id=class_id, date=date).exists():
                    get_attend = CRUDOperations.getFilteredData(model=models.AttendanceModel,serializer=serializer.AttendanceSerializer,student_id=student_id,class_id=class_id,date=date)
                    s_id = get_attend[0]['id']
                    response = CRUDOperations.updateExistingData(model=models.AttendanceModel,serializer=serializer.AttendanceSerializer,id=s_id,data=attendance_data)
                else:
                    response = CRUDOperations.addNewData(serializer=serializer.AttendanceSerializer,data=attendance_data)

                    if not response['status']:
                        errors.append({"student_id": student_id, "message": "Failed to update attendance"})

            if errors:
                return Response({"message": "Some records failed to update", "errors": errors})
            
            return Response(data="updated",status=status.HTTP_200_OK)
            
        
    
    
class AttendanceByDate(APIView):
    #  ? post method to get attendance details by date 
    def post(self,request):
        class_id=request.headers['Class-Id']
        date=request.POST['date']
        if date is None:
            return Response({'error':"Date is Required"},status=status.HTTP_404_NOT_FOUND)
        else:
            data={
                'date':date,
                'attendance_list':[]
            }
            attendance_response=CRUDOperations.getFilteredData(model=models.AttendanceModel,serializer=serializer.AttendanceSerializer,class_id=class_id,date=date)
            for entry in attendance_response:
                student_id=entry['student_id']
                student_response=CRUDOperations.getSpecificData(model=StudentModel,serializer=StudentSerializer,id=student_id,student_class_id=class_id)
                student_data={
                    'student_id':student_response['data']['id'],
                    'student_name':student_response['data']['student_name'],
                    'student_image':student_response['data']['student_image'],
                    'attendance_status':entry['attendance_status']
                    
                    }
                
                data['attendance_list'].append(student_data)
            return Response(data=data,status=status.HTTP_200_OK)
        
            