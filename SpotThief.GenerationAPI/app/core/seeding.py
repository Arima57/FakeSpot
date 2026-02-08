import hashlib
import struct

def get_identity_seed(global_seed: str, index: int) -> int:
    """Port of C# GetStableIntSeed to ensure parity."""
    combined = f"{global_seed}_{index}".encode('utf-8')
    hash_bytes = hashlib.sha256(combined).digest()
    return struct.unpack('<i', hash_bytes[:4])[0]