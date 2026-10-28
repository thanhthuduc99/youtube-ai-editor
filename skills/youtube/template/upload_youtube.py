# Uploads a finished video to YouTube with title, description and thumbnail. OAuth from env vars or .env (never printed).
# Usage: python upload_youtube.py <video.mp4> <title> <description.txt> [--thumb thumb.jpg] [--privacy private|unlisted|public]
import argparse, json, os, re, time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

ap = argparse.ArgumentParser()
ap.add_argument('video'); ap.add_argument('title'); ap.add_argument('desc')
ap.add_argument('--thumb')
ap.add_argument('--privacy', default='private', choices=['private', 'unlisted', 'public'])
args = ap.parse_args()

# YOUTUBE_OAUTH_* from the environment, else from the .env file named by YOUTUBE_ENV (default ./.env)
ENV = Path(os.environ.get('YOUTUBE_ENV', '.env'))
ENV = ENV.read_text(encoding='utf-8') if ENV.exists() else ''
env = lambda k: os.environ.get(k) or re.search(rf'^\s*{k}\s*=\s*["\']?([^"\'\r\n]+)', ENV, re.M)[1].strip()
creds = Credentials(None, refresh_token=env('YOUTUBE_OAUTH_REFRESH_TOKEN'), client_id=env('YOUTUBE_OAUTH_CLIENT_ID'),
                    client_secret=env('YOUTUBE_OAUTH_CLIENT_SECRET'), token_uri='https://oauth2.googleapis.com/token',
                    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)
desc = Path(args.desc).read_text(encoding='utf-8').strip()
assert len(args.title) <= 100 and len(desc.encode('utf-8')) <= 5000, 'title > 100 chars or description > 5000 bytes'

body = {'snippet': {'title': args.title, 'description': desc, 'categoryId': '28', 'defaultLanguage': 'vi', 'defaultAudioLanguage': 'vi'},
        'status': {'privacyStatus': args.privacy, 'selfDeclaredMadeForKids': False}}
req = yt.videos().insert(part='snippet,status', body=body,
                         media_body=MediaFileUpload(args.video, mimetype='video/mp4', chunksize=16*1024*1024, resumable=True))
resp, tries = None, 0
while resp is None:
    try:
        st, resp = req.next_chunk()
        if st:
            print(f'{st.progress()*100:.0f}%', flush=True)
    except HttpError as e:
        if e.resp.status not in (500, 502, 503, 504) or tries >= 5:
            raise
        tries += 1; time.sleep(2**tries)
vid = resp['id']
if args.thumb:
    yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(args.thumb, mimetype='image/jpeg')).execute()
it = yt.videos().list(part='status,processingDetails', id=vid).execute()['items'][0]
print(json.dumps({'id': vid, 'url': f'https://youtu.be/{vid}', 'studio': f'https://studio.youtube.com/video/{vid}/edit',
                  'thumb': bool(args.thumb), 'status': it['status'], 'processing': it.get('processingDetails', {})}, ensure_ascii=False, indent=1))
