"""
LogPulse Mini SIEM — Parser Service & Rule Engine
Parses incoming log messages, matches against rules, assigns severity,
and triggers alerts when rules match.
"""

import json
import os
import logging
from typing import Optional, Tuple
from datetime import datetime

logger = logging.getLogger("logpulse.parser")

# Load rules from JSON file
RULES_PATH = os.path.join(os.path.dirname(__file__), "..", "rules", "rules.json")


def load_rules() -> list:
    """Load rule definitions from rules.json."""
    try:
        with open(RULES_PATH, "r") as f:
            rules = json.load(f)
            logger.info(f"Loaded {len(rules)} rules from {RULES_PATH}")
            return rules
    except FileNotFoundError:
        logger.warning(f"Rules file not found at {RULES_PATH}, using empty rules")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse rules.json: {e}")
        return []


# Load rules at module level
_rules = load_rules()


def reload_rules():
    """Reload rules from disk (useful if rules.json is updated)."""
    global _rules
    _rules = load_rules()


def match_rule(message: str) -> Optional[dict]:
    """
    Check a log message against all defined rules.
    Returns the first matching rule or None.
    Rules are checked in order — first match wins.
    """
    message_lower = message.lower()
    for rule in _rules:
        if rule["keyword"].lower() in message_lower:
            return rule
    return None


def parse_log(message: str, source: str = "unknown") -> dict:
    """
    Parse a raw log message:
    1. Match against rule engine
    2. Assign severity (from rule or default INFO)
    3. Return structured log event data

    Returns a dict with keys: timestamp, severity, source, message, rule_matched, is_alert
    """
    timestamp = datetime.utcnow().isoformat()

    # Try to match a rule
    matched_rule = match_rule(message)

    if matched_rule:
        severity = matched_rule["severity"]
        rule_description = matched_rule["description"]
        is_alert = severity in ("ERROR", "WARNING")
        logger.info(f"Rule matched: '{matched_rule['keyword']}' → {severity}")
    else:
        severity = "INFO"
        rule_description = None
        is_alert = False

    return {
        "timestamp": timestamp,
        "severity": severity,
        "source": source,
        "message": message,
        "rule_matched": rule_description,
        "is_alert": is_alert,
    }
