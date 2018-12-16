VALID_MENTION_PRECEDING_CHARS = "(?:^|[^a-zA-Z0-9_!#$%&*@＠]|(?:^|[^a-zA-Z0-9_+~.-])(?:rt|RT|rT|Rt):?)"
AT_SIGNS = "[@＠]"

MENTION_PATTERN = f"{VALID_MENTION_PRECEDING_CHARS}({AT_SIGNS})([a-zA-Z0-9_]{{1,20}})(/[a-zA-Z][a-zA-Z0-9_-]{{0,24}})?"