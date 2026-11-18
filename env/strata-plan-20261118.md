# STRATA 엔진 E0 빌드와 `--plan` 결과 (2026-11-18)

## E0 — 고정 커밋 소스 빌드

| 항목 | 값 |
| --- | --- |
| 엔진 | Niko1221/Strata `v0.2.15` = `c77572806996349b49995e4f98d41b5294d36a21`, 작업 트리 깨끗함 |
| 위치 | `C:\strata-lab\engine` (git 밖), 빌드 폴더 `build-e0` |
| 설정 | `cmake -G Ninja -DCMAKE_BUILD_TYPE=Release -DSTRATA_ENABLE_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=120` |
| 빌드 | `cmake --build build-e0 --target strata -j 12`, 157단계, 2.8분, 종료 코드 0 |
| 툴체인 | VS 2022 Build Tools cl 19.44.35230, CUDA 13.2.86, CMake 4.1.2, Ninja 1.13.1 |
| 산출물 | `build-e0\strata.exe` 63.7 MB, sha256 `907008dae59e5575d4123eca8a1eaa7e36cbf25c80e2cf12c9229b098e764367` |
| 경고 | MSVC C4211(cudafe stub) 등 경고만, 오류 없음. 전체 로그는 `engine\build-e0.log` |

업스트림 `requirements-build.txt` 는 CMake 4.4.3 · Ninja 1.13.2 를 고정하지만, 최소 요구는 CMake 3.24 이고 4.1.2 로 빌드가 끝났다.

## Python 런타임

엔진의 `requirements.txt`(numpy 2.5.3, jinja2 3.1.6, regex 2026.9.10, pyyaml 6.0.3, tqdm 4.70.1, requests 2.34.2, pillow 13.0.0, psutil 7.2.2 등)를 conda 환경 `strata_local_llm` 에 pip 로 고정 버전 그대로 설치했다. `.venv` 는 만들지 않고 `scripts/strata.cmd` 가 `STRATA_PYTHON` 으로 이 환경을 지정한다.

## `strata launch --plan` (아무것도 바꾸지 않음, 다운로드 없음)

### M0 후보 — `qwen36 UD-Q4_K_XL`, 8K, parallel 1

```
model     qwen36 UD-Q4_K_XL
context   8K    pictures off    parallel 1
download  Nothing to download: the model is already on this computer. ...
drafting  MTP
same as   strata launch --model ud-q4_k_xl --family qwen36 --data-dir "C:\strata-lab\data" --context 8k --vision off --parallel 1 --tune skip --access local --port 8080
```

- **"이미 이 컴퓨터에 있다"는 문구는 틀렸다.** `C:\strata-lab\data` 는 비어 있다. JSON 출력에서 `model_gb: null`, `parts: []` 이다. 이 리비전의 계획기가 qwen36 의 다운로드 크기를 모르는 것이지, 모델이 있다는 뜻이 아니다. 실제 크기는 `docs/MODELS.md` 기준 22.9GB(그림 리더 0.9GB 별도)다.
- `engine_missing: true` — launcher 는 **릴리스 엔진을 내려받으려 한다.** 소스 빌드(E0)를 launcher 에 연결하는 방법은 다음 단계에서 확인한다 (RULES 1번: E0 는 소스 빌드).
- 기본값은 KV `int8`, MTP 켜짐. `--kv int8|q4_0|k8v4|fp16` 이 있으므로 KV 정밀도는 실행 설정 탐색(B1) 후보가 될 수 있다 (prep-plan 2-3 보완).

### 진단 후보 — `coder IQ1_M`, 8K, parallel 1

```
model     Qwen3.8-Flash-Next Coder IQ1_M, 58 GB
download  About 64.5 GB: the model (58.4 GB), the draft layer (5.2 GB) and the picture reader (0.9 GB)
same as   strata launch --model iq1_m --family coder --data-dir "C:\strata-lab\data" --context 8k --vision cpu --parallel 1 --tune skip --access local --port 8080
```

- 받을 양이 64.5GB 로, prep-plan 에 적은 shard 1 크기(29.6GB)보다 훨씬 크다. RAM 32GB 에서는 대부분 SSD 에서 읽으므로 진단용으로만 둔다.

## 부수 효과

CLI 가 `C:\Users\jinsan\AppData\Local\Strata\{install,launch}` 빈 폴더를 만들었다 (09:45). 내용 없음.
