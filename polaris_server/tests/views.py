from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from django.core.paginator import Paginator

from .models import *
from .serializers import *

class FilteredListMixin:
    def filter_queryset(self, model, serializer_class, request, time_field='timestamp'):
        queryset = model.objects.all()
        client_id = request.query_params.get("client_id")
        start = request.query_params.get("start")
        end = request.query_params.get("end")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 50))

        if client_id:
            queryset = queryset.filter(client_id=client_id)

        if start:
            start_dt = parse_datetime(start)
            if start_dt:
                queryset = queryset.filter(**{f"{time_field}__gte": start_dt})

        if end:
            end_dt = parse_datetime(end)
            if end_dt:
                queryset = queryset.filter(**{f"{time_field}__lte": end_dt})

        paginator = Paginator(queryset.order_by(f"-{time_field}"), page_size)
        page_obj = paginator.get_page(page)
        serialized = serializer_class(page_obj, many=True)
        return Response({
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page,
            "results": serialized.data
        })


class PingTestView(APIView, FilteredListMixin):
    def post(self, request):
        serializer = PingTestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        return self.filter_queryset(PingTest, PingTestSerializer, request)


class DNSTestView(APIView, FilteredListMixin):
    def post(self, request):
        serializer = DNSTestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        return self.filter_queryset(DNSTest, DNSTestSerializer, request)


class WebResponseTestView(APIView, FilteredListMixin):
    def post(self, request):
        serializer = WebResponseTestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        return self.filter_queryset(WebResponseTest, WebResponseTestSerializer, request)


class HTTPUploadTestView(APIView, FilteredListMixin):
    def post(self, request):
        serializer = HTTPUploadTestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        return self.filter_queryset(HTTPUploadTest, HTTPUploadTestSerializer, request)


class HTTPDownloadTestView(APIView, FilteredListMixin):
    def post(self, request):
        serializer = HTTPDownloadTestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        return self.filter_queryset(HTTPDownloadTest, HTTPDownloadTestSerializer, request)


class SMSTestView(APIView, FilteredListMixin):
    def post(self, request):
        serializer = SMSTestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        return self.filter_queryset(SMSTest, SMSTestSerializer, request, time_field='timestamp_sent')
