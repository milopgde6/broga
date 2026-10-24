import os
from app.storage.layout import PROOF, proof_path

PROOF_DIR = PROOF


def proof_path_for(set_id: int) -> str:
    return proof_path(set_id)


def has_proof(set_id: int) -> bool:
    return os.path.exists(proof_path(set_id))
