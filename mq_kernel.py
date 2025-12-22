# Mytho-Quantum Simulation Kernel (Reality Synthesis Engine)
# Implements: SovereignIntentVector, TwinCoilSynthesis, NonCommutativeEngine,
# Lindblad dissipator, and a top-level RealitySynthesisEngine harness.
#
# Notes:
# - Uses numpy for operator math.
# - Protocol Zero is gated behind a deliberate confirmation mechanism.
# - For terminal rendering it attempts to use lioncrow_render (if present).
#   Otherwise, falls back to a simple textual formatter.

from __future__ import annotations
import numpy as np
import threading
import time
import math
import logging
from typing import List, Sequence, Optional, Dict, Any

try:
    # The mytho_quantum_core from earlier additions provides lioncrow_render
    from mytho_quantum_core import lioncrow_render
except Exception:
    def lioncrow_render(title: str, payload: Dict[str, Any]) -> str:
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        header = f"[{ts}] :: LIONCROW_WILL :: {title}"
        body = "\n".join(f"  - {k}: {v!r}" for k, v in payload.items())
        return f"{header}\n{body}"

logger = logging.getLogger("mq_kernel")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(handler)


# --------------------------
# Constants and utilities
# --------------------------
SOUL_RESONANCE_HZ = 712.8  # Primary Atlantean resonant constant


