import requests
from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import KeyValue
from .serializers import KeyValueSerializer
from datetime import datetime

PEER_NODES = [
    "http://localhost:8001",
    "http://localhost:8002"
]

class KeyValueStoreView(APIView):
    def get(self, request, key):
        values = []
        timestamps = []

        for peer in PEER_NODES:
            try:
                response = requests.get(f"{peer}/api/store/{key}/")
                if response.status_code == 200:
                    data = response.json()
                    values.append(data['value'])
                    timestamps.append(datetime.fromisoformat(data['timestamp']))
            except requests.RequestException:
                continue

        try:
            kv = KeyValue.objects.get(key=key)
            values.append(kv.value)
            timestamps.append(kv.timestamp)
        except KeyValue.DoesNotExist:
            pass

        if values:
            latest_value = values[timestamps.index(max(timestamps))]
            return Response({"key": key, "value": latest_value})

        return Response({"error": "Key not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, key):
        data = request.data
        data['key'] = key
        serializer = KeyValueSerializer(data=data)

        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()


            successful_writes = 1  
            for peer in PEER_NODES:
                try:
                    response = requests.post(f"{peer}/api/store/{key}/", json=request.data)
                    if response.status_code == status.HTTP_201_CREATED:
                        successful_writes += 1
                except requests.RequestException:
                    continue

            if successful_writes >= 2:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Write quorum not reached"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
