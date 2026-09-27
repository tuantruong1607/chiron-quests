# SPIKE CAP-003 — faster-whisper trên 2 nhân CPU (2026-09-27)

Máy: container 4 nhân / 15 GB, giới hạn `taskset -c 0,1` + `cpu_threads=2`; faster-whisper (SYSTRAN, MIT) int8, `word_timestamps=True`, `vad_filter=True`, `beam_size=1`, 240 s audio (ghép bản ghi tiếng Anh bản ngữ từ assets OpenPronounce, lặp lại). Script: `faster_whisper_spike.py`.

| Model | Nạp | Chép 240 s | RTF | Max RSS |
|---|---|---|---|---|
| tiny.en | 3,9 s | 11,3 s | 0,047 | 514 MB |
| base.en | 4,6 s | 23,5 s | 0,098 | 711 MB |
| small.en | 8,5 s | 57,5 s | 0,240 | 1.580 MB |

Suy ra cho bài Speaking ~12 phút audio (3 phần): base.en ≈ 70 s, small.en ≈ 173 s nếu chép một lần. Nếu chép **từng phần ngay khi upload**, độ trễ sau khi nộp phần cuối ≈ thời lượng phần cuối × RTF (base.en ≈ 25 s cho 4 phút).

Giới hạn bằng chứng: (1) CPU container có thể nhanh hơn vCPU VPS Gold — cần chạy lại trên VPS thật; (2) audio là giọng bản ngữ đọc câu Harvard, **chưa đo WER với giọng người Việt nói tự do**; (3) chưa đo khi nhiều job song song.
