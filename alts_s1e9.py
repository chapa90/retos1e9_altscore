from fastapi import FastAPI, Query
from typing import Dict

app = FastAPI()

# Datos de referencia (presión en MPa y volúmenes específicos en m³/kg)
SATURATION_DATA = {
    1: (0.001043, 1.694),
    5: (0.001012, 0.3153),
    10: (0.000942, 0.1914),
    15: (0.000885, 0.1318),
    20: (0.000843, 0.1002),
    25: (0.000808, 0.08079),
}

@app.get("/phase-change-diagram")
def get_phase_change_data(pressure: float = Query(..., description="Pressure in MPa")) -> Dict[str, float]:
    """Returns specific volume for liquid and vapor at given pressure."""
    if pressure in SATURATION_DATA:
        specific_volume_liquid, specific_volume_vapor = SATURATION_DATA[pressure]
    else:
        # Interpolación lineal en caso de presiones intermedias
        sorted_pressures = sorted(SATURATION_DATA.keys())
        for i in range(len(sorted_pressures) - 1):
            p1, p2 = sorted_pressures[i], sorted_pressures[i + 1]
            if p1 < pressure < p2:
                v1_l, v1_v = SATURATION_DATA[p1]
                v2_l, v2_v = SATURATION_DATA[p2]
                factor = (pressure - p1) / (p2 - p1)
                specific_volume_liquid = v1_l + factor * (v2_l - v1_l)
                specific_volume_vapor = v1_v + factor * (v2_v - v1_v)
                break
        else:
            return {"error": "Pressure out of range"}

    return {
        "specific_volume_liquid": specific_volume_liquid,
        "specific_volume_vapor": specific_volume_vapor
    }
