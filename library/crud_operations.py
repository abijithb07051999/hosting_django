
class CRUDOperations:
 
    @staticmethod
    def getAllData(model, serializer):
        allObjects = model.objects.all()
        serializedData = serializer(allObjects, many=True).data
        return serializedData
        
    @staticmethod
    def getSpecificData(model, serializer, **condition) -> dict:
        try:
            specificObject = model.objects.get(**condition)
            serializedData = serializer(specificObject).data
            return {'status' : True, 'data' : serializedData}
        except:
            return {'status' : False}
        
    @staticmethod
    def getFilteredData(model, serializer, **args) -> list[dict]:
        getExistingObjects = model.objects.filter(**args)
        serializedData = serializer(getExistingObjects, many=True).data
        return serializedData
    
    @staticmethod
    def addNewData(serializer, data) -> dict:
        serializedData = serializer(data=data)
        if serializedData.is_valid():
            serializedData.save()
            return {'status' : True, 'data' : serializedData.data}
        else:
            return {'status' : False}
    
    @staticmethod
    def updateExistingData(model, serializer, id, data) -> dict:
        try:
            getOldObject = model.objects.get(id=id)
            serializedData = serializer(getOldObject, data=data, partial=True)
            if serializedData.is_valid():
                serializedData.save()
                return {'status' : True, 'data' : serializedData.data}
            else:
                return {'status' : False}
        except:
             return {'status' : False}
             
    @staticmethod
    def deleteExistingData(model, id) -> bool:
        try:
            model.objects.get(id=id).delete()
            return True
        except:
            return False

