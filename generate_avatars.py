import math
from PIL import Image, ImageDraw, ImageFilter

def create_avatar_base(bg1, bg2, ring_col):
    # Create 512x512 image for supersampling
    im = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    # Outer ring
    d.ellipse([16, 16, 496, 496], fill=bg2)
    
    # Radial/concentric background gradient
    for r in range(230, 0, -6):
        t = r / 230.0
        r_c = int(bg1[0]*t + bg2[0]*(1-t))
        g_c = int(bg1[1]*t + bg2[1]*(1-t))
        b_c = int(bg1[2]*t + bg2[2]*(1-t))
        d.ellipse([256-r, 256-r, 256+r, 256+r], fill=(r_c, g_c, b_c, 255))
        
    return im, d

def finalize_avatar(im, ring_col, filename):
    d = ImageDraw.Draw(im)
    # Circular mask to keep within bounds
    mask = Image.new('L', (512, 512), 0)
    ImageDraw.Draw(mask).ellipse([20, 20, 492, 492], fill=255)
    
    # Border ring
    d.ellipse([20, 20, 492, 492], outline=ring_col, width=14)
    # Inner thin ring
    d.ellipse([34, 34, 478, 478], outline=(255, 255, 255, 90), width=4)
    
    # Downsample with Lanczos for smooth anti-aliased 256x256 result
    final = im.resize((256, 256), Image.Resampling.LANCZOS)
    final.save(f"avatars/{filename}")
    final.save(f"app/src/main/assets/avatars/{filename}")
    print(f"Generated {filename}")

# 1. FEMALE RACER (Elena - Speed Queen)
def gen_female():
    im, d = create_avatar_base((180, 20, 110), (35, 10, 45), (255, 60, 180))
    # Ponytail behind
    d.polygon([(140, 220), (80, 310), (100, 390), (170, 310)], fill=(70, 20, 45))
    d.polygon([(372, 220), (432, 310), (412, 390), (342, 310)], fill=(70, 20, 45))
    # Shoulders / Racing Suit
    d.polygon([(140, 510), (190, 400), (322, 400), (372, 510)], fill=(230, 30, 110))
    d.polygon([(210, 510), (230, 410), (282, 410), (302, 510)], fill=(30, 20, 45))
    # Neck
    d.rectangle([232, 350, 280, 410], fill=(245, 195, 170))
    # Head/Face
    d.ellipse([186, 170, 326, 370], fill=(255, 212, 185))
    # Cheeks
    d.ellipse([196, 290, 230, 315], fill=(255, 160, 160, 180))
    d.ellipse([282, 290, 316, 315], fill=(255, 160, 160, 180))
    # Hair / Front bangs
    d.polygon([(170, 220), (200, 150), (256, 170), (312, 150), (342, 220), (310, 210), (256, 220), (202, 210)], fill=(90, 25, 55))
    # Eyes & Lashes
    d.ellipse([210, 260, 236, 286], fill=(40, 20, 50))
    d.ellipse([276, 260, 302, 286], fill=(40, 20, 50))
    d.ellipse([214, 264, 226, 276], fill=(0, 230, 255))
    d.ellipse([280, 264, 292, 276], fill=(0, 230, 255))
    d.ellipse([220, 266, 224, 270], fill=(255, 255, 255))
    d.ellipse([286, 266, 290, 270], fill=(255, 255, 255))
    d.line([(206, 256), (240, 254)], fill=(20, 10, 20), width=4)
    d.line([(272, 254), (306, 256)], fill=(20, 10, 20), width=4)
    # Nose & Confident Smile
    d.line([(256, 285), (256, 295)], fill=(210, 150, 130), width=3)
    d.arc([240, 305, 272, 330], 10, 170, fill=(210, 40, 80), width=4)
    # Racing Visor Cap
    d.arc([165, 130, 347, 240], 180, 360, fill=(255, 45, 130), width=30)
    d.ellipse([160, 195, 352, 230], fill=(20, 20, 30, 220))
    d.ellipse([170, 200, 342, 222], outline=(0, 240, 255), width=4)
    finalize_avatar(im, (255, 60, 180), "avatar_female.png")

