from django.contrib import admin

from .models import *


admin.site.register(PingTest  )
admin.site.register(DNSTest  )
admin.site.register(WebResponseTest  )
admin.site.register(SMSTest  )
admin.site.register(HTTPUploadTest  )
admin.site.register(HTTPDownloadTest  )



