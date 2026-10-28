# Example (2026-10-14): one instance of every talking-head template (th-*) on the raw Upwork intro, fed with real material:
# the Upwork profile screen recording, the 3 portfolio videos, the YouTube thumbnails. Copy the pattern, not the paths.
import json
from pathlib import Path

PROJ = Path(r'C:/work/youtube/projects/upwork-intro-th')
UP = 'C:/work/youtube/videos/2026/upwork'
INTRO, CHAT, VID, WEB = f'{UP}/intro.mp4', f'{UP}/chatbot upwork final.mp4', f'{UP}/video upwork final.mp4', f'{UP}/website final upwork.mp4'
TH = Path('C:/work/youtube/videos/thumbnail')
thumbs = [str(TH/n) for n in ('3d showroom.png', '45688fc8-afa1-4d05-a8dc-05b4dc67a849.png', '740460a1-9b05-481a-a7c1-dbf24474a2fd.png',
                              'b71e801e-1a5b-44cd-b6e6-1631e70581a7.png', 'buildchatbot.png', 'ChatGPT Image Aug 4, 2026, 11_44_23 PM.png',
                              'claude edit thumb.png', 'content.png', 'gemini 4.png', 'gpt 6 astra.png', 'he thnog content.png',
                              'jev new.png', 'lightrag.png', 'opus 5.5.png', 'self host n8n_yout.png', 'sonnet vs opus.png',
                              'youtube claude code.png', 'channel-thumb.png')]
portfolio = ([f'{CHAT}@{t}' for t in (2.5, 37.0)] + [f'{VID}@{t}' for t in (3.5, 24.4, 45.3, 66.2, 73.2)]
             + [f'{WEB}@{t}' for t in (20.3, 36.6, 77.3, 85.5, 109.9)] + [f'{INTRO}@{t}' for t in (41.6, 67.2)])
ov = []
add = lambda t, at, d, props, say: ov.append({'type': t, 'at': at, 'dur': d, 'props': props, 'say': say})
add('th-text', 1.52, 4.4, {'text': 'Thử thách *10k đô*', 'sub': 'trên Upwork', 'logo': 'upwork', 'side': 'right'},
    'video này sẽ kết thúc cho đến khi nào mình đạt được 10k đô ở trên Upwork')
add('th-side', 6.30, 7.6, {'clip': [INTRO, 0.0, 2], 'badge': 'Upwork', 'text': 'Freelancer nhận job *nước ngoài*', 'side': 'right'},
    'Upwork là một nền tảng giúp cho những người freelancer có thể tìm được những cái job ở thị trường nước ngoài')
add('th-chips', 14.24, 4.6, {'items': ['Tìm job', 'Gửi proposal', 'Làm việc', 'Nhận *tiền đô*']},
    'và nhận tiền đô cho những cái công việc đó')
add('th-lower', 19.08, 4.2, {'name': 'Thành Vũ Đức', 'role': 'AI Automation · *Contentta*'},
    'thì lý do mình bắt đầu cái thử thách này')
add('th-text', 27.64, 3.6, {'text': 'Mong ước *từ nhỏ*', 'sub': 'làm việc, nhận lương bằng đô', 'side': 'left'}, 'đó là một cái mong ước của mình từ hồi rất là nhỏ rồi')
add('th-wall', 35.76, 5.6, {'imgs': portfolio, 'text': 'Dự án cho *khách trong nước*'},
    'mình làm việc cho những người khách hàng ở trong nước và mình đã có một số cái kinh nghiệm')
add('th-page', 44.12, 6.2, {'img': f'{INTRO}@3.2', 'text': 'Mục tiêu *10.000$* trên Upwork'},
    'cái mục tiêu của cái thử thách lần này đó là cho đến khi nào mà mình đạt được 10.000$ ở trên Upwork')
add('th-blurcard', 54.40, 6.0, {'text': 'Từ *con số 0*', 'sub': 'bio trống, chưa có đồng nào', 'clip': [INTRO, 0.0, 3]},
    'mình sẽ show toàn bộ những cái quá trình mà mình làm từ một con số 0, từ một cái bio')
add('th-pip', 88.55, 5.8, {'clip': [INTRO, 28.0, 3]}, 'mình sẽ quay lại toàn bộ cái quá trình mà mình sẽ làm ở cái nền tảng Upwork này')
add('th-row', 110.05, 5.4, {'logo': 'upwork', 'text': 'Proposal, cover letter, *tips*', 'cards': [
    {'img': f'{INTRO}@3.2', 'label': 'Hồ sơ'}, {'img': f'{INTRO}@41.6', 'label': 'Portfolio'}, {'img': f'{INTRO}@67.2', 'label': 'Dự án'}]},
    'mình làm proposal như thế nào, mình viết cover letter như thế nào, tips and tricks')
add('th-column', 123.30, 6.2, {'imgs': thumbs, 'text': 'Xem hết *series* nhé', 'sub': 'kênh Thành Vũ Đức'},
    'Rất mong bạn sẽ xem hết video và có một cái điều gì đó bổ ích từ cái video này')
plan = {'style': 'basic', 'layout': {'face': [740, 140, 1180, 600]}, 'sections': [], 'zooms': [], 'overlays': ov}
(PROJ/'edit-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(ov), 'overlays')
