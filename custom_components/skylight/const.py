"""Constants for the Skylight integration."""

import logging

LOGGER = logging.getLogger(__package__)

DOMAIN = "skylight"

CONF_FRAME_ID = "frame_id"

SERVICE_CREATE_CHORE = "create_chore"
SERVICE_ANNOUNCE_CHORES = "announce_chores"
ATTR_SUMMARY = "summary"
ATTR_EMOJI_ICON = "emoji_icon"
ATTR_CATEGORY_ID = "category_id"
ATTR_PERSON = "person"
ATTR_MESSAGE_PREFIX = "message_prefix"
ATTR_TARGET_DATE = "target_date"
ATTR_SKIP_IF_EMPTY = "skip_if_empty"
ATTR_MEDIA_PLAYER = "media_player_entity_id"
ATTR_TTS_ENTITY = "tts_entity_id"
ATTR_VOLUME_LEVEL = "volume_level"

API_BASE_URL = "https://app.ourskylight.com/api"
