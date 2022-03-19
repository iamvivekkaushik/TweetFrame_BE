from typing import Dict
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from sqlalchemy.orm import Session

from starlette.datastructures import Headers
from app import config
from app.discord import helper
from app.user.repository import UserRepository


def verify_request(body: str, headers: Headers):
    """Verify the request."""
    signature = headers.get('X-Signature-Ed25519')
    timestamp = headers.get('X-Signature-Timestamp')

    if not signature or not timestamp:
        raise BadSignatureError('Missing signature or timestamp')

    PUBLIC_KEY = config.DISCORD_PUBLIC_KEY
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))


def route_slash_commands(body: Dict, db: Session):
    """Route slash commands."""
    data = body["data"]
    slash_command = data["name"]
    response = {}

    if slash_command == 'stats':
        # Return some superframes stats
        sub_command = data['options'][0]['name']

        if sub_command == 'users':
            response = helper.handle_user_stat_command(db)
        elif sub_command == 'frame_usage':
            response = helper.handle_frame_stat_command(db)
    
    return response
