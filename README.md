# 등대 키친 · 설치 가이드 (Windows + iPad)

항구 마을의 낡은 등대 식당을 되살리는 합성 & 스토리 게임입니다.
이 폴더는 **iPad/iPhone 앱(iOS)** 과 **Android 앱**을 함께 담고 있는 앱 프로젝트예요.

Mac이 없어도 iPad 앱을 만들 수 있도록, **GitHub의 무료 Mac 빌드 서버**가 설치 파일(.ipa)을 대신 만들게 설정해 두었어요.

---

## 전체 흐름 (약 20~30분, 처음 한 번)

1. GitHub에 이 폴더 올리기
2. GitHub가 자동으로 iPad 설치 파일(.ipa) 만들기 (약 10분)
3. Windows의 **Sideloadly**로 iPad에 설치하기 (USB 케이블)

---

## 1단계. GitHub에 올리기

1. https://github.com 에 가입하고 로그인해요.
2. **GitHub Desktop**을 설치해요: https://desktop.github.com
3. 이 zip을 풀어서 나온 `lighthouse-kitchen` 폴더를 원하는 곳에 둬요.
4. GitHub Desktop에서 **File → Add local repository** → 폴더 선택
   - "This directory does not appear to be a Git repository"가 뜨면 **create a repository** 를 눌러 그대로 만들어요.
5. 왼쪽 아래 **Commit to main** → 위쪽 **Publish repository**
   - "Keep this code private"는 체크해도 되고 안 해도 돼요.
   - 공개(Public)로 올리면 빌드 시간이 무제한 무료예요. 비공개는 월 2,000분 무료이고, Mac 빌드는 10배로 계산돼요 (한 번 빌드하는 데 약 100분).

> 💡 웹사이트의 "Upload files" 기능은 한 번에 100개까지만 올라가서 이 프로젝트에는 맞지 않아요. GitHub Desktop을 써 주세요.

## 2단계. iPad 설치 파일(.ipa) 받기

1. GitHub에서 방금 만든 저장소를 열고 상단 **Actions** 탭을 눌러요.
2. 처음이라면 "I understand my workflows, go ahead and enable them"을 눌러요.
3. 왼쪽 **앱 빌드 (iPad + Android)** → 오른쪽 **Run workflow** → **Run workflow**
4. 10분쯤 지나 초록색 체크가 뜨면 실행 기록을 눌러요.
5. 맨 아래 **Artifacts**에서 **LighthouseKitchen-iPad**를 내려받고 압축을 풀면 `LighthouseKitchen.ipa`가 나와요.

## 3단계. Sideloadly로 iPad에 설치

준비물: iPad, USB 케이블, Apple ID

1. Windows에 **iTunes**와 **iCloud**를 설치해요. Microsoft Store 버전이 아니라 Apple 홈페이지에서 받는 버전을 권장해요 (Sideloadly 안내 참고).
2. **Sideloadly**를 설치해요: https://sideloadly.io
3. iPad를 USB로 연결하고, iPad에서 **"이 컴퓨터를 신뢰"** 를 눌러요.
4. Sideloadly에 `LighthouseKitchen.ipa`를 끌어다 놓고, Apple ID를 입력한 뒤 **Start**를 눌러요.
5. iPad에서 할 일
   - **설정 → 일반 → VPN 및 기기 관리** → 내 Apple ID → **신뢰**
   - iPadOS 16 이상이면 **설정 → 개인정보 보호 및 보안 → 개발자 모드** 켜기 → 재시동
6. 홈 화면의 **등대 키친** 아이콘을 누르면 주소창이나 하단 바 없이 전체 화면으로 실행돼요. 인터넷이 없어도 돼요.

### 알아둘 점
- **무료 Apple ID는 7일마다 다시 설치해야 해요.** 같은 방법으로 Sideloadly에서 Start만 다시 누르면 되고, 앱을 지우지 않고 덮어 설치하면 게임 진행은 그대로 남아요.
- 유료 Apple 개발자 계정(연 $99)을 쓰면 1년 동안 유지돼요.
- Sideloadly는 Apple이 아닌 제3자 도구예요. Apple ID 로그인이 걱정되면 게임 설치용 Apple ID를 따로 만들어서 써도 돼요.

---

## (선택) 7일 제한 없이 쓰는 방법: 홈 화면 앱

설치 없이 Safari에서 "홈 화면에 추가"로 쓰는 방법이에요. 주소창 없이 전체 화면으로 열리고 오프라인에서도 동작해요.

1. GitHub 저장소 **Settings → Pages → Source**를 **GitHub Actions**로 바꿔요.
2. **Actions → 홈 화면 앱 배포 (GitHub Pages) → Run workflow**
3. 완료되면 나오는 주소(`https://아이디.github.io/저장소이름/`)를 iPad Safari로 열어요.
4. 공유 버튼 → **홈 화면에 추가** → 홈 화면 아이콘으로 실행해요.

## (선택) Android 휴대폰

- Actions 결과의 **LighthouseKitchen-Android**에 있는 `app-debug.apk`를 Android 폰에 설치하면 돼요.
- 또는 Android Studio에서 `android` 폴더를 열고 ▶ Run을 눌러요.

---

## 폴더 구성

| 폴더 | 내용 |
|---|---|
| `www/` | 게임 본체 (HTML, 3D 그래픽, 글꼴) |
| `ios/` | iPad/iPhone 앱 프로젝트 |
| `android/` | Android 앱 프로젝트 |
| `.github/workflows/` | 자동 빌드 설정 |
| `tools/` | 게임을 고칠 때 쓰는 원본과 빌드 스크립트 |

## 사용한 오픈소스

- 3D 그래픽: Microsoft Fluent Emoji 3D (MIT 라이선스, `@lobehub/fluent-emoji-3d`)
- 글꼴: Jua, Gowun Dodum (SIL Open Font License, `www/fonts/` 안의 라이선스 파일 참고)
- 앱 프레임워크: Capacitor (MIT 라이선스)
