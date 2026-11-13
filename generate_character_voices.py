import asyncio
import base64
import json
import os
import subprocess
import time
import edge_tts

VOICE_DEFINITIONS = [
    # Sakamoto Sensei - English
    ("en_sensei_stop", "en-US-AriaNeural", "Hey! Stop right there!", "+15%", "+10Hz"),
    ("en_sensei_trash", "en-US-AriaNeural", "That toy is going in the trash!", "+15%", "+10Hz"),
    ("en_sensei_snap", "en-US-AriaNeural", "I'll snap that thing in half!", "+15%", "+10Hz"),
    ("en_sensei_detention", "en-US-AriaNeural", "Detention for a month!", "+15%", "+10Hz"),
    ("en_sensei_driving", "en-US-AriaNeural", "You call THAT driving?!", "+15%", "+10Hz"),
    ("en_sensei_confiscate", "en-US-AriaNeural", "I'm confiscating that junk!", "+15%", "+10Hz"),
    ("en_sensei_where", "en-US-AriaNeural", "Where is that toy?!", "+15%", "+10Hz"),
    ("en_sensei_whose", "en-US-AriaNeural", "Whose toy is that?!", "+15%", "+10Hz"),
    ("en_sensei_quiet", "en-US-AriaNeural", "Quiet down in class! Homework on my desk!", "+12%", "+8Hz"),
    ("en_sensei_gotcha", "en-US-AriaNeural", "Gotcha! That toy is confiscated!", "+18%", "+12Hz"),
    ("en_sensei_caught", "en-US-AriaNeural", "Caught you! Detention after class!", "+15%", "+10Hz"),
    ("en_sensei_fall1", "en-US-AriaNeural", "Gyaaaah! Missed!!", "+20%", "+15Hz"),
    ("en_sensei_fall2", "en-US-AriaNeural", "OOF! My face! Wait till I get back up!!", "+18%", "+12Hz"),
    ("en_sensei_way", "en-US-AriaNeural", "Hmph! This way then!", "+15%", "+8Hz"),
    ("en_sensei_nope", "en-US-AriaNeural", "Hmph! You had better not be lying!", "+12%", "+8Hz"),
    ("en_sensei_patrol", "en-US-AriaNeural", "No running in the hallway!", "+10%", "+6Hz"),

    # Sakamoto Sensei - Japanese Anime
    ("ja_sensei_stop", "ja-JP-NanamiNeural", "ちょっと！待ちなさい！", "+15%", "+12Hz"),
    ("ja_sensei_trash", "ja-JP-NanamiNeural", "そのおもちゃをゴミ箱に捨てるわよ！", "+18%", "+14Hz"),
    ("ja_sensei_snap", "ja-JP-NanamiNeural", "放課後職員室に来なさい！", "+15%", "+12Hz"),
    ("ja_sensei_confiscate", "ja-JP-NanamiNeural", "没収！絶対に返しません！", "+18%", "+14Hz"),
    ("ja_sensei_whose", "ja-JP-NanamiNeural", "そのおもちゃは誰の？！", "+15%", "+12Hz"),
    ("ja_sensei_where", "ja-JP-NanamiNeural", "あのおもちゃはどこへ行ったの？！", "+15%", "+12Hz"),
    ("ja_sensei_quiet", "ja-JP-NanamiNeural", "廊下を走らない！静かに自習しなさい！", "+12%", "+10Hz"),
    ("ja_sensei_gotcha", "ja-JP-NanamiNeural", "捕まえたわよ！観念しなさい！", "+18%", "+14Hz"),
    ("ja_sensei_fall1", "ja-JP-NanamiNeural", "きゃあっ！転んだ！", "+22%", "+16Hz"),
    ("ja_sensei_fall2", "ja-JP-NanamiNeural", "いたたた…！待ちなさい！", "+18%", "+12Hz"),
    ("ja_sensei_way", "ja-JP-NanamiNeural", "ふん！あっちね！逃がさないわよ！", "+15%", "+12Hz"),
    ("ja_sensei_nope", "ja-JP-NanamiNeural", "ふん！嘘をついてたら承知しないわよ！", "+15%", "+10Hz"),

    # Sakamoto Sensei - Tamil
    ("ta_sensei_stop", "ta-IN-PallaviNeural", "ஏய்! அங்கேயே நில்லு!", "+12%", "+8Hz"),
    ("ta_sensei_trash", "ta-IN-PallaviNeural", "அந்த பொம்மையை குப்பைத்தொட்டியில போடப்போறேன்!", "+14%", "+8Hz"),
    ("ta_sensei_confiscate", "ta-IN-PallaviNeural", "அந்த பழைய வண்டியை பறிமுதல் பண்றேன்!", "+14%", "+8Hz"),
    ("ta_sensei_gotcha", "ta-IN-PallaviNeural", "பிடிச்சிட்டேன்! இனிமேல் தப்ப முடியாது!", "+16%", "+10Hz"),
    ("ta_sensei_caught", "ta-IN-PallaviNeural", "மாட்டுனியா! வகுப்பு முடிஞ்சதும் ஸ்டாப் ரூமுக்கு வா!", "+14%", "+8Hz"),
    ("ta_sensei_fall", "ta-IN-PallaviNeural", "ஐயோ! வழுக்கி விழுந்துட்டேனே!!", "+18%", "+12Hz"),
    ("ta_sensei_quiet", "ta-IN-PallaviNeural", "அமைதியா இருங்க எல்லாரும்!", "+10%", "+6Hz"),
    ("ta_sensei_whose", "ta-IN-PallaviNeural", "அந்த பொம்மை யாருடையது?!", "+12%", "+8Hz"),

    # Sakura-kun - English
    ("en_sakura_behind", "en-US-GuyNeural", "Quick, behind me!", "+15%", "+14Hz"),
    ("en_sakura_hide", "en-US-GuyNeural", "Hide under my desk! Stay low!", "+16%", "+14Hz"),
    ("en_sakura_way", "en-US-GuyNeural", "It went that way, Sensei!", "+15%", "+12Hz"),
    ("en_sakura_nope", "en-US-GuyNeural", "I didn't see anything, Sensei...", "+10%", "+10Hz"),
    ("en_sakura_cheer", "en-US-GuyNeural", "Awesome drift! Keep going!", "+18%", "+15Hz"),

    # Sakura-kun - Japanese
    ("ja_sakura_behind", "ja-JP-KeitaNeural", "早く！僕の後ろに隠れて！", "+16%", "+16Hz"),
    ("ja_sakura_hide", "ja-JP-KeitaNeural", "こっちだ！僕の机の下に隠れろ！", "+16%", "+16Hz"),
    ("ja_sakura_way", "ja-JP-KeitaNeural", "先生！あっちに行きましたよ！", "+15%", "+14Hz"),
    ("ja_sakura_nope", "ja-JP-KeitaNeural", "えっ？何も見てませんけど…", "+12%", "+12Hz"),
    ("ja_sakura_cheer", "ja-JP-KeitaNeural", "いいぞ！その調子だ！", "+18%", "+16Hz"),

    # Sakura-kun - Tamil
    ("ta_sakura_hide", "ta-IN-ValluvarNeural", "சீக்கிரம், என் பின்னாடி ஒளிஞ்சுக்கோ!", "+14%", "+10Hz"),
    ("ta_sakura_way", "ta-IN-ValluvarNeural", "டீச்சர்! அது அந்த பக்கமா போச்சு!", "+14%", "+10Hz"),
    ("ta_sakura_nope", "ta-IN-ValluvarNeural", "நான் எதுவும் பார்க்கலையே டீச்சர்...", "+10%", "+8Hz"),

    # Hinata-chan - English
    ("en_hinata_hide", "en-US-AnaNeural", "Hide under my desk! I'll cover you!", "+14%", "+16Hz"),
    ("en_hinata_cheer", "en-US-AnaNeural", "Yay! You can do it! Go RC Car!", "+16%", "+18Hz"),
    ("en_hinata_way", "en-US-AnaNeural", "Sensei! It sped by the window!", "+15%", "+16Hz"),
    ("en_hinata_warn", "en-US-AnaNeural", "Look out! Sensei is turning!", "+18%", "+20Hz"),

    # Hinata-chan - Japanese
    ("ja_hinata_hide", "ja-JP-NanamiNeural", "こっちだよ！私の机の下に隠れて！", "+22%", "+30Hz"),
    ("ja_hinata_cheer", "ja-JP-NanamiNeural", "すごい！がんばって！", "+24%", "+32Hz"),
    ("ja_hinata_way", "ja-JP-NanamiNeural", "先生！窓の方へ走っていきました！", "+20%", "+28Hz"),
    ("ja_hinata_warn", "ja-JP-NanamiNeural", "危ない！先生が来るよ！", "+24%", "+32Hz"),

    # Hinata-chan - Tamil
    ("ta_hinata_hide", "ta-IN-PallaviNeural", "என் மேஜைக்கு அடியில ஒளிஞ்சுக்கோ!", "+18%", "+22Hz"),
    ("ta_hinata_cheer", "ta-IN-PallaviNeural", "சூப்பர்! உன்னால முடியும்!", "+20%", "+24Hz"),

    # Ren-kun - English & Japanese
    ("en_ren_hide", "en-US-AndrewNeural", "Under here, hurry! I've got your back.", "+12%", "+4Hz"),
    ("en_ren_cheer", "en-US-AndrewNeural", "Smooth drift. Clean line.", "+12%", "+4Hz"),
    ("ja_ren_hide", "ja-JP-KeitaNeural", "こっちだ、任せろ！", "+12%", "+6Hz"),
    ("ja_ren_cheer", "ja-JP-KeitaNeural", "すげえドリフトだ！", "+14%", "+8Hz"),

    # Classmates - English, Japanese & Tamil
    ("en_class_cool1", "en-US-RogerNeural", "Whoa! Cool!", "+18%", "+15Hz"),
    ("en_class_cool2", "en-US-EmmaNeural", "So cool! Sick car!", "+18%", "+16Hz"),
    ("en_class_warn", "en-US-RogerNeural", "Run! Sensei is mad!", "+20%", "+15Hz"),
    ("en_class_drift", "en-US-EmmaNeural", "Look at that drift!", "+18%", "+18Hz"),
    ("ja_class_cool", "ja-JP-KeitaNeural", "すっげー！超かっこいい！", "+20%", "+18Hz"),
    ("ja_class_warn", "ja-JP-NanamiNeural", "逃げろー！先生が怒ってるぞ！", "+22%", "+24Hz"),
    ("ja_class_drift", "ja-JP-NanamiNeural", "すげえドリフト！", "+22%", "+26Hz"),
    ("ta_class_cool", "ta-IN-ValluvarNeural", "செம! மாஸான கார்!", "+16%", "+12Hz"),
    ("ta_class_warn", "ta-IN-PallaviNeural", "ஓடுங்க! டீச்சருக்கு பயங்கர கோபம் வருது!", "+18%", "+16Hz"),
    ("ta_class_drift", "ta-IN-ValluvarNeural", "வாவ், என்ன ஒரு டிரிஃப்ட்!", "+16%", "+12Hz"),

    # Character Panic Reactions: Kick & Throw (Except Sensei)
    # Sakura-kun - English
    ("en_sakura_kick", "en-US-GuyNeural", "Don't touch my sneakers! KICK!", "+18%", "+16Hz"),
    ("en_sakura_throw", "en-US-GuyNeural", "Get outta here! YEET!", "+20%", "+18Hz"),

    # Sakura-kun - Japanese
    ("ja_sakura_kick", "ja-JP-KeitaNeural", "足元に来るな！蹴っ飛ばすぞ！", "+20%", "+20Hz"),
    ("ja_sakura_throw", "ja-JP-KeitaNeural", "邪魔だ！あっちへ飛んでけーーっ！", "+22%", "+22Hz"),

    # Sakura-kun - Tamil
    ("ta_sakura_kick", "ta-IN-ValluvarNeural", "என் ஷூல படாதே! எட்டி உதை!", "+16%", "+12Hz"),
    ("ta_sakura_throw", "ta-IN-ValluvarNeural", "தூக்கி எறிஞ்சிருவேன்! போ!", "+18%", "+14Hz"),

    # Hinata-chan - English
    ("en_hinata_kick", "en-US-AnaNeural", "Kyaaa! It's too close! KICK!", "+20%", "+24Hz"),
    ("en_hinata_throw", "en-US-AnaNeural", "Gross, get it away from me! THROW!", "+22%", "+26Hz"),

    # Hinata-chan - Japanese
    ("ja_hinata_kick", "ja-JP-NanamiNeural", "キャーッ！近すぎ！えいっ！", "+25%", "+35Hz"),
    ("ja_hinata_throw", "ja-JP-NanamiNeural", "あっち行けーーっ！ポイッ！", "+26%", "+36Hz"),

    # Hinata-chan - Tamil
    ("ta_hinata_kick", "ta-IN-PallaviNeural", "அய்யயோ கிட்ட வராதே! உதைப்பேன்!", "+20%", "+26Hz"),
    ("ta_hinata_throw", "ta-IN-PallaviNeural", "தொலைஞ்சு போ! தூக்கி வீசு!", "+22%", "+28Hz"),

    # Ren-kun - English & Japanese
    ("en_ren_kick", "en-US-AndrewNeural", "Watch my feet! Outta the way!", "+15%", "+8Hz"),
    ("en_ren_throw", "en-US-AndrewNeural", "Flying car! Take this!", "+16%", "+10Hz"),
    ("ja_ren_kick", "ja-JP-KeitaNeural", "邪魔だ！踏んづけちまうぞ！", "+16%", "+12Hz"),
    ("ja_ren_throw", "ja-JP-KeitaNeural", "飛べーっ！邪魔だ！", "+18%", "+14Hz"),

    # Classmates - English, Japanese & Tamil
    ("en_class_kick", "en-US-RogerNeural", "Eeeek! Stay away! KICK!", "+22%", "+18Hz"),
    ("en_class_throw", "en-US-EmmaNeural", "Get away from my desk! YEET!", "+22%", "+20Hz"),
    ("ja_class_kick", "ja-JP-KeitaNeural", "いやぁぁ！来ないで！キック！", "+22%", "+22Hz"),
    ("ja_class_throw", "ja-JP-NanamiNeural", "投げちゃうからねーーっ！ポイッ！", "+24%", "+28Hz"),
    ("ta_class_kick", "ta-IN-ValluvarNeural", "பயமா இருக்கு! தள்ளி போ!", "+18%", "+14Hz"),
    ("ta_class_throw", "ta-IN-PallaviNeural", "தூக்கி எறியுறேன் பாரு!", "+20%", "+18Hz"),
]

