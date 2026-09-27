"""Score D and G on the frozen EP-1 evaluation rows.

Pins are in research/docs/primitive_pins_dg.md. No selector is fit.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, f1_score

sys.path.insert(0, str(Path(__file__).resolve().parent))
import measure_p0_p1 as base

ROOT = base.ROOT
OUT = base.OUT
RESULT = OUT / "performance_dg.json"
TASKS = [
    "sms_spam",
    "pubmedqa_fold0",
    "banking77",
    "clinc_oos_plus",
    "ledgar",
    "civil_comments_binary",
    "vitaminc",
    "esci_en_us_task2",
]


def rows_for(task: str):
    loaded = base.LOADERS[task]()
    saved = json.loads((OUT / f"{task}_eval_indices.json").read_text(encoding="utf-8"))
    if task == "esci_en_us_task2":
        train_x, train_y, ev_x, ev_y, idx = loaded
        if idx != saved:
            raise SystemExit(f"{task} eval indices changed")
        return ev_x, ev_y, sorted(set(train_y))
    train_x, train_y, ev_x, ev_y = loaded
    ev_x, ev_y, idx = base.subset(ev_x, ev_y, task)
    if idx != saved:
        raise SystemExit(f"{task} eval indices changed")
    return ev_x, ev_y, sorted(set(train_y))


def metrics(y_true, pred, legal):
    scored = [p if p in set(legal) else "__invalid__" for p in pred]
    return {
        "Q_macro_f1": float(f1_score(y_true, scored, average="macro", zero_division=0)),
        "accuracy": float(accuracy_score(y_true, scored)),
        "invalid_outputs": sum(p not in set(legal) for p in pred),
    }


def store(task, primitive, row):
    existing = json.loads(RESULT.read_text(encoding="utf-8")) if RESULT.exists() else []
    existing = [r for r in existing if not (r["task"] == task and r["primitive"] == primitive)]
    existing.append(row)
    RESULT.write_text(json.dumps(existing, indent=2), encoding="utf-8")


def finish(task, primitive, y, pred, legal, lat, infer_s, load_s, **extra):
    lat_a = np.asarray(lat)
    row = {
        "task": task,
        "primitive": primitive,
        **metrics(y, pred, legal),
        "C_train_seconds": 0.0,
        "C_infer_seconds": infer_s,
        "C_api_usd": 0.0,
        "L_p50_ms": float(np.percentile(lat_a, 50, method="linear")),
        "L_p95_ms": float(np.percentile(lat_a, 95, method="linear")),
        "load_seconds": load_s,
        "n_train_fit": 0,
        "n_eval": len(y),
        **extra,
    }
    store(task, primitive, row)
    print(task, primitive, round(row["Q_macro_f1"], 4), row["invalid_outputs"], row["n_eval"], flush=True)


def run_d(tasks):
    from laya import Router

    t0 = time.perf_counter()
    router = Router(preload=True, max_loaded=1)
    load_s = time.perf_counter() - t0
    for task in tasks:
        ev_x, ev_y, legal = rows_for(task)
        questions = {
            "label": {
                "type": "choice",
                "instructions": "Which label applies?",
                "criteria": {name: name for name in legal},
            }
        }
        pred, lat = [], []
        t1 = time.perf_counter()
        for text in ev_x:
            a = time.perf_counter()
            result = router.predict(
                text, questions, model="english", max_len=2048, head_max_len=1024
            )
            choice = result["answers"]["label"].get("choice")
            pred.append(choice if isinstance(choice, str) else "__invalid__")
            lat.append((time.perf_counter() - a) * 1000)
        infer_s = time.perf_counter() - t1
        finish(task, "D", ev_y, pred, legal, lat, infer_s, load_s, checkpoint="convaiinnovations/laya", model_name="english")


def parse_generation(text, legal):
    s = text.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1].strip()
    return s if s in legal else "__invalid__"


def run_g(tasks):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    name = "Qwen/Qwen2.5-0.5B-Instruct"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    t0 = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name, torch_dtype=dtype)
    model.to(device)
    model.eval()
    load_s = time.perf_counter() - t0
    for task in tasks:
        ev_x, ev_y, legal = rows_for(task)
        label_block = "\n".join(legal)
        pred, lat = [], []
        t1 = time.perf_counter()
        for text in ev_x:
            prompt = (
                "Return exactly one valid class label.\n"
                "Do not explain.\n\n"
                "Labels:\n"
                f"{label_block}\n\n"
                "Text:\n"
                f"{text}"
            )
            messages = [{"role": "user", "content": prompt}]
            packed = tokenizer.apply_chat_template(
                messages, add_generation_prompt=True, return_tensors="pt", return_dict=True
            )
            input_ids = packed["input_ids"].to(device)
            attention = packed.get("attention_mask")
            if attention is not None:
                attention = attention.to(device)
            a = time.perf_counter()
            with torch.no_grad():
                out = model.generate(
                    input_ids=input_ids,
                    attention_mask=attention,
                    do_sample=False,
                    max_new_tokens=32,
                )
            new = out[0, input_ids.shape[1]:]
            decoded = tokenizer.decode(new, skip_special_tokens=True)
            pred.append(parse_generation(decoded, legal))
            lat.append((time.perf_counter() - a) * 1000)
        infer_s = time.perf_counter() - t1
        finish(task, "G", ev_y, pred, legal, lat, infer_s, load_s, checkpoint=name, max_new_tokens=32, do_sample=False, device=device, dtype=str(dtype).replace("torch.", ""))


if __name__ == "__main__":
    which = sys.argv[1]
    tasks = sys.argv[2:] or TASKS
    if which == "D":
        run_d(tasks)
    elif which == "G":
        run_g(tasks)
    else:
        raise SystemExit("use D or G")
