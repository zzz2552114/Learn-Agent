from typing import Any
Tools : list[dict[str,Any]] = []

def Toolregister(func):
    name = func.__module__.rsplit('.',1)[-1]
    description = func.__doc__ or "No description"
    Tools.append({
        "name" : name,
        "description" : description,
        "func" : func
    })
    return func

from . import serp_search
from . import tavily_search
