from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from library.crud_operations import CRUDOperations

from . import models, serializer
from subject.models import SubjectModel
from subject.serializer import SubjectSerializer
from teacher.models import TeacherModel
from teacher.serializer import TeacherSerializer

class TimetableView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            cid = request.headers['Class-Id']
            timetable_data = CRUDOperations.getFilteredData(model=models.TimetableModel, serializer=serializer.TimetableSerializer, class_id = cid)
            data = {}
            for entry in timetable_data:
                weekday = entry['weekday']
                if weekday not in data:
                    data[weekday] = []
                if entry['subject_id'] is None:
                    class_entry={
                        'timetable_id':entry['id'],
                        'subject_name': entry['subject_name'],
                        'start_time': entry['start_time'],
                        'end_time': entry['end_time'],
                    }
                else:
                    subject_data = CRUDOperations.getSpecificData(model=SubjectModel,serializer=SubjectSerializer,id=entry['subject_id'])
                    teacher_data = CRUDOperations.getSpecificData(model=TeacherModel,serializer=TeacherSerializer,id=subject_data['data']['subject_teacher_id'])
                    class_entry = {
                            'timetable_id':entry['id'],
                            'subject_id' : entry['subject_id'],
                            'subject_name': subject_data['data']['subject_name'],
                            'staff_name': teacher_data['data']['teacher_name'],
                            'start_time': entry['start_time'],
                            'end_time': entry['end_time']
                        }   
                    
                data[weekday].append(class_entry)    
            formatted_data = [{'weekday': day, 'time_table': schedule}for day, schedule in data.items()] 
            return Response(data=formatted_data, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.TimetableModel, serializer=serializer.TimetableSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Post Method
    def post(self, request):
        response = CRUDOperations.addNewData(serializer=serializer.TimetableSerializer, data=request.data)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Update Method   
    def put(self, request, id):
        response = CRUDOperations.updateExistingData(model=models.TimetableModel, serializer=serializer.TimetableSerializer, id=id, data=request.data)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Delete Method  
    def delete(self ,request, id):
        print(id)
        response = CRUDOperations.deleteExistingData(model=models.TimetableModel, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
