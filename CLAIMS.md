# Slot claims

Groups claim a slot by opening a PR that replaces `(unclaimed)` with
their group name for **one** row below. Claims are first-come,
first-served. CI rejects PRs that claim a slot twice.

Each slot's `Owned paths` column lists the directories the assigned
group may touch. The boundary CI check
([`scripts/check_pr_boundaries.py`](scripts/check_pr_boundaries.py))
rejects PRs whose diff strays outside the owned paths. If a slot
needs a shared-code change, open a separate PR scoped to that change
under `@course-maintainers` review.

The CLAIMS.md PR is reviewed and merged separately from the
implementation PR. If your implementation PR has not opened within
two weeks of the claim, TAs may reset the claim.

## Channels (15)

| Slot           | Group         | Owned paths                                                                          |
|----------------|---------------|--------------------------------------------------------------------------------------|
| telegram       | (unclaimed)   | `glc/channels/catalogue/telegram/` `glc/channels/catalogue/telegram/**`               |
| discord        | (unclaimed)   | `glc/channels/catalogue/discord/` `glc/channels/catalogue/discord/**`                 |
| slack          | (unclaimed)   | `glc/channels/catalogue/slack/` `glc/channels/catalogue/slack/**`                     |
| whatsapp       | (unclaimed)   | `glc/channels/catalogue/whatsapp/` `glc/channels/catalogue/whatsapp/**`               |
| teams          | (unclaimed)   | `glc/channels/catalogue/teams/` `glc/channels/catalogue/teams/**`                     |
| matrix         | (unclaimed)   | `glc/channels/catalogue/matrix/` `glc/channels/catalogue/matrix/**`                   |
| line           | (unclaimed)   | `glc/channels/catalogue/line/` `glc/channels/catalogue/line/**`                       |
| signal         | (unclaimed)   | `glc/channels/catalogue/signal/` `glc/channels/catalogue/signal/**`                   |
| gmail          | (unclaimed)   | `glc/channels/catalogue/gmail/` `glc/channels/catalogue/gmail/**`                     |
| imap           | (unclaimed)   | `glc/channels/catalogue/imap/` `glc/channels/catalogue/imap/**`                       |
| twilio_sms     | (unclaimed)   | `glc/channels/catalogue/twilio_sms/` `glc/channels/catalogue/twilio_sms/**`           |
| twilio_voice   | (unclaimed)   | `glc/channels/catalogue/twilio_voice/` `glc/channels/catalogue/twilio_voice/**`       |
| webui          | (unclaimed)   | `glc/channels/catalogue/webui/` `glc/channels/catalogue/webui/**`                     |
| webhook        | (unclaimed)   | `glc/channels/catalogue/webhook/` `glc/channels/catalogue/webhook/**`                 |
| local_mic      | (unclaimed)   | `glc/channels/catalogue/local_mic/` `glc/channels/catalogue/local_mic/**`             |

## Voice providers — STT (3)

| Slot           | Group         | Owned paths                                                                                                              |
|----------------|---------------|--------------------------------------------------------------------------------------------------------------------------|
| groq_whisper   | (unclaimed)   | `glc/voice/stt/providers/groq_whisper/` `glc/voice/stt/providers/groq_whisper/**`                                         |
| whisper_cpp    | (unclaimed)   | `glc/voice/stt/providers/whisper_cpp/` `glc/voice/stt/providers/whisper_cpp/**`                                           |
| gemini_live_stt| (unclaimed)   | `glc/voice/stt/providers/gemini_live/` `glc/voice/stt/providers/gemini_live/**`                                           |

## Voice providers — TTS (4)

| Slot              | Group         | Owned paths                                                                              |
|-------------------|---------------|------------------------------------------------------------------------------------------|
| kokoro            | (unclaimed)   | `glc/voice/tts/providers/kokoro/` `glc/voice/tts/providers/kokoro/**`                     |
| elevenlabs        | (unclaimed)   | `glc/voice/tts/providers/elevenlabs/` `glc/voice/tts/providers/elevenlabs/**`             |
| cartesia          | (unclaimed)   | `glc/voice/tts/providers/cartesia/` `glc/voice/tts/providers/cartesia/**`                 |
| gemini_live_tts   | (unclaimed)   | `glc/voice/tts/providers/gemini_live/` `glc/voice/tts/providers/gemini_live/**`           |

`system_fallback` is **not** a group slot — it ships fully implemented
under the maintainers.

## How to claim

1. Fork the repo and create a branch.
2. Replace `(unclaimed)` for **one** slot with your group name.
3. Open a PR titled `claim: <slot> for <group>`.
4. Once merged, start your implementation PR in a separate branch.
   The branch only touches files inside your `Owned paths` — the
   boundary CI check enforces this.

## How the boundary check reads this file

`scripts/check_pr_boundaries.py` parses each table row, extracts the
slot name, the claimed group, and the owned-path glob list. When a
PR is opened, the script runs `git diff` against the merge base and
fails if any changed file lies outside the owned paths of the slot
that group has claimed. For implementation PRs, the script reads the
PR author's group via a `# Group: <name>` marker required in the PR
description.

## Shared-code path

Changes outside any slot's owned paths require:

- A separate PR scoped only to the shared code.
- `@course-maintainers` review.
- Branch-protection bypass for the boundary check (the check passes
  trivially because the PR has no group marker).
