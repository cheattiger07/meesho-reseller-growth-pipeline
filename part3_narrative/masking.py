def alias_for(reseller_id: str) -> str:
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(
    text: str, reseller_names: list[str]
) -> bool:
    for name in reseller_names:
        if name in text:
            return False

    return True