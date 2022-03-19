from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.views import View
from django.shortcuts import render
from .camera import *


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        try:
            cam = VideoCamera()
            return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
        except Exception as e:
            print(e)
        return render(request, self.template_name)

