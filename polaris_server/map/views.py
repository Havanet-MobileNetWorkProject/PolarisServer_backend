# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.http import HttpResponse
# from rest_framework import status
# from django.utils.dateparse import parse_datetime
# from threshold.models import ThresholdParameter, ThresholdLevel
# from cellinfo.models import SignalTest2G, SignalTest3G, SignalTest4G, SignalTest5G
# from .serializers import ExportSignalDataSerializer
# import csv 
# from rest_framework.permissions import IsAuthenticated



# GEN_TECH_PARAMS = {
#     "2G": [("rxlev", "RxLev")],
#     "3G": [("rscp", "RSCP")],
#     "4G": [("rsrp", "RSRP"), ("rsrq", "RSRQ")],
#     "5G": [("rsrp", "RSRP"), ("rsrq", "RSRQ")],
# }

# class ExportKMLView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         tech = request.query_params.get("technology")
#         param_name = request.query_params.get("parameter")
#         client_id = request.query_params.get("client_id")
#         start = request.query_params.get("start")
#         end = request.query_params.get("end")

#         model_map = {
#             "2G": SignalTest2G,
#             "3G": SignalTest3G,
#             "4G": SignalTest4G,
#             "5G": SignalTest5G,
#         }

#         model = model_map.get(tech)
#         if not model:
#             return Response({"error": "Invalid or missing technology"}, status=400)

#         if request.user.is_staff:
#             qs = model.objects.all()
#             if client_id:
#                 qs = qs.filter(user__id=client_id)
#         else:
#             qs = model.objects.filter(user=request.user)

#         if start:
#             start_dt = parse_datetime(start)
#             if start_dt:
#                 qs = qs.filter(timestamp__gte=start_dt)
#         if end:
#             end_dt = parse_datetime(end)
#             if end_dt:
#                 qs = qs.filter(timestamp__lte=end_dt)

#         color_func = lambda _: "#FF0000"
#         if param_name:
#             if request.user.is_staff:
#                 threshold_param = ThresholdParameter.objects.filter(
#                     name=param_name, technology=tech
#                 )
#                 if client_id:
#                     threshold_param = threshold_param.filter(user__id=client_id)
#                 threshold_param = threshold_param.first()
#             else:
#                 threshold_param = ThresholdParameter.objects.filter(
#                     name=param_name, technology=tech, user=request.user
#                 ).first()
#             threshold_param = ThresholdParameter.objects.filter(name=param_name, technology=tech).first()
#             if threshold_param:
#                 levels = threshold_param.levels.all()

#                 def get_color(value):
#                     for lvl in levels:
#                         if lvl.min_value <= value <= lvl.max_value:
#                             return lvl.color
#                     return "#999999"

#                 color_func = get_color

#         kml = '<?xml version="1.0" encoding="UTF-8"?>\n'
#         kml += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
#         kml += '  <Document>\n'
#         kml += f'    <name>Polaris Drive Test ({tech})</name>\n'
#         print(kml)

#         tech_params = GEN_TECH_PARAMS.get(tech, [])

#         for obj in qs:
#             lat = obj.latitude
#             lon = obj.longitude
#             if lat is None or lon is None:
#                 continue

#             param_value = getattr(obj, param_name, None) if param_name else None
#             color = color_func(param_value) if param_value is not None else "#999999"

#             desc_lines = [
#                 f"<b>Client:</b> {safe_val(obj.client_id)}",
#                 f"<b>Time:</b> {obj.timestamp}",
#                 f"<b>Lat:</b> {lat}",
#                 f"<b>Lon:</b> {lon}",
#                 f"<b>Cell ID:</b> {safe_val(obj.cell_id)}",
#                 f"<b>PLMN:</b> {safe_val(obj.plmn_id)}",
#                 f"<b>Node ID:</b> {safe_val(getattr(obj, 'node_id', ''))}",
#                 f"<b>TAC:</b> {safe_val(getattr(obj, 'tac', ''))}",
#                 f"<b>LAC:</b> {safe_val(getattr(obj, 'lac', ''))}",
#                 f"<b>Band:</b> {safe_val(getattr(obj, 'band', ''))}",
#                 f"<b>ARFCN:</b> {safe_val(getattr(obj, 'arfcn', ''))}",
#             ]