async def generate():
    raw_dir = "/tmp/voices_raw"
    opt_dir = "/workspace/bold-faraday/audio/voices"
    android_opt_dir = "/workspace/bold-faraday/app/src/main/assets/audio/voices"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(opt_dir, exist_ok=True)
    os.makedirs(android_opt_dir, exist_ok=True)

    voice_bank = {}

    for name, voice, text, rate, pitch in VOICE_DEFINITIONS:
        raw_path = os.path.join(raw_dir, f"{name}.mp3")
        opt_path = os.path.join(opt_dir, f"{name}.mp3")
        android_path = os.path.join(android_opt_dir, f"{name}.mp3")

        # Check if already generated
        if not os.path.exists(opt_path) or os.path.getsize(opt_path) < 1000:
            success = False
            for attempt in range(4):
                try:
                    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
                    await comm.save(raw_path)
                    success = True
                    break
                except Exception as e:
                    print(f"Retry {attempt+1} for {name}: {e}")
                    await asyncio.sleep(1.5)

            if not success:
                print(f"Failed to generate {name}, falling back to Guy/Jenny...")
                fb_voice = "en-US-GuyNeural" if "Neural" in voice else "en-US-JennyNeural"
                comm = edge_tts.Communicate(text, fb_voice, rate=rate, pitch=pitch)
                await comm.save(raw_path)

            # Compress and trim silence via ffmpeg: 22050Hz mono, 32kbps
            cmd = [
                "ffmpeg", "-y", "-i", raw_path,
                "-af", "silenceremove=start_periods=1:start_duration=0.04:start_threshold=-40dB:detection=peak",
                "-ar", "22050", "-ac", "1", "-b:a", "32k",
                opt_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            with open(opt_path, "rb") as f:
                data = f.read()
            with open(android_path, "wb") as f:
                f.write(data)
            print(f"Done fresh: {name} ({len(data)} bytes) - '{text}'")
            await asyncio.sleep(0.5)
        else:
            with open(opt_path, "rb") as f:
                data = f.read()
            if not os.path.exists(android_path):
                with open(android_path, "wb") as f:
                    f.write(data)
            print(f"Cached: {name} ({len(data)} bytes)")

        # Base64 encode for offline bundle
        b64 = base64.b64encode(data).decode('ascii')
        voice_bank[name] = {
            "text": text,
            "data": f"data:audio/mp3;base64,{b64}",
            "size": len(data)
        }

    # Write audio/voices.js (for standalone offline execution in browser & webview)
    js_content = "window.VOICE_BANK = " + json.dumps(voice_bank, indent=1) + ";\n"
    with open("/workspace/bold-faraday/audio/voices.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    with open("/workspace/bold-faraday/app/src/main/assets/audio/voices.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"Successfully finished all {len(VOICE_DEFINITIONS)} voice clips and voice_bank bundles!")

if __name__ == "__main__":
    asyncio.run(generate())
