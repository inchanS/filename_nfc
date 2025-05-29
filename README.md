# 한글 파일명 NFC 정규화 도구

macOS에서 한글 파일명을 NFC(완성형) 유니코드로 정규화하여 검색 성능과 다른 OS와의 호환성을 개선하는 Python CLI 도구입니다.

## 배경

macOS는 기본적으로 한글 파일명을 NFD(조합형) 방식으로 저장합니다. 이로 인해 다음과 같은 문제가 발생할 수 있습니다:

- **검색 문제**: Spotlight, Alfred 등에서 한글 파일명 검색이 부정확하게 동작
- **호환성 문제**: Windows, Linux 등 다른 OS에서 파일명이 깨져 보임
- **공유 문제**: 클라우드 서비스나 협업 도구에서 파일명 호환성 문제

이 도구는 파일명을 NFC(완성형)로 변환하여 이러한 문제를 해결합니다.

## 기능

- ✅ 지정된 폴더와 하위 폴더의 모든 파일/폴더명을 재귀적으로 처리
- ✅ NFD → NFC 유니코드 정규화 수행
- ✅ 파일명 충돌 방지 및 안전한 변환
- ✅ CLI 인터페이스로 유연한 경로 지정
- ✅ 상세한 진행 상황 출력 (verbose 모드)
- ✅ 예외 처리를 통한 안정성 확보
- ✅ 전체 스캔 결과 및 통계 표시


## 설치 및 요구사항

- **Python 3.x** (macOS에 기본 설치됨)
- 추가 패키지 설치 불필요 (표준 라이브러리만 사용)


## 사용 방법

### 기본 사용법

```bash
# 현재 폴더 처리
python3 normalize_nfc.py

# 특정 폴더 처리
python3 normalize_nfc.py /Users/yourname/Documents

# 상대 경로 사용
python3 normalize_nfc.py ./Downloads

# 상세한 출력과 함께
python3 normalize_nfc.py /Users/yourname/Documents --verbose
```


### 명령행 옵션

```bash
python3 normalize_nfc.py [-h] [-v] [path]
```

**위치 인수:**

- `path`: 정규화할 폴더 경로 (기본값: 현재 폴더)

**선택 옵션:**

- `-h, --help`: 도움말 표시
- `-v, --verbose`: 상세한 출력 표시 (스캔 과정, 개별 파일 변환 정보 등)


## 테스트 방법

### 1. 기본 테스트

```bash
# 현재 폴더에서 기본 실행
python3 normalize_nfc.py

# 결과 예시:
# Processing directory: /Users/user/test
# Total items scanned: 15
# Found 3 files and 1 directories to rename
# Renamed file: 파이썬이란.pdf -> 파이썬이란.pdf
# Completed processing /Users/user/test
```


### 2. 상세 모드 테스트

```bash
# 상세 출력으로 실행하여 전체 과정 확인
python3 normalize_nfc.py . -v

# 결과 예시:
# Target directory: /Users/user/test
# Starting NFC normalization...
# Scanning: /Users/user/test
#   File needs rename: 파이썬이란.pdf -> 파이썬이란.pdf
# Scanning: /Users/user/test/subfolder
#   Dir needs rename: 한글폴더 -> 한글폴더
# Processing directory: /Users/user/test
# Total items scanned: 15
# Found 3 files and 1 directories to rename
```


### 3. 변환 확인 테스트

변환이 제대로 되었는지 확인:

```bash
# 개별 파일 NFC 상태 확인
python3 -c "
import os
import unicodedata
for f in os.listdir('.'):
    if '한글' in f:
        is_nfc = unicodedata.normalize('NFC', f) == f
        print(f'파일: {f}, NFC: {is_nfc}')
"
```


### 4. 테스트 폴더 생성

안전한 테스트를 위한 샘플 폴더 생성:

```bash
# 테스트 폴더 생성
mkdir test_nfc
cd test_nfc

# 샘플 파일 생성 (NFD 상태로)
touch "파이썬이란.pdf"
touch "보고서_최종.docx"
mkdir "한글폴더"

# 스크립트 실행
python3 ../normalize_nfc.py . -v
```