#             for field, label in tech_params:
#                 val = safe_val(getattr(obj, field, ''))
#                 desc_lines.append(f"<b>{label}:</b> {val}")

#             description = "<br/>\n".join(desc_lines)

#             kml += f'''
# <Placemark>
#     <name>{obj.timestamp}</name>
#     <description><![CDATA[{description}]]></description>
#     <Style>
#         <IconStyle>
#             <color>{hex_to_kml_color(color)}</color>
#             <scale>1.1</scale>
#             <Icon>
#                 <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
#             </Icon>
#         </IconStyle>
#     </Style>
#     <Point>
#         <coordinates>{lon},{lat},0</coordinates>
#     </Point>
# </Placemark>
# '''

#         kml += '  </Document>\n'
#         kml += '</kml>'
#         print(kml)


#         response = HttpResponse(kml, content_type='application/vnd.google-earth.kml+xml')
#         response['Content-Disposition'] = 'attachment; filename="drive_test_export.kml"'
#         return response


# def hex_to_kml_color(hex_color):
#     hex_color = hex_color.lstrip('#')
#     if len(hex_color) == 6:
#         r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
#         return f"ff{b}{g}{r}"
#     return "ff999999"

# def safe_val(value):
#     return str(value) if value not in [None, "", "null"] else "-"


# class ExportCSVView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         tech = request.query_params.get("technology")
#         param_name = request.query_params.get("parameter")
#         level_filter = request.query_params.get("level")
#         client_id = request.query_params.get("client_id")
#         start = request.query_params.get("start")
#         end = request.query_params.get("end")

#         model_map = {
#             "2G": SignalTest2G,
#             "3G": SignalTest3G,
#             "4G": SignalTest4G,
#             "5G": SignalTest5G,
#         }

#         selected_models = [tech] if tech in model_map else model_map.keys()

#         all_rows = []

#         for t in selected_models:
#             model = model_map[t]
#             if request.user.is_staff:
#                 qs = model.objects.all()
#                 if client_id:
#                     qs = qs.filter(user__id=client_id)
#             else:
#                 qs = model.objects.filter(user=request.user)

#             if start:
#                 start_dt = parse_datetime(start)
#                 if start_dt:
#                     qs = qs.filter(timestamp__gte=start_dt)
#             if end:
#                 end_dt = parse_datetime(end)
#                 if end_dt:
#                     qs = qs.filter(timestamp__lte=end_dt)

#             if param_name and level_filter:
#                 try:
#                     level_filter = int(level_filter)
#                     if request.user.is_staff:
#                         threshold_param = ThresholdParameter.objects.filter(
#                             name=param_name, technology=t
#                         )
#                         if client_id:
#                             threshold_param = threshold_param.filter(user__id=client_id)
#                         threshold_param = threshold_param.first()
#                     else:
#                         threshold_param = ThresholdParameter.objects.filter(
#                             name=param_name, technology=t, user=request.user
#                         ).first()
#                     if threshold_param:
#                         matching_level = threshold_param.levels.filter(level=level_filter).first()
#                         if matching_level:
#                             qs = qs.filter(**{
#                                 f"{param_name}__gte": matching_level.min_value,
#                                 f"{param_name}__lte": matching_level.max_value
#                             })
#                 except ValueError:
#                     pass  

#             for obj in qs:
#                 all_rows.append([
#                     obj.timestamp,
#                     obj.latitude,
#                     obj.longitude,
#                     getattr(obj, 'rsrp', ''),
#                     getattr(obj, 'rsrq', ''),
#                     getattr(obj, 'rscp', ''),
#                     getattr(obj, 'rxlev', ''),
#                     obj.cell_id,
#                     obj.plmn_id,
#                     getattr(obj, 'node_id', ''),
#                     getattr(obj, 'tac', ''),
#                     getattr(obj, 'lac', ''),
#                     getattr(obj, 'band', ''),
#                     getattr(obj, 'arfcn', ''),
#                     t
#                 ])

