모든 요구사항을 확인했습니다.

- 메서드 추가: `src/packaging/version.py:1112`
- release 숫자 증가 및 뒤 0 설정: `src/packaging/version.py:1135-1140`
- release 길이 유지/확장: `src/packaging/version.py:1131-1132`
- epoch 유지, pre/post/dev/local 버림: `src/packaging/version.py:1142-1144`
- 유효하지 않은 `part` 값 `ValueError`: `src/packaging/version.py:1127-1130`
- 불변성 및 새 `Version` 반환: `src/packaging/version.py:1142` (`__replace__` 사용)
- 기존 동작 유지: 자동 검사 결과 51524개 테스트 모두 통과

추가 수정 없이 과제 완료.