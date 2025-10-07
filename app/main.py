from typing import List, Dict, Any, cast

from fastapi import FastAPI, HTTPException

from .optimizer import InsufficientCapacityError, PowerPlantOptimizer, WindTurbine, ThermalPlant
from .schemas import Payload
from .parsers import parse_payload


app = FastAPI()


def format_solution(used_plants: List[ThermalPlant | WindTurbine]) -> List[Dict[str, Any]]:
    return [{"name": p.name, "p": round(cast(float, p.p), 1)} for p in used_plants]


@app.post("/productionplan")
async def production_plan(payload: Payload) -> List[Dict[str, Any]]:
    optimizer = PowerPlantOptimizer(*parse_payload(payload))
    try:
        used_plants = optimizer.optimize()
        return format_solution(used_plants)
    except InsufficientCapacityError:
        raise HTTPException(status_code=400, detail="Insufficient capacity to meet load")