# 2. MALE RACER (Kai - Turbo Drift)
def gen_male():
    im, d = create_avatar_base((0, 140, 200), (10, 25, 45), (0, 220, 255))
    # Shoulders / Racing Suit
    d.polygon([(130, 510), (180, 395), (332, 395), (382, 510)], fill=(20, 80, 170))
    d.polygon([(210, 510), (230, 405), (282, 405), (302, 510)], fill=(255, 210, 60))
    # Neck
    d.rectangle([232, 345, 280, 405], fill=(240, 190, 160))
    # Head/Face
    d.ellipse([186, 170, 326, 365], fill=(250, 205, 175))
    # Spiky Dark Hair
    spikes = [(160, 200), (150, 130), (190, 150), (210, 100), (256, 130), (290, 95), (320, 145), (355, 125), (352, 200), (326, 210), (186, 210)]
    d.polygon(spikes, fill=(35, 35, 45))
    # Cyan Headband / Bandana
    d.rectangle([186, 195, 326, 228], fill=(0, 220, 255))
    d.line([(186, 228), (326, 228)], fill=(255, 255, 255), width=3)
    # Headset on ears
    d.ellipse([168, 240, 194, 290], fill=(255, 60, 60))
    d.ellipse([318, 240, 344, 290], fill=(255, 60, 60))
    d.arc([176, 180, 336, 270], 190, 350, fill=(40, 40, 50), width=6)
    # Eyebrows
    d.line([(206, 250), (238, 256)], fill=(30, 30, 40), width=6)
    d.line([(274, 256), (306, 250)], fill=(30, 30, 40), width=6)
    # Eyes
    d.ellipse([212, 264, 236, 288], fill=(25, 25, 35))
    d.ellipse([276, 264, 300, 288], fill=(25, 25, 35))
    d.ellipse([216, 268, 226, 278], fill=(0, 220, 255))
    d.ellipse([280, 268, 290, 278], fill=(0, 220, 255))
    d.ellipse([222, 268, 225, 272], fill=(255, 255, 255))
    d.ellipse([286, 268, 289, 272], fill=(255, 255, 255))
    # Nose & Grin
    d.line([(256, 288), (256, 298)], fill=(200, 150, 120), width=3)
    d.polygon([(242, 314), (270, 314), (266, 326), (246, 326)], fill=(255, 255, 255))
    d.arc([238, 308, 274, 332], 0, 180, fill=(30, 20, 20), width=4)
    finalize_avatar(im, (0, 220, 255), "avatar_male.png")

# 3. TEENAGE RACER (Zack - Cyber Gamer)
def gen_teen():
    im, d = create_avatar_base((110, 30, 180), (20, 10, 35), (180, 80, 255))
    # Neon Hoodie Shoulders
    d.polygon([(130, 510), (180, 390), (332, 390), (382, 510)], fill=(80, 25, 140))
    # Hoodie Strings (Neon Lime)
    d.line([(230, 410), (230, 490)], fill=(50, 255, 120), width=5)
    d.line([(282, 410), (282, 490)], fill=(50, 255, 120), width=5)
    # Neck & Chin
    d.rectangle([232, 345, 280, 400], fill=(245, 200, 175))
    # Head
    d.ellipse([186, 170, 326, 365], fill=(250, 205, 180))
    # Messy Purple Anime Hair
    hair = [(170, 210), (160, 150), (185, 140), (205, 110), (240, 140), (270, 95), (310, 130), (345, 115), (350, 180), (335, 210)]
    d.polygon(hair, fill=(130, 40, 210))
    # Cyber Visor / Neon Shades
    d.polygon([(190, 250), (322, 250), (310, 288), (202, 288)], fill=(20, 15, 30))
    d.polygon([(194, 254), (318, 254), (308, 284), (204, 284)], fill=(0, 255, 170))
    d.line([(204, 269), (308, 269)], fill=(255, 255, 255), width=2)
    # Nose & Smirk
    d.line([(256, 296), (256, 304)], fill=(210, 150, 130), width=3)
    d.arc([244, 314, 276, 332], 20, 160, fill=(30, 20, 30), width=4)
    # Big Gaming Headset
    d.ellipse([160, 230, 192, 295], fill=(50, 255, 120))
    d.ellipse([320, 230, 352, 295], fill=(50, 255, 120))
    d.arc([165, 150, 347, 260], 190, 350, fill=(40, 30, 60), width=10)
    finalize_avatar(im, (180, 80, 255), "avatar_teen.png")

