import time
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from template_package.utils.api_utils import patch_fastapi

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None) -> dict:
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item) -> dict:
    return {"item_name": item.name, "item_id": item_id}


@app.get("/ext-call")
def ext_call() -> dict:
    return slow_call_to_external_url()


def slow_call_to_external_url() -> dict:
    print("Slow call started")
    time.sleep(10)
    return {"duration": 10}


# Patch Fastapi to allow relative path resolution.
patch_fastapi(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host="0.0.0.0", port=8081, log_level="info"
    )  # cannot use reload=True anymore
