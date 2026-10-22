"""Candidate test inputs for jo 1.9. pbkit records the expected results from the gold binary.

Sources:
  probe      hand-written probes, one behaviour each, organised by the man page sections
  harvested  the upstream tests/ scripts, translated to argv form
  coverage   added after reading authoring/coverage/uncovered.txt
  fuzz       seeded random words built from the same grammar
"""

import random

PROG = "jo"

CASES = []


def C(id, group, args, stdin=None, files=None, env=None, doc=None, source="probe"):
    CASES.append({"id": id, "group": group, "args": list(args), "stdin": stdin, "files": files,
                  "env": env, "doc": doc, "source": source})


NESTED_JSON = b'{"field1":123,"field2":"abc"}\n'
ARR_JSON = b'["base64.c","jo.c","json.c"]\n'
BINARY = bytes(range(256))


def cli():
    g = "cli"
    C("version", g, ["-v"], doc="-v prints the version and exits")
    C("version_json", g, ["-V"])
    C("version_json_pretty", g, ["-p", "-V"])
    C("version_json_pretty_after", g, ["-V", "-p"])
    C("version_json_array", g, ["-a", "-V"])
    C("version_json_with_words", g, ["-V", "a=1"])
    C("version_before_V", g, ["-v", "-V"])
    C("help", g, ["-h"], doc="-h prints usage to stderr and exits 0")
    C("help_after_words", g, ["a=1", "-h"])
    C("invalid_option", g, ["-x"])
    C("invalid_option_upper", g, ["-Z", "a=1"])
    C("invalid_long_option", g, ["--pretty"])
    C("missing_d_argument", g, ["-d"])
    C("missing_f_argument", g, ["-f"])
    C("missing_o_argument", g, ["-o"])
    C("options_after_words_are_options", g, ["a=1", "-p", "b=2"], doc="glibc getopt permutes argv")
    C("array_flag_after_word", g, ["x", "-a", "y"])
    C("double_dash_stops_options", g, ["--", "-p", "a=1"])
    C("double_dash_then_dash_word", g, ["-a", "--", "-x", "-"])
    C("single_dash_word", g, ["-a", "-"])
    C("clustered_flags", g, ["-pa", "1", "2"])
    C("clustered_flags_with_arg", g, ["-pd.", "a.b=1"])
    C("d_attached_argument", g, ["-d/", "a/b=1"])
    C("d_multichar_uses_first", g, ["-d", "::", "a:b=1", "a::c=2"])
    C("d_empty_argument", g, ["-d", "", "a.b=1"])
    C("e_without_words", g, ["-e"], stdin=b"a=1\n")
    C("e_with_words", g, ["-e", "a=1"])
    C("e_array", g, ["-e", "-a"])
    C("no_words_empty_stdin", g, [], stdin=b"")
    C("no_words_empty_stdin_array", g, ["-a"], stdin=b"")
    C("no_words_empty_stdin_pretty", g, ["-p"], stdin=b"")
    C("pretty_empty_array", g, ["-p", "-a"], stdin=b"")
    C("repeated_pretty", g, ["-p", "-p", "a=1"])
    C("all_flags", g, ["-a", "-B", "-D", "-n", "-p", "true", "null", "", "x"])


