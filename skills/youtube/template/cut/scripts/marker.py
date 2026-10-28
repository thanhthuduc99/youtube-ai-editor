# Spoken cut command ("Hey Ryan, cắt đoạn này"): the speaker flags the take they just botched and says it again.
# Whisper spells the English name many ways, so tokens are matched without diacritics.
import re, unicodedata

WAKE = {'ryan', 'rayan', 'raian', 'rian', 'rain', 'rai', 'ran', 'run', 'rien', 'brian', 'bryan', 'rhyan'}
HEY = {'hey', 'hay', 'he', 'e', 'ey', 'ay', 'ei', 'hi'}
CMD = {'doan', 'cho', 'cau', 'khuc', 'lai', 'di'}
TAIL = {'nay', 'nha', 'di', 'nhe', 'ne', 'ha', 'lai', 'nhen'}


def fold(s):
    s = unicodedata.normalize('NFD', s.lower().replace('đ', 'd'))
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))


def find_markers(words):
    """(first, last) word index of each cut command in a time-ordered word list: wake word, then "cắt <đoạn|chỗ|...>"."""
    t = [fold(w['w']) for w in words]
    out = []
    for i, x in enumerate(t):
        if x != 'cat' or i+1 >= len(t) or t[i+1] not in CMD:
            continue
        j = next((k for k in range(i-1, max(-1, i-4), -1) if t[k] in WAKE), None)
        if j is None:
            continue
        if j > 0 and t[j-1] in HEY:
            j -= 1
        e = i+1
        while e+1 < len(t) and e-i < 3 and t[e+1] in TAIL:
            e += 1
        if not out or j > out[-1][1]:
            out.append((j, e))
    return out


# Spoken edit request ("Hey Claude, chèn ảnh chụp trang này vào", "Hey Claude, quay màn hình đoạn này"): the speaker asks
# for a B-roll / screenshot / screen recording at this point. The request is cut out of the video and becomes a note.
# The video itself often talks about Claude, so the wake word only counts right after "hey" / "ê" (fold makes ê -> e).
CLAUDE = {'claude', 'claud', 'claudee', 'cloud', 'clau', 'clao', 'clo', 'clot', 'clod', 'klaud', 'klod', 'clause', 'claus', 'clow', 'colot'}


def find_edit_requests(words):
    """Word index where each "Hey Claude ..." request starts (the "hey")."""
    t = [fold(w['w']) for w in words]
    return [i-1 for i, x in enumerate(t) if x in CLAUDE and i > 0 and t[i-1] in HEY]
