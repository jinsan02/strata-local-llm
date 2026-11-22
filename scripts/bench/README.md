# scripts/bench — 측정 러너 · 자체 점검 · 측정 체인

본체(`desktop-5070`)에서 conda 환경 `strata_local_llm` 으로 돈다. 결과는 러너가 `experiments/LEDGER.tsv` 에 한 줄씩 쓰고, 실행 기록은 `experiments/runs/<run_id>/` 에 남는다.
지난 체인 스크립트도 지우지 않는다. 원장 행과 커밋이 "어느 스크립트로 쟀는지"를 경로로 가리키기 때문이다.

## 러너

| 파일 | 하는 일 | 쓰는 실험 |
| --- | --- | --- |
| `run_x3.py` | 긴 문맥 코딩(X3): 도구(list_files · grep · read_file · edit_file · run_tests)를 주고 턴을 돌린 뒤 비공개 테스트로 채점. 하네스 옵션(`--edit-apply`, `--effort`, `--sampling` …)을 여기서 고른다 | X3 하네스 · 샘플링 · 64K · 노력치 · Q1 G3/G4 |
| `run_bench.py` | 처리량 · 지연 · VRAM/RAM · MTP 초안을 원장에 | X1 · X2 · B1 |
| `run_coding.py` | 짧은 코딩 과제 출력 예산 시험 | XB |
| `run_swe.py` · `setup_swe.py` | SWE 2건(flask · pytest) 하네스 건전성 확인 | X3 교차 확인 |
| `make_def.py` · `validate_def.py` | X3 과제 정의 만들기 · 검사(기준 실패 · 참조 통과 · 회귀 통과) | 과제 추가 |
| `summarize.py` | 원장 요약 표 | 보고서 |

## 점검 · 프로브

| 파일 | 하는 일 |
| --- | --- |
| `probe_cache.py` · `cache_ab.py` | 후속 턴 캐시 재사용 측정 (T-013) |
| `probe_tools.py` | Chat · Messages · Responses API 도구 왕복 |
| `mtp_probe.py` · `d0_probe.py` | MTP 초안 · 결정성(같은 입력 같은 출력) 확인 |
| `replay_edit_apply.py` | 저장된 답에 편집 적용 규칙만 다시 돌려 보기 (H7) |
| `selftest_*.py` | 러너 기능별 가짜 응답 자체 점검. 러너를 고치면 해당 점검을 같이 돌린다 |

## 측정 체인 (.ps1)

밤샘 · 무인 측정은 WMI 로 띄워 ssh 를 끊어도 산다(T-012). 끝 표시는 `engine\<이름>.log` 의 `done` 줄.

| 상태 | 파일 |
| --- | --- |
| **지금 쓰는 것** | `g3-chain.ps1`(X3 6과제 × N회 공통 체인, `-Effort` · `-Model` 등) · `effort-chain.ps1`(노력치) · `tools-chain.ps1`(T1/T2 도구) |
| 지난 측정 (기록용) | `matrix-*.ps1`(X1 · X2 · XB · B1-1 · X3 파일럿 · SWE · 점검), `night-chain*.ps1` · `launch_night*.ps1`(11-18~19 하네스 A/B), `master-chain.ps1` · `launch_master.ps1`, `cache-chain.ps1` · `launch_cache.ps1`(T-013), `ctx64-chain.ps1` · `k64curve-chain.ps1`(64K 점검), `pdiag-chain.ps1`, `h1conf-chain.ps1`, `hadd-chain.ps1`, `s1-chain.ps1`, `t1-chain.ps1`, `c1conf-chain.ps1`, `h2k-chain.ps1`, `a4d-chain.ps1`, `nrg-chain.ps1`, `l2-chain.ps1` |

어느 체인이 어떤 원장 접두사를 만들었는지는 `STATE.md` 결정 기록과 각 record 커밋 메시지에 있다.
