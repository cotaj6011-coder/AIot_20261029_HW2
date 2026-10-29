from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import ipaddress
from pathlib import Path
import socket
from urllib.parse import urlparse

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 10 * 1024 * 1024
MAX_ROWS = 100_000
MAX_COLUMNS = 200


@dataclass(frozen=True)
class DatasetSpec:
    id: str
    label: str
    path: Path
    target: str
    excluded: tuple[str, ...]
    source_url: str
    license_note: str
    description: str


DATASETS = {
    "human_ai": DatasetSpec(
        id="human_ai",
        label="Problem A — Human–AI Trust（Kaggle）",
        path=ROOT / "data" / "human_ai_interaction.csv",
        target="latent_trust_score",
        excluded=(),
        source_url="https://www.kaggle.com/datasets/eshaalnmalik/human-ai-interaction",
        license_note="CC0 Public Domain；合成教育資料，非真人觀測。",
        description="依人類、AI、互動與情境因素預測 0–100 信任分數。",
    ),
    "startups": DatasetSpec(
        id="startups",
        label="Problem B — 50 Startups Profit",
        path=ROOT / "data" / "50_Startups.csv",
        target="Profit",
        excluded=(),
        source_url="https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv",
        license_note="教學資料；沿用 DIC2，非本作業正式 Kaggle 14–39 特徵題。",
        description="依研發、行政、行銷支出與州別預測新創公司利潤。",
    ),
}


def load_builtin(dataset_id: str) -> tuple[pd.DataFrame, DatasetSpec]:
    spec = DATASETS[dataset_id]
    if not spec.path.exists():
        raise FileNotFoundError(f"缺少資料檔：{spec.path.name}")
    return pd.read_csv(spec.path), spec


def _is_public_ip(value: str) -> bool:
    ip = ipaddress.ip_address(value)
    return not any((ip.is_private, ip.is_loopback, ip.is_link_local,
                    ip.is_reserved, ip.is_multicast, ip.is_unspecified))


def validate_public_https_url(url: str, resolver=socket.getaddrinfo) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username:
        raise ValueError("僅接受不含帳密的公開 HTTPS URL。")
    if parsed.hostname.lower() == "localhost" or "." not in parsed.hostname:
        raise ValueError("不接受本機或內部主機名稱。")
    try:
        addresses = {item[4][0] for item in resolver(parsed.hostname, 443, type=socket.SOCK_STREAM)}
    except socket.gaierror as exc:
        raise ValueError("無法解析 URL 主機名稱。") from exc
    if not addresses or any(not _is_public_ip(address) for address in addresses):
        raise ValueError("URL 指向非公開 IP，已拒絕載入。")


def load_csv_url(url: str, *, session=requests, timeout: tuple[int, int] = (5, 20)) -> pd.DataFrame:
    validate_public_https_url(url)
    try:
        response = session.get(url, timeout=timeout, stream=True, allow_redirects=True)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ValueError(f"無法下載 CSV：{exc}") from exc
    validate_public_https_url(response.url)
    content_type = response.headers.get("Content-Type", "").lower()
    chunks, total = [], 0
    for chunk in response.iter_content(64 * 1024):
        if not chunk:
            continue
        total += len(chunk)
        if total > MAX_BYTES:
            raise ValueError("CSV 超過 10 MB 上限。")
        chunks.append(chunk)
    payload = b"".join(chunks)
    if not payload:
        raise ValueError("URL 回傳空內容。")
    prefix = payload[:512].lstrip().lower()
    if "html" in content_type or prefix.startswith((b"<!doctype html", b"<html")):
        raise ValueError("URL 回傳 HTML，不是 CSV。")
    try:
        frame = pd.read_csv(BytesIO(payload))
    except Exception as exc:
        raise ValueError("無法解析為 CSV。") from exc
    if frame.shape[1] < 2:
        raise ValueError("CSV 至少需要一個特徵欄與一個 target 欄。")
    if len(frame) > MAX_ROWS or frame.shape[1] > MAX_COLUMNS:
        raise ValueError("CSV 超過 100,000 列或 200 欄上限。")
    return frame

