import math
import random
import time
from dataclasses import dataclass, astuple
from typing import Optional

from comet.emulator import IEC60488Emulator, message, run
from comet.emulator.utils import Error


@dataclass
class Correction:
    open_val: int = 0
    short_val: int = 0
    load_val: int = 0


class K4215CVUEmulator(IEC60488Emulator):
    IDENTITY: str = "KEITHLEY INSTRUMENTS,KI4200A,1489223,V1.14 (Emulator)"

    MODEL_MAP = {
        "ZTHETA": 0,
        "RPLUSJX": 1,
        "CPRP": 2,
        "CPGP": 2,  # alias: some stacks treat CPRP/CPGP similarly
        "CSRS": 3,
        "CPD": 4,
        "CSD": 5,
        "YTHETA": 7,
    }
    MODEL_MAP_INV = {v: k for k, v in MODEL_MAP.items()}

    def __init__(self) -> None:
        super().__init__()
        self.error_queue: list[Error] = []

        # Core state
        self.cvu_mode: int = 0  # 0=user mode
        self.cvu_output: bool = False

        self.config_acvhi: int = 1
        self.config_dcvhi: int = 1

        # AC Zero (auto-zero?) range
        self.cvu_acz_range: float = 0.0

        # Corrections
        self.cvu_correction: Correction = Correction(0, 0, 0)
        self.cvu_length_m: float = 0.0  # cable length correction (0, 1.5, 3.0)

        # Stimulus/config
        self.acv: float = 0.1  # Volts (10mV .. 1V typical)
        self.freq_hz: int = 100000  # 1kHz .. 10MHz typical
        self.dcv: float = 0.0  # -30 .. +30
        self.dcv_offset: float = 0.0  # -30 .. +30

        # Speed/aperture
        # speed_mode: 0..3 are common on instruments (we allow 0..3)
        self.speed_mode: int = 3
        self.delay_factor: float = 1.0
        self.filter_factor: float = 1.0
        self.aperture_plc: float = 0.1

        # Display / results model
        self.model_code: int = self.MODEL_MAP["RPLUSJX"]

        # For drift / reproducibility
        self._t0 = time.time()
        self._seed = random.random() * 1e6

    def _push_error(self, code: int, msg: str) -> None:
        self.error_queue.append(Error(code, msg))

    def _parse_float(self, s: str) -> Optional[float]:
        try:
            return float(s)
        except Exception:
            self._push_error(-104, "Data type error")
            return None

    def _parse_int(self, s: str) -> Optional[int]:
        try:
            return int(s)
        except Exception:
            self._push_error(-104, "Data type error")
            return None

    def _clamp(self, x: float, lo: float, hi: float) -> float:
        return lo if x < lo else hi if x > hi else x

    def _noise(self, scale: float) -> float:
        # scale is approximate RMS-ish; keep it simple
        return random.gauss(0.0, scale)

    def _drift(self) -> float:
        # slow bounded drift in [-1, 1] scaled later
        t = time.time() - self._t0
        return math.sin(2 * math.pi * (t / 90.0) + self._seed)

    def _effective_bias(self) -> float:
        return self.dcv + self.dcv_offset

    @message(r'^\*IDN\?$')
    def get_idn(self) -> str:
        return self.IDENTITY

    @message(r'^\*RST$')
    def set_rst(self) -> None:
        self.error_queue.clear()

        self.cvu_mode = 0
        self.cvu_output = False

        self.cvu_acz_range = 0.0

        self.cvu_correction = Correction(0, 0, 0)
        self.cvu_length_m = 0.0

        self.acv = 0.1
        self.freq_hz = 100000
        self.dcv = 0.0
        self.dcv_offset = 0.0

        self.speed_mode = 3
        self.delay_factor = 1.0
        self.filter_factor = 1.0
        self.aperture_plc = 0.1

        self.model_code = self.MODEL_MAP["RPLUSJX"]

        self.config_acvhi = 1
        self.config_dcvhi = 1

        # keep drift seed but reset time reference
        self._t0 = time.time()

    @message(r'^\*CLS$')
    def set_cls(self) -> None:
        self.error_queue.clear()

    @message(r"^BC\s*$")
    def set_buffer_clear(self) -> None:
        ...

    @message(r'^:?ERROR:LAST:GET$')
    def get_last_error(self) -> str:
        if self.error_queue:
            error = self.error_queue[-1]
        else:
            error = Error(0, "No error")
        return f'{error.code}, "{error.message}"'

    @message(r'^:?ERROR:LAST:CLEAR$')
    def clear_last_error(self) -> None:
        if self.error_queue:
            self.error_queue.pop()

    @message(r'^:CVU:MODE\s(\d+)$')
    def set_mode(self, mode: str) -> None:
        m = self._parse_int(mode)
        if m is None:
            return
        # allow 0..3 for safety
        if not (0 <= m <= 3):
            self._push_error(-222, "Data out of range")
            return
        self.cvu_mode = m

    @message(r'^:CVU:MODE\?$')
    def get_mode(self) -> str:
        return str(self.cvu_mode)

    @message(r"^:CVU:CONFIG:ACVHI\s(1|2)$")
    def set_config_acvhi(self, val: str) -> None:
        self.config_acvhi = int(val)

    @message(r"^:CVU:CONFIG:ACVHI\?$")
    def get_config_acvhi(self) -> str:
        return str(self.config_acvhi)

    @message(r"^:CVU:CONFIG:DCVHI\s(1|2)$")
    def set_config_dcvhi(self, val: str) -> None:
        self.config_dcvhi = int(val)

    @message(r"^:CVU:CONFIG:DCVHI\?$")
    def get_config_dcvhi(self) -> str:
        return str(self.config_dcvhi)

    @message(r"^:CVU:ACZ:RANGE\s(.+)$")
    def set_acz_range(self, level: str) -> None:
        v = self._parse_float(level)
        if v is None:
            return
        if v < 0:
            self._push_error(-222, "Data out of range")
            return
        self.cvu_acz_range = v

    @message(r"^:CVU:ACZ:RANGE\?$")
    def get_acz_range(self) -> str:
        return f"{self.cvu_acz_range:g}"

    @message(r"^:CVU:OUTPUT\s(0|1)$")
    def set_cvu_output(self, state: str) -> None:
        self.cvu_output = bool(int(state))

    @message(r"^:CVU:OUTPUT\?$")
    def get_cvu_output(self) -> str:
        return "1" if self.cvu_output else "0"

    @message(r"^:CVU:CORRECT\s(0|1),(0|1),(0|1)$")
    def set_correction(self, open_val: str, short_val: str, load_val: str) -> None:
        self.cvu_correction = Correction(int(open_val), int(short_val), int(load_val))

    @message(r"^:CVU:CORRECT\?$")
    def get_correction(self) -> str:
        open_val, short_val, load_val = astuple(self.cvu_correction)
        return f"{open_val},{short_val},{load_val}"

    @message(r"^:CVU:LENGTH\s(.+)$")
    def set_length(self, length_m: str) -> None:
        v = self._parse_float(length_m)
        if v is None:
            return
        # allow only 0, 1.5, 3.0
        allowed = (0.0, 1.5, 3.0)
        # accept small rounding errors
        if min(abs(v - a) for a in allowed) > 1e-6:
            self._push_error(-222, "Data out of range")
            return
        self.cvu_length_m = v

    @message(r"^:CVU:LENGTH\?$")
    def get_length(self) -> str:
        # keep one decimal like typical instruments
        return f"{self.cvu_length_m:.1f}"

    @message(r"^:CVU:ACV\s(.+)$")
    def set_acv(self, voltage: str) -> None:
        v = self._parse_float(voltage)
        if v is None:
            return
        if not (0.01 <= v <= 1.0):
            self._push_error(-222, "Data out of range")
            return
        self.acv = v

    @message(r"^:CVU:ACV\?$")
    def get_acv(self) -> str:
        return f"{self.acv:.6E}"

    @message(r"^:CVU:FREQ\s(.+)$")
    def set_freq(self, frequency: str) -> None:
        v = self._parse_float(frequency)
        if v is None:
            return
        if not (1e3 <= v <= 1e7):
            self._push_error(-222, "Data out of range")
            return
        self.freq_hz = int(round(v))

    @message(r"^:CVU:FREQ\?$")
    def get_freq(self) -> str:
        return str(self.freq_hz)

    @message(r"^:CVU:DCV\s(.+)$")
    def set_dcv(self, level: str) -> None:
        v = self._parse_float(level)
        if v is None:
            return
        if not (-30.0 <= v <= 30.0):
            self._push_error(-222, "Data out of range")
            return
        self.dcv = v

    @message(r"^:CVU:DCV\?$")
    def get_dcv(self) -> str:
        return f"{self.dcv:.3E}"

    @message(r"^:CVU:DCV:OFFSET\s(.+)$")
    def set_dcv_offset(self, offset: str) -> None:
        v = self._parse_float(offset)
        if v is None:
            return
        if not (-30.0 <= v <= 30.0):
            self._push_error(-222, "Data out of range")
            return
        self.dcv_offset = v

    @message(r"^:CVU:DCV:OFFSET\?$")
    def get_dcv_offset(self) -> str:
        return f"{self.dcv_offset:.3E}"

    @message(r"^:CVU:SPEED\s(\d+),(.+),(.+),(.+)$")
    def set_speed(self, mode: str, delay_factor: str, filter_factor: str, aperture: str) -> None:
        m = self._parse_int(mode)
        d = self._parse_float(delay_factor)
        f = self._parse_float(filter_factor)
        a = self._parse_float(aperture)
        if m is None or d is None or f is None or a is None:
            return

        if not (0 <= m <= 3):
            self._push_error(-222, "Data out of range")
            return
        if not (0.0 <= d <= 100.0):
            self._push_error(-222, "Data out of range")
            return
        if not (0.0 <= f <= 707.0):
            self._push_error(-222, "Data out of range")
            return
        if not (0.006 <= a <= 10.002):
            self._push_error(-222, "Data out of range")
            return

        self.speed_mode = m
        self.delay_factor = d
        self.filter_factor = f
        self.aperture_plc = a

    @message(r"^:CVU:SPEED\?$")
    def get_speed(self) -> str:
        # Keep scientific formatting like typical SCPI
        return f"{self.speed_mode},{self.delay_factor:.3E},{self.filter_factor:.3E},{self.aperture_plc:.3E}"

    @message(r"^:CVU:MODEL\s(.+)$")
    def set_model(self, model: str) -> None:
        token = model.strip().upper()
        if token in self.MODEL_MAP:
            self.model_code = self.MODEL_MAP[token]
            return

        code = self._parse_int(token)
        if code is None:
            return
        if code not in self.MODEL_MAP_INV:
            self._push_error(-222, "Data out of range")
            return
        self.model_code = code

    @message(r"^:CVU:MODEL\?$")
    def get_model(self) -> str:
        # return numeric code like many instruments do
        return str(self.model_code)

    @message(r"^:CVU:MEASZ\?$")
    def get_measz(self) -> str:
        """
        Return two comma-separated values.
        We emulate a DUT that looks like a capacitor with loss and bias dependence.

        If output is OFF -> near-zero / noisy baseline (many instruments do something like that).
        """
        # If output off, return something close to zeros with a bit of noise
        if not self.cvu_output:
            v1 = self._noise(1e-6)
            v2 = self._noise(1e-6)
            return f"{v1:.6E},{v2:.6E}"

        f = float(self.freq_hz)
        w = 2.0 * math.pi * f

        # Emulated DUT parameters
        # Base capacitance ~ 100 pF, mild frequency dependence + bias dependence
        bias = self._effective_bias()
        c0 = 100e-12
        c_bias = c0 * (1.0 + 0.002 * self._clamp(bias, -30.0, 30.0))  # ~ +/-6% across range
        c_freq = c_bias * (1.0 - 0.01 * math.log10(max(f, 1.0) / 1e5))  # slight slope vs freq

        # Loss tangent / dissipation factor (small)
        d0 = 0.01 + 0.002 * abs(bias) / 30.0  # 0.01..~0.012
        # ESR model (derived-ish)
        # For a capacitor: D ≈ ESR * w * C
        esr = d0 / max(w * c_freq, 1e-30)

        # A tiny series inductance to make impedance less “perfect”
        l_series = 5e-9 + 1e-9 * (self.cvu_length_m / 3.0)

        # AC amplitude affects noise a bit
        noise_scale = 1e-3 * (0.2 / max(self.acv, 1e-3))
        noise_scale = self._clamp(noise_scale, 1e-6, 5e-3)

        # Compute impedance of (ESR + j*w*L + 1/(j*w*C)) series
        # Zc = 1/(j*w*C) = -j/(w*C)
        x_c = -1.0 / max(w * c_freq, 1e-30)
        x_l = w * l_series
        r = esr
        x = x_l + x_c

        # Add some noise + drift
        r_meas = r * (1.0 + 0.01 * self._drift()) + self._noise(abs(r) * 0.02 + noise_scale)
        x_meas = x * (1.0 + 0.01 * self._drift()) + self._noise(abs(x) * 0.02 + noise_scale)

        # Apply "corrections" in a naive way:
        # if open/short/load enabled, reduce systematic error a bit.
        open_val, short_val, load_val = astuple(self.cvu_correction)
        corr_strength = 1.0 - 0.03 * (open_val + short_val + load_val)  # up to ~9% improvement
        r_meas *= corr_strength
        x_meas *= corr_strength

        model = self.model_code

        # Produce two values depending on model
        # All return as "<a>,<b>" in scientific notation.
        if model == self.MODEL_MAP["RPLUSJX"]:
            a, b = r_meas, x_meas

        elif model == self.MODEL_MAP["ZTHETA"]:
            z = math.hypot(r_meas, x_meas)
            theta = math.degrees(math.atan2(x_meas, r_meas))
            a, b = z, theta

        elif model in (self.MODEL_MAP["CPRP"], self.MODEL_MAP["CPGP"]):
            # Parallel capacitance / parallel resistance approximation:
            # From admittance Y = 1/Z = G + jB, C_p = B / w, R_p = 1/G
            denom = (r_meas * r_meas + x_meas * x_meas)
            g = r_meas / max(denom, 1e-30)
            b = -x_meas / max(denom, 1e-30)
            c_p = b / max(w, 1e-30)
            r_p = 1.0 / max(g, 1e-30)
            a, b = c_p, r_p

        elif model == self.MODEL_MAP["CSRS"]:
            # Series capacitance / series resistance
            # C_s ≈ -1/(w*X) when X is capacitive (negative)
            c_s = -1.0 / max(w * x_meas, -1e-30) if x_meas < 0 else 0.0
            a, b = c_s, r_meas

        elif model == self.MODEL_MAP["CPD"]:
            # Cp, D  (D ~ ESR*w*C for series -> rough; for parallel, D ~ G/B)
            denom = (r_meas * r_meas + x_meas * x_meas)
            g = r_meas / max(denom, 1e-30)
            bb = -x_meas / max(denom, 1e-30)
            c_p = bb / max(w, 1e-30)
            d = g / max(bb, 1e-30) if bb != 0 else 0.0
            a, b = c_p, d

        elif model == self.MODEL_MAP["CSD"]:
            # Cs, D
            c_s = -1.0 / max(w * x_meas, -1e-30) if x_meas < 0 else 0.0
            d = abs(r_meas * w * c_s) if c_s != 0 else 0.0
            a, b = c_s, d

        elif model == self.MODEL_MAP["YTHETA"]:
            # Y magnitude and phase (degrees)
            denom = (r_meas * r_meas + x_meas * x_meas)
            g = r_meas / max(denom, 1e-30)
            bb = -x_meas / max(denom, 1e-30)
            y = math.hypot(g, bb)
            theta = math.degrees(math.atan2(bb, g))
            a, b = y, theta

        else:
            # Unknown model code -> instrument might error; we'll return something sane + error
            self._push_error(-222, "Data out of range")
            a, b = r_meas, x_meas

        return f"{a:.6E},{b:.6E}"

    @message(r'^(.*)$')
    def unknown_message(self, request: str) -> None:
        # ignore empty lines quietly
        if request.strip() == "":
            return
        self._push_error(-113, "Undefined header")


if __name__ == "__main__":
    run(K4215CVUEmulator())
