from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from library.crud_operations import CRUDOperations

from . import models, serializer
from  exam.models import ExamModel,ExamTimetableModel
from exam.serializer import ExamSerializer,ExamTimetableSerializer
from  subject.models import SubjectModel
from subject.serializer import SubjectSerializer



# class ExamresultView(APIView):
#     # ? Get Method
#     def get(self, request, id=None):
#         if id is None:
#             eid = request.headers['Exam-Id']
#             response = CRUDOperations.getFilteredData(model=models.ExamresultModel, serializer=serializer.ExamresultSerializer, exam_id=eid)
#             return Response(response, status=status.HTTP_200_OK)
#         else:
#             response = CRUDOperations.getSpecificData(model=models.ExamresultModel, serializer=serializer.ExamresultSerializer, id=id)
#             if response['status']:
#                 return Response(data=response['data'], status=status.HTTP_200_OK)
#             else:
#                 return Response(status=status.HTTP_400_BAD_REQUEST)
    
#     # ? Post Method
#     def post(self, request):
#         response = CRUDOperations.addNewData(serializer=serializer.ExamresultSerializer, data=request.data)
#         if response['status']:
#             return Response(data=response['data'], status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#     # ? Update Method   
#     def put(self, request, id):
#         response = CRUDOperations.updateExistingData(model=models.ExamresultModel, serializer=serializer.ExamresultSerializer, id=id, data=request.data)
#         if response['status']:
#             return Response(data=response['data'], status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#     # ? Delete Method  
#     def delete(self ,request, id):
#         response = CRUDOperations.deleteExistingData(model=models.ExamresultModel, id=id)
#         if response:
#             return Response(status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        


# class OverallExamresultView(APIView):
#     # ? Get Method
#     def get(self, request, id=None):
#         if id is None:
#             eid = request.headers['Exam-Id']
#             response = CRUDOperations.getFilteredData(model=models.OverallExamresultModel, serializer=serializer.OverallExamresultSerializer, exam_id=eid)
#             return Response(response, status=status.HTTP_200_OK)
#         else:
#             response = CRUDOperations.getSpecificData(model=models.OverallExamresultModel, serializer=serializer.OverallExamresultSerializer, id=id)
#             if response['status']:
#                 return Response(data=response['data'], status=status.HTTP_200_OK)
#             else:
#                 return Response(status=status.HTTP_400_BAD_REQUEST)
    
#     # ? Post Method
#     def post(self, request):
#         response = CRUDOperations.addNewData(serializer=serializer.OverallExamresultSerializer, data=request.data)
#         if response['status']:
#             return Response(data=response['data'], status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#     # ? Update Method   
#     def put(self, request, id):
#         response = CRUDOperations.updateExistingData(model=models.OverallExamresultModel, serializer=serializer.OverallExamresultSerializer, id=id, data=request.data)
#         if response['status']:
#             return Response(data=response['data'], status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#     # ? Delete Method  
#     def delete(self ,request, id):
#         response = CRUDOperations.deleteExistingData(model=models.OverallExamresultModel, id=id)
#         if response:
#             return Response(status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        

