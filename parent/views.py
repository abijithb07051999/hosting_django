from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import assignment.models
import assignment.serializer
import attendance.models
import attendance.serializer
import classes.models
import classes.serializer
import exam.models
import exam.serializer
import examresult.models
import examresult.serializer
import fees.models
import fees.serializer
import holiday.models
import holiday.serializer
from library.crud_operations import CRUDOperations
from django.core.files.storage import FileSystemStorage
from django.http import QueryDict
from datetime import datetime
from calendar import month_name
from collections import defaultdict

import portion.models
import portion.serializer
from  remainder.models import RemainderModels
from remainder.serializer import RemainderSerializer
import school.models
import school.serializer
import student.models
import student.serializer
import subject.models
import subject.serializer
import teacher.models
import teacher.serializer
import timetable.models
import timetable.serializer
from . import models
import school,classes,student,attendance,holiday
import examresult
import exam
import timetable
import fees
import remainder,portion,assignment
import subject,teacher


class LoginView(APIView):
    def post(self, request):
        found = False
        suid=request.data.get('student_unique_id')
        s_passkey=request.data.get('school_passkey')
        student_response= CRUDOperations.getFilteredData(model=student.models.StudentModel, serializer=student.serializer.StudentSerializer,student_unique_id = suid)
        if len(student_response) != 0:
            student_data = student_response[0] if isinstance(student_response, list) else student_response 
            school_response = CRUDOperations.getSpecificData(model=school.models.SchoolModel, serializer=school.serializer.SchoolSerializer,id=student_data.get('student_school_id'))
            found = school_response['data']['school_enabled']
            passkey=school_response['data']['school_passkey']
            if found and passkey==s_passkey:
                data = {
                    'student_id': student_data.get('id'),
                    'class_id': student_data.get('student_class_id'),
                    'school_id': student_data.get('student_school_id'),
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'School is not enabled'}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
       
