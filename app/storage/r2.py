"""Cloudflare R2 (S3-compatible) object storage client.

boto3 is imported lazily so the bot still runs locally without R2 configured.
"""
import logging
import threading

from config.settings import (
    R2_ACCOUNT_ID,
    R2_ACCESS_KEY_ID,
    R2_BUCKET,
    R2_ENDPOINT,
    R2_SECRET_ACCESS_KEY,
)

log = logging.getLogger("theez.r2")

_client = None
_client_lock = threading.Lock()


def enabled() -> bool:
    return bool(
        R2_ACCESS_KEY_ID
        and R2_SECRET_ACCESS_KEY
        and R2_BUCKET
        and (R2_ENDPOINT or R2_ACCOUNT_ID)
    )


def _endpoint() -> str:
    if R2_ENDPOINT:
        return R2_ENDPOINT.rstrip("/")
    return f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"


def client():
    """Return a shared boto3 S3 client for R2."""
    global _client
    if not enabled():
        raise RuntimeError("R2 is not configured")
    if _client is None:
        with _client_lock:
            if _client is None:
                import boto3
                from botocore.config import Config

                _client = boto3.client(
                    "s3",
                    endpoint_url=_endpoint(),
                    aws_access_key_id=R2_ACCESS_KEY_ID,
                    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
                    region_name="auto",
                    config=Config(
                        signature_version="s3v4",
                        retries={"max_attempts": 3, "mode": "standard"},
                    ),
                )
    return _client


def upload_file(local_path: str, key: str, content_type: str | None = None) -> str:
    extra = {"ContentType": content_type} if content_type else {}
    client().upload_file(local_path, R2_BUCKET, key, ExtraArgs=extra)
    return key


def put_bytes(key: str, data: bytes, content_type: str | None = None) -> str:
    extra = {"ContentType": content_type} if content_type else {}
    client().put_object(Bucket=R2_BUCKET, Key=key, Body=data, **extra)
    return key


def get_bytes(key: str) -> bytes:
    return client().get_object(Bucket=R2_BUCKET, Key=key)["Body"].read()


def iter_chunks(key: str, chunk: int = 1 << 20):
    body = client().get_object(Bucket=R2_BUCKET, Key=key)["Body"]
    try:
        yield from body.iter_chunks(chunk)
    finally:
        body.close()


def exists(key: str) -> bool:
    from botocore.exceptions import ClientError

    try:
        client().head_object(Bucket=R2_BUCKET, Key=key)
        return True
    except ClientError as exc:
        code = str(exc.response.get("Error", {}).get("Code", ""))
        if code in ("404", "NoSuchKey", "NotFound"):
            return False
        raise


def size(key: str) -> int:
    return client().head_object(Bucket=R2_BUCKET, Key=key)["ContentLength"]


def presigned_url(key: str, expires: int = 300) -> str:
    return client().generate_presigned_url(
        "get_object",
        Params={"Bucket": R2_BUCKET, "Key": key},
        ExpiresIn=int(expires),
    )


def delete(key: str) -> None:
    client().delete_object(Bucket=R2_BUCKET, Key=key)
