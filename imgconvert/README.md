# imgconverter

## 개요

1. 프로젝트명 : imgconverter
2. command line 3개를 인자로 받음 1. target_folder, 2. src image format name, 3. des image format name
3. 인자로 받은 폴더를 target_folder에서 확장자가 src image format name인 것들만 대상으로
4. des image format name으로 변환하여 저장함.
5. 원본 src image는 그대로 유지함.
6. target_folder의 하위 폴더는 순회하지 않음.

## 사용법

- 3 개의 인자
  - 1번째 인자 : 이미지 폴더
  - 2번재 인자 : 소스이미지의 확장자
  - 3번째 인자 : 확장자가 변경되면서 생길 이미지의 확장자

```text
python ./imgconverter.py c:\\tmp webp png
```