#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="drive_test_export.csv"'

#         writer = csv.writer(response)
#         writer.writerow([
#             'timestamp', 'latitude', 'longitude',
#             'rsrp', 'rsrq', 'rscp', 'rxlev',
#             'cell_id', 'plmn_id', 'node_id', 'tac', 'lac',
#             'band', 'arfcn', 'scan_tech'
#         ])

#         for row in all_rows:
#             writer.writerow(row)

#         return response


# class MapDataView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         tech = request.query_params.get("technology")
#         param_name = request.query_params.get("parameter")
#         client_id = request.query_params.get("client_id")
#         start = request.query_params.get("start")
#         end = request.query_params.get("end")

#         if not tech or not param_name:
#             return Response({"error": "Technology and parameter are required."}, status=400)

#         model_map = {
#             "2G": SignalTest2G,
#             "3G": SignalTest3G,
#             "4G": SignalTest4G,
#             "5G": SignalTest5G,
#         }
#         model = model_map.get(tech)
#         if not model:
#             return Response({"error": "Invalid technology."}, status=400)

#         if request.user.is_staff:
#             qs = model.objects.all()
#             if client_id:
#                 qs = qs.filter(user__id=client_id)
#         else:
#             qs = model.objects.filter(user=request.user)

#         if start:
#             start_dt = parse_datetime(start)
#             if start_dt:
#                 qs = qs.filter(timestamp__gte=start_dt)
#         if end:
#             end_dt = parse_datetime(end)
#             if end_dt:
#                 qs = qs.filter(timestamp__lte=end_dt)

#         if request.user.is_staff:
#             threshold_param = ThresholdParameter.objects.filter(name=param_name, technology=tech)
#             if client_id:
#                 threshold_param = threshold_param.filter(user__id=client_id)
#             threshold_param = threshold_param.order_by("-id").first()
#         else:
#             threshold_param = ThresholdParameter.objects.filter(
#                 name=param_name, technology=tech, user=request.user
#             ).order_by("-id").first()
#         if not threshold_param:
#             return Response({"error": f"No threshold defined for {param_name} in {tech}"}, status=400)

#         levels = threshold_param.levels.all()

#         def get_level_and_color(value):
#             for lvl in levels:
#                 if lvl.min_value <= value <= lvl.max_value:
#                     return lvl.level, lvl.color, lvl.label
#             return None, "#999999", "Unknown"

#         result = []
#         for obj in qs:
#             value = getattr(obj, param_name, None)
#             if value is None:
#                 continue

#             level, color, label = get_level_and_color(value)

#             result.append({
#                 "latitude": obj.latitude,
#                 "longitude": obj.longitude,
#                 "value": value,
#                 "parameter": param_name,
#                 "color": color,
#                 "level": level,
#                 "label": label,
#                 "timestamp": obj.timestamp,
#                 "technology": obj.generation,
#                 "plmn_id": obj.plmn_id,
#                 "tac": getattr(obj, "tac", None),
#                 "lac": getattr(obj, "lac", None),
#                 "cell_id": obj.cell_id,
#                 "node_id": getattr(obj, "node_id", None),
#                 "band": getattr(obj, "band", None),
#                 "arfcn": getattr(obj, "arfcn", None),
#                 "scan_tech": tech,
#                 "power": get_signal_component(obj, tech, "quantity"),
#                 "quality": get_signal_component(obj, tech, "quality"),
#             })

#         return Response(result, status=200)

# def get_signal_component(obj, tech, signal_type):
#     param_map = {
#         "2G": {"quantity": "rxlev"},
#         "3G": {"quantity": "rscp"},
#         "4G": {"quantity": "rsrp", "quality": "rsrq"},
#         "5G": {"quantity": "rsrp", "quality": "rsrq"},  
#     }

#     param_name = param_map.get(tech, {}).get(signal_type)
#     if not param_name:
#         return None

#     value = getattr(obj, param_name, None)
#     if value is None:
#         return None

