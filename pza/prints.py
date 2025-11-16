DEFAULT_LABEL_WIDTH = 30
DEFAULT_LINE_WIDTH = 80

def print_error(current_exception: Exception, description: str = "An error occurred:") -> None:
    print(f"{description}")
    print(f"{current_exception}")

def print_subheader(header_text: str = "") -> None:
    print()
    print(f"{header_text}:")
    print()
    return

def print_header(header_text: str = "") -> None:
    print()
    print(f"--- {header_text} ---")
    print()
    return

def print_separator(separator_text: str = "") -> None:
    print(f"--- {separator_text} ---")
    return

def print_footer(footer_text: str = "") -> None:
    print()
    print(f"--- {footer_text} ---")
    print()
    return

def print_line(line_width: int = DEFAULT_LINE_WIDTH) -> None:
    print(f"{'=' * line_width}")
    return

def get_label(label_text: str, padding: int = DEFAULT_LABEL_WIDTH, suffix: str = ":") -> str:
    suffix = suffix or ""
    label_text = f"{label_text.strip()}{suffix}" # Leave suffix unstripped to allow spaces
    if padding > 0:
        label_text = pad_left(label_text, padding, " ")
    return label_text

def print_label(label_text: str, padding: int = DEFAULT_LABEL_WIDTH, suffix: str = "") -> None:
    label_text = get_label(label_text, padding, suffix)
    print(f"{label_text}")
    return

def print_with_label(label_text: str, value_text: str, padding: int = DEFAULT_LABEL_WIDTH, suffix: str = ":") -> None:
    label_text = get_label(label_text, padding, suffix)
    print(f"{label_text} {value_text}")
    return

def pad_left(target_text: str, padding: int = DEFAULT_LABEL_WIDTH, pad_character: str = " "):
    target_text = target_text.rjust(padding, pad_character)
    return target_text

def pad_right(target_text: str, padding: int = DEFAULT_LABEL_WIDTH, pad_character: str = " "):
    target_text = target_text.ljust(padding, pad_character)
    return target_text

def print_zen() -> None:
    zen = f"""
        Beautiful is better than ugly.
        Explicit is better than implicit.
        Simple is better than complex.
        Complex is better than complicated.
        Flat is better than nested.
        Sparse is better than dense.
        Readability counts.
        Special cases aren't special enough to break the rules.
        Although practicality beats purity.
        Errors should never pass silently.
        Unless explicitly silenced.
        In the face of ambiguity, refuse the temptation to guess.
        There should be one-- and preferably only one --obvious way to do it.
        Although that way may not be obvious at first unless you are Dutch.
        Now is better than never.
        Although never is often better than *right* now.
        If the implementation is hard to explain, it is a bad idea.
        If the implementation is easy to explain, it may be a good idea.
        Namespaces are one honking great idea -- let's do more of those!

        Source: Tim Peters, "The Zen of Python" (PEP 20) — also available in CPython via `import this`.
    """
    print_line()
    print(zen)
    print_line()
    return

if __name__ == "__main__":

    print_header(f"{__file__}")

    print_separator()

    print_zen()

    print_separator()

    print_footer()
