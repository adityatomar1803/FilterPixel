from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from googleapiclient.discovery import build
import os
import boto3
from botocore import UNSIGNED
from botocore.config import Config
import os


from django.contrib.auth.views import LoginView




image_urls_s3 = []
image_urls = []

def getDriveData():
    api_key = 'AIzaSyC9EsfZeCgz44HlsV3GoFprD7FgltvO-Fo'

    service = build('drive', 'v3', developerKey=api_key)

    folder_id = '1_qOJ0z3kI_e2IJq4X6HqF0T1ROBESygS'

    results = service.files().list(q=f"'{folder_id}' in parents and mimeType contains 'image/'",
                                    fields="files(id)").execute()
    files = results.get('files', [])


    for file in files:
        exact_url = 'https://drive.google.com/uc?export=view&id=' + file['id']
        image_urls.append(exact_url)

def getS3Data():

    os.environ['AWS_DEFAULT_REGION'] = "ap-south-1"

    s3 = boto3.resource('s3',config=Config(signature_version=UNSIGNED))

    bucket = s3.Bucket('testbucketfp')

    for obj in bucket.objects.all():
        exact_url = 'https://testbucketfp.s3.amazonaws.com/'+obj.key
        image_urls_s3.append(exact_url)

getDriveData()
getS3Data()

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class UserLogin(LoginView):
    template_name = 'login.html'

class RedirectToLoginOrHomeView(LoginRequiredMixin, RedirectView):
    pattern_name = 'login'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse_lazy('home')  # Replace 'home' with the name of your home view URL pattern
        else:
            return reverse_lazy('login')

from django.http import JsonResponse

def get_data(request, id, index):

    data = []

    if not id and index <= len(image_urls_s3):
        if index+6 < len(image_urls_s3):
            data = image_urls_s3[index:index+6]
        else:
            data = image_urls_s3[index:]
        # data = image_urls_s3[index:index+6]

    elif id and index <= len(image_urls):
        if index+6 < len(image_urls):
            data = image_urls[index:index+6]
        else:
            data = image_urls[index:]

    print("data is" , data)
    return JsonResponse(data, safe=False)

class Home(LoginRequiredMixin, TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user

        context['drive_image_len'] = len(image_urls)
        context['s3_image_len'] = len(image_urls_s3)

        return context