def scalars():
    g = "value_types"
    values = [
        "1", "0", "-0", "-1", "+1", "007", "0x1F", "0X1f", "1e5", "1E5", "1e-3", "-2.5e+10", ".5", "5.", "-.5",
        "1.0", "1.50", "3.14159", "3.14159.26", "1e309", "-1e309", "1e-400", "inf", "-inf", "Infinity", "nan",
        "NaN", "12345678901234567890", "123456789012345678901234567890", "9007199254740993", "0.1", "1/2",
        "1,5", " 5", "5 ", " ", "", "abc", "1abc", "abc1", "true", "false", "null", "True", "FALSE", "Null",
        "t", "T", "yes", '"quoted"', '"1.0"', "'single'", "a b c", "tab\there", "new\nline", "back\\slash",
        "quote\"inside", "/slash", "\x01ctl", "\x7f", "\x1f", "émoji😀", "日本語", " ", "<>&", "%", "@", ":",
        "\\@x", "\\%x", "\\:x", "\\\\", "\\", "[1,2]", "[ 1 , 2 ]", "[]", "{}", '{"a":1}', '{"a":[1,{"b":null}]}',
        "[1,2", "{", "[", "]", "}", "[x]", '{"a"}', '[1,2]x', ' [1]', "[\"a\\u00e9\"]", "[1e400]", "[-]", "[01]",
        "=", "==", "a=b", "x@y",
    ]
    for i, v in enumerate(values):
        C(f"object_value_{i:02d}", g, [f"k={v}"], doc=f"type guess for value {v!r}")
        C(f"array_value_{i:02d}", g, ["-a", v], doc=f"type guess for array element {v!r}")
    for i, v in enumerate(["true", "false", "null", "1", '"x"', "[1]", "{}", ""]):
        C(f"nobool_object_{i}", g, ["-B", f"k={v}"])
        C(f"nobool_array_{i}", g, ["-B", "-a", v])
    C("number_formats_mixed", g, ["a=1", "b=1.0", "c=1e2", "d=0.000001", "e=1e21", "f=1e-7", "g=123456.789",
                                  "h=0.1e1", "i=-0.0", "j=1e15", "k=1e16", "l=1e17", "m=2.5e-5"])


def keys_and_words():
    g = "object_words"
    C("tst_example", g, ["tst=1457081292", "lat=12.3456", "cc=FR", "badfloat=3.14159.26", "name=JP Mens", "nada=", "coffee@T"],
      doc="first example from the man page")
    C("word_without_separator", g, ["justaword"])
    C("words_without_separator", g, ["a", "b=1", "c"])
    C("empty_key", g, ["=value"])
    C("empty_word", g, [""])
    C("empty_word_array", g, ["-a", ""])
    C("equals_in_value", g, ["a=b=c"])
    C("double_equals", g, ["form==ok", "this===sure"], source="harvested")
    C("at_in_value_after_equals", g, ["a=x@y"])
    C("equals_after_at", g, ["a@x=y"])
    C("at_in_key_first", g, ["@a=1"])
    C("colon_equals_missing_file", g, ["a:=nofile.json"])
    C("colon_equals_vs_colon_value", g, ["a=:nofile.json"])
    C("colon_in_key", g, ["a:b=1"])
    C("colon_equals_empty_key", g, [":=f.json"], files={"f.json": b"[1]"})
    C("key_with_spaces", g, ["my key=my value"])
    C("key_unicode", g, ["ключ=значение", "日本=語"])
    C("key_needs_escaping", g, ['q"uote=1', "back\\slash=2", "tab\tkey=3", "nl\nkey=4"])
    C("duplicate_keys_kept", g, ["a=1", "b=2", "a=3"])
    C("dedup_keys", g, ["-D", "a=1", "b=2", "a=3"])
    C("dedup_three", g, ["-D", "a=1", "a=2", "a=3"])
    C("dedup_mixed_types", g, ["-D", "a=1", "a@1", "a="])
    C("dedup_with_nested", g, ["-D", "a[]=1", "a=2", "a[]=3"])
    C("skip_nulls", g, ["-n", "a=", "b=1", "c=null", "d"])
    C("skip_nulls_array", g, ["-n", "-a", "", "null", "1"])
    C("skip_nulls_bool_empty", g, ["-n", "a@", "b@0"])
    C("long_value", g, ["k=" + "x" * 5000])
    C("many_words", g, [f"k{i}={i}" for i in range(300)])
    C("pass_true", g, ["pass=true", "type=text"], source="harvested")
    C("nested_jo_output", g, ["name=Jane Jolie", 'data={"age":null,"country":"ES"}'], source="harvested")
    C("quoted_message", g, ['msg="All\'s Well", she said.'], source="harvested")
    C("location_pretty", g, ["-p", "type=location", "cog=120", "t=u", "lat=48.85833", "lon=2.29513", "acc=5",
                             "tid=JJ", "tst=1457767154"], source="harvested")
    C("artist_pretty", g, ["-p", "artist=Vanessa Paradis", "song=Joe le taxi", "year=1987"], source="harvested")
    C("seasons_array", g, ["-a", "spring", "summer", "autumn", "winter"], source="harvested")
    C("array_bool_strings", g, ["-a", "true", "false", "null", '"true"', '"false"', '"null"'], source="harvested")
    C("array_single", g, ["-a", "jo"], source="harvested")
    C("array_from_stdin_single", g, ["-a"], stdin=b"jo\n", source="harvested")