# 4. MIDDLE AGE RACER (Marcus - Veteran Pro)
def gen_middle():
    im, d = create_avatar_base((190, 100, 20), (35, 20, 10), (255, 170, 40))
    # Brown Leather Racing Jacket
    d.polygon([(125, 510), (175, 385), (337, 385), (387, 510)], fill=(90, 50, 25))
    d.polygon([(220, 510), (236, 400), (276, 400), (292, 510)], fill=(210, 40, 35))
    # Collar
    d.polygon([(175, 385), (230, 430), (220, 385)], fill=(130, 75, 35))
    d.polygon([(337, 385), (282, 430), (292, 385)], fill=(130, 75, 35))
    # Neck
    d.rectangle([232, 340, 280, 400], fill=(235, 185, 150))
    # Head (Squarish jaw)
    d.ellipse([186, 170, 326, 360], fill=(240, 190, 155))
    # Short styled hair with silver temples
    d.arc([176, 150, 336, 240], 180, 360, fill=(60, 50, 45), width=24)
    d.rectangle([180, 160, 332, 205], fill=(60, 50, 45))
    d.polygon([(180, 220), (188, 195), (200, 220)], fill=(180, 180, 185))
    d.polygon([(332, 220), (324, 195), (312, 220)], fill=(180, 180, 185))
    # Aviator Sunglasses
    d.polygon([(200, 245), (245, 245), (242, 285), (206, 285)], fill=(20, 20, 25))
    d.polygon([(267, 245), (312, 245), (306, 285), (270, 285)], fill=(20, 20, 25))
    d.line([(198, 245), (314, 245)], fill=(255, 215, 60), width=3)
    d.line([(245, 252), (267, 252)], fill=(255, 215, 60), width=3)
    d.line([(208, 255), (235, 275)], fill=(255, 255, 255, 120), width=3)
    d.line([(275, 255), (302, 275)], fill=(255, 255, 255, 120), width=3)
    # Stubble beard & mustache
    d.arc([238, 298, 274, 320], 0, 180, fill=(70, 55, 50), width=5)
    d.ellipse([215, 308, 297, 345], outline=(100, 80, 70), width=3)
    finalize_avatar(im, (255, 170, 40), "avatar_middle.png")

# 5. OLD RACER (Grandpa Nitro - Senior Master)
def gen_old():
    im, d = create_avatar_base((100, 110, 125), (25, 28, 35), (210, 220, 235))
    # Classic Tweed Racing Vest & Scarf
    d.polygon([(125, 510), (175, 385), (337, 385), (387, 510)], fill=(65, 75, 60))
    d.polygon([(215, 395), (256, 440), (297, 395), (280, 510), (232, 510)], fill=(215, 190, 70))
    # Neck
    d.rectangle([232, 340, 280, 400], fill=(235, 185, 155))
    # Head & Wrinkles
    d.ellipse([186, 170, 326, 360], fill=(240, 190, 160))
    # Bushy White / Silver Hair
    d.arc([170, 150, 342, 260], 175, 365, fill=(230, 230, 235), width=28)
    # Round Retro Goggles resting on forehead
    d.ellipse([196, 190, 246, 236], fill=(40, 35, 30), outline=(215, 175, 50), width=5)
    d.ellipse([266, 190, 316, 236], fill=(40, 35, 30), outline=(215, 175, 50), width=5)
    d.line([(246, 213), (266, 213)], fill=(215, 175, 50), width=5)
    d.ellipse([204, 198, 238, 228], fill=(135, 206, 235, 140))
    d.ellipse([274, 198, 308, 228], fill=(135, 206, 235, 140))
    # Bushy eyebrows
    d.line([(206, 252), (238, 248)], fill=(230, 230, 235), width=7)
    d.line([(274, 248), (306, 252)], fill=(230, 230, 235), width=7)
    # Friendly smiling eyes with crow's feet
    d.arc([210, 262, 236, 282], 190, 350, fill=(35, 25, 20), width=4)
    d.arc([276, 262, 302, 282], 190, 350, fill=(35, 25, 20), width=4)
    d.line([(198, 268), (206, 272)], fill=(180, 140, 120), width=2)
    d.line([(314, 268), (306, 272)], fill=(180, 140, 120), width=2)
    # Big Bushy White Mustache
    d.ellipse([220, 298, 292, 330], fill=(235, 235, 240))
    finalize_avatar(im, (210, 220, 235), "avatar_old.png")

