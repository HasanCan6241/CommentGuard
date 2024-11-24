from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from transformers import AutoTokenizer, TextClassificationPipeline, TFBertForSequenceClassification
from .models import Comment, Video
from urllib.parse import urlparse, parse_qs
import warnings
warnings.filterwarnings("ignore")
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  # Giriş kontrolü için gerekli modül
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from dotenv import load_dotenv
import os


load_dotenv()

# API anahtarı
API_KEY = os.getenv("API_KEY")  # Kendi API anahtarınızı buraya ekleyin
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Model ve tokenizer'ı yükleyin
tokenizer = AutoTokenizer.from_pretrained("nanelimon/bert-base-turkish-bullying")
model = TFBertForSequenceClassification.from_pretrained("nanelimon/bert-base-turkish-bullying", from_pt=True)

# Pipeline oluşturun
pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True, top_k=4)

# URL'den video ID'si çekme fonksiyonu
def get_video_id_from_url(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query).get('v', [None])[0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        elif parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    return None

@login_required
def youtube_search(request):
    return render(request, 'youtube_analyz.html')

def index(request):
    return render(request, 'index.html')

@login_required
def fetch_and_analyze_comments(request):
    if request.method == 'POST':
        # Get the URL from the POST request
        url = request.POST.get('url')

        # Extract video ID from the URL
        video_id = get_video_id_from_url(url)

        if video_id:
            # Fetch video details
            video_response = youtube.videos().list(part='snippet', id=video_id).execute()
            video_title = video_response['items'][0]['snippet']['title']
            video_description = video_response['items'][0]['snippet']['description']
            video_thumbnail = video_response['items'][0]['snippet']['thumbnails']['high']['url']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Fetch comments
            comment_response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=500
            ).execute()

            comments_data = []
            for item in comment_response['items']:
                comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                author_image_url = item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl']

                # Classify comment
                prediction = pipe(comment_text)
                category = prediction[0][0]['label']

                # Save comment to the database
                comment_entry = Comment(
                    video_id=video_id,
                    author=author,
                    text=comment_text,
                    category=category,
                    author_image_url=author_image_url
                )
                comment_entry.save()

                comments_data.append({
                    'author': author,
                    'text': comment_text,
                    'category': category
                })

            # Save video information to the database if not already present
            if not Video.objects.filter(video_id=video_id).exists():
                Video.objects.create(
                    video_id=video_id,
                    title=video_title,
                    description=video_description,
                    thumbnail_url=video_thumbnail,
                    video_url=video_url
                )

    videos = Video.objects.all()  # Get all videos from the database
    return render(request, 'search_videos.html', {'videos': videos})

def delete_video(request, video_id):
    if request.method == 'POST':
        # Video ve ilgili yorumları sil
        video = get_object_or_404(Video, video_id=video_id)
        Comment.objects.filter(video_id=video_id).delete()
        video.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def video_details(request, video_id):
    video = Video.objects.get(video_id=video_id)  # Get the video object from DB
    comments = Comment.objects.filter(video_id=video_id)  # Get the associated comments
    return render(request, 'video_details.html', {'video': video, 'comments': comments})

# Kullanıcı girişi view fonksiyonu

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('analyze')  # Ana sayfaya yönlendirme
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı')  # Hata mesajı ekleniyor
    return render(request, 'login.html')


# Kullanıcı çıkışı view fonksiyonu
@login_required
def logout_view(request):
    logout(request)
    return redirect('index')  # Giriş sayfasına yönlendirme