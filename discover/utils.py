def translate_address(address: bytes) -> str:
    """
    Translates a given address to a human-readable format.
    """
    return '.'.join(str(bin) for bin in address)
