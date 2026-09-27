"""Draw v0.2 figures from the frozen result files. Does not refit anything."""

import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "raw"
OUT = ROOT / "paper" / "latex" / "figures"
PUBLIC_FIGURES = ROOT / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
PUBLIC_FIGURES.mkdir(parents=True, exist_ok=True)

PRIM = {"R": "Rule", "C": "Classifier", "D": "Laya", "G": "Qwen"}
MARK = {"R": "s", "C": "o", "D": "D", "G": "^"}


def load_matrix():
    rows = []
    for name in ("performance_p0_p1.json", "performance_dg.json"):
        for row in json.loads((RAW / name).read_text(encoding="utf-8")):
            p = row["primitive"]
            if p in ("Cfull", "C100k"):
                p = "C"
            rows.append(
                {
                    "task": row["task"],
                    "p": p,
                    "Q": row["Q_macro_f1"],
                    "L": row["L_p50_ms"],
                    "V": row["invalid_outputs"] / row["n_eval"],
                }
            )
    return rows


def fig1():
    fig, ax = plt.subplots(figsize=(8.2, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    boxes = [
        (0.3, 1.6, 1.7, 0.9, "Task"),
        (2.4, 1.6, 2.2, 0.9, "Frozen\nfingerprint"),
        (5.0, 2.5, 2.2, 0.9, "Ridge\n(seven coordinates)"),
        (5.0, 0.7, 2.2, 0.9, "Training-fold\nprimitive mean"),
        (7.6, 1.6, 2.0, 0.9, "Policy"),
    ]
    for x, y, w, h, text in boxes:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.04,rounding_size=0.08",
                linewidth=0.8,
                edgecolor="black",
                facecolor="white",
            )
        )
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8)
    ax.annotate("", xy=(2.4, 2.05), xytext=(2.0, 2.05), arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate("", xy=(5.0, 2.95), xytext=(4.6, 2.2), arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate("", xy=(5.0, 1.15), xytext=(4.6, 1.9), arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate("", xy=(7.6, 2.15), xytext=(7.2, 2.9), arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate("", xy=(7.6, 1.95), xytext=(7.2, 1.2), arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.text(5.0, 3.55, "Primitive identity is an input to both predictors", fontsize=8, ha="left")
    fig.tight_layout()
    fig.savefig(OUT / "fig1_pipeline.pdf")
    fig.savefig(OUT / "fig1_pipeline.png", dpi=160)
    plt.close()


def fig2(rows):
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for p in ("R", "C", "D", "G"):
        pts = [r for r in rows if r["p"] == p]
        sc = ax.scatter(
            [r["L"] for r in pts],
            [r["Q"] for r in pts],
            c=[r["V"] for r in pts],
            marker=MARK[p],
            s=46,
            cmap="viridis",
            vmin=0,
            vmax=1,
            label=PRIM[p],
            edgecolors="black",
            linewidths=0.4,
        )
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label("Invalid-output rate")
    ax.set_xscale("log")
    ax.set_xlabel("Median latency (ms, log scale)")
    ax.set_ylabel("Macro-F1")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_quality_latency.pdf")
    fig.savefig(OUT / "fig2_quality_latency.png", dpi=160)
    plt.close()


def heldout_pairs():
    folds = json.loads((RAW / "selector_sd1.json").read_text(encoding="utf-8"))["folds"]
    pairs = []
    mae = []
    for fold in folds:
        pairs.extend(fold["pairs"])
        for row in fold["task_mae"]:
            mae.append((row["task"], row["Q"], row["V"]))
    return pairs, mae


def fig3(pairs):
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6))
    for ax, key, label in (
        (axes[0], "Q", "Macro-F1"),
        (axes[1], "V", "Invalid-output rate"),
    ):
        ax.plot([0, 1], [0, 1], color="0.5", lw=0.8, zorder=0)
        ax.scatter(
            [c["actual"][key] for c in pairs],
            [c["learned"][key] for c in pairs],
            marker="o",
            s=28,
            label="Ridge",
            facecolors="none",
            edgecolors="black",
        )
        ax.scatter(
            [c["actual"][key] for c in pairs],
            [c["mean"][key] for c in pairs],
            marker="x",
            s=28,
            label="Training-fold mean",
            color="0.25",
        )
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel(f"Measured {label}")
        ax.set_ylabel(f"Predicted {label}")
        ax.set_aspect("equal")
        ax.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "fig3_predicted_measured.pdf")
    fig.savefig(OUT / "fig3_predicted_measured.png", dpi=160)
    plt.close()


SHORT = {
    "banking77": "Banking77",
    "clinc_oos_plus": "CLINC150",
    "pubmedqa_fold0": "PubMedQA",
    "vitaminc": "VitaminC",
    "civil_comments_binary": "Civil",
    "sms_spam": "SMS",
    "ledgar": "LEDGAR",
    "esci_en_us_task2": "ESCI",
}


def fig4(mae):
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    names = [SHORT[t] for t, _, _ in mae]
    x = range(len(names))
    q = [a["learned_minus_mean"] for _, a, _ in mae]
    v = [b["learned_minus_mean"] for _, _, b in mae]
    ax.axhline(0, color="0.4", lw=0.8)
    ax.bar([i - 0.18 for i in x], q, width=0.36, label="Macro-F1", color="0.25")
    ax.bar([i + 0.18 for i in x], v, width=0.36, label="Invalid rate", color="0.7")
    ax.set_xticks(list(x))
    ax.set_xticklabels(names, rotation=30, ha="right")
    ax.set_ylabel("Ridge error minus mean error")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig4_error_difference.pdf")
    fig.savefig(OUT / "fig4_error_difference.png", dpi=160)
    plt.close()


def fig5(mae):
    esci = next(row for row in mae if row[0] == "esci_en_us_task2")
    fig, ax = plt.subplots(figsize=(4.8, 3.6))
    labels = ["Macro-F1", "Invalid rate"]
    ridge = [esci[1]["learned"], esci[2]["learned"]]
    mean = [esci[1]["mean"], esci[2]["mean"]]
    x = range(2)
    ax.bar([i - 0.18 for i in x], mean, width=0.36, label="Training-fold mean", color="0.75")
    ax.bar([i + 0.18 for i in x], ridge, width=0.36, label="Ridge", color="0.2")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Mean absolute error")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig5_esci.pdf")
    fig.savefig(OUT / "fig5_esci.png", dpi=160)
    plt.close()


if __name__ == "__main__":
    rows = load_matrix()
    pairs, mae = heldout_pairs()
    fig1()
    fig2(rows)
    fig3(pairs)
    fig4(mae)
    fig5(mae)
    for pdf in OUT.glob("*.pdf"):
        shutil.copy2(pdf, PUBLIC_FIGURES / pdf.name)
    print("wrote", OUT)