def booleans():
    g = "booleans"
    vals = ["", "T", "t", "true", "True", "TRUE", "F", "f", "false", "0", "1", "2", "-1", "0.5", "-0.5", "0.0",
            "1e3", "yes", "no", "x", "Tx", "tango", "null", " 1", "0x1", "inf", "nan", "@", "=1"]
    for i, v in enumerate(vals):
        C(f"at_value_{i:02d}", g, [f"b@{v}"], doc=f"key@value with {v!r}")
    C("coffee_and_morning", g, ["switch=true", "morning@0"])
    C("nobool_with_at", g, ["-B", "switch=true", "morning@0"])
    C("at_in_array_mode", g, ["-a", "b@1", "c@0"])
    C("at_nested_path", g, ["a[b]@1", "a[c]@0", "l[]@t"])


def nesting():
    g = "nesting"
    C("brackets_example", g, ["-p", "name=Jane", "point[]=1", "point[]=2", "geo[lat]=10", "geo[lon]=20"])
    C("object_path_example", g, ["-p", "-d.", "name=Jane", "point[]=1", "point[]=2", "geo.lat=10", "geo.lon=20"])
    C("dots_without_d", g, ["-p", "name=Jane", "point[]=1", "point[]=2", "geo.lat=10", "geo.lon=20"])
    C("harvest_05", g, ["a[]=1", "a[]=2", "geo[lat]=111", "geo[lon]=222"], source="harvested")
    C("harvest_18_plain", g, ["a.b=0", "a.c.d=1", "a.d.e[]=2", "a.d.e[]=sam", "a.c[f]@1", "b.e[]g=hi"], source="harvested")
    C("harvest_18_dot", g, ["-d.", "a.b=0", "a.c.d=1", "a.d.e[]=2", "a.d.e[]=sam", "a.c[f]@1", "b.e[]g=hi"], source="harvested")
    C("harvest_18_pipe", g, ["-d|first_char_only", "a|b=0", "a|c|d=1", "a|d|e[]=2", "a|d|e[]=sam", "a|c[f]@1", "b|e[]g=hi"],
      source="harvested")
    C("harvest_13_logo", g, ["-p", "name=This is jo", "px[]=300", "face=%logo.png", "meta[width]=300", "px[]=300",
                             "meta[height]=300", "meta[bytes]=8082", "meta[type]=png", "meta[creator]=JP"],
      files={"logo.png": bytes(range(0, 256, 3)) * 3}, source="harvested")
    words = [
        ["a[]=1"], ["a[]="], ["a[]"], ["a[b]=1"], ["a[b]="], ["a[b][c]=1"], ["a[b][]=1", "a[b][]=2"], ["a[][b]=1"],
        ["a[]=1", "a=2"], ["a=2", "a[]=1"], ["a[b]=1", "a[]=2"], ["a[]=1", "a[b]=2"], ["a[]=1", "b[]=2", "a[]=3"],
        ["[]=1"], ["[x]=1"], ["a[=1"], ["a]=1"], ["a[b=1"], ["a[b]c=1"], ["a[ b ]=1"], ["a[]]=1"], ["a[[]]=1"],
        ["a[]@1"], ["a[]=[1,2]"], ["a[]={}"], ["a[b]=[1]"], ["a[]=null"], ["a[x]=1", "a[x]=2"],
        ["a[]=1", "a[]=2", "-p"], ["x[y][z][w]=deep"],
    ]
    for i, w in enumerate(words):
        C(f"brackets_{i:02d}", g, w)
        C(f"brackets_array_mode_{i:02d}", g, ["-a"] + w)
    paths = [
        ["a.b=1"], ["a.b.c=1", "a.b.d=2"], ["a.b=1", "a=2"], ["a=2", "a.b=1"], [".a=1"], ["a.=1"], ["a..b=1"], ["."],
        ["a.b[]=1", "a.b[]=2"], ["a.b[c]=1"], ["a.b@1"], ["a.b"], ["a.b="], ["a.b=1", "a.b=2"], ["a.b.c.d.e.f=1"],
    ]
    for i, w in enumerate(paths):
        C(f"object_path_{i:02d}", g, ["-d."] + w)
        C(f"object_path_dedup_{i:02d}", g, ["-D", "-d", "."] + w)
    C("object_path_slash", g, ["-d", "/", "a/b=1", "a/c=2"])
    C("object_path_space", g, ["-d", " ", "a b=1"])
    C("object_path_equals", g, ["-d=", "a=b=1"])
    C("object_path_bracket_delim", g, ["-d[", "a[b=1"])
    C("object_path_array_mode", g, ["-a", "-d.", "a.b=1"])
    C("object_path_pretty", g, ["-p", "-d.", "a.b.c=1", "a.b.d=x", "a.e[]=1", "f=2"])


