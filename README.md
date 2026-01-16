# amakusa

유튜브 음악 채널용 메타데이터를 자동 생성하는 스크립트입니다.

## 빠른 시작 (초보자용)

1. 이미지를 `input/background` 폴더에 넣습니다.
2. 아래 명령을 실행합니다.

```bash
python3 generate_metadata.py
```

### 테마를 직접 지정하고 싶다면

```bash
python3 generate_metadata.py --theme FOCUS
```

실행 후 `output/metadata` 폴더에 이미지 파일명과 매칭되는 메타데이터 txt 파일이 생성됩니다.