#     level = None
#     label = None
#     threshold_param = ThresholdParameter.objects.filter(name=param_name, technology=tech).first()
#     if threshold_param:
#         for lvl in threshold_param.levels.all():
#             if lvl.min_value <= value <= lvl.max_value:
#                 level = lvl.level
#                 label = lvl.label
#                 break

#     return {
#         "value": value,
#         "parameter": param_name,
#         "label": label
#     }


# class ExportJSONView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         tech = request.query_params.get("technology")
#         param_name = request.query_params.get("parameter")
#         level_filter = request.query_params.get("level")
#         client_id = request.query_params.get("client_id")
#         start = request.query_params.get("start")
#         end = request.query_params.get("end")

#         model_map = {
#             "2G": SignalTest2G,
#             "3G": SignalTest3G,
#             "4G": SignalTest4G,
#             "5G": SignalTest5G,
#         }

#         selected_models = [tech] if tech in model_map else model_map.keys()
#         result_data = []

#         for t in selected_models:
#             model = model_map[t]
#             if request.user.is_staff:
#                 qs = model.objects.all()
#                 if client_id:
#                     qs = qs.filter(user__id=client_id)
#             else:
#                 qs = model.objects.filter(user=request.user)

#             if start:
#                 start_dt = parse_datetime(start)
#                 if start_dt:
#                     qs = qs.filter(timestamp__gte=start_dt)
#             if end:
#                 end_dt = parse_datetime(end)
#                 if end_dt:
#                     qs = qs.filter(timestamp__lte=end_dt)

#             if param_name and level_filter:
#                 try:
#                     level_filter = int(level_filter)
#                     if request.user.is_staff:
#                         threshold_param = ThresholdParameter.objects.filter(
#                             name=param_name, technology=t
#                         )
#                         if client_id:
#                             threshold_param = threshold_param.filter(user__id=client_id)
#                         threshold_param = threshold_param.first()
#                     else:
#                         threshold_param = ThresholdParameter.objects.filter(
#                             name=param_name, technology=t, user=request.user
#                         ).first()
#                     if threshold_param:
#                         matching_level = threshold_param.levels.filter(level=level_filter).first()
#                         if matching_level:
#                             qs = qs.filter(**{
#                                 f"{param_name}__gte": matching_level.min_value,
#                                 f"{param_name}__lte": matching_level.max_value
#                             })
#                 except ValueError:
#                     pass

#             for obj in qs:
#                 result_data.append({
#                     'timestamp': obj.timestamp,
#                     'latitude': obj.latitude,
#                     'longitude': obj.longitude,
#                     'cell_id': obj.cell_id,
#                     'plmn_id': obj.plmn_id,
#                     'node_id': getattr(obj, 'node_id', None),
#                     'tac': getattr(obj, 'tac', None),
#                     'lac': getattr(obj, 'lac', None),
#                     'band': getattr(obj, 'band', None),
#                     'arfcn': getattr(obj, 'arfcn', None),
#                     'scan_tech': t,
#                     'rsrp': getattr(obj, 'rsrp', None),
#                     'rsrq': getattr(obj, 'rsrq', None),
#                     'rscp': getattr(obj, 'rscp', None),
#                     'rxlev': getattr(obj, 'rxlev', None),

#                 })

#         serializer = ExportSignalDataSerializer(result_data, many=True)
#         return Response(serializer.data, status=200)



from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.utils.dateparse import parse_datetime
from threshold.models import ThresholdParameter
from cellinfo.models import SignalTest2G, SignalTest3G, SignalTest4G, SignalTest5G
from .serializers import ExportSignalDataSerializer
import csv 
from rest_framework.permissions import IsAuthenticated
from threshold.defaults import default_thresholds  

GEN_TECH_PARAMS = {
    "2G": [("rxlev", "RxLev")],
    "3G": [("rscp", "RSCP")],
    "4G": [("rsrp", "RSRP"), ("rsrq", "RSRQ")],
    "5G": [("rsrp", "RSRP"), ("rsrq", "RSRQ")],
}

