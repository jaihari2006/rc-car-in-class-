import sys
import math
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
FPS = 30
TOTAL_FRAMES = 1020 # 34.0 seconds

# Load fonts
try:
    font_hero = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 72)
    font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 52)
    font_heading = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
    font_badge = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
    font_body = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
    font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
except:
    font_hero = font_title = font_heading = font_badge = font_body = font_small = None

# Pre-load all assets
img_classroom = Image.open('attachments/407deb83-404f-4e7f-9d34-a45dea19b75d/1794374394518.png').convert('RGB')
img_logo = Image.open('logo.png').convert('RGBA')
img_gameplay = Image.open('images/gameplay-nitro.jpg').convert('RGB')
img_multiplayer = Image.open('images/multiplayer-sensei.jpg').convert('RGB')
img_characters = Image.open('images/characters.png').convert('RGBA')
img_banner = Image.open('images/banner.jpg').convert('RGB')

# Pre-rendered Scene 5 backdrop + crew
scene5_bg = img_classroom.resize((W, H), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(14))
c_h = 1080
c_w = int(img_characters.width * (c_h / img_characters.height))
crew_resized = img_characters.resize((c_w, c_h), Image.Resampling.LANCZOS)
scene5_base = scene5_bg.copy()
scene5_base.paste(crew_resized, ((W - c_w) // 2, 0), crew_resized)

def get_ken_burns(img, p, z_start=1.0, z_end=1.12, cx_start=0.5, cx_end=0.5, cy_start=0.5, cy_end=0.5):
    iw, ih = img.size
    zoom = z_start + (z_end - z_start) * p
    cx = cx_start + (cx_end - cx_start) * p
    cy = cy_start + (cy_end - cy_start) * p
    
    crop_w = int(iw / zoom)
    crop_h = int(crop_w * (H / W))
    if crop_h > ih:
        crop_h = int(ih / zoom)
        crop_w = int(crop_h * (W / H))
        
    left = max(0, min(iw - crop_w, int(cx * iw - crop_w / 2)))
    top = max(0, min(ih - crop_h, int(cy * ih - crop_h / 2)))
    
    crop = img.crop((left, top, left + crop_w, top + crop_h))
    return crop.resize((W, H), Image.Resampling.BILINEAR)

def draw_card(draw, box, fill, border=None, r=16, border_width=3):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=border, width=border_width if border else 0)

def draw_text_centered(draw, text, cx, cy, font, fill, shadow_fill=(0, 0, 0, 230), offset=(3, 3)):
    if not font:
        draw.text((cx, cy), text, fill=fill)
        return
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = cx - tw // 2
    y = cy - th // 2
    if shadow_fill:
        draw.text((x + offset[0], y + offset[1]), text, fill=shadow_fill, font=font)
    draw.text((x, y), text, fill=fill, font=font)

def draw_letterbox(draw, thickness=70, accent_color=(255, 215, 80)):
    draw.rectangle([0, 0, W, thickness], fill=(8, 6, 14))
    draw.rectangle([0, H - thickness, W, H], fill=(8, 6, 14))
    if accent_color:
        draw.line([(0, thickness), (W, thickness)], fill=accent_color, width=2)
        draw.line([(0, H - thickness), (W, H - thickness)], fill=accent_color, width=2)

def render_frame(f):
    t = f / FPS # seconds
    
    # SCENE 1: The Classroom Hook (0.0s to 4.5s -> f: 0..134)
    if f < 135:
        p = f / 135
        base = get_ken_burns(img_classroom, p, z_start=1.0, z_end=1.08, cx_start=0.5, cx_end=0.52, cy_start=0.48, cy_end=0.52)
        
        # Vignette
        vignette = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        vd = ImageDraw.Draw(vignette)
        vd.rectangle([0, 0, W, H], fill=(10, 8, 16, int(60 + 25 * math.sin(p * math.pi))))
        base = Image.alpha_composite(base.convert('RGBA'), vignette).convert('RGB')
        
        draw = ImageDraw.Draw(base)
        draw_letterbox(draw, thickness=75, accent_color=(0, 240, 255))
        
        # Fade in text 1
        if t >= 0.5:
            alpha_p = min(1.0, (t - 0.5) / 0.8)
            draw_card(draw, [400, 130, 1520, 205], (16, 12, 28, int(225 * alpha_p)), (0, 240, 255, int(220 * alpha_p)), r=14)
            draw_text_centered(draw, 'WHEN CLASS IS IN SESSION...', 960, 167, font_heading, (255, 255, 255))
            
        # Fade in text 2
        if t >= 2.0:
            alpha_p = min(1.0, (t - 2.0) / 0.8)
            draw_card(draw, [440, 225, 1480, 305], (24, 16, 12, int(235 * alpha_p)), (255, 215, 80, int(240 * alpha_p)), r=14)
            draw_text_centered(draw, '...THE RACING ESCAPE BEGINS.', 960, 265, font_title, (255, 215, 80))
            
        # Voice subtitled alert
        if 1.4 <= t <= 4.0:
            draw_card(draw, [480, 860, 1440, 930], (180, 20, 30, 235), (255, 255, 255), r=12)
            draw_text_centered(draw, '★ SENSEI: "Hey! Who is driving that RC car?!" ★', 960, 895, font_badge, (255, 255, 255))
            
        # Transition out flash
        if f > 125:
            flash_p = (f - 125) / 10
            flash = Image.new('RGBA', (W, H), (255, 255, 255, int(255 * flash_p)))
            base = Image.alpha_composite(base.convert('RGBA'), flash).convert('RGB')
            
        return base

    # SCENE 2: The Acceleration & Title Blast (4.5s to 8.5s -> f: 135..254)
    elif f < 255:
        p = (f - 135) / 120
        # Background: high-energy dark racing grid with neon cyan streaks
        base = Image.new('RGB', (W, H), (12, 8, 22))
        draw = ImageDraw.Draw(base)
        
        # Perspective speed lines
        for i in range(24):
            ang = (i / 24) * 2 * math.pi + p * 1.5
            x2 = 960 + math.cos(ang) * 1200
            y2 = 540 + math.sin(ang) * 800
            col = (0, 220, 255) if i % 2 == 0 else (255, 120, 0)
            draw.line([(960, 540), (x2, y2)], fill=col, width=3)
            
        # Center glow
        glow_r = int(320 + 40 * math.sin(p * 8))
        draw.ellipse([960 - glow_r, 540 - glow_r, 960 + glow_r, 540 + glow_r], fill=(20, 16, 40))
        
        # Animated Logo Zoom
        logo_scale = min(1.0, 0.45 + p * 0.65)
        lw = int(480 * logo_scale)
        lh = int(500 * logo_scale)
        logo_resized = img_logo.resize((lw, lh), Image.Resampling.LANCZOS)
        base.paste(logo_resized, (960 - lw // 2, 280 - lh // 2), logo_resized)
        
        draw = ImageDraw.Draw(base)
        draw_letterbox(draw, thickness=65, accent_color=(255, 215, 80))
        
        # Giant 3D Title
        draw_card(draw, [280, 560, 1640, 680], (16, 12, 28, 240), (0, 240, 255), r=20, border_width=4)
        draw_text_centered(draw, 'RC CAR IN CLASS', 960, 620, font_hero, (255, 255, 255))
        
        draw_card(draw, [420, 710, 1500, 780], (30, 20, 10, 230), (255, 215, 80), r=14, border_width=2)
        draw_text_centered(draw, '★ 3D CLASSROOM ESCAPE RACER ★', 960, 745, font_heading, (255, 215, 80))
        
        # Badges row
        draw_card(draw, [320, 810, 680, 870], (5, 120, 80, 235), (52, 211, 153), r=12)
        draw_text_centered(draw, '★ 21 TUNED CARS', 500, 840, font_badge, (255, 255, 255))
        
        draw_card(draw, [720, 810, 1200, 870], (180, 80, 10, 235), (245, 158, 11), r=12)
        draw_text_centered(draw, '★ PORSCHE FLAT-6 SOUND', 960, 840, font_badge, (255, 255, 255))
        
        draw_card(draw, [1240, 810, 1600, 870], (120, 40, 180, 235), (192, 132, 252), r=12)
        draw_text_centered(draw, '⚡ REAL DRIFT PHYSICS', 1420, 840, font_badge, (255, 255, 255))
        
        # Voice subtitle
        if 6.8 <= t <= 8.5:
            draw_card(draw, [540, 910, 1380, 965], (16, 140, 100, 235), (255, 255, 255), r=12)
            draw_text_centered(draw, '★ HINATA: "Let\'s race, Senpai! Full throttle!" ★', 960, 937, font_badge, (255, 255, 255))
            
        return base

    # SCENE 3: High-Octane Drift & Nitro Gameplay (8.5s to 14.5s -> f: 255..434)
    elif f < 435:
        p = (f - 255) / 180
        base = get_ken_burns(img_gameplay, p, z_start=1.02, z_end=1.14, cx_start=0.48, cx_end=0.55, cy_start=0.52, cy_end=0.48)
        
        draw = ImageDraw.Draw(base)
        draw_letterbox(draw, thickness=70, accent_color=(0, 240, 255))
        
        # Dynamic Top Banner
        draw_card(draw, [60, 90, 740, 160], (14, 10, 24, 230), (0, 240, 255), r=14, border_width=3)
        draw_text_centered(draw, '⚡ HIGH-OCTANE DRIFTING & NITRO', 400, 125, font_badge, (0, 240, 255))
        
        # Feature Highlights Cards on Right
        draw_card(draw, [1180, 105, 1860, 195], (20, 16, 34, 230), (52, 211, 153), r=14, border_width=2)
        draw_text_centered(draw, '★ 4 UNIQUE CLASSROOM TRACKS', 1520, 135, font_badge, (255, 255, 255))
        draw_text_centered(draw, 'Classic Lab • Gym Ramp • Art Studio • Sunset', 1520, 168, font_small, (52, 211, 153))
        
        draw_card(draw, [1180, 215, 1860, 305], (20, 16, 34, 230), (255, 215, 80), r=14, border_width=2)
        draw_text_centered(draw, '★ 21 UNLOCKABLE CARS', 1520, 245, font_badge, (255, 255, 255))
        draw_text_centered(draw, 'Porsche 911 GT3 RS, Muscle, Cyber & Karts', 1520, 278, font_small, (255, 215, 80))
        
        draw_card(draw, [1180, 325, 1860, 415], (20, 16, 34, 230), (244, 63, 94), r=14, border_width=2)
        draw_text_centered(draw, '★ UNDERGLOW & CUSTOM PAINTS', 1520, 355, font_badge, (255, 255, 255))
        draw_text_centered(draw, 'Neon lighting, turbo boost & custom tuning', 1520, 388, font_small, (244, 63, 94))
        
        # Voice subtitle
        if 10.0 <= t <= 13.5:
            draw_card(draw, [540, 880, 1380, 945], (2, 132, 199, 235), (255, 255, 255), r=12)
            draw_text_centered(draw, '★ CLASSMATE: "Look at that drift!" ★', 960, 912, font_badge, (255, 255, 255))
            
        return base

    # SCENE 4: Sensei Tag Multiplayer Mayhem (14.5s to 20.5s -> f: 435..614)
    elif f < 615:
        p = (f - 435) / 180
        base = get_ken_burns(img_multiplayer, p, z_start=1.0, z_end=1.12, cx_start=0.52, cx_end=0.48, cy_start=0.48, cy_end=0.52)
        
        # Alarm siren red pulse
        siren_alpha = int(45 * (0.5 + 0.5 * math.sin(p * 16)))
        siren = Image.new('RGBA', (W, H), (200, 20, 20, siren_alpha))
        base = Image.alpha_composite(base.convert('RGBA'), siren).convert('RGB')
        
        draw = ImageDraw.Draw(base)
        draw_letterbox(draw, thickness=70, accent_color=(255, 60, 60))
        
        # Alert Badge
        draw_card(draw, [60, 90, 800, 160], (160, 20, 20, 235), (255, 200, 200), r=14, border_width=3)
        draw_text_centered(draw, '★ SENSEI TAG MULTIPLAYER MODE ★', 430, 125, font_badge, (255, 255, 255))
        
        # Feature Badges
        draw_card(draw, [80, 200, 760, 290], (24, 16, 30, 230), (245, 158, 11), r=14, border_width=2)
        draw_text_centered(draw, '★ OUTRUN DETENTION', 420, 230, font_badge, (255, 255, 255))
        draw_text_centered(draw, 'Sensei patrols the room - stay fast or get caught!', 420, 262, font_small, (245, 158, 11))
        
        draw_card(draw, [80, 310, 760, 400], (24, 16, 30, 230), (0, 240, 255), r=14, border_width=2)
        draw_text_centered(draw, '⚡ 6 COMBAT GADGETS', 420, 340, font_badge, (255, 255, 255))
        draw_text_centered(draw, 'Slingshot, Magnet, Gale, Ink Cloud, Chalk & Jump!', 420, 372, font_small, (0, 240, 255))
        
        # Dialogue Subtitles
        if 15.2 <= t <= 17.8:
            draw_card(draw, [520, 870, 1400, 935], (180, 20, 30, 235), (255, 255, 255), r=12)
            draw_text_centered(draw, '★ SENSEI: "I\'m confiscating this!" ★', 960, 902, font_badge, (255, 255, 255))
        elif 18.0 <= t <= 20.2:
            draw_card(draw, [500, 870, 1420, 935], (220, 120, 10, 235), (255, 255, 255), r=12)
            draw_text_centered(draw, '★ SENSEI: "Whoa! Watch out!" (Sensei slips!) ★', 960, 902, font_badge, (255, 255, 255))
            
        return base

    # SCENE 5: Anime Crew & Real Voice Acting (20.5s to 26.5s -> f: 615..794)
    elif f < 795:
        p = (f - 615) / 180
        # High quality framed characters on subtle blurred classroom
        base = scene5_base.copy()
        
        draw = ImageDraw.Draw(base)
        draw_letterbox(draw, thickness=65, accent_color=(192, 132, 252))
        
        # Languages Cards at y = 730 (keeps bodies and heads pristine!)
        draw_card(draw, [100, 730, 620, 815], (20, 16, 32, 235), (244, 63, 94), r=14, border_width=2)
        draw_text_centered(draw, '★ JAPANESE CAST', 360, 757, font_badge, (255, 255, 255))
        draw_text_centered(draw, 'Authentic Anime Voice Acting', 360, 788, font_small, (244, 180, 195))
        
        draw_card(draw, [680, 730, 1240, 815], (20, 16, 32, 235), (56, 189, 248), r=14, border_width=2)
        draw_text_centered(draw, '★ ENGLISH CAST', 960, 757, font_badge, (255, 255, 255))
        draw_text_centered(draw, 'Sensei, Hinata & Ren', 960, 788, font_small, (180, 230, 255))
        
        draw_card(draw, [1300, 730, 1820, 815], (20, 16, 32, 235), (255, 215, 80), r=14, border_width=2)
        draw_text_centered(draw, '★ TAMIL CAST', 1560, 757, font_badge, (255, 255, 255))
        draw_text_centered(draw, 'Classroom Slang & Cheers', 1560, 788, font_small, (255, 235, 180))
        
        # Voice clips center badge
        draw_card(draw, [460, 835, 1460, 895], (45, 18, 65, 240), (192, 132, 252), r=14, border_width=2)
        draw_text_centered(draw, '★ 95+ REAL OFFLINE VOICE CLIPS • SENSEI & STUDENTS ★', 960, 865, font_badge, (255, 255, 255))
        
        # Active Voice Subtitles Showcase
        if 21.0 <= t <= 22.8:
            draw_card(draw, [420, 915, 1500, 980], (244, 63, 94, 240), (255, 255, 255), r=12)
            draw_text_centered(draw, '★ SENSEI (JAPANESE): "Tsukamaeta! (Detention for all of you!)" ★', 960, 947, font_badge, (255, 255, 255))
        elif 22.9 <= t <= 24.8:
            draw_card(draw, [420, 915, 1500, 980], (217, 119, 6, 240), (255, 255, 255), r=12)
            draw_text_centered(draw, '★ CLASSMATE (TAMIL): "Semma Drift! (Awesome Drift!)" ★', 960, 947, font_badge, (255, 255, 255))
        elif 24.9 <= t <= 26.5:
            draw_card(draw, [420, 915, 1500, 980], (180, 20, 30, 240), (255, 255, 255), r=12)
            draw_text_centered(draw, '★ SENSEI (ENGLISH): "You\'re all staying after class!" ★', 960, 947, font_badge, (255, 255, 255))
            
        return base

    # SCENE 6: Grand Finale & Call to Action (26.5s to 34.0s -> f: 795..1019)
    else:
        p = (f - 795) / 225
        base = get_ken_burns(img_banner, p, z_start=1.06, z_end=1.0, cx_start=0.5, cx_end=0.5, cy_start=0.5, cy_end=0.5)
        
        # Darkening for end card
        vignette = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        vd = ImageDraw.Draw(vignette)
        vd.rectangle([0, 0, W, H], fill=(12, 10, 20, int(110 + 70 * p)))
        base = Image.alpha_composite(base.convert('RGBA'), vignette).convert('RGB')
        
        draw = ImageDraw.Draw(base)
        draw_letterbox(draw, thickness=65, accent_color=(255, 215, 80))
        
        # Giant Title
        draw_card(draw, [250, 95, 1670, 215], (12, 16, 30, 240), (0, 240, 255), r=20, border_width=4)
        draw_text_centered(draw, 'RC CAR IN CLASS', 960, 155, font_hero, (255, 255, 255))
        
        draw_card(draw, [480, 235, 1440, 300], (35, 25, 10, 235), (255, 215, 80), r=14, border_width=2)
        draw_text_centered(draw, '★ OFFICIAL RELEASE v1.2.1 ★', 960, 267, font_heading, (255, 215, 80))
        
        # Platform Badges
        draw_card(draw, [200, 335, 680, 430], (12, 50, 32, 235), (52, 211, 153), r=15, border_width=3)
        draw_text_centered(draw, '★ ANDROID (APK)', 440, 368, font_badge, (255, 255, 255))
        draw_text_centered(draw, 'Native 60 FPS • Offline Play', 440, 403, font_small, (210, 255, 235))
        
        draw_card(draw, [720, 335, 1200, 430], (16, 38, 68, 235), (56, 189, 248), r=15, border_width=3)
        draw_text_centered(draw, '★ WINDOWS PC', 960, 368, font_badge, (255, 255, 255))
        draw_text_centered(draw, 'Gamepad Support • Ultra GFX', 960, 403, font_small, (210, 245, 255))
        
        draw_card(draw, [1240, 335, 1720, 430], (45, 20, 60, 235), (192, 132, 252), r=15, border_width=3)
        draw_text_centered(draw, '★ WEB BROWSER', 1480, 368, font_badge, (255, 255, 255))
        draw_text_centered(draw, 'Instant Play • GitHub Pages', 1480, 403, font_small, (240, 220, 255))
        
        # Free to play highlight
        draw_card(draw, [380, 465, 1540, 525], (20, 16, 32, 230), (255, 215, 80), r=14, border_width=2)
        draw_text_centered(draw, '100% FREE TO PLAY • NO ADS • NO IN-APP PURCHASES', 960, 495, font_badge, (255, 215, 80))
        
        # Download CTA
        draw_card(draw, [280, 560, 1640, 675], (12, 145, 90, 245), (255, 255, 255), r=18, border_width=3)
        draw_text_centered(draw, '★ DOWNLOAD FREE: GITHUB RELEASES v1.2.1 ★', 960, 603, font_heading, (255, 255, 255))
        draw_text_centered(draw, 'github.com/jaihari2006/rc-car-in-class-/releases', 960, 645, font_badge, (220, 255, 240))
        
        # Final voice cheer
        if 28.5 <= t <= 32.0:
            draw_card(draw, [620, 725, 1300, 785], (2, 132, 199, 235), (0, 230, 255), r=14)
            draw_text_centered(draw, '★ REN: "Awesome speed!" ★', 960, 755, font_badge, (255, 255, 255))
            
        # Fade to black at the very end (32.5s to 34.0s)
        if t >= 32.5:
            fade_p = min(1.0, (t - 32.5) / 1.5)
            black = Image.new('RGBA', (W, H), (0, 0, 0, int(255 * fade_p)))
            base = Image.alpha_composite(base.convert('RGBA'), black).convert('RGB')
            
        return base

if __name__ == '__main__':
    stdout = sys.stdout.buffer
    for f in range(TOTAL_FRAMES):
        frame = render_frame(f)
        stdout.write(frame.tobytes())
