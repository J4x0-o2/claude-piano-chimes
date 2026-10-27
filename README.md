<p align="center">
  <img src="assets/icon.svg" alt="piano-chimes icon: a white lotus over calm ripples" width="160">
</p>

<h1 align="center">piano-chimes</h1>

Gentle piano sounds for [Claude Code](https://claude.com/claude-code), so you can step away from the terminal and still know when Claude needs you.

| When | Sound |
| --- | --- |
| A response is ready | A low, warm F major arpeggio (F3 – A3 – C4) |
| Claude is waiting for you (a permission prompt, or a question with options to pick from) | Two calm rising notes (A3 → D4), like a soft question |

The tones are deliberately low, quiet (about 24% volume) and short (under 2 seconds), with a soft felt-hammer attack and very few bright overtones: noticeable, never stressful.

## Install

At the prompt of a Claude Code terminal session:

```
/plugin install piano-chimes --marketplace J4x0-o2/claude-piano-chimes
```

Answer `y` to add the marketplace, then pick a scope (`user` makes it active in every session). New sessions load it automatically.

To turn it off without uninstalling:

```
claude plugin disable piano-chimes@claude-piano-chimes
```

## How it works

The plugin is a Claude Code hooks module (`hooks/register.ts`):

- `classic.Stop` plays `sounds/done.wav`.
- `classic.PermissionRequest`, `classic.Notification` (`permission_prompt`, `elicitation_dialog`) and the main session's `AskUserQuestion` tool play `sounds/ask.wav`.
- A 2-second debounce makes sure one wait plays a single chime even when several events announce it.
- Questions asked inside subagents stay silent.

Sounds are played with PowerShell's `System.Media.SoundPlayer`, because Claude Code's built-in clip player is silent in a Windows terminal. The plugin currently targets **Windows**.

## Customize the sounds

The WAV files are synthesized, not recorded. `tools/gen_piano.py` builds each note from a few decaying harmonics. Edit the notes, durations or volume at the bottom of the script and regenerate:

```
python tools/gen_piano.py sounds
```

Then run `/reload-plugins` in Claude Code.

## License

[MIT](LICENSE)
