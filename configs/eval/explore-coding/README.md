# 탐색용 코딩 과제 (explore-coding)

출력·reasoning 예산 단계 시험(XB)과 X3 탐색에 쓴다. **최종 평가 50문항이 아니다** — 튜닝에 써도 된다.
과제마다 `prompt.md`(모델에게 보내는 지시)와 `test_solution.py`(고정 단위 테스트)가 있다.
모델 답의 마지막 ```python 블록을 `solution.py` 로 저장하고 본체 conda 환경의 pytest 로 돌린다.

| 과제 | 확인하는 것 |
| --- | --- |
| `merge_intervals` | 정렬·경계(맞닿은 구간)·빈 입력 |
| `lru_cache` | O(1) 자료구조, 갱신 시 순서, 용량 0 |
| `parse_duration` | 문자열 파싱, 잘못된 입력에 ValueError |
| `topo_sort` | 결정적 순서(사전순), 순환 탐지 |

테스트를 바꾸면 이 폴더의 커밋이 바뀌고, 이전 결과와 비교하지 않는다 (RULES 3).
