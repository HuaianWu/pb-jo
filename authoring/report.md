# jo: test-suite report

- candidate cases: 1212
- kept tests: **1158**
- gold sha256: `23d6999eb84d26fffd2fca7cdc6a165329ac3113037fe692582cb67a333a77b4`

## Dropped

| reason | count |
|---|---|
| duplicate input | 14 |
| gold crashes (signal) | 20 |
| output too large | 1 |
| undefined behaviour (sanitizer) | 8 |
| uninformative (dummy passes) | 11 |

gold crashes (signal) examples: invalid_utf8_line, invalid_utf8_value_0, invalid_utf8_array_0, invalid_utf8_key_0, invalid_utf8_value_1, invalid_utf8_array_1, invalid_utf8_key_1, invalid_utf8_value_2, invalid_utf8_array_2, invalid_utf8_key_2, invalid_utf8_value_3, invalid_utf8_array_3, invalid_utf8_key_3, invalid_utf8_value_4, invalid_utf8_array_4

output too large examples: percent_big_txt

undefined behaviour (sanitizer) examples: coerce_file_value, at_empty, at_nl, at_bin, at_directory, percent_directory, at_dev_null, nul_file_value

uninformative (dummy passes) examples: e_without_words, e_array, fuzz_071, fuzz_103, fuzz_134, fuzz_149, fuzz_164, fuzz_178, fuzz_192, fuzz_243, fuzz_360

## Kept by group

| group | tests |
|---|---|
| booleans | 33 |
| cli | 32 |
| coercion | 73 |
| file_values | 86 |
| fuzz | 401 |
| input_file | 32 |
| json_values | 122 |
| nesting | 104 |
| object_words | 36 |
| output | 12 |
| stdin_words | 16 |
| unicode | 2 |
| value_types | 209 |

## Kept by source

| source | tests |
|---|---|
| coverage | 166 |
| fuzz | 401 |
| harvested | 25 |
| probe | 566 |

## Exit codes

| exit code | tests |
|---|---|
| 0 | 1035 |
| 1 | 106 |
| 255 | 17 |

## Coverage of the gold source by the kept suite

Columns: regions, missed, cover | functions, missed, executed | lines, missed, cover | branches, missed, cover

```
TOTAL                            1450               416    71.31%          81                11    86.42%        1568               337    78.51%         938               322    65.67%
```

Per-file numbers: `coverage/summary.txt`; uncovered lines: `coverage/uncovered.txt`.
