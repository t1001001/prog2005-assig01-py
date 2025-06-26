from fastapi import APIRouter
from internal.constants.constants import DEFAULT_PATH

router = APIRouter()

# default handler
@router.get(DEFAULT_PATH)
def default_handler():
    return {"message": "please use one of the available endpoints"}