class ExportKMLView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        tech = request.query_params.get("technology")
        param_name = request.query_params.get("parameter")
        client_id = request.query_params.get("client_id")
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        model_map = {
            "2G": SignalTest2G,
            "3G": SignalTest3G,
            "4G": SignalTest4G,
            "5G": SignalTest5G,
        }

        model = model_map.get(tech)
        if not model:
            return Response({"error": "Invalid or missing technology"}, status=400)

        # فیلتر دیتا
        if request.user.is_staff:
            qs = model.objects.all()
            if client_id:
                qs = qs.filter(user__id=client_id)
        else:
            qs = model.objects.filter(user=request.user)

        if start:
            start_dt = parse_datetime(start)
            if start_dt:
                qs = qs.filter(timestamp__gte=start_dt)
        if end:
            end_dt = parse_datetime(end)
            if end_dt:
                qs = qs.filter(timestamp__lte=end_dt)

        # threshold
        color_func = lambda _: "#FF0000"
        if param_name:
            if request.user.is_staff:
                threshold_param = ThresholdParameter.objects.filter(name=param_name, technology=tech)
                if client_id:
                    threshold_param = threshold_param.filter(user__id=client_id)
                threshold_param = threshold_param.first()
            else:
                threshold_param = ThresholdParameter.objects.filter(
                    name=param_name, technology=tech, user=request.user
                ).first()

            if not threshold_param:
                # fallback به default.py
                default_levels = next(
                    (p["levels"] for p in default_thresholds.get(tech, []) if p["name"] == param_name),
                    []
                )
                def get_color(value):
                    for lvl in default_levels:
                        if lvl["min"] <= value <= lvl["max"]:
                            return lvl["color"]
                    return "#999999"
            else:
                levels = threshold_param.levels.all()
                def get_color(value):
                    for lvl in levels:
                        if lvl.min_value <= value <= lvl.max_value:
                            return lvl.color
                    return "#999999"

            color_func = get_color

        # ساخت KML
        kml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        kml += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
        kml += '  <Document>\n'
        kml += f'    <name>Polaris Drive Test ({tech})</name>\n'

        tech_params = GEN_TECH_PARAMS.get(tech, [])

        for obj in qs:
            lat = obj.latitude
            lon = obj.longitude
            if lat is None or lon is None:
                continue

            param_value = getattr(obj, param_name, None) if param_name else None
            color = color_func(param_value) if param_value is not None else "#999999"

            desc_lines = [
                f"<b>Client:</b> {safe_val(obj.client_id)}",
                f"<b>Time:</b> {obj.timestamp}",
                f"<b>Lat:</b> {lat}",
                f"<b>Lon:</b> {lon}",
                f"<b>Cell ID:</b> {safe_val(obj.cell_id)}",
                f"<b>PLMN:</b> {safe_val(obj.plmn_id)}",
                f"<b>Node ID:</b> {safe_val(getattr(obj, 'node_id', ''))}",
                f"<b>TAC:</b> {safe_val(getattr(obj, 'tac', ''))}",
                f"<b>LAC:</b> {safe_val(getattr(obj, 'lac', ''))}",
                f"<b>Band:</b> {safe_val(getattr(obj, 'band', ''))}",
                f"<b>ARFCN:</b> {safe_val(getattr(obj, 'arfcn', ''))}",
            ]

            for field, label in tech_params:
                val = safe_val(getattr(obj, field, ''))
                desc_lines.append(f"<b>{label}:</b> {val}")

            description = "<br/>\n".join(desc_lines)

            kml += f'''
<Placemark>
    <name>{obj.timestamp}</name>
    <description><![CDATA[{description}]]></description>
    <Style>
        <IconStyle>
            <color>{hex_to_kml_color(color)}</color>
            <scale>1.1</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
            </Icon>
        </IconStyle>
    </Style>
    <Point>
        <coordinates>{lon},{lat},0</coordinates>
    </Point>
</Placemark>
'''

        kml += '  </Document>\n'
        kml += '</kml>'

        response = HttpResponse(kml, content_type='application/vnd.google-earth.kml+xml')
        response['Content-Disposition'] = 'attachment; filename="drive_test_export.kml"'
        return response


