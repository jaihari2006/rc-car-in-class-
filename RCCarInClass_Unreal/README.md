# 🏎️ RC Car in Class - Unreal Engine 5 Project

This is the dedicated **Unreal Engine 5** project edition of **RC Car in Class?**, featuring high-fidelity 3D Chaos vehicle physics, Sakamoto Sensei AI chase logic, and full PBR rendering.

---

## 📁 Project Architecture & Directory Layout

```
RCCarInClass_Unreal/
├── RCCarInClass.uproject          # Unreal Engine 5 Project Descriptor (UE 5.4 compatible)
├── Config/                        # Project configuration & settings
│   ├── DefaultEngine.ini          # Renderer (Lumen, Nanite, Bloom), Chaos Physics, Android setup
│   ├── DefaultGame.ini            # Game name, version, and metadata
│   ├── DefaultInput.ini           # Action & Axis bindings (WASD, Arrows, Gamepad, Nitro, Brake)
│   ├── DefaultEditor.ini          # Editor settings
│   └── DefaultDeviceProfiles.ini  # Android & Mobile scalability profiles
├── Source/                        # C++ Gameplay Framework
│   ├── RCCarInClass.Target.cs
│   ├── RCCarInClassEditor.Target.cs
│   └── RCCarInClass/
│       ├── RCCarInClass.Build.cs
│       ├── RCCarInClass.h / .cpp
│       ├── RCCarPawn.h / .cpp             # Chaos Wheeled Vehicle with Nitro, Drifting & Audio Hooks
│       ├── TeacherAIController.h / .cpp   # Sakamoto Sensei AI Perception, Patrol & Chase
│       ├── ClassroomGameMode.h / .cpp     # 120s timer, combo multipliers, game over states
│       └── HomeworkPaperPickup.h / .cpp   # Collectible homework papers with rotating bob
└── Content/                       # Asset Library
    ├── Models/                    # Original 3D Meshy AI GLB Models
    │   ├── porsche_911.glb        # Blue Horizon Porsche 911 GTS
    │   ├── fiery_sensei.glb       # Sakamoto Sensei (The Chaser)
    │   ├── sakura_kun.glb         # Sakura-kun (Anime Protagonist)
    │   ├── hinata_chan.glb        # Hinata-chan (Heroine)
    │   ├── ren_sakuragi.glb       # Ren Sakuragi (Student NPC)
    │   └── sakura_classmate.glb   # Sakura Classmate (Student NPC)
    ├── Audio/                     # Engine Sounds, BGM & Multilingual Voice Packs
    │   ├── accelerated_porsche_911wav-93455.mp3  # Flat-6 engine audio
    │   ├── wildlife_racing.mp3                   # High-energy racing soundtrack
    │   └── voicepack_*.json                      # English, Japanese, Tamil lines
    ├── Textures/                  # Branding, icons & classroom art
    │   ├── icon.png               # Official app icon
    │   ├── home_bg.jpg / .png     # Classroom backdrop
    │   └── Avatars/               # 10 character avatar presets
    ├── Blueprints/                # Blueprint templates
    └── Maps/                      # Level maps
```

---

## 🚀 How to Open in Unreal Engine 5 (Local PC / Mac / Linux)

### Step 1: Requirements
- **Unreal Engine 5.3, 5.4, or 5.5** installed via Epic Games Launcher.
- Visual Studio 2022 (with *Game development with C++*) on Windows, or Xcode on macOS.

### Step 2: Generate Project Files
1. Download or copy the `RCCarInClass_Unreal` folder to your computer.
2. Right-click on `RCCarInClass.uproject` and select:
   - **Windows**: `Generate Visual Studio project files`
   - **Mac**: `Generate Xcode Project`
3. Double-click `RCCarInClass.uproject` to open the project in Unreal Editor. If prompted to build missing modules, click **Yes**.

### Step 3: Setting Up the 3D Models in UE5
1. In the Content Browser, navigate to `Content/Models/`.
2. Drag and drop `porsche_911.glb` into your Content Browser to import it as a **Skeletal Mesh** or **Static Mesh** with PBR materials.
3. For the vehicle, create a **Wheeled Vehicle Blueprint** inheriting from `ARCCarPawn`:
   - Assign the `porsche_911` mesh.
   - Configure wheel offsets and radius in the `ChaosVehicleMovementComponent`.
   - Connect the engine sound to a **MetaSound** or Sound Cue referencing `accelerated_porsche_911wav-93455.mp3`.
4. Import `fiery_sensei.glb` as a Character Skeletal Mesh:
   - Create a Character Blueprint inheriting from `ACharacter`.
   - Set its AI Controller Class to `ATeacherAIController`.
   - Add a `NavMeshBoundsVolume` covering the classroom floor.

---

## 🎮 Input Controls

| Action | Keyboard | Gamepad | Description |
| :--- | :--- | :--- | :--- |
| **Throttle / Reverse** | `W` / `S` or `Up` / `Down` | Left Stick / Right Trigger | Accelerate / Reverse |
| **Steering** | `A` / `D` or `Left` / `Right` | Left Stick X | Analog steering |
| **Handbrake / Drift** | `SpaceBar` | `Button Bottom` (A / Cross) | Power slide / Drift |
| **Nitro Boost** | `Left Shift` or `N` | `Button Right` (B / Circle) | 1.65x Speed Burst |
| **Reset Car** | `R` | `Button Top` (Y / Triangle) | Reset flipped car |
| **Toggle Camera** | `C` | Right Stick Press (R3) | Toggle Chase vs Top-Down View |
| **Pause** | `P` or `Escape` | `Special Right` (Menu/Start) | Pause match |

---

## 📦 Packaging for Android APK & Windows

### Packaging Windows (PC Standalone):
1. Go to **Platforms** > **Windows** > **Binary Configuration: Shipping**.
2. Click **Package Project** and select your output directory.

### Packaging Android (Mobile APK):
1. Go to **Project Settings** > **Platforms** > **Android**.
2. Accept the Android SDK license agreement.
3. Set **Package name**: `com.rccar.inclass.unreal`.
4. Go to **Platforms** > **Android** > **Android (ASTC)** > **Package Project**.
