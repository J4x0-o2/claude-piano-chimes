import type { EngineInterface, Register } from "claude-code";

type Chime = "done" | "ask";

// Notification types that mean Claude is blocked on the person.
const WAITING_NOTIFICATIONS = new Set(["permission_prompt", "elicitation_dialog"]);
// Several events can announce the same wait (permission request + notification); play it once.
const DEBOUNCE_MS = 2000;

const lastPlayed: Record<Chime, number> = { done: 0, ask: 0 };

function play($: EngineInterface, chime: Chime) {
  const now = Date.now();
  if (now - lastPlayed[chime] < DEBOUNCE_MS) return;
  lastPlayed[chime] = now;

  const file = `${$.plugin.root}/sounds/${chime}.wav`.replace(/'/g, "''");
  // The Windows terminal has no clip player for $.audio.play, so hand the WAV to .NET's SoundPlayer.
  // Fire and forget: the hook must never wait on the sound.
  void $.process
    .run(
      ["powershell", "-NoProfile", "-NonInteractive", "-Command", `(New-Object System.Media.SoundPlayer '${file}').PlaySync()`],
      { timeoutMs: 10000 },
    )
    .catch(() => {});
}

export const register: Register = (on) => {
  on("classic.Stop", ($, e, next) => {
    play($, "done");
    return next(e);
  });

  on("classic.PermissionRequest", ($, e, next) => {
    play($, "ask");
    return next(e);
  });

  on("classic.Notification", ($, e, next) => {
    if (WAITING_NOTIFICATIONS.has(e.notification_type)) play($, "ask");
    return next(e);
  });

  on("tool.call", { tool: "AskUserQuestion" }, ($, e, next) => {
    if (e.agentId === undefined) play($, "ask");
    return next(e);
  });
};
