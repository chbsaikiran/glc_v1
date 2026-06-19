# Channel adapter PR

## Group

- **Channel claimed**: <!-- e.g. telegram -->
- **Group name**: <!-- e.g. group-04 -->
- **Members**: <!-- one line per member -->

## What this PR adds

- [ ] `glc/channels/catalogue/<channel>/adapter.py` — `on_message` + `send`
- [ ] `glc/channels/catalogue/<channel>/schemas.py` — channel-specific types
- [ ] Tests at `tests/channels/test_<channel>.py` pass

## Demo

<!-- Link to the YouTube demo showing your adapter handling a real
     message end to end, with the agent-cursor / chat-trace overlay
     visible. -->

## Channel quirks you hit

<!-- 2-4 sentences. What was surprising about this channel's wire
     format, auth model, rate-limit behaviour, or trust posture? -->

## Tests-included checklist

- [ ] All tests in `tests/channels/test_<channel>.py` pass locally
- [ ] `ruff check glc/channels/catalogue/<channel>/` is clean
- [ ] `mypy glc/channels/catalogue/<channel>/` is clean
- [ ] Adapter does **not** hold long-lived credentials in code or env files
- [ ] Adapter consults `glc.security.trust_level.classify()` before
      constructing the envelope
- [ ] Adapter respects the channel's `allowed_senders` setting

## Notes for reviewers

<!-- Anything the TA should know before merge. -->
