# Q1 양자화 레시피 (`llama-quantize --tensor-type-file`)

`docs/q1-plan-20261120.md` 3절의 후보. 원본은 BF16(`unsloth/Qwen3.6-35B-A3B-MTP-GGUF` 리비전 `5bc3e23`), 기본 형식 `Q8_0`(expert 밖 텐서는 M0 와 같은 Q8_0),
`--imatrix` 는 `scripts/quant/build_calib.py` 보정 세트로 만든 것. 한 줄 = `정규식=형식`, **위에서부터 처음 맞는 줄이 이긴다**(llama.cpp v1.0.0 `llama-quant.cpp`).
층 0~39 는 본층, 40 은 MTP 블록.

| 파일 | 후보 | gate / up | down |
| --- | --- | --- | --- |
| `r0.txt` | R0 (M0 재현) | Q4_K, 39층 Q5_K | Q5_K, 34 · 38 · 39층 Q6_K |
| `m1a.txt` | M1a | R0 와 같음 | IQ4_XS, 34 · 38 · 39층 Q6_K |
| `m1b.txt` | M1b | IQ4_XS, 39층 Q5_K | M1a 와 같음 |
| `m1c.txt` | M1c | IQ3_S, 민감 층(0 · 1 · 2 · 37 · 38 · 40) Q4_K, 39층 Q5_K | M1a 와 같음 |
| `m1d.txt` | M1d | IQ3_XXS, 민감 층은 M1c 와 같음 | M1a 와 같음 |

민감 층은 첫 판(11-20 결정): 앞 3층 · 뒤 층 · MTP 층. G2 층별 결과를 보고 바꾸면 새 파일(`m1c2.txt` …)로 둔다.
