import subprocess
import logging
from utils.logger import setup_logger
_logger = setup_logger()

def restart_service(service_name):
    """
    Restart a Linux systemd service via systemctl.
    No service names are hard-coded; caller must supply a valid name.

    Safety note: automatic restarts can mask underlying issues and
    should be rate-limited and combined with proper alerting.
    """
    try:
        subprocess.run(
            ["systemctl", "restart", service_name],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True
    except subprocess.CalledProcessError as exc:
        # Log failure details for later investigation
        logging.error("Failed to restart %s: %s", service_name, exc.stderr.strip())
        return False


def log_healing_action(action, logger=None):
    """
    Record an automatic healing action.

    Parameters
    ----------
    action : str
        Human-readable description of the healing step taken.
    logger : logging.Logger, optional
        Logger instance to use.  If omitted, the root logger is used.
    """
    if logger is None:
        logger = logging.getLogger()
    logger.warning("AUTO-HEAL: %s", action)

def trigger_auto_heal(anomaly, logger=None):
    if logger is None:
        logger = _logger
    try:
        is_anom = anomaly.get("anomaly") if isinstance(anomaly, dict) else bool(anomaly)
    except Exception:
        is_anom = False
    if not is_anom:
        return False
    score = anomaly.get("score", 0.0) if isinstance(anomaly, dict) else 0.0
    logger.warning(f"Auto-heal triggered for anomaly score={score:.4f}")
    return True
