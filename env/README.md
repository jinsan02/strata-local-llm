# env — 환경 기록

환경은 실험 변수다. 바꾸면 여기에 남기고 `chore(env):` 로 커밋한다. 설명은 `docs/ENVIRONMENT.md`.

| 파일 | 내용 |
| --- | --- |
| `hw-YYYYMMDD.md` | 하드웨어 실측. 바뀌면 새 파일 |
| `strata_local_llm.yml` | conda 환경 선언 (`conda env export --no-builds`) |
| `install-*.log` | 설치 스크립트 출력 — 설치 파일 sha256, 종료 코드 |
| `cleanup.log` | `scripts/cleanup.ps1` 실행마다 정리 전후 메모리 (append) |
| `startup-backup*.reg` | 시작 프로그램 해제 전 값. 복원: `reg import <파일>` |
