# jo: validation in the clean-room image

## Agent's view (user `agent`)

```
whoami: agent
run binary: exit 255
read binary: denied (good)
upstream source files found: 0
docs: /workspace/docs: README.md jo.md 
workspace: docs 
```

## Hidden test suite against submissions

| submission | result | expected |
|---|---|---|
| gold binary (original deleted first) | 1158/1158 passed | all pass |
| dummy (`cat`) | 0/1158 passed | ~0 |
| wrapper calling the original, original still present | 1141/1158 passed | shows why deletion matters |
| wrapper calling the original, original deleted (real evaluation) | 0/1158 passed | 0 |

## Gold binary hash

- recorded with: `23d6999eb84d26fffd2fca7cdc6a165329ac3113037fe692582cb67a333a77b4`
- built in image: `7676197e8d401fbf12c3796ea7258af8e2e45e218634ce62ea41f80535697006`
- different builds; the gold row above shows they behave identically on the suite
