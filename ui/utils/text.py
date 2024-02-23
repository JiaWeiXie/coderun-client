import difflib


WINDOWS_LINE_ENDING = b"\r\n"
UNIX_LINE_ENDING = b"\n"


def normalization_text(txt: str) -> str:
    contexts = []
    txt = txt.encode("utf-8").replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING).decode()
    for line in txt.splitlines():
        s = line.strip()
        if s:
            contexts.append(s)

    return "\n".join(contexts) + "\n"


def generate_diff(old_text, new_text):
    diff = difflib.ndiff(
        old_text.splitlines(),
        new_text.splitlines(),
    )
    left = []
    right = []
    is_diff = False
    for line in diff:
        if line.startswith("- "):
            is_diff = True
            left.append(line)
        elif line.startswith("+ ") and is_diff:
            right.append(line)
            is_diff = False
        else:
            left.append(line)
            right.append(line)
    return "\n".join(left), "\n".join(right)