## 실행 결과 예시

### 정상 실행 시

```
Processing directory: /Users/user/Documents
Total items scanned: 25
Found 3 files and 1 directories to rename
Renamed file: 파이썬이란.pdf -> 파이썬이란.pdf
Renamed file: 보고서_최종.docx -> 보고서_최종.docx
Renamed folder: 한글폴더 -> 한글폴더
Completed processing /Users/user/Documents
```


### 변환할 파일이 없을 때

```
Processing directory: /Users/user/Documents
Total items scanned: 10
Found 0 files and 0 directories to rename
모든 파일과 폴더가 이미 NFC 형태입니다.
Completed processing /Users/user/Documents
```


### 오류 발생 시

```
Processing directory: /Users/user/Documents
Total items scanned: 5
Found 1 files and 0 directories to rename
Error renaming /Users/user/Documents/파일.pdf: [Errno 13] Permission denied
Completed processing /Users/user/Documents
```


## 문제 해결

### 일반적인 오류

**권한 오류:**

```bash
Error renaming /path/to/file: [Errno 13] Permission denied
```

→ 파일/폴더에 대한 쓰기 권한을 확인하세요.

**경로 오류:**

```bash
Error: 경로가 존재하지 않습니다: /invalid/path
```

→ 올바른 경로를 입력했는지 확인하세요.

### NFC 변환 확인

변환 전후 상태 비교:

```bash
# 변환 전 확인
python3 -c "import unicodedata; print('Before:', unicodedata.normalize('NFC', '파일명.txt') == '파일명.txt')"

# 스크립트 실행
python3 normalize_nfc.py

# 변환 후 확인
python3 -c "import unicodedata; print('After:', unicodedata.normalize('NFC', '파일명.txt') == '파일명.txt')"
```


## 주의사항

- ⚠️ **백업 권장**: 중요한 파일이 있는 폴더에서는 미리 백업하고 실행하세요
- ⚠️ **권한 확인**: 파일/폴더 수정 권한이 있는지 확인하세요
- ⚠️ **테스트 실행**: 중요한 데이터에 적용하기 전에 테스트 폴더에서 먼저 실행해보세요
- ⚠️ **재귀적 처리**: 하위 폴더까지 모두 처리되므로 범위를 신중히 선택하세요

## 동작 원리

1. `os.walk()`를 사용해 지정된 폴더와 하위 폴더를 재귀적으로 탐색
2. 각 파일/폴더명을 `unicodedata.normalize('NFC', name)`로 정규화
3. 원본과 정규화된 이름이 다른 경우만 변경 대상으로 수집
4. 전체 스캔 완료 후 통계 정보 출력
5. 파일을 먼저 처리한 후, 폴더를 깊은 경로부터 역순으로 처리
6. `os.rename()`을 사용해 안전하게 파일명 변경

## 고급 사용법

### Automator와 연동

macOS Automator의 "빠른 동작"으로 만들어 Finder 우클릭 메뉴에서 사용:

1. **Automator 실행** → "빠른 동작" 선택
2. **"셸 스크립트 실행" 추가**
3. **스크립트 내용:**

```bash
for folder in "$@"; do
    python3 /path/to/normalize_nfc.py "$folder" --verbose
done
```


### 배치 처리

여러 폴더를 한 번에 처리:

```bash
#!/bin/bash
folders=(
    "/Users/yourname/Documents"
    "/Users/yourname/Downloads"
    "/Users/yourname/Desktop"
)

for folder in "${folders[@]}"; do
    echo "Processing: $folder"
    python3 normalize_nfc.py "$folder" --verbose
    echo "---"
done
```


## 라이선스

MIT License

## 기여

버그 리포트나 개선 제안은 언제든 환영합니다.

## 관련 링크

- [유니코드 정규화에 대한 자세한 정보](https://unicode.org/reports/tr15/)
- [macOS 파일 시스템과 유니코드](https://developer.apple.com/library/archive/technotes/tn/tn1150.html)

<div style="text-align: center">⁂</div>

