# Coderbyte practice

Timed problems that work like Coderbyte: each file has a function to write and
a few sample tests you can see. `run.py` also runs hidden tests and shows only
how many passed, plus a short label for each failure.

```powershell
uv run python coderbyte/run.py 3      # check one problem
uv run python coderbyte/run.py all    # scoreboard
```

If `uv` isn't on your PATH: `.venv\Scripts\python.exe coderbyte\run.py 3`

| # | Problem | Level | Time |
| --- | --- | --- | --- |
| 1 | Version sort | easy | 15 min |
| 2 | First unique character | easy | 15 min |
| 3 | Run-length encoding | easy | 15 min |
| 4 | Error summary from logs | medium | 25 min |
| 5 | Balanced brackets | medium | 20 min |
| 6 | Merge maintenance windows | medium | 25 min |
| 7 | Longest run without repeats (stretch) | medium-hard | 25 min |
| 8 | Bug hunt: write tests that catch 5 planted bugs | QA | 40 min |
| 9 | Mock interview: flatten a nested config | medium | 40 min |

## Rules, to make it realistic

- Start a timer for each problem and stop when it runs out, finished or not.
- No AI help. Python docs are fine, since many Coderbyte setups allow it.
- Run the sample tests early and often; only submit (`run.py`) when you think
  you're done, then fix what the hidden-test labels point at.
- Before coding, write down the edge cases you'd test. That's your habit to show on Friday.
- Don't open `_hidden.py`.
