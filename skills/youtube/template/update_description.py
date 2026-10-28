# Replaces the description of an uploaded video with work/description.txt. OAuth from env vars or .env (never printed).
# Usage: python work/update_description.py <video id> <description.txt>
import os, re, sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# YOUTUBE_OAUTH_* from the environment, else from the .env file named by YOUTUBE_ENV (default ./.env)
ENV = Path(os.environ.get('YOUTUBE_ENV', '.env'))
ENV = ENV.read_text(encoding='utf-8') if ENV.exists() else ''
env = lambda k: os.environ.get(k) or re.search(rf'^\s*{k}\s*=\s*["\']?([^"\'\r\n]+)', ENV, re.M)[1].strip()
creds = Credentials(None, refresh_token=env('YOUTUBE_OAUTH_REFRESH_TOKEN'), client_id=env('YOUTUBE_OAUTH_CLIENT_ID'),
                    client_secret=env('YOUTUBE_OAUTH_CLIENT_SECRET'), token_uri='https://oauth2.googleapis.com/token',
                    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)
vid, desc = sys.argv[1], Path(sys.argv[2]).read_text(encoding='utf-8').strip()
sn = yt.videos().list(part='snippet', id=vid).execute()['items'][0]['snippet']
body = {'id': vid, 'snippet': {k: sn[k] for k in ('title', 'categoryId', 'defaultLanguage', 'defaultAudioLanguage', 'tags') if k in sn}}
body['snippet']['description'] = desc
yt.videos().update(part='snippet', body=body).execute()
print(yt.videos().list(part='snippet', id=vid).execute()['items'][0]['snippet']['description'][-200:])