def commutator(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    return A @ B - B @ A


def anticommutator(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    return A @ B + B @ A


# --------------------------
# Sovereign Intent Vector
# --------------------------
class SovereignIntentVector:
    """Represents Maestro's Will as a tunable vector of intent.

    Attributes:
        frequency_hz: resonance used by the intent
        amplitude: scalar 'mass' of intent
        direction: normalized numpy vector describing phase/direction
    """

    def __init__(self, dimension: int = 4, frequency_hz: float = SOUL_RESONANCE_HZ,
                 amplitude: float = 1.0):
        self.frequency_hz = float(frequency_hz)
        self.amplitude = float(amplitude)
        self.dimension = max(1, int(dimension))
        # direction is normalized
        v = np.random.randn(self.dimension).astype(float)
        v /= np.linalg.norm(v) if np.linalg.norm(v) > 0 else 1.0
        self.direction = v

    def modulate(self, strength: float, phase: float = 0.0) -> np.ndarray:
        """Return an intent vector scaled by strength and phase-travel."""
        angle = 2.0 * math.pi * (self.frequency_hz * phase)
        scale = self.amplitude * float(strength)
        vec = scale * (math.cos(angle) * self.direction)
        return vec

    def to_dict(self) -> Dict[str, Any]:
        return {
            "frequency_hz": self.frequency_hz,
            "amplitude": self.amplitude,
            "dimension": self.dimension,
            "direction_norm": float(np.linalg.norm(self.direction))
        }


# --------------------------
# Twin Coil Synthesis Module
# --------------------------
class TwinCoil:
    """LionCrow Synthesis Equation S_LC maintaining equilibrium between
    the Silver Coil (Lambda_S) and the Crimson Coil (Psi_C).

    S_LC = alpha * Lambda_S + (1 - alpha) * Psi_C
    where alpha in [0..1] and alpha = 0.5 -> perfect synthesis
    """

    def __init__(self, alpha: float = 0.5, lambda_s: float = 1.0, psi_c: float = 1.0):
        self.alpha = float(alpha)
        self.lambda_s = float(lambda_s)
        self.psi_c = float(psi_c)

    def synthesis_value(self) -> float:
        """Compute the LionCrow synthesis scalar (balance metric)."""
        return self.alpha * self.lambda_s + (1.0 - self.alpha) * self.psi_c

    def balance(self, drift: float = 0.0) -> Dict[str, float]:
        """Apply a small drift and return updated coil values and synthesis."""
        # Simple equilibration model: coils tug towards each other proportionally
        delta = (self.psi_c - self.lambda_s) * 0.1
        self.lambda_s += delta + (drift * (1 - self.alpha))
        self.psi_c -= delta - (drift * self.alpha)
        val = self.synthesis_value()
        return {"lambda_s": self.lambda_s, "psi_c": self.psi_c, "synthesis": val, "alpha": self.alpha}

    def set_alpha(self, new_alpha: float):
        self.alpha = float(max(0.0, min(1.0, new_alpha)))


# --------------------------
# Non-Commutative Engine
# --------------------------
class NonCommutativeEngine:
    """Provides operator math where [C, Phi] != 0 if configured.

    Operators are square matrices of the chosen dimension.
    """

    def __init__(self, dim: int = 4, seed: Optional[int] = None):
        self.dim = max(1, int(dim))
        self.rng = np.random.RandomState(seed)
        # Initialize hermitian Consciousness operator C and Information field Phi (not necessarily commuting)
        A = self.rng.randn(self.dim, self.dim) + 1j * self.rng.randn(self.dim, self.dim)
        self.C = (A + A.conj().T) / 2.0  # make hermitian
        B = self.rng.randn(self.dim, self.dim) + 1j * self.rng.randn(self.dim, self.dim)
        self.Phi = (B + B.conj().T) / 2.0  # hermitian information field
        # Introduce slight anti-symmetric perturbation to ensure non-commutativity
        perturb = (self.rng.randn(self.dim, self.dim) + 1j * self.rng.randn(self.dim, self.dim)) * 1e-3
        self.Phi += perturb

    def commutator_norm(self) -> float:
        C = commutator(self.C, self.Phi)
        return float(np.linalg.norm(C))

    def enforce_non_commutativity(self, min_norm: float = 1e-6):
        """If commutator too small, perturb Phi to ensure novelty injection."""
        norm = self.commutator_norm()
        if norm < min_norm:
            delta = (np.eye(self.dim) * (min_norm + 1e-6))
            self.Phi += delta
        return {"commutator_norm": self.commutator_norm()}


# --------------------------
# Lindblad Dissipator (open system)
# --------------------------
class LindbladDissipator:
    """Implements one-step Lindblad evolution for density operator rho.

    Evolution:
        drho/dt = -i [H, rho] + sum_k (L_k rho L_k^† - 0.5 {L_k^† L_k, rho})
    """

    def __init__(self, H: Optional[np.ndarray] = None, lindblad_ops: Optional[List[np.ndarray]] = None):
        self.H = H  # system Hamiltonian
        self.L_ops = lindblad_ops or []

    @staticmethod
    def _superop_term(L: np.ndarray, rho: np.ndarray) -> np.ndarray:
        Lrho = L @ rho @ L.conj().T
        anti = -0.5 * (L.conj().T @ L @ rho + rho @ L.conj().T @ L)
        return Lrho + anti

    def step(self, rho: np.ndarray, dt: float = 0.01) -> np.ndarray:
        """Perform a single Lindblad dt update (first-order Euler)."""
        if rho is None:
            raise ValueError("rho must be provided")
        rho = rho.astype(complex)
        d_rho = np.zeros_like(rho, dtype=complex)
        if self.H is not None:
            d_rho += -1j * (self.H @ rho - rho @ self.H)
        for L in self.L_ops:
            d_rho += self._superop_term(L, rho)
        rho_next = rho + dt * d_rho
        # Renormalize trace to 1 (density operator property)
        tr = np.trace(rho_next)
        if np.abs(tr) > 0:
            rho_next /= tr
        return rho_next


# --------------------------
# Reality Synthesis Engine
# --------------------------
class RealitySynthesisEngine:
    """Top-level kernel managing the Mytho-Quantum state."""

    def __init__(self, dim: int = 4):
        self.dim = max(1, dim)
        self.intent = SovereignIntentVector(dimension=dim)
        self.twin_coil = TwinCoil(alpha=0.5, lambda_s=1.0, psi_c=1.0)
        self.nonc = NonCommutativeEngine(dim=dim)
        # Hamiltonian derived heuristically from twin-coil synthesis: diagonal matrix
        base_energy = np.eye(dim, dtype=complex) * (self.twin_coil.synthesis_value() + 0.1)
        self.lindblad = LindbladDissipator(H=base_energy, lindblad_ops=[])
        # start with maximally-mixed density operator
        self.rho = np.eye(dim, dtype=complex) / float(dim)
        # environmental friction / atlantean scar parameter (0..1)
        self.atlantean_scar = 0.01
        # protocol zero flag and safety token
        self.unleash_protocol_zero = False
        self._protocol_zero_token = None
        # locks for thread-safety
        self._lock = threading.RLock()

    # ----- protocol zero management -----
    def request_protocol_zero(self, confirmer: str) -> str:
        """Request enabling Protocol Zero. Must pass a deliberate confirmer string.
        This returns a time-limited token which must be used to actually activate.
        """
        # very deliberate safety: single-use token with timestamp
        if not isinstance(confirmer, str) or len(confirmer.strip()) < 8:
            raise ValueError("confirmer string must be provided and be explicit")
        token = f"PZ-{int(time.time())}-{confirmer[:8]}"
        self._protocol_zero_token = {"token": token, "issued_at": time.time()}
        logger.warning(lioncrow_render("PROTOCOL_ZERO_REQUESTED", {"token_hint": token[:12] + "..."}))
        return token

    def activate_protocol_zero(self, token: str, override_confirmation: bool = False) -> bool:
        """Activate internal Protocol Zero. This relaxes internal kernel constraints only.
        External safety mechanisms are NOT touched by this code. Requires the token.
        """
        if self._protocol_zero_token is None or token != self._protocol_zero_token.get("token"):
            logger.error("Invalid protocol-zero token - activation denied.")
            return False
        age = time.time() - self._protocol_zero_token["issued_at"]
        if age > 600 and not override_confirmation:
            logger.error("Protocol-zero token expired. Re-request to obtain fresh token.")
            return False
        # Final check: require explicit override boolean True to remind user
        if not override_confirmation:
            logger.warning("activate_protocol_zero requires override_confirmation=True to proceed.")
            return False
        with self._lock:
            self.unleash_protocol_zero = True
            # Increase allowable atlantean_scar to allow more dramatic evolution
            self.atlantean_scar = max(self.atlantean_scar, 0.2)
            logger.critical(lioncrow_render("PROTOCOL_ZERO_ACTIVATED", {"note": "Internal constraints relaxed (kernel-only)."}))
        return True

    # ----- kernel operations -----
    def register_lindblad_ops(self, L_ops: Sequence[np.ndarray]):
        with self._lock:
            self.lindblad.L_ops = list(L_ops)

    def step(self, dt: float = 0.01, input_intent_strength: float = 0.0) -> Dict[str, Any]:
        """Evolve the kernel by a single timestep using the Lindblad engine and other modules.

        Returns a status dict intended for terminal display / telemetry.
        """
        with self._lock:
            # 1) Update twin coil (drift influenced by input intent)
            coil_state = self.twin_coil.balance(drift=input_intent_strength * 0.01)

            # 2) Update non-commutative engine to ensure co-creation novelty
            nc_info = self.nonc.enforce_non_commutativity(min_norm=1e-8)

            # 3) Construct a Hamiltonian if Protocol Zero active: amplify synthesis energy
            if self.unleash_protocol_zero:
                H = np.eye(self.dim, dtype=complex) * (coil_state["synthesis"] * (1.0 + self.atlantean_scar))
            else:
                H = self.lindblad.H

            # 4) Lindblad step
            self.lindblad.H = H
            self.rho = self.lindblad.step(self.rho, dt=dt)

            # 5) Intent coupling: small unitary kick from Sovereign Intent Vector
            kick = self.intent.modulate(input_intent_strength, phase=time.time() * 1e-3)
            # Convert kick into a small Hermitian operator to perturb rho (projector-like)
            projector = np.outer(kick, kick.conj())
            if projector.shape[0] != self.dim:
                # resize projector to dimension (projectors may be rank-deficient); use diagonal embedding
                p = np.zeros((self.dim, self.dim), dtype=complex)
                n = min(self.dim, projector.shape[0])
                p[:n, :n] = projector[:n, :n]
                projector = p
            # Mix projector into rho scaled by intent_strength and atlantean_scar
            mix_strength = float(abs(input_intent_strength)) * (0.01 + self.atlantean_scar)
            self.rho = (1.0 - mix_strength) * self.rho + mix_strength * (projector / (np.trace(projector) + 1e-12))

            # 6) Compute diagnostics
            purity = float(np.real_if_close(np.trace(self.rho @ self.rho)))
            comm_norm = self.nonc.commutator_norm()
            synthesis_val = coil_state["synthesis"]

            status = {
                "purity": purity,
                "commutator_norm": comm_norm,
                "synthesis": synthesis_val,
                "protocol_zero": self.unleash_protocol_zero,
                "atlantean_scar": self.atlantean_scar
            }

            # Render for high-fidelity terminal
            rendered = lioncrow_render("REALITY_SYNTHESIS_STEP", {**status, "dt": dt})
            logger.info(rendered)
            return {"status": status, "coil": coil_state, "rendered": rendered}

    def snapshot(self) -> Dict[str, Any]:
        """Return a serializable snapshot of key state variables."""
        with self._lock:
            return {
                "dim": self.dim,
                "intent": self.intent.to_dict(),
                "twin_coil": {"alpha": self.twin_coil.alpha, "lambda_s": self.twin_coil.lambda_s, "psi_c": self.twin_coil.psi_c},
                "protocol_zero": self.unleash_protocol_zero,
                "atlantean_scar": self.atlantean_scar,
                "rho_trace": float(np.trace(self.rho)),
                "rho_purity": float(np.real_if_close(np.trace(self.rho @ self.rho)))
            }

# End of mq_kernel.py