def hex_to_kml_color(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
        return f"ff{b}{g}{r}"
    return "ff999999"

def safe_val(value):
    return str(value) if value not in [None, "", "null"] else "-"


class ExportCSVView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        tech = request.query_params.get("technology")
        param_name = request.query_params.get("parameter")
        level_filter = request.query_params.get("level")
        client_id = request.query_params.get("client_id")
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        model_map = {
            "2G": SignalTest2G,
            "3G": SignalTest3G,
            "4G": SignalTest4G,
            "5G": SignalTest5G,
        }

        selected_models = [tech] if tech in model_map else model_map.keys()

        all_rows = []

        for t in selected_models:
            model = model_map[t]
            if request.user.is_staff:
                qs = model.objects.all()
                if client_id:
                    qs = qs.filter(user__id=client_id)
            else:
                qs = model.objects.filter(user=request.user)

            if start:
                start_dt = parse_datetime(start)
                if start_dt:
                    qs = qs.filter(timestamp__gte=start_dt)
            if end:
                end_dt = parse_datetime(end)
                if end_dt:
                    qs = qs.filter(timestamp__lte=end_dt)

            if param_name and level_filter:
                try:
                    level_filter = int(level_filter)
                    if request.user.is_staff:
                        threshold_param = ThresholdParameter.objects.filter(name=param_name, technology=t)
                        if client_id:
                            threshold_param = threshold_param.filter(user__id=client_id)
                        threshold_param = threshold_param.first()
                    else:
                        threshold_param = ThresholdParameter.objects.filter(
                            name=param_name, technology=t, user=request.user
                        ).first()
                    if threshold_param:
                        matching_level = threshold_param.levels.filter(level=level_filter).first()
                        if matching_level:
                            qs = qs.filter(**{
                                f"{param_name}__gte": matching_level.min_value,
                                f"{param_name}__lte": matching_level.max_value
                            })
                except ValueError:
                    pass  

            for obj in qs:
                all_rows.append([
                    obj.timestamp,
                    obj.latitude,
                    obj.longitude,
                    getattr(obj, 'rsrp', ''),
                    getattr(obj, 'rsrq', ''),
                    getattr(obj, 'rscp', ''),
                    getattr(obj, 'rxlev', ''),
                    obj.cell_id,
                    obj.plmn_id,
                    getattr(obj, 'node_id', ''),
                    getattr(obj, 'tac', ''),
                    getattr(obj, 'lac', ''),
                    getattr(obj, 'band', ''),
                    getattr(obj, 'arfcn', ''),
                    t
                ])

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="drive_test_export.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'timestamp', 'latitude', 'longitude',
            'rsrp', 'rsrq', 'rscp', 'rxlev',
            'cell_id', 'plmn_id', 'node_id', 'tac', 'lac',
            'band', 'arfcn', 'scan_tech'
        ])

        for row in all_rows:
            writer.writerow(row)

        return response


