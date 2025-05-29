for f in "$@"; do
    dir=$(dirname "$f")
    base=$(basename "$f")
    
    # 1. 한글 NFC 정규화 (안전한 방식)
    nfc_name=$(python3 -c "
import sys
import unicodedata
filename = sys.argv[1]
print(unicodedata.normalize('NFC', filename))
" "$base")
    
    # Python 실행 실패 시 원본 파일명 사용
    if [ $? -ne 0 ]; then
        nfc_name="$base"
        echo "Warning: NFC normalization failed for $base"
    fi
    
    # 2. 공백을 언더스코어로 변경
    final_name=$(echo "$nfc_name" | tr ' ' '_')
    
    # 3. 파일명이 변경되었는지 확인
    if [ "$base" != "$final_name" ]; then
        # 대상 파일이 이미 존재하는지 확인
        if [ -e "$dir/$final_name" ]; then
            echo "Skipped (already exists): $dir/$final_name"
        else
            # 파일명 변경 시도
            if mv "$f" "$dir/$final_name" 2>/dev/null; then
                echo "Renamed: $base -> $final_name"
            else
                echo "Error: Failed to rename $base"
            fi
        fi
    else
        echo "No change needed: $base"
    fi
done
