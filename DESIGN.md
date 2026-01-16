# Celestria Nova 유튜브 롱폼 음악 채널 메타데이터 자동 생성기 설계

## 목표
`youtube-thumbnail-tool`의 톤과 일관되게, Celestria Nova 세계관을 유지하면서 롱폼 음악 채널용 메타데이터(제목/설명/태그/고정댓글)를 자동 생성한다.

## 입력
- **테마**: `FOCUS | SLEEP | DRIVE`
- **TPO 문구**: 사용자 입력 (예: "늦은 밤 집중 작업", "비 오는 고속도로", "새벽 수면 루틴")
- **길이**: `1H | 2H`

## 출력
1) **제목 3안**: SEO형 / 감성형 / 믹스형
2) **설명란**: 첫 2줄 후킹 포함, 이후 본문 텍스트
3) **태그**: 20~30개
4) **고정댓글**: 트랙리스트 자리 표시 포함

---

## 세계관 & 톤 가이드 (Celestria Nova)
- **키워드**: celestial, nova, starlight, orbit, aurora, quiet, drift, cosmic lounge
- **톤**: 차분하지만 세련됨, 몽환적이되 과장되지 않음, 과학적+감성적 결합
- **일관성 규칙**:
  - 제목/설명/댓글에서 1~2개의 세계관 단어를 **필수**로 포함
  - 과도한 밈/과장, 클릭베이트는 제외
  - 썸네일에 사용되는 색감(네이비/보라/블루 계열)을 암시하는 문구 허용

---

## 생성 로직

### 1) 전처리
- 입력값 정규화:
  - 테마 대문자화
  - 길이 `1H -> 1 Hour`, `2H -> 2 Hours`
- TPO 문구는 그대로 유지하되, 문장 끝에 불필요한 조사/기호 제거

### 2) 테마별 고정 어휘
| 테마 | 핵심 어휘 | 보조 어휘 |
| --- | --- | --- |
| FOCUS | focus, study, deep work | steady, pulse, clarity, orbit | 
| SLEEP | sleep, relax, lull, calm | drift, moonlight, soft, nebula | 
| DRIVE | drive, night ride, highway | motion, velocity, horizon, starlight | 

### 3) 제목 템플릿
- **SEO형** (검색 최적화):
  - `[테마 키워드] + [길이] + [TPO] + [세계관 키워드]`
- **감성형** (정서/서사):
  - `[세계관 키워드] + [감성 문장] + [테마 힌트]`
- **믹스형** (균형형):
  - `[테마 키워드] + [세계관 키워드] + [TPO] + [길이]`

### 4) 설명 템플릿
- **첫 2줄 후킹 규칙**:
  - 1줄: 세계관 + 테마 + 길이 강조
  - 2줄: TPO 문구를 감성적으로 재배치
- 본문 구성(권장 순서):
  1. 세션 목적(집중/수면/드라이브)
  2. 사운드 특징(ambient, chill, lofi, synth 등)
  3. 재생 환경 안내(이어폰, 밤, 비, 창문 등)
  4. 채널 구독 유도(짧고 부드럽게)

### 5) 태그 구성
- **기본 태그**(세계관/장르/상황/길이): 12~15개
- **테마 태그**(FOCUS/SLEEP/DRIVE 특화): 8~12개
- **롱폼 태그**: 2~3개

### 6) 고정댓글 템플릿
- 첫 문장에 세계관 키워드 포함
- 트랙리스트 자리 표시
- 구독/좋아요 안내는 1문장으로 제한

---

## 출력 예시 템플릿

> 입력 예시
> - 테마: FOCUS
> - TPO: 늦은 밤 집중 작업
> - 길이: 2H

### 1) 제목 3안
- **SEO형**: `Focus Music 2 Hours | 늦은 밤 집중 작업 | Celestria Nova Orbit`
- **감성형**: `Starlight Orbit에서 흐르는 집중의 파동`
- **믹스형**: `Focus × Celestria Nova | 늦은 밤 집중 작업 | 2 Hours`

### 2) 설명란
```
Celestria Nova의 고요한 궤도에서 2시간 동안 집중을 유지하세요.
늦은 밤 집중 작업을 위한 부드러운 starlight 사운드.

이 믹스는 deep work, study, writing에 최적화된 steady pulse를 제공합니다.
헤드폰으로 들으면 더욱 선명한 공간감을 느낄 수 있습니다.
좋아요와 구독은 새로운 항성의 항로를 밝히는 데 큰 도움이 됩니다.
```

### 3) 태그 (예시 25개)
```
celestria nova, focus music, deep work, study music, ambient, chill, starlight,
cosmic lounge, orbit, steady pulse, night study, productivity, lo-fi,
space ambience, 집중 음악, 공부 음악, work music, 2 hours, longform,
background music, calm focus, coding music, midnight study, galaxy sounds,
relaxing synth
```

### 4) 고정댓글
```
Celestria Nova의 항로에 오신 것을 환영합니다. ✨

[Tracklist]
00:00 - Intro
00:00 - Track 01
00:00 - Track 02
...

좋아요/구독으로 다음 항로를 함께 만들어주세요!
```

---

## 구현 체크리스트
- [ ] 입력값 검증 (테마/길이)
- [ ] 세계관 키워드 최소 1개 강제 삽입
- [ ] 제목 3종 템플릿 적용
- [ ] 설명 2줄 후킹 보장
- [ ] 태그 20~30개 생성
- [ ] 고정댓글 트랙리스트 플레이스홀더 포함