def coercion():
    g = "coercion"
    for i, v in enumerate(["", "string", '"quoted"', "12345", "true", "false", "null", "1.5", "-3", "0", " ", "1e3", "0x10"]):
        C(f"table_{i:02d}", g, ["--", "-s", f"s={v}", "-n", f"n={v}", "-b", f"b={v}", f"a={v}"],
          doc=f"coercion table row for {v!r}", source="harvested" if i < 7 else "probe")
    C("man_object_example", g, ["-p", "--", "-s", "a=true", "b=true", "-s", "c=123", "d=123", "-b", "e=1", "-b", "f=true",
                                "-n", "g=This is a test", "-b", "h=This is a test"])
    C("man_array_example", g, ["-a", "--", "-s", "123", "-n", "This is a test", "-b", "C_Rocks", "456"])
    C("coerce_without_double_dash", g, ["-s", "a=1"])
    C("coerce_n_without_double_dash", g, ["-n", "a=1"])
    C("coerce_twice", g, ["--", "-s", "-n", "a=1"])
    C("coerce_dangling", g, ["--", "a=1", "-s"])
    C("coerce_unknown_letter", g, ["--", "-x", "a=1"])
    C("coerce_dash_alone", g, ["--", "-", "a=1"])
    C("coerce_at_word", g, ["--", "-s", "a@1"])
    C("coerce_n_at_word", g, ["--", "-n", "a@1"])
    C("coerce_nested", g, ["--", "-s", "a[]=1", "-n", "a[]=xyz", "-b", "o[k]=0"])
    C("coerce_path", g, ["-d.", "--", "-s", "a.b=1", "-n", "a.c=abc"])
    C("coerce_file_value", g, ["--", "-n", "a=@f.txt", "-s", "b=@f.txt", "-b", "c=@empty"],
      files={"f.txt": b"hello\n", "empty": b""})
    C("coerce_json_value", g, ["--", "-s", "a=[1,2]", "-n", "b={\"x\":1}", "-b", "c=[]"])
    C("coerce_array_mode_all", g, ["-a", "--", "-s", "", "-n", "", "-b", "", "-s", "null", "-n", "null", "-b", "null"])
    C("coerce_with_nobool", g, ["-B", "--", "-b", "a=true", "-n", "b=true", "c=true"])
    C("coerce_skip_nulls", g, ["-n", "--", "-s", "a=", "-n", "b=", "c="])
    C("coerce_unicode_length", g, ["--", "-n", "a=日本語", "-n", "b=é"])
    C("coerce_n_float_string", g, ["--", "-n", "a=1.5x", "-n", "b=1.5"])


def pick(fs, *names):
    return {n: fs[n] for n in names}