class ProfileView(APIView):
    def get(self, request):
        school_id=request.headers['School-Id']
        student_id = request.headers['Student-Id']
        school_response=CRUDOperations.getSpecificData(model=school.models.SchoolModel,serializer=school.serializer.SchoolSerializer,id=school_id)
        if school_response['status']:
            if school_response['data']['school_enabled']:
                student_response=CRUDOperations.getSpecificData(model=student.models.StudentModel,serializer=student.serializer.StudentSerializer,id=student_id)
                data=student_response['data']
                class_response=CRUDOperations.getSpecificData(model=classes.models.ClassesModel,serializer=classes.serializer.ClassesSerializer,id=data['student_class_id'])
                data['class_name']=class_response['data']['class_name']
                transformed_data = {
                'image': data["student_image"],
                'name': data["student_name"],
                'date_of_birth': data["student_date_of_birth"],
                'class_name': data['class_name'], 
                'gender': data["student_gender"],
                'blood_group': data["student_blood_group"],
                'address': data["student_address"],
                'class_id': data["student_class_id"],
                'guardians': [
                    {
                        'guardian_image': data["guardian_1_image"],
                        'guardian_name': data["guardian_1_name"],
                        'guardian_relation': data["guardian_1_relation"],
                        'guardian_contact': [
                            data["guardian_1_contact_1"],
                            data["guardian_1_contact_2"]
                        ]
                    },
                    {
                        'guardian_image': data["guardian_2_image"],
                        'guardian_name': data["guardian_2_name"],
                        'guardian_relation': data["guardian_2_relation"],
                        'guardian_contact': [
                            data["guardian_2_contact_1"],
                            data["guardian_2_contact_2"]
                        ]
                    }
                ]
            }
                return Response(data=transformed_data,status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    
class AttendanceView(APIView):
    def get(self ,request):
        school_id=request.headers['School-Id']
        student_id = request.headers['Student-Id']
        school_response=CRUDOperations.getSpecificData(model=school.models.SchoolModel,serializer=school.serializer.SchoolSerializer,id=school_id)
        if school_response['status']:
            if school_response['data']['school_enabled']:
                attendance_records = CRUDOperations.getFilteredData(model=attendance.models.AttendanceModel,serializer=attendance.serializer.AttendanceSerializer,student_id=student_id)
                monthly_data = defaultdict(lambda: {'present': [], 'absent': [], 'holiday': []})
                for record in attendance_records:
                    record_date = datetime.strptime(record['date'], '%Y-%m-%d')
                    is_present = record['attendance_status'] 
                    
                    month = month_name[record_date.month]
                    weekday = record_date.strftime('%A')
                    entry = {
                    'date': record_date.strftime('%Y-%m-%d'),
                    'weekday': weekday
                    }
                    if is_present:
                        monthly_data[month]['present'].append(entry)
                    else:
                        monthly_data[month]['absent'].append(entry)  
                holiday_records= CRUDOperations.getFilteredData(model=holiday.models.HolidayModel,serializer=holiday.serializer.HolidaySerializer,school_id=school_id)
                for holiday_date in holiday_records:
                    holiday_date = datetime.strptime(holiday_date['date'], '%Y-%m-%d')  
                    month = month_name[holiday_date.month]
                    weekday = holiday_date.strftime('%A')
                    holiday_entry = {
                        'date': holiday_date.strftime('%Y-%m-%d'),
                        'weekday': weekday
                    }
                    monthly_data[month]['holiday'].append(holiday_entry)
                    
                data = [
                    {
                        'month': month,
                        'present': details['present'],
                        'absent': details['absent'],
                        'holiday': details['holiday'],
                    }
                    for month, details in monthly_data.items()
                    ]
                
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class ReportCardView(APIView):
    def get(self, request):
        school_id=request.headers['School-Id']
        student_id = request.headers['Student-Id']
        school_response=CRUDOperations.getSpecificData(model=school.models.SchoolModel,serializer=school.serializer.SchoolSerializer,id=school_id)
        if school_response['status'] and school_response['data']['school_enabled']:
            # passmark_data = CRUDOperations.getFilteredData(model=examresult.models.PassmarkModel,serializer=examresult.serializer.PassmarkSerializer,school_id=school_id)
            overall_results = CRUDOperations.getFilteredData(model=examresult.models.OverallExamresultModel,serializer=examresult.serializer.OverallExamresultSerializer,student_id=student_id)
            data = []
            for overall in overall_results:
                
                exam_results= CRUDOperations.getFilteredData(examresult.models.ExamresultModel,serializer=examresult.serializer.ExamresultSerializer,exam_id=overall['exam_id'],student_id=student_id)
                exam_id = overall['exam_id']
                exam_data = CRUDOperations.getSpecificData(model=exam.models.ExamModel,serializer=exam.serializer.ExamSerializer,id=exam_id)
                exam_entry = {
                    'exam_name': exam_data['data']['exam_name'],
                    'exam_grade': overall['exam_grade'],
                    'exam_total': overall['exam_total'],
                    'exam_subjects': []
                    }
                
                for result in exam_results:
                    exam_ttid=result['exam_time_table']
                    exam_timetable=CRUDOperations.getSpecificData(exam.models.ExamTimetableModel,serializer=exam.serializer.ExamTimetableSerializer,id=exam_ttid)
                    sub_id=exam_timetable['data']['subject_id']
                    subject_data=CRUDOperations.getSpecificData(model=subject.models.SubjectModel,serializer=subject.serializer.SubjectSerializer,id=sub_id)
                    
                    subject_entry = {
                        'subject_name': subject_data['data']['subject_name'],  
                        'date': exam_timetable['data']['exam_date'],
                        'grade': result['grade'],
                        'mark': result['mark']
                    }
                    exam_entry['exam_subjects'].append(subject_entry)
        
                data.append(exam_entry)
                
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class TimeTableView(APIView):
    # ? get Class Based Timetable
    def get(self, request):
        class_id = request.headers.get('Class-Id')
        if not class_id:
            return Response({"error": "Class-Id are required in headers."},status=status.HTTP_400_BAD_REQUEST)
        data = {
            'Monday': [],
            'Tuesday': [],
            'Wednesday': [],
            'Thursday': [],
            'Friday': [],
            'Saturday': []
        }

        timetable_data = CRUDOperations.getFilteredData(model=timetable.models.TimetableModel,serializer=timetable.serializer.TimetableSerializer,class_id=class_id)

        for entry in timetable_data:
            weekday = entry['weekday']
            class_entry = {
                'timetable_id': entry['id'],
                'start_time': entry['start_time'],
                'end_time': entry['end_time']
            }

            if entry['subject_id']:
                subject_data = CRUDOperations.getSpecificData(model=subject.models.SubjectModel,serializer=subject.serializer.SubjectSerializer,id=entry['subject_id'])
                teacher_data = CRUDOperations.getSpecificData(model=teacher.models.TeacherModel,serializer=teacher.serializer.TeacherSerializer,id=subject_data['data']['subject_teacher_id'])
                class_entry.update({
                    'subject_name': subject_data['data']['subject_name'],
                    'staff_name': teacher_data['data']['teacher_name']
                    })
            else:
                class_entry['subject_name'] = entry['subject_name']

            data[weekday].append(class_entry)

        formatted_data = [
            {'weekday': day, 'time_table': schedule}
            for day, schedule in data.items()
        ]

        return Response(data=formatted_data, status=status.HTTP_200_OK)            
               
class ExamTimeTableView(APIView):
    def get(self ,request):
        school_id=request.headers['School-Id']
        class_id = request.headers['Class-Id']
        school_response=CRUDOperations.getSpecificData(model=school.models.SchoolModel,serializer=school.serializer.SchoolSerializer,id=school_id)
        if school_response['status']:
            if school_response['data']['school_enabled']:
                exam_type_list=CRUDOperations.getFilteredData(exam.models.ExamModel,serializer=exam.serializer.ExamSerializer,exam_class_id=class_id)
                exam_type = sorted(exam_type_list, key=lambda x: x['id'], reverse=True)[0] if exam_type_list else None
                if exam_type:
                    data={
                    'exam_name' : exam_type['exam_name'],
                    'start_date' : exam_type['exam_start_date'],
                    'end_date' : exam_type['exam_end_date'],
                    'subjects':[]
                    }
                    exam_timetable=CRUDOperations.getFilteredData(exam.models.ExamTimetableModel,serializer=exam.serializer.ExamTimetableSerializer,exam_id=exam_type['id'])
                    for timetable in exam_timetable:
                        subjects=CRUDOperations.getSpecificData(model=subject.models.SubjectModel,serializer=subject.serializer.SubjectSerializer,id=timetable['subject_id'])
                        subject_entry={
                            'subject_name':subjects['data']['subject_name'],
                            'date':timetable['exam_date'],
                            'start_time':timetable['start_time'],
                            'end_time':timetable['end_time'],
                            'portions':timetable['portions']
                        }
                        
                        data['subjects'].append(subject_entry)
                    return Response(data=data, status=status.HTTP_200_OK)
                else:
                    data=[]
                    return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
class FacultiesView(APIView):
    def get(self ,request):
        school_id=request.headers['School-Id']
        class_id = request.headers['Class-Id']
        school_response=CRUDOperations.getSpecificData(model=school.models.SchoolModel,serializer=school.serializer.SchoolSerializer,id=school_id)
        if school_response['status']:
            if school_response['data']['school_enabled']:
                classes_data=CRUDOperations.getSpecificData(model=classes.models.ClassesModel,serializer=classes.serializer.ClassesSerializer,id=class_id)
                inchargeid=classes_data['data']['teacher_id']
                incharge=CRUDOperations.getSpecificData(model=teacher.models.TeacherModel,serializer=teacher.serializer.TeacherSerializer,id=inchargeid)
                data={
                    'incharge':{
                        'name': incharge['data']['teacher_name'],
                        'image':incharge['data']['teacher_image']
                    },
                    'staffs':[]
                }
                subjects_wise=CRUDOperations.getFilteredData(model=subject.models.SubjectModel,serializer=subject.serializer.SubjectSerializer,subject_class_id=class_id)
                for subjects in subjects_wise: 
                    staffs=CRUDOperations.getSpecificData(model=teacher.models.TeacherModel,serializer=teacher.serializer.TeacherSerializer,id=subjects['subject_teacher_id'])
                    staff_entry={
                        'name':staffs['data']['teacher_name'],
                        'subject': subjects['subject_name'],
                        'image':staffs['data']['teacher_image']
                        }
                    data['staffs'].append(staff_entry)
                    
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
class FeesView(APIView):
    def get(self, request):
        school_id = request.headers['School-Id']
        class_id = request.headers['Class-Id']
        student_id = request.headers['Student-Id']
        school_response = CRUDOperations.getSpecificData(model=school.models.SchoolModel,serializer=school.serializer.SchoolSerializer,id=school_id)
        if school_response['status']and school_response['data']['school_enabled']:
            data = {
                'unpaid': [],
                'paid': []
            }
            
            fees_status = CRUDOperations.getFilteredData(model=fees.models.FeesStatusModel,serializer=fees.serializer.FeesStatusSerializer,fees_student_id=student_id,fees_class_id=class_id)
            all_fees = CRUDOperations.getFilteredData(model=fees.models.FeesModel,serializer=fees.serializer.FeesSerializer,fees_class_id=class_id)              
            fees_status_ids = {entry['fees_id'] for entry in fees_status}
            for entry in fees_status:
                fees_data = CRUDOperations.getSpecificData(model=fees.models.FeesModel,serializer=fees.serializer.FeesSerializer,id=entry['fees_id'])  
                paid = entry['paid_status']
                if paid:
                    fees_entry = {
                        'paid_date': entry['fees_paid_date'],
                        'amount': fees_data['data']['fees_amount'],
                        'reason': fees_data['data']['fees_reason']
                    }
                    data['paid'].append(fees_entry)
                else:
                    fees_entry = {
                        'last_date': fees_data['data']['fees_last_date'],
                        'amount': fees_data['data']['fees_amount'],
                        'reason': fees_data['data']['fees_reason']
                    }
                    data['unpaid'].append(fees_entry)
            for fee in all_fees:
                if fee['id'] not in fees_status_ids:
                    fees_entry = {
                        'last_date': fee['fees_last_date'],
                        'amount': fee['fees_amount'],
                        'reason': fee['fees_reason']
                    }
                    data['unpaid'].append(fees_entry)
            
            return Response(data=data, status=status.HTTP_200_OK)
            
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
        
class RemainderView(APIView):
    def get(self, request):
        school_id = request.headers['School-Id']
        class_id = request.headers['Class-Id']
        school_response = CRUDOperations.getSpecificData(model=school.models.SchoolModel,serializer=school.serializer.SchoolSerializer,id=school_id)
        if school_response['status']:
            if school_response['data']['school_enabled']:
                data=[]
                remainder_by_date={}
                remainder_response=CRUDOperations.getFilteredData(model=RemainderModels,serializer=RemainderSerializer,class_id=class_id)[::-1]
                for remain in remainder_response:
                    date=remain['date']
                    if date not in remainder_by_date:
                        remainder_by_date[date]=[]
                    
                    remainder_by_date[date].append(remain['remainder']) 
                for date, remainder in remainder_by_date.items():
                    data.append({'date': date, 'remainders': remainder})
                return Response(data=data, status=status.HTTP_200_OK)
                
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class PortionView(APIView):
    def get(self, request):
        school_id = request.headers['School-Id']
        class_id = request.headers['Class-Id']
        school_response = CRUDOperations.getSpecificData(model=school.models.SchoolModel,serializer=school.serializer.SchoolSerializer,id=school_id)
        if school_response['status']:
            if school_response['data']['school_enabled']:
                class_portions=CRUDOperations.getFilteredData(model=portion.models.PortionModel,serializer=portion.serializer.PortionSerializer,class_id=class_id)[::-1]
                data = []
                portions_by_date = defaultdict(lambda: defaultdict(list))
            
                for entry in class_portions:
                    date = entry['date']
                    subject_id = entry['subject_id']
                    
                    subjects_data = CRUDOperations.getSpecificData(model=subject.models.SubjectModel,serializer=subject.serializer.SubjectSerializer,id=subject_id
                    )
                    subject_name = subjects_data['data']['subject_name']
                    portions_by_date[date][subject_name].append(entry['portion'])
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
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
class AssignmentView(APIView):
    def get(self, request):
        school_id = request.headers['School-Id']
        class_id = request.headers['Class-Id']
        school_response = CRUDOperations.getSpecificData(model=school.models.SchoolModel,serializer=school.serializer.SchoolSerializer,id=school_id)
        if school_response['status']:
            if school_response['data']['school_enabled']:
                class_assignments=CRUDOperations.getFilteredData(model=assignment.models.AssignmentModel,serializer=assignment.serializer.AssignmentSerializer,class_id=class_id)[::-1]
                data = []
                assignments_by_date = defaultdict(lambda: defaultdict(list))
            
                for entry in class_assignments:
                    date = entry['date']
                    subject_id = entry['subject_id']
                    
                    subjects_data = CRUDOperations.getSpecificData(model=subject.models.SubjectModel,serializer=subject.serializer.SubjectSerializer,id=subject_id)               
                    subject_name = subjects_data['data']['subject_name']
                    assignments_by_date[date][subject_name].append(entry['assignment'])
                for date, subjects in assignments_by_date.items():
                    assignments = [
                        {
                            'subject': subject,
                            'assignments': assignments
                        }
                        for subject, assignments in subjects.items()
                    ]
                    data.append({'date': date, 'assignment': assignments})
                
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
       