# 6. BABY RACER (Toby - Little Nitro)
def gen_baby():
    im, d = create_avatar_base((0, 160, 220), (10, 30, 50), (255, 220, 50))
    # Cute little baby romper
    d.polygon([(145, 510), (190, 410), (322, 410), (367, 510)], fill=(255, 180, 0))
    d.ellipse([236, 420, 276, 460], fill=(255, 255, 255))
    # Big chubby cheeks & round head
    d.ellipse([175, 190, 337, 360], fill=(255, 218, 195))
    d.ellipse([180, 275, 230, 315], fill=(255, 140, 150, 190))
    d.ellipse([282, 275, 332, 315], fill=(255, 140, 150, 190))
    # Oversized Gold Racing Helmet with Stars
    d.arc([160, 115, 352, 280], 175, 365, fill=(255, 200, 30), width=32)
    d.ellipse([160, 115, 352, 240], fill=(255, 205, 40))
    # Star on helmet
    d.polygon([(256, 140), (262, 155), (278, 155), (265, 165), (270, 180), (256, 170), (242, 180), (247, 165), (234, 155), (250, 155)], fill=(255, 50, 80))
    # Big Cute Baby Eyes
    d.ellipse([208, 245, 240, 280], fill=(25, 25, 35))
    d.ellipse([272, 245, 304, 280], fill=(25, 25, 35))
    d.ellipse([214, 250, 226, 262], fill=(255, 255, 255))
    d.ellipse([278, 250, 290, 262], fill=(255, 255, 255))
    d.ellipse([228, 268, 234, 274], fill=(255, 255, 255))
    d.ellipse([292, 268, 298, 274], fill=(255, 255, 255))
    # Cute Racing Pacifier
    d.ellipse([236, 302, 276, 334], fill=(0, 210, 255), outline=(255, 255, 255), width=3)
    d.arc([244, 320, 268, 344], 0, 180, fill=(0, 210, 255), width=4)
    finalize_avatar(im, (255, 220, 50), "avatar_baby.png")