def files():
    g = "file_values"
    fs = {"AUTHORS": b"Jan-Piet Mens <jpmens@gmail.com>\n", "nested.json": NESTED_JSON, "source.json": ARR_JSON,
          "empty": b"", "nl": b"\n", "two_lines": b"line1\nline2\n", "no_trailing_nl": b"abc",
          "crlf": b"a\r\nb\r\n", "bin": BINARY, "utf8": "héllo wörld ✓\n".encode(), "bad.json": b"{oops",
          "scalar.json": b"42\n", "str.json": b'"hi"', "big.txt": b"0123456789" * 20000, "nul": b"a\0b\n",
          "ws.json": b"  \n [ 1 , 2 ] \n\n", "deep.json": b"[" * 50 + b"]" * 50}
    C("at_file", g, ["program=jo", "authors=@AUTHORS"], files=pick(fs, "AUTHORS"))
    C("percent_file", g, ["filename=AUTHORS", "content=%AUTHORS"], files=pick(fs, "AUTHORS"))
    C("colon_file", g, ["nested=:nested.json"], files=pick(fs, "nested.json"))
    for name in fs:
        C(f"at_{name}", g, [f"v=@{name}"], files=pick(fs, name))
        C(f"percent_{name}", g, [f"v=%{name}"], files=pick(fs, name))
        C(f"colon_{name}", g, [f"v=:{name}"], files=pick(fs, name))
        C(f"assign_{name}", g, [f"v:={name}"], files=pick(fs, name))
    C("at_missing", g, ["v=@missing"])
    C("percent_missing", g, ["v=%missing"])
    C("colon_missing", g, ["v=:missing"])
    C("at_directory", g, ["v=@dir"], files={"dir/x": b"1"})
    C("percent_directory", g, ["v=%dir"], files={"dir/x": b"1"})
    C("at_dev_null", g, ["foo=bar", "baz=@/dev/null"], source="harvested")
    C("escaped_at", g, ["name=JP Mens", "twitter=\\@jpmens"])
    C("escaped_percent", g, ["char= ", "URIescape=\\%20"])
    C("escaped_colon", g, ["action=split window", "vimcmd=\\:split"])
    C("array_at_file", g, ["-a", "@AUTHORS", "%AUTHORS", ":nested.json", ":source.json"], files=pick(fs, "AUTHORS", "nested.json", "source.json"))
    C("array_two_json_files", g, ["-a", ":source.json", ":nested.json"], files=pick(fs, "source.json", "nested.json"))
    C("array_escaped", g, ["-a", "\\@x", "\\%y", "\\:z", "\\\\w"])
    C("assign_from_stdin", g, ["foo:=-"], stdin=b'["hello world"]\n', source="harvested")
    C("assign_from_stdin_object", g, ["a=1", "foo:=-"], stdin=b'{"x":[1,2]}')
    C("assign_from_stdin_invalid", g, ["foo:=-"], stdin=b"not json")
    C("assign_from_stdin_empty", g, ["foo:=-"], stdin=b"")
    C("assign_twice_from_stdin", g, ["a:=-", "b:=-"], stdin=b"[1]")
    C("assign_array_file", g, ["name=Jane", "obj:=arr.json"], files={"arr.json": b'["eX","whY","Zed"]\n'}, source="harvested")
    C("assign_in_array_mode", g, ["-a", "x:=source.json"], files=pick(fs, "source.json"))
    C("assign_nested_key", g, ["a[b]:=nested.json", "c[]:=source.json"], files=pick(fs, "nested.json", "source.json"))
    C("assign_path_key", g, ["-d.", "a.b:=nested.json"], files=pick(fs, "nested.json"))
    C("value_at_then_nested", g, ["a[]=@AUTHORS", "b[k]=%AUTHORS"], files=pick(fs, "AUTHORS"))


def input_files():
    g = "input_file"
    fs = {"obj.json": b'{"a":1,"b":[1,2]}', "arr.json": b"[1,2]", "scalar.json": b"3", "str.json": b'"x"',
          "bad.json": b"{", "empty.json": b"", "null.json": b"null", "dup.json": b'{"a":1,"a":2}',
          "nested.json": NESTED_JSON, "ws.json": b"\n\n {} \n"}
    for name in fs:
        C(f"f_{name.split('.')[0]}", g, ["-f", name, "c=3"], files=fs)
        C(f"f_{name.split('.')[0]}_noword", g, ["-f", name], files=fs, stdin=b"")
    C("f_obj_array_flag", g, ["-a", "-f", "obj.json", "x"], files=fs)
    C("f_arr_object_words", g, ["-f", "arr.json", "k=v", "z"], files=fs)
    C("f_dedup", g, ["-D", "-f", "obj.json", "a=9"], files=fs)
    C("f_dedup_dup_file", g, ["-D", "-f", "dup.json", "b=1"], files=fs)
    C("f_pretty", g, ["-p", "-f", "obj.json", "c[]=1"], files=fs)
    C("f_missing", g, ["-f", "missing.json", "a=1"])
    C("f_stdin", g, ["-f", "-", "status=Rickrolled"], stdin=b'{"type":"video","n":1}')
    C("f_stdin_array", g, ["-f", "-", "2", "3"], stdin=b'["base64.c","jo.c","json.c",1]', source="harvested")
    C("f_stdin_empty", g, ["-f", "-", "a=1"], stdin=b"")
    C("f_stdin_no_words", g, ["-f", "-"], stdin=b'{"a":1}')
    C("f_twice_last_wins", g, ["-f", "obj.json", "-f", "arr.json", "x"], files=fs)
    C("f_with_brackets", g, ["-f", "obj.json", "b[]=3", "n[k]=v"], files=fs)


