from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import numpy as np


@dataclass
class ModelResult:
  label: str
  score: float
  explanation: str


class RansomwareHeuristicModel:
  """Very lightweight heuristic model for ransomware-like behaviour.

  This is NOT a real detector – it's a deterministic scoring function
  so the demo works without heavy dependencies or real training.
  """

  name = "ransomware_heuristic_v1"

  def predict(self, features: Dict[str, Any]) -> ModelResult:
    score = 0.0

    ext = str(features.get("extension", "")).lower()
    if ext in {".lock", ".locked", ".enc", ".crypted"}:
      score += 0.4

    if features.get("suspicious_process", False):
      score += 0.3

    if features.get("high_entropy", False):
      score += 0.2

    if features.get("rapid_file_changes", False):
      score += 0.3

    score = float(max(0.0, min(1.0, score)))

    label = "malicious" if score >= 0.7 else "benign"

    explanation_parts = []
    if ext in {".lock", ".locked", ".enc", ".crypted"}:
      explanation_parts.append("suspicious encrypted file extension")
    if features.get("suspicious_process", False):
      explanation_parts.append("known ransomware process pattern")
    if features.get("high_entropy", False):
      explanation_parts.append("high file entropy (likely encrypted)")
    if features.get("rapid_file_changes", False):
      explanation_parts.append("rapid file changes detected")

    explanation = ", ".join(explanation_parts) or "no strong ransomware indicators"

    return ModelResult(label=label, score=score, explanation=explanation)


class BeaconingHeuristicModel:
  """Heuristic model for simple C2 beaconing patterns."""

  name = "beaconing_heuristic_v1"

  def predict(self, features: Dict[str, Any]) -> ModelResult:
    score = 0.0

    jitter = float(features.get("jitter", 0.0))
    interval = float(features.get("interval_seconds", 0.0))
    dest_rep = float(features.get("dest_reputation", 0.5))

    if 20 <= interval <= 120 and jitter < 0.2:
      score += 0.5

    if dest_rep < 0.2:
      score += 0.3

    if features.get("suspicious_user_agent", False):
      score += 0.2

    score = float(max(0.0, min(1.0, score)))
    label = "malicious" if score >= 0.7 else "benign"

    explanation = """interval={:.1f}s, jitter={:.2f}, dest_rep={:.2f}""".format(
      interval, jitter, dest_rep
    )

    return ModelResult(label=label, score=score, explanation=explanation)


class LOLBASHeuristicModel:
  """Detect suspicious use of living-off-the-land binaries."""

  name = "lolbas_heuristic_v1"

  SUSPICIOUS_BINARIES = {
    "powershell.exe",
    "cmd.exe",
    "wmic.exe",
    "mshta.exe",
    "rundll32.exe",
    "regsvr32.exe",
  }

  def predict(self, features: Dict[str, Any]) -> ModelResult:
    score = 0.0

    binary = str(features.get("binary_name", "")).lower()
    has_encoded = bool(features.get("uses_encoded_command", False))
    net_ops = int(features.get("network_ops", 0))

    if binary in self.SUSPICIOUS_BINARIES:
      score += 0.4

    if has_encoded:
      score += 0.3

    if net_ops > 0:
      score += 0.2

    score = float(max(0.0, min(1.0, score)))
    label = "malicious" if score >= 0.6 else "benign"

    reasons = []
    if binary in self.SUSPICIOUS_BINARIES:
      reasons.append(f"binary {binary} is commonly abused (LOLBAS)")
    if has_encoded:
      reasons.append("uses encoded/obfuscated command line")
    if net_ops > 0:
      reasons.append("performs network operations")

    explanation = ", ".join(reasons) or "no suspicious LOLBAS usage detected"
    return ModelResult(label=label, score=score, explanation=explanation)


class ModelManager:
  """Lightweight manager aggregating all demo models."""

  def __init__(self) -> None:
    self.ransomware = RansomwareHeuristicModel()
    self.beaconing = BeaconingHeuristicModel()
    self.lolbas = LOLBASHeuristicModel()

  def predict_ransomware(self, features: Dict[str, Any]) -> ModelResult:
    return self.ransomware.predict(features)

  def predict_beaconing(self, features: Dict[str, Any]) -> ModelResult:
    return self.beaconing.predict(features)

  def predict_lolbas(self, features: Dict[str, Any]) -> ModelResult:
    return self.lolbas.predict(features)
