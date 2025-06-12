from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from threshold.models import ThresholdParameter, ThresholdLevel
from cellinfo.models import SignalTest2G, SignalTest3G, SignalTest4G, SignalTest5G
class MapDataView(APIView):
    def get(self, request):
        tech = request.query_params.get("technology")
        param_name = request.query_params.get("parameter")
        client_id = request.query_params.get("client_id")
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        if not tech or not param_name:
            return Response({"error": "Technology and parameter are required."}, status=400)

        model_map = {
            "2G": SignalTest2G,
            "3G": SignalTest3G,
            "4G": SignalTest4G,
            "5G": SignalTest5G,
        }
        model = model_map.get(tech)
        if not model:
            return Response({"error": "Invalid technology."}, status=400)

        qs = model.objects.all()
        if client_id:
            qs = qs.filter(client_id=client_id)
        if start:
            start_dt = parse_datetime(start)
            if start_dt:
                qs = qs.filter(timestamp__gte=start_dt)
        if end:
            end_dt = parse_datetime(end)
            if end_dt:
                qs = qs.filter(timestamp__lte=end_dt)

        threshold_param = (
            ThresholdParameter.objects
            .filter(name=param_name, technology=tech)
            .order_by('-id')
            .first()
        )
        if not threshold_param:
            return Response({"error": f"No threshold defined for {param_name} in {tech}"}, status=400)

        levels = threshold_param.levels.all()

        def get_level_and_color(value):
            for lvl in levels:
                if lvl.min_value <= value <= lvl.max_value:
                    return lvl.level, lvl.color, lvl.label
            return None, "#999999", "Unknown"

        result = []
        for obj in qs:
            value = getattr(obj, param_name, None)
            if value is None:
                continue

            level, color, label = get_level_and_color(value)

            result.append({
                "latitude": obj.latitude,
                "longitude": obj.longitude,
                "value": value,
                "parameter": param_name,
                "color": color,
                "level": level,
                "label": label,
                "timestamp": obj.timestamp,
                "technology": obj.generation,
                "plmn_id": obj.plmn_id,
                "tac": getattr(obj, "tac", None),
                "lac": getattr(obj, "lac", None),
                "cell_id": obj.cell_id,
                "node_id": getattr(obj, "node_id", None),
                "band": getattr(obj, "band", None),
                "arfcn": getattr(obj, "arfcn", None),
                "scan_tech": tech,
                "power": get_signal_component(obj, tech, "quantity"),
                "quality": get_signal_component(obj, tech, "quality"),
            })

        return Response(result, status=200)

def get_signal_component(obj, tech, signal_type):
    param_map = {
        "2G": {"quantity": "rxlev"},
        "3G": {"quantity": "rscp", "quality": "ecn0"},
        "4G": {"quantity": "rsrp", "quality": "rsrq"},
        "5G": {"quantity": "rsrp", "quality": "rsrq"},  # فرض بر مشابهت
    }

    param_name = param_map.get(tech, {}).get(signal_type)
    if not param_name:
        return None

    value = getattr(obj, param_name, None)
    if value is None:
        return None

    level = None
    label = None
    threshold_param = ThresholdParameter.objects.filter(name=param_name, technology=tech).first()
    if threshold_param:
        for lvl in threshold_param.levels.all():
            if lvl.min_value <= value <= lvl.max_value:
                level = lvl.level
                label = lvl.label
                break

    return {
        "value": value,
        "parameter": param_name,
        "label": label
    }

def get_label_for_level(level):
    labels = {
        1: "Very Weak",
        2: "Weak",
        3: "Moderate",
        4: "Good",
        5: "Excellent"
    }
    return labels.get(level, "Unknown")
