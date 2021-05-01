"""Support for Lobe classification on images."""
from datetime import timedelta
import logging
import base64
import requests

import voluptuous as vol

from homeassistant.components.image_processing import (
    CONF_ENTITY_ID,
    CONF_NAME,
    PLATFORM_SCHEMA,
    ImageProcessingEntity,
)
from homeassistant.core import split_entity_id
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

ATTR_MATCHES = "matches"
CONF_SERVER = "server"
SCAN_INTERVAL = timedelta(seconds=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ENTITY_ID): cv.entity_id,
        vol.Required(CONF_SERVER): cv.string,
        vol.Optional(CONF_NAME): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Lobe image processing platform."""
    add_entities(
        [
            LobeImageProcessor(
                hass, config[CONF_ENTITY_ID], config.get(CONF_NAME), config[CONF_SERVER]
            )
        ]
    )


class LobeImageProcessor(ImageProcessingEntity):
    """Representation of an Lobe image processor."""

    def __init__(self, hass, camera_entity, name, server):
        """Initialize the Lobe entity."""
        self.hass = hass
        self._camera_entity = camera_entity
        if name:
            self._name = name
        else:
            self._name = f"Lobe {split_entity_id(camera_entity)[1]}"
        self._server = server
        self._result = ""
        self._matches = []

    @property
    def camera_entity(self):
        """Return camera entity id from process pictures."""
        return self._camera_entity

    @property
    def name(self):
        """Return the name of the image processor."""
        return self._name

    @property
    def state(self):
        """Return the state of the entity."""
        return self._result

    @property
    def extra_state_attributes(self):
        """Return device specific state attributes."""
        return {ATTR_MATCHES: self._matches}

    def process_image(self, image):
        encoded_image = base64.b64encode(image)
        try:
            response = requests.post(
                self._server + "/predict", json={"image": encoded_image}
            )
            response.raise_for_status()
            response = response.json()
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.models.complexjson.decoder.JSONDecodeError,
        ) as exception:
            _LOGGER.warning("Could not connect to prediction server due to %s", exception)
            return
        self._result = response["Prediction"]
        self._matches = {}
        for label, confidence in response["Labels"]:
            self._matches[label] = round(confidence * 100, 2)
