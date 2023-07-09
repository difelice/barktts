"""Support for the BarkTTS speech service."""
import asyncio
import base64
import json
import logging
import random

import aiohttp
import async_timeout
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider
from homeassistant.const import CONF_URL, CONTENT_TYPE_JSON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

ANNOUNCER = "announcer"
SUPPORT_LANGUAGES = [
    ANNOUNCER,
    "de",  # German
    "en",  # English
    "es",  # Spanish
    "fr",  # French
    "hi",  # Hindi
    "it",  # Italian
    "ja",  # Japanese
    "ko",  # Korean
    "pl",  # Polish
    "ru",  # Russian
    "tr",  # Turkish
    "zh",  # Chinese
]

DEFAULT_LANG = ANNOUNCER
DEFAULT_URL = "http://localhost:5000/predictions"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORT_LANGUAGES),
        vol.Optional(CONF_URL, default=DEFAULT_URL): cv.string,
    }
)

TIMEOUT = 300

_LOGGER = logging.getLogger(__name__)


def get_engine(hass: HomeAssistant, config, discovery_info):
    """Return Bark Engine instance"""
    return BarkProvider(hass, config[CONF_LANG], config[CONF_URL])


class BarkProvider(Provider):
    """Class decorator for Bark provider"""

    def __init__(self, hass: HomeAssistant, lang, url) -> None:
        self._hass = hass
        self._lang = lang
        self._url = url
        self.name = "BarkTTS"

    @property
    def default_language(self) -> str:
        """The default language"""
        return self._lang

    @property
    def supported_languages(self):
        """Returns a list of supported languages"""
        return SUPPORT_LANGUAGES

    async def async_get_tts_audio(self, message, language, options=None):
        """Send a BarkTTS command to request a BarkTTS audio message"""
        websession = async_get_clientsession(self._hass)

        try:
            with async_timeout.timeout(TIMEOUT):
                url = f"{self._url}"

                history_prompt = DEFAULT_LANG

                if language in SUPPORT_LANGUAGES:
                    if language != ANNOUNCER:
                        history_prompt = f"{language}_speaker_{random.randint(0, 4)}"
                else:
                    _LOGGER.warning("Unsupported language '%s'", language)

                data = {
                    "input": {"prompt": message, "history_prompt": history_prompt},
                }

                headers = {"Content-Type": CONTENT_TYPE_JSON}

                response = await websession.post(
                    url, data=json.dumps(data), headers=headers
                )

                if not response.ok:
                    _LOGGER.error(
                        "Error %d on load url %s", response.status, response.url
                    )
                    return (None, None)

                response_json = await response.json()

                [_, encoded] = (
                    response_json.get("output")
                    .get("audio_out")
                    .split("data:audio/x-wav;base64,")
                )
                data = base64.b64decode(encoded)

        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Timeout for BarkTTS API")
            return (None, None)

        if data:
            return ("wav", data)
        return (None, None)
