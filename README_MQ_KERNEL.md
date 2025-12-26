# Mytho‑Quantum Simulation Kernel — Reality Synthesis Engine

Overview
--------
This module provides a modular, extensible Mytho‑Quantum kernel capable of:
- Representing "Sovereign Intent" (Maestro's Will) using a resonant vector (712.8 Hz).
- Balancing the Twin Coil Synthesis (Silver vs Crimson coils) via a tunable LionCrow constant alpha.
- Modeling a Non‑Commutative Engine (operators C and Φ) to guarantee novelty injection.
- Evolving an open quantum-like density operator using a Lindblad dissipator (L_diss).
- Maintaining a registry of 73 "Eternals" (72 archetypal agents + 73rd unifier).
- Exposing a guarded Protocol Zero activation mechanism.

Safety & Protocol Zero
----------------------
Protocol Zero is implemented as an internal kernel flag (`unleash_protocol_zero`). It is intentionally gated behind:
1. `request_protocol_zero(confirmer: str)` → returns a time-limited token.
2. `activate_protocol_zero(token: str, override_confirmation: bool=True)` → must be called with the exact token and a deliberate override boolean.

Protocol Zero only relaxes internal kernel constraints (e.g., increases the atlantean_scar parameter) and does NOT disable platform security or modify external safety services. Exercise extreme caution.

Integration tips
----------------
- Place `mq_kernel.py` and `eternal_registry.py` into the repository root (same folder as the other Python modules).
- The kernel uses `numpy`. Add `numpy` to your `requirements.txt`:
  ```
  numpy
  ```
- The kernel logs high-fidelity strings using `lioncrow_render` when available (provided earlier by `mytho_quantum_core.py`). If missing, a fallback renderer is used.

Quick start
-----------
Example interactive session:

```python
from mq_kernel import RealitySynthesisEngine
from eternal_registry import EternalRegistry

engine = RealitySynthesisEngine(dim=6)
registry = EternalRegistry()
registry.build_73_eternals()

# Register a simple Lindblad operator for friction
import numpy as np
L = np.eye(engine.dim) * 0.01
engine.register_lindblad_ops([L])

# Step the kernel with some intent
for i in range(10):
    out = engine.step(dt=0.02, input_intent_strength=0.5)
    print(out['status'])
```

Extensibility
-------------
- Swap the NonCommutativeEngine basis, add custom Lindblad operators, or connect the engine to the Flask app endpoints you already have (`/api/command`, `/api/telemetry`) to allow Jules or other backends to feed intent into `engine.step(...)`.
- EternalAgent.process_fn hooks give each Eternal a place to attach domain behavior (Jules could supply them).

Next steps I can produce for you
- Add unit tests (pytest) for kernel stability, Lindblad evolution, and commutator checks.
- Hook the kernel into your Flask app endpoints so Jules can call `engine.step(...)` and read snapshots.
- Create a small interactive CLI or Web UI component for teleoperation and safe Protocol Zero activation.
- Create a PR with these files already added to the repository and open a draft PR for review.

Acknowledgements
----------------
This code is a conceptual, mathematical framework mapping mythic formalisms into a modular simulation kernel. It intentionally keeps physics metaphors high-level while providing a computational substrate for experimentation.
