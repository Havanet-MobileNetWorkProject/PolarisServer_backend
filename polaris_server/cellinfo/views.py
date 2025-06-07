from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.utils.dateparse import parse_datetime

from .serializers import (
    SignalTest2GSerializer,
    SignalTest3GSerializer,
    SignalTest4GSerializer,
    SignalTest5GSerializer,
)
from .models import (
    SignalTest2G,
    SignalTest3G,
    SignalTest4G,
    SignalTest5G,
)


class UnifiedSignalTestView(APIView):
    def post(self, request, *args, **kwargs):
        technology = request.data.get("technology", None)

        if technology in ["GSM", "GPRS", "EDGE"]:
            serializer = SignalTest2GSerializer(data=request.data)
        elif technology in ["UMTS", "HSPA", "HSPA+"]:
            serializer = SignalTest3GSerializer(data=request.data)
        elif technology in ["LTE", "LTE-Adv"]:
            serializer = SignalTest4GSerializer(data=request.data)
        elif technology == "5G":
            serializer = SignalTest5GSerializer(data=request.data)
        else:
            return Response({"error": "Invalid or missing technology field"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        technology = request.query_params.get("technology")
        start = request.query_params.get("start")
        end = request.query_params.get("end")
        client_id = request.query_params.get("client_id")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 50))

        if technology in ["GSM", "GPRS", "EDGE"]:
            model = SignalTest2G
            serializer_class = SignalTest2GSerializer
        elif technology in ["UMTS", "HSPA", "HSPA+"]:
            model = SignalTest3G
            serializer_class = SignalTest3GSerializer
        elif technology in ["LTE", "LTE-Adv"]:
            model = SignalTest4G
            serializer_class = SignalTest4GSerializer
        elif technology == "5G":
            model = SignalTest5G
            serializer_class = SignalTest5GSerializer
        else:
            return Response({"error": "Missing or invalid technology"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = model.objects.all()

        if client_id:
            queryset = queryset.filter(client_id=client_id)

        if start:
            start_dt = parse_datetime(start)
            if start_dt:
                queryset = queryset.filter(timestamp__gte=start_dt)

        if end:
            end_dt = parse_datetime(end)
            if end_dt:
                queryset = queryset.filter(timestamp__lte=end_dt)

        paginator = Paginator(queryset.order_by("-timestamp"), page_size)
        paginated = paginator.get_page(page)

        serializer = serializer_class(paginated, many=True)
        return Response({
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page,
            "results": serializer.data
        }, status=status.HTTP_200_OK)