class PassmarkView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            sid = request.headers['School-Id']
            response = CRUDOperations.getFilteredData(model=models.PassmarkModel, serializer=serializer.PassmarkSerializer, school_id=sid)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.PassmarkModel, serializer=serializer.PassmarkSerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Post Method
    def post(self, request):
        response = CRUDOperations.addNewData(serializer=serializer.PassmarkSerializer, data=request.data)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Update Method   
    def put(self, request, id):
        response = CRUDOperations.updateExistingData(model=models.PassmarkModel, serializer=serializer.PassmarkSerializer, id=id, data=request.data)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Delete Method  
    def delete(self ,request, id):
        response = CRUDOperations.deleteExistingData(model=models.PassmarkModel, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class ExamResultForStudentView(APIView):
    # ? Exam Result based on StudentID and ExamId
    def post(self, request):
        class_id = request.headers['Class-Id']
        exam_id = request.POST['exam_id']
        student_id = request.POST['student_id']

        exam_entry = {
            'exam_id':int(exam_id),
            'exam_name': None,
            'exam_grade': None,
            'exam_total': None,
            'exam_results': []
        }

        
        exam_data = CRUDOperations.getSpecificData(model=ExamModel, serializer=ExamSerializer, id=exam_id)
        if not exam_data.get('data'):  
            return Response(data=exam_entry, status=status.HTTP_200_OK)
        exam_entry['exam_name'] = exam_data['data']['exam_name']

        
        overall_results = CRUDOperations.getFilteredData(
            model=models.OverallExamresultModel,
            serializer=serializer.OverallExamresultSerializer,
            student_id=student_id,
            exam_id=exam_id
        )

        for overall in overall_results:
            exam_entry.update({
                'exam_grade': overall['exam_grade'],
                'exam_total': overall['exam_total'],
            })

            exam_results = CRUDOperations.getFilteredData(
                model=models.ExamresultModel,
                serializer=serializer.ExamresultSerializer,
                exam_id=exam_id,
                student_id=student_id
            )

            for result in exam_results:
                exam_ttid = result['exam_time_table']
                exam_timetable = CRUDOperations.getSpecificData(model=ExamTimetableModel, serializer=ExamTimetableSerializer, id=exam_ttid)
                sub_id = exam_timetable['data']['subject_id']
                subject_data = CRUDOperations.getSpecificData(model=SubjectModel, serializer=SubjectSerializer, id=sub_id, subject_class_id=class_id)

                subject_entry = {
                    'subject_id': subject_data['data']['id'],
                    'subject_name': subject_data['data']['subject_name'],
                    'exam_date': exam_timetable['data']['exam_date'],
                    'grade': result['grade'],
                    'mark': result['mark']
                }
                exam_entry['exam_results'].append(subject_entry)

        return Response(data=exam_entry, status=status.HTTP_200_OK)

  
        
class AddStudentExamResult(APIView):
    #? post/put Student Exam result 
    def post(self,request):
        student_id=request.headers['Student-Id'] 
        exam_id=request.data.get('exam_id' )
        exam_grade=request.data.get('exam_grade')
        exam_total=request.data.get('exam_total')
        exam_result_list=request.data.get('exam_results')
        if not student_id or not exam_result_list:
            return Response({"message": "Student ID and Exam Result List are required."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = []
            for result in exam_result_list:
                subject_id=result.get('subject_id')
                mark=result.get('mark')
                grade=result.get('grade')
                if subject_id is None or mark is None or grade is None:
                    errors.append({"subject_id": subject_id, "message": "Invalid data"})
                    continue
                exam_timetable=CRUDOperations.getSpecificData(model=ExamTimetableModel,serializer=ExamTimetableSerializer,exam_id=exam_id,subject_id=subject_id)
                exam_timetable_id=exam_timetable['data']['id']
                exam_result_data={
                    'exam_id':exam_id,
                    'mark':mark,
                    'grade':grade,
                    'student_id':student_id,
                    'exam_time_table':exam_timetable['data']['id'],
                }
                if models.ExamresultModel.objects.filter(student_id=student_id,exam_id=exam_id,exam_time_table_id=exam_timetable_id).exists():
                    get_examresult= CRUDOperations.getSpecificData(model=models.ExamresultModel,serializer=serializer.ExamresultSerializer,student_id=student_id,exam_id=exam_id,exam_time_table_id=exam_timetable_id)
                    er_id = get_examresult['data']['id']
                    response = CRUDOperations.updateExistingData(model=models.ExamresultModel,serializer=serializer.ExamresultSerializer,id=er_id,data=exam_result_data)
                else:
                    response = CRUDOperations.addNewData(serializer=serializer.ExamresultSerializer,data=exam_result_data)
                    print("Add New Data Response",response)
                    if not response['status']:
                        errors.append({"subject_id": subject_id, "message": "Failed to update exam Mark"})
            overall_data={
                'exam_total':exam_total,
                'exam_grade':exam_grade,
                'exam_id': exam_id,
                'student_id':student_id,
                
            }
            if models.OverallExamresultModel.objects.filter(student_id=student_id,exam_id=exam_id).exists():
                get_result=CRUDOperations.getFilteredData(model=models.OverallExamresultModel,serializer=serializer.OverallExamresultSerializer,student_id=student_id,exam_id=exam_id)
                overall_id=get_result[0]['id']
                up_overall = CRUDOperations.updateExistingData(model=models.OverallExamresultModel,serializer=serializer.OverallExamresultSerializer,id=overall_id,data=overall_data)
            else:
                up_overall = CRUDOperations.addNewData(serializer=serializer.OverallExamresultSerializer,data=overall_data)
                
                if not up_overall['status']:
                    errors.append({"Exam Total": exam_total,"Grade":exam_grade, "message": "Failed to update Overall Result"})
            if errors:
                return Response({"message": "Some records failed to update", "errors": errors})
            
            return Response(data="updated", status=status.HTTP_200_OK)
   
            