# 7. PET DOG (Buster - Racer Pup)
def gen_pet_dog():
    im, d = create_avatar_base((210, 60, 30), (40, 15, 10), (255, 110, 60))
    # Checkered Racing Bandana
    d.polygon([(150, 510), (256, 430), (362, 510)], fill=(220, 30, 40))
    d.polygon([(256, 430), (220, 510), (256, 510)], fill=(255, 255, 255))
    d.polygon([(292, 510), (256, 430), (328, 510)], fill=(255, 255, 255))
    # Golden Puppy Head & Floppy Ears
    # Ears
    d.ellipse([130, 190, 195, 310], fill=(195, 125, 45))
    d.ellipse([317, 190, 382, 310], fill=(195, 125, 45))
    # Face
    d.ellipse([175, 180, 337, 350], fill=(235, 165, 80))
    # Cream Muzzle
    d.ellipse([210, 255, 302, 340], fill=(255, 235, 205))
    # Dog Nose
    d.ellipse([240, 265, 272, 288], fill=(30, 20, 20))
    d.ellipse([245, 268, 253, 274], fill=(255, 255, 255))
    # Dog Mouth & Happy Tongue
    d.line([(256, 288), (256, 302)], fill=(30, 20, 20), width=3)
    d.arc([238, 290, 256, 310], 0, 180, fill=(30, 20, 20), width=3)
    d.arc([256, 290, 274, 310], 0, 180, fill=(30, 20, 20), width=3)
    d.ellipse([248, 304, 264, 324], fill=(255, 90, 110))
    # Eyes
    d.ellipse([206, 232, 232, 258], fill=(35, 20, 15))
    d.ellipse([280, 232, 306, 258], fill=(35, 20, 15))
    d.ellipse([212, 236, 220, 244], fill=(255, 255, 255))
    d.ellipse([286, 236, 294, 244], fill=(255, 255, 255))
    # Aviator Goggles on forehead
    d.ellipse([196, 165, 248, 205], fill=(30, 30, 35), outline=(255, 215, 60), width=4)
    d.ellipse([264, 165, 316, 205], fill=(30, 30, 35), outline=(255, 215, 60), width=4)
    d.line([(248, 185), (264, 185)], fill=(255, 215, 60), width=4)
    d.line([(160, 185), (196, 185)], fill=(150, 75, 30), width=6)
    d.line([(316, 185), (352, 185)], fill=(150, 75, 30), width=6)
    finalize_avatar(im, (255, 110, 60), "avatar_pet_dog.png")

# 8. PET CAT (Luna - Speedy Kitty)
def gen_pet_cat():
    im, d = create_avatar_base((10, 150, 120), (5, 30, 25), (40, 230, 180))
    # Pilot Scarf & Golden Bell
    d.polygon([(170, 510), (256, 420), (342, 510)], fill=(235, 55, 95))
    d.ellipse([242, 425, 270, 453], fill=(255, 215, 50), outline=(200, 160, 30), width=2)
    # Cat Pointy Ears
    d.polygon([(160, 210), (180, 130), (225, 190)], fill=(45, 45, 50))
    d.polygon([(175, 200), (185, 145), (215, 185)], fill=(255, 150, 170))
    d.polygon([(352, 210), (332, 130), (287, 190)], fill=(45, 45, 50))
    d.polygon([(337, 200), (327, 145), (297, 185)], fill=(255, 150, 170))
    # Cat Head
    d.ellipse([175, 180, 337, 340], fill=(55, 55, 65))
    # Big Glowing Emerald Eyes
    d.ellipse([202, 225, 240, 265], fill=(30, 230, 140))
    d.ellipse([272, 225, 310, 265], fill=(30, 230, 140))
    # Slit pupils
    d.ellipse([218, 228, 224, 262], fill=(15, 20, 20))
    d.ellipse([288, 228, 294, 262], fill=(15, 20, 20))
    d.ellipse([214, 232, 220, 238], fill=(255, 255, 255))
    d.ellipse([284, 232, 290, 238], fill=(255, 255, 255))
    # Pink Nose & Whiskers
    d.polygon([(250, 275), (262, 275), (256, 283)], fill=(255, 130, 160))
    d.arc([244, 280, 256, 294], 0, 180, fill=(200, 200, 210), width=2)
    d.arc([256, 280, 268, 294], 0, 180, fill=(200, 200, 210), width=2)
    # Whiskers
    d.line([(180, 276), (235, 282)], fill=(230, 230, 240), width=3)
    d.line([(180, 292), (235, 290)], fill=(230, 230, 240), width=3)
    d.line([(332, 276), (277, 282)], fill=(230, 230, 240), width=3)
    d.line([(332, 292), (277, 290)], fill=(230, 230, 240), width=3)
    finalize_avatar(im, (40, 230, 180), "avatar_pet_cat.png")

