import os
import sys
import argparse
import unicodedata

def normalize_filenames_to_nfc(target_dir='.', verbose=False):
    # 먼저 모든 파일/폴더 경로를 수집
    all_items = []
    items_to_rename = []
    
    for root, dirs, files in os.walk(target_dir):
        if verbose:
            print(f"Scanning: {root}")
        
        # 파일 처리
        for name in files:
            all_items.append(('file', os.path.join(root, name)))
            nfc_name = unicodedata.normalize('NFC', name)
            if name != nfc_name:
                src = os.path.join(root, name)
                dst = os.path.join(root, nfc_name)
                items_to_rename.append(('file', src, dst))
                if verbose:
                    print(f"  File needs rename: {name} -> {nfc_name}")
        
        # 폴더 처리
        for name in dirs:
            all_items.append(('dir', os.path.join(root, name)))
            nfc_name = unicodedata.normalize('NFC', name)
            if name != nfc_name:
                src = os.path.join(root, name)
                dst = os.path.join(root, nfc_name)
                items_to_rename.append(('dir', src, dst))
                if verbose:
                    print(f"  Dir needs rename: {name} -> {nfc_name}")
    
    print(f"Processing directory: {target_dir}")
    print(f"Total items scanned: {len(all_items)}")
    print(f"Found {len([x for x in items_to_rename if x[0] == 'file'])} files and {len([x for x in items_to_rename if x[0] == 'dir'])} directories to rename")
    
    if not items_to_rename:
        print("모든 파일과 폴더가 이미 NFC 형태입니다.")
        return
    
    # 폴더는 깊은 경로부터 처리 (역순)
    dirs_to_rename = [item for item in items_to_rename if item[0] == 'dir']
    dirs_to_rename.sort(key=lambda x: x[1], reverse=True)
    
    files_to_rename = [item for item in items_to_rename if item[0] == 'file']
    
    # 파일 먼저 처리
    for item_type, src, dst in files_to_rename:
        try:
            if not os.path.exists(dst):
                os.rename(src, dst)
                print(f"Renamed file: {os.path.basename(src)} -> {os.path.basename(dst)}")
            else:
                print(f"Skipped (already exists): {dst}")
        except OSError as e:
            print(f"Error renaming {src}: {e}")
    
    # 폴더 나중에 처리 (깊은 것부터)
    for item_type, src, dst in dirs_to_rename:
        try:
            if not os.path.exists(dst):
                os.rename(src, dst)
                print(f"Renamed folder: {os.path.basename(src)} -> {os.path.basename(dst)}")
            else:
                print(f"Skipped (already exists): {dst}")
        except OSError as e:
            print(f"Error renaming {src}: {e}")
    
    print(f"Completed processing {target_dir}")

def main():
    parser = argparse.ArgumentParser(
        description='한글 파일명을 NFC(완성형) 유니코드로 정규화합니다.',
        epilog='예시: python3 normalize_nfc.py /Users/yourname/Documents'
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='정규화할 폴더 경로 (기본값: 현재 폴더)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='상세한 출력 표시'
    )
    
    args = parser.parse_args()
    
    # 경로 유효성 검사
    if not os.path.exists(args.path):
        print(f"Error: 경로가 존재하지 않습니다: {args.path}")
        sys.exit(1)
    
    if not os.path.isdir(args.path):
        print(f"Error: 지정된 경로가 폴더가 아닙니다: {args.path}")
        sys.exit(1)
    
    # 절대 경로로 변환
    target_path = os.path.abspath(args.path)
    
    if args.verbose:
        print(f"Target directory: {target_path}")
        print("Starting NFC normalization...")
    
    try:
        normalize_filenames_to_nfc(target_path, args.verbose)
    except KeyboardInterrupt:
        print("\n작업이 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