def stdin_words():
    g = "stdin_words"
    C("lines_as_words", g, [], stdin=b"a=1\nb=2\n")
    C("lines_array", g, ["-a"], stdin=b"x\ny\n3\n")
    C("stops_at_blank_line", g, [], stdin=b"a=1\n\nb=2\n")
    C("leading_blank_line", g, ["-a"], stdin=b"\nx\n")
    C("no_trailing_newline", g, [], stdin=b"a=1\nb=2")
    C("crlf_lines", g, [], stdin=b"a=1\r\nb=2\r\n")
    C("spaces_kept", g, ["-a"], stdin=b"  spaced  \n")
    C("tabs", g, [], stdin=b"k=a\tb\n")
    C("long_line", g, ["-a"], stdin=b"y" * 100000 + b"\n")
    C("many_lines", g, ["-a"], stdin=b"".join(b"%d\n" % i for i in range(2000)))
    C("utf8_lines", g, [], stdin="ключ=значение\n日本=語\n".encode())
    C("invalid_utf8_line", g, ["-a"], stdin=b"\xff\xfe\n\xc3\x28\n")
    C("dash_lines_not_options", g, ["-a"], stdin=b"-p\n-s\n--\n")
    C("pretty_from_stdin", g, ["-p"], stdin=b"a[]=1\na[]=2\nb[c]=3\n")
    C("ls_like", g, ["-a"], stdin=b"AUTHORS\nCOPYING\nChangeLog\n")
    C("nul_in_line", g, ["-a"], stdin=b"a\0b\nc\n")
    C("stdin_ignored_with_words", g, ["a=1"], stdin=b"b=2\n")


def output():
    g = "output"
    C("pretty_nested_example", g, ["-p", "name=JP", 'object={"fruit":"Orange","hungry":false,"point":{"x":10,"y":20,'
                                   '"list":[1,2,3,4,5]},"number":17}', "sunday@0"])
    C("pretty_empty_containers", g, ["-p", "a={}", "b=[]", "c[]=", "d=[[],{}]"])
    C("pretty_strings_escaped", g, ["-p", "-a", "a\"b", "c\\d", "\t", "\x01", "é", " "])
    C("terse_escaping", g, ["-a", "\b\f\n\r\t", "\x00x"[1:], "\x1b[31m", "</script>", "ÿ"])
    C("outfile", g, ["-o", "out.json", "a=1"])
    C("outfile_pretty", g, ["-p", "-o", "out.json", "-a", "1", "2"])
    C("outfile_overwrites", g, ["-o", "out.json", "a=2"], files={"out.json": b"old content that is longer\n"})
    C("outfile_bad_dir", g, ["-o", "nodir/out.json", "a=1"])
    C("outfile_is_directory", g, ["-o", "d", "a=1"], files={"d/x": b""})
    C("outfile_empty_object", g, ["-o", "o.json"], stdin=b"")
    C("outfile_last_wins", g, ["-o", "1.json", "-o", "2.json", "a=1"])
    C("outfile_version_json", g, ["-o", "v.json", "-V"])


