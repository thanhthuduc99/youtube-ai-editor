# Downloads open-licensed fonts (SIL OFL), GSAP and Three.js into assets/ (free CDNs, no key). Run once per project.
# Everything is vendored so nothing is fetched at render time.
import re, urllib.request
from common import R

UA = {'User-Agent': 'Mozilla/5.0'}  # plain UA -> Google Fonts returns one full .ttf with Vietnamese glyphs
FONTS = {
    'display.ttf': 'https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800',
    'body.ttf': 'https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@500',
    'body-bold.ttf': 'https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@700',
    'mono.ttf': 'https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500',
    'ui.ttf': 'https://fonts.googleapis.com/css2?family=Inter:wght@500',  # app chrome in slides (browser, editor)
    'ui-bold.ttf': 'https://fonts.googleapis.com/css2?family=Inter:wght@600',
    'yt.ttf': 'https://fonts.googleapis.com/css2?family=Roboto:wght@400',  # YouTube page
    'yt-medium.ttf': 'https://fonts.googleapis.com/css2?family=Roboto:wght@500',
}
JS = {
    'gsap.min.js': 'https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js',
    'three/three.module.js': 'https://cdn.jsdelivr.net/npm/three@0.181.2/build/three.module.js',
    'three/three.core.js': 'https://cdn.jsdelivr.net/npm/three@0.181.2/build/three.core.js',
    'three/addons/loaders/GLTFLoader.js': 'https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/loaders/GLTFLoader.js',
    'three/addons/utils/BufferGeometryUtils.js': 'https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/utils/BufferGeometryUtils.js',
    'three/addons/environments/RoomEnvironment.js': 'https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/environments/RoomEnvironment.js',
    'three/addons/loaders/DRACOLoader.js': 'https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/loaders/DRACOLoader.js',
    'three/addons/renderers/CSS3DRenderer.js': 'https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/renderers/CSS3DRenderer.js',
    'three/draco/draco_decoder.js': 'https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/libs/draco/draco_decoder.js',
    'three/draco/draco_decoder.wasm': 'https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/libs/draco/draco_decoder.wasm',
    'three/draco/draco_wasm_wrapper.js': 'https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/libs/draco/draco_wasm_wrapper.js',
}
# Real app icons for the slide UIs: Material Symbols (Apache-2.0, YouTube/Chrome) and VS Code codicons (CC-BY-4.0).
MAT = 'https://cdn.jsdelivr.net/npm/@material-symbols/svg-400@0.40.2/rounded/{}.svg'
COD = 'https://cdn.jsdelivr.net/npm/@vscode/codicons@0.0.40/src/icons/{}.svg'
ICONS = {**{f'm-{n}': MAT.format(n) for n in (
    'play_arrow-fill', 'pause-fill', 'skip_next-fill', 'volume_up-fill', 'settings', 'closed_caption', 'fullscreen',
    'thumb_up', 'thumb_down', 'share', 'download', 'more_horiz', 'more_vert', 'search', 'mic-fill', 'notifications',
    'video_call', 'menu', 'lock', 'tune', 'arrow_back', 'arrow_forward', 'refresh', 'star', 'add', 'close',
    'check_circle-fill', 'content_cut', 'movie', 'account_circle-fill')},
    **{f'c-{n}': COD.format(n) for n in (
        'files', 'search', 'source-control', 'debug-alt', 'extensions', 'account', 'settings-gear', 'json',
        'chevron-down', 'chevron-right', 'close', 'split-horizontal', 'ellipsis', 'sparkle', 'terminal', 'file', 'play')}}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


F = R/'assets'/'fonts'; F.mkdir(parents=True, exist_ok=True)
for name, css_url in FONTS.items():
    if not (F/name).exists():
        url = re.findall(r'url\((https:[^)]+)\)', get(css_url).decode())[0]
        (F/name).write_bytes(get(url))
    print('font', name)
V = R/'assets'/'vendor'
for name, url in JS.items():
    (V/name).parent.mkdir(parents=True, exist_ok=True)
    if not (V/name).exists():
        (V/name).write_bytes(get(url))
    print('vendor', name)
I = R/'assets'/'ui'/'icons'; I.mkdir(parents=True, exist_ok=True)
for name, url in ICONS.items():
    if not (I/f'{name}.svg').exists():
        (I/f'{name}.svg').write_bytes(get(url))
print('icons', len(ICONS))
