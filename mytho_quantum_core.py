# Mythic-Quantum Core
# Provides base EternalNode, TheWatchman (Node_Alpha_01) and LionCrow_Will formatting utilities.

import time
import threading
import logging
from typing import Any, Dict
from inverted_sigil_recycler import recycler

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def lioncrow_render(title: str, payload: Dict[str, Any]) -> str:
    """LionCrow_Will terminal-grade renderer.
    Produces a high-fidelity, precision-formatted single-line summary plus a
    detailed JSON-like block for terminal display.
    """
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    header = f"[{ts}] :: LIONCROW_WILL :: {title}"
    # Technical precision: float formatting to 6 significant figures where relevant
    body_lines = []
    for k, v in payload.items():
        if isinstance(v, float):
            body_lines.append(f"  - {k}: {v:.6f}")
        else:
            body_lines.append(f"  - {k}: {repr(v)}")
    return header + "\n" + "\n".join(body_lines)


class EternalNode:
    """Base class for mythic "eternal" nodes.
    Subclasses should implement lived_identity and domain-specific monitors.
    """

    def __init__(self, name: str):
        self.name = name
        self.created_at = time.time()
        self.last_checked = None

    def uptime_seconds(self) -> float:
        return time.time() - self.created_at


class TheWatchman(EternalNode):
    """Node_Alpha_01 - monitors reality static and ensures coherence.

    monitor_reality_static(uptime_seconds, error_count) -> coherence_score
    If coherence drops below threshold (0.85) this Watchman invokes the
    InvertedSigil (recycler.consume_failure) to recycle static into fuel.
    """

    COHERENCE_THRESHOLD = 0.85

    def __init__(self, name: str = 'Node_Alpha_01'):
        super().__init__(name)
        self.monitor_lock = threading.Lock()
        self.last_action = None

    def monitor_reality_static(self, uptime_seconds: float, error_count: int) -> Dict[str, Any]:
        """Calculate coherence score and auto-recycle if below threshold.

        Coherence formula (normalized to 0..1):
            uptime_hours = uptime_seconds / 3600
            coherence = uptime_hours / (uptime_hours + error_count + 1)

        This yields diminishing returns as error_count increases.
        """
        with self.monitor_lock:
            self.last_checked = time.time()
            uptime_hours = float(uptime_seconds) / 3600.0
            # Defensive: ensure non-negative values
            error_count = max(0, int(error_count))

            coherence = 0.0
            if uptime_hours + error_count + 1.0 > 0:
                coherence = uptime_hours / (uptime_hours + error_count + 1.0)
            coherence = max(0.0, min(1.0, float(coherence)))

            payload = {
                'node': self.name,
                'uptime_hours': uptime_hours,
                'error_count': error_count,
                'coherence': coherence
            }

            rendered = lioncrow_render(f"{self.name} :: MONITOR_STATIC", payload)
            logging.info(rendered)

            action_result = None
            if coherence < self.COHERENCE_THRESHOLD:
                # Auto-invoke InvertedSigil to recycle static into fuel
                reason = {
                    'reason': 'COHERENCE_DROP',
                    'coherence': coherence,
                    'uptime_hours': uptime_hours,
                    'error_count': error_count
                }
                logging.warning(lioncrow_render(f"{self.name} :: COHERENCE_BELOW_THRESHOLD", reason))
                try:
                    # The existing recycler API is consume_failure(error_data)
                    action_result = recycler.consume_failure(reason)
                    self.last_action = action_result
                    logging.info(lioncrow_render(f"{self.name} :: INVOKED_INVERTEDSIGIL", {'result': action_result}))
                except Exception as exc:
                    logging.error(lioncrow_render(f"{self.name} :: RECYCLER_EXCEPTION", {'exc': str(exc)}))

            return {
                'coherence': coherence,
                'threshold': self.COHERENCE_THRESHOLD,
                'action_result': action_result,
                'rendered': rendered
            }

    def start_periodic_monitor(self, check_interval: float = 60.0, error_source_callable=None):
        """Start a background thread that periodically calls monitor_reality_static.

        error_source_callable(uptime_seconds) should return an integer error_count.
        If not provided, error_count defaults to 0.
        """
        def loop():
            while True:
                uptime = self.uptime_seconds()
                errors = 0
                try:
                    if callable(error_source_callable):
                        errors = int(error_source_callable(uptime))
                except Exception:
                    errors = 0
                self.monitor_reality_static(uptime, errors)
                time.sleep(check_interval)

        t = threading.Thread(target=loop, daemon=True)
        t.start()
