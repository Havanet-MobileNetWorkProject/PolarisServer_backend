from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import ThresholdParameter, ThresholdLevel
from .serializers import UnifiedThresholdInputSerializer, ThresholdParameterSerializer

class ThresholdCreateView(APIView):
    def post(self, request):
        serializer = UnifiedThresholdInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data
        technology = data['technology']
        parameters = data['parameters']

        if technology in ['3G', '4G']:
            types = {p['signal_type'] for p in parameters}
            if 'quantity' not in types or 'quality' not in types:
                return Response(
                    {"error": f"{technology} must include both quantity and quality parameters."},
                    status=400
                )

        for param in parameters:
            if len(param['levels']) < 3:
                return Response(
                    {"error": f"Parameter '{param['name']}' must have at least 3 levels."}, status=400
                )

            param_obj = ThresholdParameter.objects.create(
                name=param['name'],
                technology=technology,
                signal_type=param['signal_type']
            )

            for lvl in param['levels']:
                ThresholdLevel.objects.create(
                    parameter=param_obj,
                    level=lvl['level'],
                    color=lvl['color'],
                    min_value=lvl['min'],
                    max_value=lvl['max']
                )

        return Response({"message": "Thresholds created successfully."}, status=201)


class ThresholdListView(ListAPIView):
    serializer_class = ThresholdParameterSerializer

    def get_queryset(self):
        qs = ThresholdParameter.objects.prefetch_related("levels").all()
        tech = self.request.query_params.get("technology")
        name = self.request.query_params.get("name")

        if tech:
            qs = qs.filter(technology=tech)
        if name:
            qs = qs.filter(name=name)

        return qs
