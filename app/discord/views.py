from typing import Dict
from nacl.exceptions import BadSignatureError

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from sqlalchemy.orm import Session
from starlette import status

from app.database.core import get_db
from app.discord import utils


discord_router = APIRouter()


@discord_router.post("/interactions", response_model=Dict, status_code=status.HTTP_200_OK)
async def handle_interaction(request: Request, db: Session = Depends(get_db)):
    """Handle discord interaction."""
    print("[+] Discord interaction occurred")
    try:
        body = await request.body()
        utils.verify_request(headers=request.headers, body=body.decode('utf-8'))

        data = await request.json()
        request_type = data["type"]

        if request_type == 1:
            return {
            "type": 1
            }
        else:
            return utils.route_slash_commands(body=data, db=db)

    except BadSignatureError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
