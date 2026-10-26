import math, struct, sys, wave

RATE = 44100

def piano_note(freq, dur, amp):
    """Additive piano-like tone: soft hammer attack, harmonics decaying faster than the fundamental."""
    n = int(RATE * dur)
    out = [0.0] * n
    harmonics = [(1, 1.0), (2, 0.22), (3, 0.06), (4, 0.015)]  # few, quiet overtones: warm, not bright
    for k, h_amp in harmonics:
        f = freq * k * math.sqrt(1 + 0.0004 * k * k)  # slight string inharmonicity
        decay = 1.6 + 1.8 * k
        for i in range(n):
            t = i / RATE
            out[i] += h_amp * math.exp(-decay * t) * math.sin(2 * math.pi * f * t)
    attack = int(RATE * 0.018)  # soft felt-hammer attack
    release = int(RATE * 0.08)
    for i in range(n):
        env = min(1.0, i / attack) if attack else 1.0
        if i > n - release:
            env *= (n - i) / release
        out[i] *= env * amp
    return out

def render(notes, total, path):
    buf = [0.0] * int(RATE * total)
    for start, freq, dur, amp in notes:
        s = int(RATE * start)
        for i, v in enumerate(piano_note(freq, dur, amp)):
            if s + i < len(buf):
                buf[s + i] += v
    peak = max(abs(v) for v in buf) or 1.0
    scale = 0.24 / peak  # gentle overall volume
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(v * scale * 32767)) for v in buf))

out_dir = sys.argv[1]
# Response ready: low, warm F major arpeggio (F3, A3, C4).
render([(0.00, 174.61, 1.6, 0.8), (0.16, 220.00, 1.5, 0.7), (0.32, 261.63, 1.5, 0.65)], 1.9, f"{out_dir}/done.wav")
# Waiting for you: two low notes, a calm rising fourth (A3 -> D4).
render([(0.00, 220.00, 1.4, 0.75), (0.28, 293.66, 1.5, 0.7)], 1.85, f"{out_dir}/ask.wav")