# 9. PET BUNNY (Pip - Turbo Bunny)
def gen_pet_bunny():
    im, d = create_avatar_base((230, 120, 30), (45, 20, 10), (255, 165, 50))
    # Long Upright Bunny Ears
    d.ellipse([185, 80, 225, 230], fill=(245, 245, 250))
    d.ellipse([195, 105, 215, 210], fill=(255, 160, 180))
    d.ellipse([287, 80, 327, 230], fill=(245, 245, 250))
    d.ellipse([297, 105, 317, 210], fill=(255, 160, 180))
    # Scarf & Carrot Charm
    d.polygon([(160, 510), (256, 410), (352, 510)], fill=(0, 180, 230))
    d.polygon([(250, 420), (262, 420), (256, 450)], fill=(255, 110, 20))
    d.polygon([(253, 415), (259, 415), (256, 422)], fill=(40, 200, 60))
    # Fluffy Round White Head
    d.ellipse([175, 180, 337, 340], fill=(250, 250, 255))
    # Big Sparkling Ruby Eyes
    d.ellipse([204, 230, 236, 266], fill=(225, 35, 75))
    d.ellipse([276, 230, 308, 266], fill=(225, 35, 75))
    d.ellipse([210, 235, 222, 247], fill=(255, 255, 255))
    d.ellipse([282, 235, 294, 247], fill=(255, 255, 255))
    d.ellipse([224, 252, 230, 258], fill=(255, 255, 255))
    d.ellipse([296, 252, 302, 258], fill=(255, 255, 255))
    # Cute Y-shaped nose & mouth
    d.polygon([(252, 276), (260, 276), (256, 282)], fill=(255, 140, 160))
    d.line([(256, 282), (256, 290)], fill=(210, 130, 140), width=2)
    d.arc([246, 286, 256, 298], 0, 180, fill=(210, 130, 140), width=2)
    d.arc([256, 286, 266, 298], 0, 180, fill=(210, 130, 140), width=2)
    # Whiskers
    d.line([(180, 282), (235, 286)], fill=(200, 200, 210), width=2)
    d.line([(332, 282), (277, 286)], fill=(200, 200, 210), width=2)
    finalize_avatar(im, (255, 165, 50), "avatar_pet_bunny.png")

# 10. CYBER ROBOT PET (Sparky - Mech Hound)
def gen_robot():
    im, d = create_avatar_base((0, 80, 180), (10, 15, 35), (0, 240, 255))
    # Metallic Armor Shoulders
    d.polygon([(130, 510), (180, 390), (332, 390), (382, 510)], fill=(45, 55, 75))
    d.polygon([(220, 510), (236, 410), (276, 410), (292, 510)], fill=(0, 210, 255))
    # Antenna with glowing tip
    d.line([(256, 175), (256, 120)], fill=(120, 140, 170), width=6)
    d.ellipse([244, 108, 268, 132], fill=(255, 40, 70), outline=(255, 255, 255), width=2)
    # Robot Head
    d.polygon([(185, 180), (327, 180), (312, 340), (200, 340)], fill=(70, 85, 110))
    d.polygon([(195, 190), (317, 190), (304, 330), (208, 330)], fill=(95, 115, 145))
    # Screws on temples
    d.ellipse([190, 200, 204, 214], fill=(30, 35, 45))
    d.ellipse([308, 200, 322, 214], fill=(30, 35, 45))
    # Glowing Cyber Visor
    d.polygon([(206, 230), (306, 230), (298, 275), (214, 275)], fill=(10, 20, 30))
    d.polygon([(210, 234), (302, 234), (295, 271), (217, 271)], fill=(0, 240, 255))
    d.line([(220, 252), (292, 252)], fill=(255, 255, 255), width=4)
    # Speaker / Grille Mouth
    for y in [295, 303, 311]:
        d.line([(236, y), (276, y)], fill=(30, 40, 55), width=3)
    finalize_avatar(im, (0, 240, 255), "avatar_robot_pet.png")

gen_female()
gen_male()
gen_teen()
gen_middle()
gen_old()
gen_baby()
gen_pet_dog()
gen_pet_cat()
gen_pet_bunny()
gen_robot()