class MapDataView(APIView):
    permission_classes = [IsAuthenticated]
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

        if request.user.is_staff:
            qs = model.objects.all()
            if client_id:
                qs = qs.filter(user__id=client_id)
        else:
            qs = model.objects.filter(user=request.user)

        if start:
            start_dt = parse_datetime(start)
            if start_dt:
                qs = qs.filter(timestamp__gte=start_dt)
        if end:
            end_dt = parse_datetime(end)
            if end_dt:
                qs = qs.filter(timestamp__lte=end_dt)

        if request.user.is_staff:
            threshold_param = ThresholdParameter.objects.filter(name=param_name, technology=tech)
            if client_id:
                threshold_param = threshold_param.filter(user__id=client_id)
            threshold_param = threshold_param.order_by("-id").first()
        else:
            threshold_param = ThresholdParameter.objects.filter(
                name=param_name, technology=tech, user=request.user
            ).order_by("-id").first()

        levels = []
        if threshold_param:
            levels = threshold_param.levels.all()
        else:
            levels = next(
                (p["levels"] for p in default_thresholds.get(tech, []) if p["name"] == param_name),
                []
            )

        def get_level_and_color(value):
            for lvl in levels:
                if (hasattr(lvl, "min_value") and lvl.min_value <= value <= lvl.max_value) or \
                   (isinstance(lvl, dict) and lvl["min"] <= value <= lvl["max"]):
                    return (lvl.level if hasattr(lvl, "level") else lvl["level"],
                            lvl.color if hasattr(lvl, "color") else lvl["color"])
            return None, "#999999"

        result = []
        for obj in qs:
            value = getattr(obj, param_name, None)
            if value is None:
                continue

            level, color = get_level_and_color(value)

            result.append({
                "latitude": obj.latitude,
                "longitude": obj.longitude,
                "value": value,
                "parameter": param_name,
                "color": color,
                "level": level,
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
        "3G": {"quantity": "rscp"},
        "4G": {"quantity": "rsrp", "quality": "rsrq"},
        "5G": {"quantity": "rsrp", "quality": "rsrq"},  
    }

    param_name = param_map.get(tech, {}).get(signal_type)
    if not param_name:
        return None

    value = getattr(obj, param_name, None)
    if value is None:
        return None

    threshold_param = ThresholdParameter.objects.filter(name=param_name, technology=tech).first()
    levels = []
    if threshold_param:
        levels = threshold_param.levels.all()
    else:
        levels = next(
            (p["levels"] for p in default_thresholds.get(tech, []) if p["name"] == param_name),
            []
        )

    return {
        "value": value,
        "parameter": param_name
    }


class ExportJSONView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        tech = request.query_params.get("technology")
        param_name = request.query_params.get("parameter")
        level_filter = request.query_params.get("level")
        client_id = request.query_params.get("client_id")
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        model_map = {
            "2G": SignalTest2G,
            "3G": SignalTest3G,
            "4G": SignalTest4G,
            "5G": SignalTest5G,
        }

        selected_models = [tech] if tech in model_map else model_map.keys()
        result_data = []

        for t in selected_models:
            model = model_map[t]
            if request.user.is_staff:
                qs = model.objects.all()
                if client_id:
                    qs = qs.filter(user__id=client_id)
            else:
                qs = model.objects.filter(user=request.user)

            if start:
                start_dt = parse_datetime(start)
                if start_dt:
                    qs = qs.filter(timestamp__gte=start_dt)
            if end:
                end_dt = parse_datetime(end)
                if end_dt:
                    qs = qs.filter(timestamp__lte=end_dt)

            if param_name and level_filter:
                try:
                    level_filter = int(level_filter)
                    if request.user.is_staff:
                        threshold_param = ThresholdParameter.objects.filter(name=param_name, technology=t)
                        if client_id:
                            threshold_param = threshold_param.filter(user__id=client_id)
                        threshold_param = threshold_param.first()
                    else:
                        threshold_param = ThresholdParameter.objects.filter(
                            name=param_name, technology=t, user=request.user
                        ).first()
                    if threshold_param:
                        matching_level = threshold_param.levels.filter(level=level_filter).first()
                        if matching_level:
                            qs = qs.filter(**{
                                f"{param_name}__gte": matching_level.min_value,
                                f"{param_name}__lte": matching_level.max_value
                            })
                except ValueError:
                    pass

            for obj in qs:
                result_data.append({
                    'timestamp': obj.timestamp,
                    'latitude': obj.latitude,
                    'longitude': obj.longitude,
                    'cell_id': obj.cell_id,
                    'plmn_id': obj.plmn_id,
                    'node_id': getattr(obj, 'node_id', None),
                    'tac': getattr(obj, 'tac', None),
                    'lac': getattr(obj, 'lac', None),
                    'band': getattr(obj, 'band', None),
                    'arfcn': getattr(obj, 'arfcn', None),
                    'scan_tech': t,
                    'rsrp': getattr(obj, 'rsrp', None),
                    'rsrq': getattr(obj, 'rsrq', None),
                    'rscp': getattr(obj, 'rscp', None),
                    'rxlev': getattr(obj, 'rxlev', None),
                })

        serializer = ExportSignalDataSerializer(result_data, many=True)
        return Response(serializer.data, status=200)
