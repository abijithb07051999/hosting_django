from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from library.crud_operations import CRUDOperations
from datetime import datetime
from calendar import month_name
from collections import defaultdict
from . import models, serializer

class HolidyView(APIView):
    # ? Get Method
    def get(self, request, id=None):
        if id is None:
            sid = request.headers['School-Id']
            holiday_records = CRUDOperations.getFilteredData(model=models.HolidayModel, serializer=serializer.HolidaySerializer, school_id=sid)
            monthly_data = defaultdict(list)

            for holiday in holiday_records:
                date_obj = datetime.strptime(holiday['date'], '%Y-%m-%d')
                year = date_obj.year
                month = date_obj.month
                month_name_str = month_name[month]
                month_year_key = f"{month_name_str} {year}"
                holiday_entry = {
                    'id':holiday.get('id'),
                    'date': holiday.get('date'),
                    'weekday': holiday.get('weekday'),
                    'reason': holiday.get('reason')
                }

                monthly_data[month_year_key].append(holiday_entry)

            formatted_data = [
                {'month': month_year, 'holidays': holidays}
                for month_year, holidays in monthly_data.items()
            ]
                
            return Response(data=formatted_data, status=status.HTTP_200_OK)
        else:
            response = CRUDOperations.getSpecificData(model=models.HolidayModel, serializer=serializer.HolidaySerializer, id=id)
            if response['status']:
                return Response(data=response['data'], status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # ? Post Method
    def post(self, request):
        
        holiday={
            **request.data.dict(),
            
            'weekday': datetime.strptime(request.data.get('date'), '%Y-%m-%d').strftime("%A")
            }
        
        response = CRUDOperations.addNewData(serializer=serializer.HolidaySerializer, data=holiday)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Update Method   
    def put(self, request, id):
        holiday={
            **request.data.dict(),
            
            }
        if 'date' in request.data:
            holiday['weekday']= datetime.strptime(request.data.get('date'), '%Y-%m-%d').strftime("%A")
            
        
        response = CRUDOperations.updateExistingData(model=models.HolidayModel, serializer=serializer.HolidaySerializer, id=id, data=holiday)
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # ? Delete Method  
    def delete(self ,request, id):
        response = CRUDOperations.deleteExistingData(model=models.HolidayModel, id=id)
        if response:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
