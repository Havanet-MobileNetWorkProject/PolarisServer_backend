from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import ThresholdParameter, ThresholdLevel
from .serializers import UnifiedThresholdInputSerializer, ThresholdParameterSerializer
from rest_framework.permissions import IsAuthenticated

class ThresholdCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UnifiedThresholdInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data
        technology = data['technology']
        parameters = data['parameters']


        for param in parameters:
            if len(param['levels']) < 3:
                return Response(
                    {"error": f"Parameter '{param['name']}' must have at least 3 levels."}, status=400
                )

            param_obj = ThresholdParameter.objects.filter(
                name=param['name'],
                technology=technology,
                signal_type=param['signal_type'],
                user=request.user.id
            ).first()

            param_obj.levels.all().delete()



            for lvl in param['levels']:
                ThresholdLevel.objects.create(
                    parameter=param_obj,
                    level=lvl['level'],
                    color=lvl['color'],
                    min_value=lvl['min'],
                    max_value=lvl['max'],
                )

        return Response({"message": "Thresholds created/updated successfully."}, status=201)



class ThresholdListView(ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ThresholdParameterSerializer

    def get_queryset(self):
        qs = ThresholdParameter.objects.prefetch_related("levels").all()
        tech = self.request.query_params.get("technology")
        name = self.request.query_params.get("name")
        user_id= self.request.query_params.get("user_id")


        if tech:
            qs = qs.filter(technology=tech)
        if name:
            qs = qs.filter(name=name)
        if user_id:
            qs = qs.filter(user=user_id)

        return qs
