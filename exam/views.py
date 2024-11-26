from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from library.crud_operations import CRUDOperations

from . import models, serializer
from school.models import SchoolModel
from school.serializer import SchoolSerializer
from timetable.models import TimetableModel
from timetable.serializer import TimetableSerializer
from subject.models import SubjectModel
from subject.serializer import SubjectSerializer
from exam.models import ExamModel,ExamTimetableModel
from exam.serializer import ExamSerializer,ExamTimetableSerializer


class ExamView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            cid = request.headers['Class-Id']
            response = CRUDOperations.getFilteredData(model=models.ExamModel, serializer=serializer.ExamSerializer, exam_class_id=cid)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.ExamModel, serializer=serializer.ExamSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
#     # ? Post Method
#     def post(self, request):
#         response = CRUDOperations.addNewData(serializer=serializer.ExamSerializer, data=request.data)
#         if response['status']:
#             return Response(data=response['data'], status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#     # ? Update Method   
#     def put(self, request, id):
#         response = CRUDOperations.updateExistingData(model=models.ExamModel, serializer=serializer.ExamSerializer, id=id, data=request.data)
#         if response['status']:
#             return Response(data=response['data'], status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#     # ? Delete Method  
#     def delete(self ,request, id):
#         response = CRUDOperations.deleteExistingData(model=models.ExamModel, id=id)
#         if response:
#             return Response(status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        

class ExamTimetableView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        cid = request.headers['Class-Id']
        eid = request.headers['Exam-Id']
        if id is None: 
            data=[]
            exam_response=CRUDOperations.getSpecificData(model=models.ExamModel, serializer=serializer.ExamSerializer,id=eid,exam_class_id=cid)
            print(exam_response)
            exam_data={'exam_name': exam_response['data']['exam_name'],
                    'exam_start_date': exam_response['data']['exam_start_date'],
                    'exam_end_date': exam_response['data']['exam_end_date'],
                    'subjects': []
                }          
            exam_timetable = CRUDOperations.getFilteredData(model=ExamTimetableModel,serializer=ExamTimetableSerializer,exam_id=eid)
            for timetable in exam_timetable:
                subjects = CRUDOperations.getSpecificData(model=SubjectModel,serializer=SubjectSerializer,id=timetable['subject_id'])
                subject_entry = {
                    'subject_id' : timetable['subject_id'],
                    'subject_name': subjects['data']['subject_name'],
                    'exam_date': timetable['exam_date'],
                    'start_time': timetable['start_time'],
                    'end_time': timetable['end_time'],
                    'portions': timetable['portions'],
                    
                }
                exam_data['subjects'].append(subject_entry)
                
            data.append(exam_data)  
            print(f"Data : f{data}")
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.ExamTimetableModel, serializer=serializer.ExamTimetableSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Post Method
    def post(self, request):
        # print(request.data)
        subjects_list = request.data.get('subjects')
        exam_table = CRUDOperations.addNewData(serializer=serializer.ExamSerializer, data=request.data)
        if exam_table['status']: 
            e_id = exam_table['data']['id']  
            for entry in subjects_list:
                print(entry)
                timetable_data = {
                    'exam_date': entry.get('exam_date'),
                    'exam_id': e_id,
                    'subject_id': entry.get('subject_id'),
                    'start_time': entry.get('start_time'),
                    'end_time': entry.get('end_time'),
                    'portions': entry.get('portions')    
                }
                response = CRUDOperations.addNewData(serializer=serializer.ExamTimetableSerializer, data=timetable_data)
                if not response['status']:
                    return Response(data="Failed to add timetable entry", status=status.HTTP_400_BAD_REQUEST)
            return Response(data="success", status=status.HTTP_200_OK)
        
        else:
            return Response(data="Exam not saved", status=status.HTTP_400_BAD_REQUEST)

    # ? Update Method   
    def put(self, request, id):
        response = CRUDOperations.updateExistingData(model=models.ExamTimetableModel, serializer=serializer.ExamTimetableSerializer, id=id, data=request.data)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Delete Method  
    def delete(self ,request, id):
        response = CRUDOperations.deleteExistingData(model=models.ExamTimetableModel, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
class Class_based_ExamTimeTable(APIView):
        
    # ? Exam TimeTable Baased on Classes
    def get(self, request):
        school_id = request.headers.get('School-Id')
        class_id = request.headers.get('Class-Id')
        school_response = CRUDOperations.getSpecificData(model=SchoolModel,serializer=SchoolSerializer,id=school_id)
        if school_response['status']and school_response['data']['school_enabled']:
            exam_type = CRUDOperations.getFilteredData(model=ExamModel,serializer=ExamSerializer,exam_class_id=class_id)
            data = []  
            for exams in exam_type:
                exam_id = exams['id']
                exam_data = {
                    'exam_id' : exams['id'],
                    'exam_name': exams['exam_name'],
                    'exam_start_date': exams['exam_start_date'],
                    'exam_end_date': exams['exam_end_date'],
                    'subjects': []
                }
                exam_timetable = CRUDOperations.getFilteredData(model=ExamTimetableModel,serializer=ExamTimetableSerializer,exam_id=exam_id)
                for timetable in exam_timetable:
                    subjects = CRUDOperations.getSpecificData(model=SubjectModel,serializer=SubjectSerializer,id=timetable['subject_id'])
                    subject_entry = {
                        'subject_name': subjects['data']['subject_name'],
                        'subject_id' : timetable['subject_id'],
                        'exam_date': timetable['exam_date'],
                        'start_time': timetable['start_time'],
                        'end_time': timetable['end_time'],
                        'portions': timetable['portions']
                    }
                    exam_data['subjects'].append(subject_entry)
                    
                data.append(exam_data)  
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    # ? Update Class Based Exam Timetable 
    def put(self,request,id):
        subjects_list = request.data.get('subjects')
        exam_table = CRUDOperations.updateExistingData(model=models.ExamModel, serializer=serializer.ExamSerializer, id=id, data=request.data)
        if exam_table['status']:
            for entry in subjects_list:
                print(entry)
                subject_id = entry['subject_id']
                timetable_data = {
                    'exam_date': entry['exam_date'],
                    'exam_id': id,
                    'subject_id': entry['subject_id'],
                    'start_time': entry['start_time'],
                    'end_time': entry['end_time'],
                    'portions': entry['portions']    
                }
                
                existing_entry= CRUDOperations.getSpecificData(model=models.ExamTimetableModel, serializer=serializer.ExamTimetableSerializer,exam_id=id,subject_id= subject_id)
                if existing_entry['status']:
                    timetable_update=CRUDOperations.updateExistingData(model=models.ExamTimetableModel, serializer=serializer.ExamTimetableSerializer, id=existing_entry['data']['id'], data=timetable_data)   
                    if not timetable_update['status']:
                        return Response(data="Failed update timetable", status=status.HTTP_400_BAD_REQUEST)
            return Response(data="success", status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Delet Class Based Exam Time Table
    def delete(self,request,id):
        delete_exam = CRUDOperations.deleteExistingData(model=models.ExamModel, id=id)
        if delete_exam:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)