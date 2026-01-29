import time

# import moved to where it's used inside the loop
from utils.config_loader import load_config
from utils.logger import setup_logger
from monitoring.metrics_collector import collect_metrics
from monitoring.threshold_checker import check_thresholds
from monitoring.network_monitor import check_network_thresholds
from ai.anomaly_detector import detect_anomaly
from healing.auto_healer import trigger_auto_heal
from utils.data_handler import save_metrics_to_csv

def main():
    # Setup logger
    logger = setup_logger()
    logger.info("System started")

    # Load configuration
    config = load_config("config/config.yaml")
    interval = config.get("monitoring_interval", 60)
    try:
        interval = int(interval)
    except Exception:
        interval = 60
    if interval < 1:
        interval = 1

    try:
        while True:
            try:
                metrics = collect_metrics()
                logger.info("Metrics collected")
                save_metrics_to_csv(metrics)
                logger.info("Metrics saved to CSV")
                threshold_issue = check_thresholds(metrics, config)
                if threshold_issue.get('threshold_exceeded'):
                    logger.warning(f"Threshold breach detected: {threshold_issue}")
                net_issue = check_network_thresholds(metrics, config)
                if net_issue.get('threshold_exceeded'):
                    logger.warning(f"Network threshold breach: {net_issue}")
                    trigger_auto_heal({'anomaly': True, 'score': 0.0})
                anomaly = detect_anomaly(metrics, config)
                if anomaly and anomaly["anomaly"]:
                    logger.warning(f"AI anomaly detected: {anomaly}")
                    trigger_auto_heal(anomaly)
                    logger.info("Auto-healing triggered")
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Shutdown requested")

if __name__ == "__main__":
    main()