def coverage_driven():
    """Added after the first coverage run: JSON parser escapes and error paths, invalid UTF-8."""
    g = "json_values"
    docs = [
        r'["\"q\"", "\\", "\/", "\b\f\n\r\t"]', r'["Aé中"]', r'["😀"]', r'["😀"]',
        r'["\uD83D"]', r'["\uD83Dx"]', r'["\uD83DA"]', r'["\uDE00"]', r'["\u00"]', r'["\uZZZZ"]', r'["\x"]',
        r'["\u0000"]', '["tab\tinside"]', '["nl\ninside"]', r'["\u001f"]', '{"a":1,}', "[1,]", '{"a" 1}', '{1:2}',
        '{"a":}', "[1 2]", "[-]", "[1.]", "[.5]", "[1e]", "[1e+]", "[01]", "[-0]", "[1E2]", "[1e-2]", "[0.0e0]",
        "[true,false,null]", "[tru]", "[nul]", "[falsey]", '{"a":{"b":{"c":[[[]]]}}}', "[" + ",".join(["1"] * 200) + "]",
        '{"dup":1,"dup":2}', '  {"ws" :  [ 1 ,2 ]  }  ', '{"a":1} trailing', "[\"\xc3\xa9\"]", '["\xff"]',
    ]
    for i, d in enumerate(docs):
        C(f"inline_json_{i:02d}", g, [f"v={d}"], source="coverage", doc=f"value parsed as JSON: {d[:40]!r}")
        C(f"file_json_{i:02d}", g, ["v=:d.json"], files={"d.json": d.encode("utf-8", "surrogateescape")}, source="coverage")
        if d.startswith(("[", "{")):
            C(f"input_json_{i:02d}", g, ["-f", "d.json", "x=1"], files={"d.json": d.encode("utf-8", "surrogateescape")},
              source="coverage")
    g = "unicode"
    for i, s in enumerate(["\udcff", "a\udcc3", "\udcc3(", "\udce2\udc82", "ok\udcf0\udc9f\udc98", "é\udcff"]):
        C(f"invalid_utf8_value_{i}", g, [f"k={s}"], source="coverage")
        C(f"invalid_utf8_array_{i}", g, ["-a", s], source="coverage")
        C(f"invalid_utf8_key_{i}", g, [f"{s}=1"], source="coverage")
    C("astral_plane", g, ["-a", "😀", "𝄞", "\U0010FFFF"], source="coverage")
    C("bom_value", g, ["k=﻿x"], source="coverage")
    C("nul_file_value", g, ["k=@z"], files={"z": b"\0\0\0"}, source="coverage")
    C("invalid_utf8_file", g, ["k=@z", "j=%z"], files={"z": b"\xff\xfe\xfd"}, source="coverage")
    g = "coercion"
    for i, w in enumerate(["-s", "-n", "-b"]):
        for j, v in enumerate(["true", "false", "null", "", "@f", "x@1", "[1]"]):
            word = v if "@" in v and not v.startswith("@") else f"k={v}"
            C(f"coerce_matrix_{i}_{j}", g, ["--", w, word, "-a" if j == 0 else "z=1"], files={"f": b"1\n"}, source="coverage")
            C(f"coerce_matrix_array_{i}_{j}", g, ["-a", "--", w, v], files={"f": b"1\n"}, source="coverage")


def fuzz(n=420, seed=1234):
    rng = random.Random(seed)
    keys = ["a", "b", "k", "name", "x y", "é", "a.b", "a[]", "a[b]", "p.q.r", "list[]", "o[k]", "o[k][]", "", "n1"]
    vals = ["1", "-2.5", "1e3", "0x1", "true", "false", "null", "", "str", "two words", '"q"', "[1,2]", "{}",
            '{"z":[true]}', "[", "@f.txt", "%f.txt", ":j.json", "\\@lit", "日本", "T", "0", "1abc", "nan"]
    flags = ["-p", "-a", "-B", "-D", "-n", "-d.", "-e"]
    files = {"f.txt": b"file text\n", "j.json": b'{"j":[1,null]}'}
    for i in range(n):
        args = [f for f in flags if rng.random() < 0.18]
        words = []
        coerce_ok = rng.random() < 0.3
        if coerce_ok:
            words.append("--")
        for _ in range(rng.randint(0, 7)):
            if coerce_ok and rng.random() < 0.3:
                words.append(rng.choice(["-s", "-n", "-b"]))
            r = rng.random()
            if r < 0.6:
                words.append(f"{rng.choice(keys)}={rng.choice(vals)}")
            elif r < 0.75:
                words.append(f"{rng.choice(keys)}@{rng.choice(vals)}")
            elif r < 0.85:
                words.append(f"{rng.choice(keys)}:=j.json")
            else:
                words.append(rng.choice(vals))
        stdin = None
        if not words and rng.random() < 0.7:
            stdin = "\n".join(f"{rng.choice(keys)}={rng.choice(vals)}" for _ in range(rng.randint(1, 4))) + "\n"
        C(f"fuzz_{i:03d}", "fuzz", args + words, stdin=stdin, files=files, source="fuzz")


def generate(src):
    for f in (cli, scalars, keys_and_words, booleans, nesting, coercion, files, input_files, stdin_words, output,
              coverage_driven, fuzz):
        f()
    return CASES
