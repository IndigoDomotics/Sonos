import urllib.parse
import datetime  # ✅ Needed for fallback print timestamp
import io
import sys
import os
from os import listdir
import copy
import json
import time
import html
import shutil
import logging
import threading
import http.server
import socketserver
import platform
import socket
import traceback
import ipaddress
import inspect
import base64
import ifaddr
import re
import requests
import http.server as BaseHTTPServer
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from xml.etree import ElementTree as ET
import xml.sax.saxutils as saxutils
from urllib import request, parse
from urllib.parse import urlparse

from AppKit import NSSpeechSynthesizer  # noqa
from AppKit import NSURL  # noqa

from PIL import Image
import io

try:
    import indigo
except ImportError:
    pass

import soco
import soco.core
import soco.events
import soco.config
from soco.core import SoCo
from soco import SoCo as SoCoDevice
from soco.events import event_listener
soco.config.EVENTS_MODULE = soco.events
logging.getLogger("Plugin.Sonos").info(
    f"🧪 The SoCo version used in this plugin was loaded from: {soco.__file__}"
)

try:
    from twisted.internet import reactor
    from twisted.internet.protocol import DatagramProtocol
    from twisted.application.internet import MulticastServer
except ImportError:
    pass

try:
    from gtts import gTTS
except ImportError:
    pass

try:
    import pyvona
except ImportError:
    pass

try:
    import boto3
except ImportError:
    pass

try:
    from mutagen.mp3 import MP3
    from mutagen.aiff import AIFF
    from mutagen.wave import WAVE
except ImportError:
    pass

try:
    from pandora import Pandora
except ImportError:
    pass

# mini_http_server.py
import http.server
import socketserver


from XMhelper import SiriusXM
from sxm import SXMClient, RegionChoice, XMChannel
import language_codes
from constants import PLUGIN_INFO, PLUGIN_VERSION

print(f"Using SoCo event listener class: {type(event_listener).__name__}")

SONOS_ZonePlayer = 0
SONOS_CONNECT = 1
SONOS_CONNECTAMP = 2
SONOS_PLAY1 = 3
SONOS_PLAY3 = 4
SONOS_PLAY5 = 5
SONOS_PLAYBAR = 6
SONOS_SUB = 7
SONOS_PLAYBASE = 8
SONOS_BEAM = 9
SONOS_ERA100 = 10
SONOS_ERA300 = 11

ZP_LIST = []
Sonos_Favorites = []
Sonos_Playlists = []
Sonos_RT_Fav_Stations = []
Sonos_Pandora = []
Sonos_SiriusXM = []
SavedState = []
Sound_Files = []
ContainerUpdateID_SQ = 0
actionBusy = 0





UPNP_ERRORS = {
    '400': 'Bad Request',
    '401': 'Invalid Action',
    '402': 'Invalid Args',
    '404': 'Invalid Var',
    '412': 'Precondition Failed',
    '501': 'Action Failed',
    '600': 'Argument Value Invalid',
    '601': 'Argument Value Out of Range',
    '602': 'Optional Action Not Implemented',
    '603': 'Out of Memory',
    '604': 'Human Invtervention Required',
    '605': 'String Argument Too Long',
    '606': 'Action Not Authorized',
    '607': 'Signature Failure',
    '608': 'Signature Missing',
    '609': 'Not Encrypted',
    '610': 'Invalid Sequence',
    '611': 'Invalid Control URL',
    '612': 'No Such Session',
    '701': 'No Such Object',
    '702': 'Invalid CurrentTagValue',
    '703': 'Invalid NewTagValue',
    '704': 'RequiredTag',
    '705': 'Read Only Tag',
    '706': 'Parameter Mismatch',
    '708': 'Unsupported or Invalid Search Criteria',
    '709': 'Unsupported or Invalid Sort Criteria',
    '710': 'No Such Container',
    '711': 'Restricted Object',
    '712': 'Bad Metadata',
    '713': 'Restricted Parent Object',
    '714': 'No Such Source Resource',
    '715': 'Resource Access Denied',
    '716': 'Transfer Busy',
    '717': 'No Such File Transfer',
    '718': 'No Such Destination Resource',
    '719': 'Destination Resource Access Denied',
    '720': 'Cannot Process the Request',
    '800': 'Unable to Play the Selected Item',
    '804': 'Invalid Queue Request'
}

uri_tv = "x-sonos-htastream:"
uri_music = "x-rincon-queue:"
uri_radio = "x-sonosapi-stream:"
uri_sonos_radio = "x-sonosapi-radio:"
uri_sonos_http = "x-sonosapi-http:"
uri_pandora = "pndrradio:"
uri_siriusxm = "x-sonosapi-hls:"
uri_spotify = "x-sonos-spotify:"
uri_jffs = "file:"
uri_file = "x-file-cifs"
uri_group = "x-rincon:"
uri_playlist = "x-rincon-playlist:"
uri_mp3radio = "x-rincon-mp3radio:"
uri_container = "x-rincon-cpcontainer"

ZoneGroupStates = {
    'ZP_ALBUM', 'ZP_ARTIST', 'ZP_SOURCE', 'ZP_MUTE','ZP_CREATOR', 'ZP_TRACK', 'ZP_NALBUM',
    'ZP_NART', 'ZP_NARTIST', 'ZP_NCREATOR', 'ZP_NTRACK', 'ZP_CurrentTrack',
    'ZP_CurrentTrackURI', 'ZP_DURATION', 'ZP_RELATIVE', 'ZP_INFO',
    'ZP_STATION', 'ZP_STATE'
}

IVONAlanguages = {
    'en-US': 'English, American',
    'en-AU': 'English, Australian',
    'en-GB': 'English, British',
    'en-IN': 'English, Indian',
    'en-GB-WLS': 'English, Welsh',
    'cy-GB': 'Welsh',
    'da-DK': 'Danish',
    'nl-NL': 'Dutch',
    'fr-FR': 'French',
    'fr-CA': 'French, Canadian',
    'de-DE': 'German',
    'is-IS': 'Icelandic',
    'it-IT': 'Italian',
    'pl-PL': 'Polish',
    'pt-PT': 'Portuguese',
    'pt-BR': 'Portuguese, Brazilian',
    'ro-RO': 'Romanian',
    'ru-RU': 'Russian',
    'es-ES': 'Spanish, Castilian',
    'es-US': 'Spanish, American',
    'sv-SE': 'Swedish',
    'tr-TR': 'Turkish',
    'nb-NO': 'Norwegian'
}

IVONAVoices = []
PollyVoices = []
NSVoices = []


class Old_save_PA():
    def __init__(self, deviceId=None, props=None):
        self.deviceId = deviceId
        self.props = props


# Safe PluginAction helper (drop-in replacement)
class _VolumeOnlySnap(object):
    """Minimal announcement snapshot for players whose full soco Snapshot fails.

    Right after grouping churn a player can report its own queue URI while
    soco's topology still calls it a slave — the stock Snapshot then dies on
    coordinator-only properties (cross_fade). Mirror what soco restores for
    slaves anyway: volume and mute only.
    """
    media_uri = ""

    def __init__(self, soco_device):
        self.device = soco_device
        self.volume = soco_device.volume
        self.mute = soco_device.mute

    def restore(self, fade=False):
        self.device.volume = self.volume
        self.device.mute = self.mute


class PA(object):
    def __init__(self, deviceId=None, props=None):
        # Always store deviceId as int when possible
        try:
            self.deviceId = int(deviceId) if deviceId is not None else 0
        except Exception:
            self.deviceId = deviceId  # fallback

        # Normalize props to a dict-like object
        norm = {}
        if isinstance(props, dict):
            norm = dict(props)  # shallow copy
        elif props is None:
            norm = {}
        else:
            # last-ditch: try to coerce to dict
            try:
                norm = dict(props)
            except Exception:
                norm = {}

        # Coerce 'setting' to str if present (prevents .split on int, etc.)
        if "setting" in norm and not isinstance(norm["setting"], str):
            try:
                norm["setting"] = str(norm["setting"])
            except Exception:
                norm["setting"] = ""

        # Prefer Indigo's Dict if available so .get() behaves like elsewhere
        try:
            d = indigo.Dict()
            for k, v in norm.items():
                d[k] = v
            self.props = d
        except Exception:
            self.props = norm




class SonosPlugin(object):

    ############################################################################################
    ### Initialize the SonosPlugin
    ############################################################################################

    # Define the class-level attribute
    #DEFAULT_ARTWORK_PATH = '/Library/Application Support/Perceptive Automation/images/Sonos/'
    DEFAULT_ARTWORK_PATH = '/Library/Application Support/Perceptive Automation/images/Sonos/default_artwork copy.jpg'

    def __init__(self, plugin, pluginPrefs):
        import uuid
        import os
        import json
        import logging
        import threading
        from sxm import SXMClient, RegionChoice, XMChannel

        # -------------------------------------------------------------------------
        # Basic Indigo/plugin wiring
        # -------------------------------------------------------------------------
        self.plugin = plugin
        self.pluginPrefs = pluginPrefs
        self.logger = logging.getLogger("Plugin.Sonos")
        self.logger.info(f"Initializing SonosPlugin... [{uuid.uuid4()}]")

        # ✅ DO NOT alias Indigo devices (read-only) into self.devices.
        #    Keep self.devices as a writable plugin-local cache, and (optionally)
        #    keep a separate read-only handle to Indigo’s DeviceList.
        try:
            import indigo
            self.indigo_devices = indigo.devices   # read-only DeviceList
        except Exception:
            self.indigo_devices = None
        self.devices = {}  # plugin-local dict you can assign into

        # -------------------------------------------------------------------------
        # Core locks & caches — initialize ONCE (no reassignments later)
        # -------------------------------------------------------------------------
        self.last_zone_group_state_hash = None
        self.zone_group_state_lock = threading.Lock()

        self.soco_by_ip = {}
        self.ip_to_indigo_device = {}
        self.uuid_to_soco = {}
        self.zone_group_state_cache = {}  # ✅ ensure this exists early
        # Cap SoCo's default 20s per-request timeout — one offline player must not
        # be able to stall dispatch-thread work for 20s at a time.
        # NOTE: 'soco' is shadowed by a local variable later in __init__, so alias
        # the module explicitly here.
        import soco.config as _soco_config
        _soco_config.REQUEST_TIMEOUT = 5.0

        # HTTP bits
        self.httpd = None
        self.httpd_thread = None

        # Network prefs
        self.targetSonosSubnet = self.pluginPrefs.get("sonosTargetSubnet", "192.168.80.0/24")

        # -------------------------------------------------------------------------
        # Safe access to pluginPrefs / providers
        # -------------------------------------------------------------------------
        self.Pandora = self.pluginPrefs.get("Pandora")
        self.PandoraEmailAddress = self.pluginPrefs.get("PandoraEmailAddress")
        self.PandoraPassword = self.pluginPrefs.get("PandoraPassword")
        self.PandoraNickname = self.pluginPrefs.get("PandoraNickname")

        global Sonos_Pandora
        if self.Pandora and self.PandoraEmailAddress and self.PandoraPassword and not Sonos_Pandora:
            self.logger.info("🔁 Preloading Pandora stations at init.")
            Sonos_Pandora = []  # Clear global list to ensure fresh load
            self.getPandora(self.PandoraEmailAddress, self.PandoraPassword, self.PandoraNickname)

        # -------------------------------------------------------------------------
        # Init internal structures (legacy layout retained)
        # -------------------------------------------------------------------------
        self.globals = plugin.globals

        self.deviceList = []
        self.event_threads = {}
        self.soco_subs = {}
        self.soco_sub = {}
        self.event_listener_started = False
        self.ZonePlayers = []
        self.ZPTypes = []
        self.zonePlayerState = {}
        self.SoundFilePath = None
        self.ttsORfile = None
        self.first_working_stream = None

        self.control_point = None
        self.SonosDeviceID = None
        self.rootZPIP = None
        self.find_sonos_interface_ip()

        # Voice + credentials init (legacy pattern)
        self.Pandora = self.PandoraEmailAddress = self.PandoraPassword = self.PandoraNickname = None
        self.Pandora2 = self.PandoraEmailAddress2 = self.PandoraPassword2 = self.PandoraNickname2 = None
        self.SiriusXM = self.SiriusXMID = self.SiriusXMPassword = None
        self.IVONA = self.IVONAaccessKey = self.IVONAsecretKey = None
        self.Polly = self.PollyaccessKey = self.PollysecretKey = None
        self.MSTranslate = self.MSTranslateClientID = self.MSTranslateClientSecret = None
        self.MSTranslateVoices = {}
        self.myLocale = None

        self.SonArray = [{}]
        self.EventProcessor = "SoCo"
        self.EventIP = None
        self.EventCheck = None
        self.SubscriptionCheck = None
        self.HTTPStreamingIP = None
        self.HTTPStreamingPort = None
        self.HTTPStreamerOn = False
        self.HTTPServer = None
        self.httpd = None

        # SiriusXM
        self.siriusxm = None
        self.siriusxm_channels = []
        self.Sonos_SiriusXM = []
        self.siriusxm_id_map = {}
        self.siriusxm_guid_map = {}            # ✅ ensure present; earlier error referenced this missing
        self.last_siriusxm_guid_by_dev = {}

        # SoCo device maps
        self.soco_devices = {}
        self.ip_to_soco_device = {}            # Maps IP -> SoCo object

        self.uuid_to_indigo_device = {}        # ✅ Required for dump_groups_to_log
        self.group_name_by_device_id = {}


        self._dump_groups_timer = None
        self._dump_groups_done  = False


        # Hardcoded fallback test entries (retained)
        self.siriusxm_guid_map.update({
            "spa73": {"guid": "66e2c540-b3f3-4934-80cd-578f30e3dbb3", "name": "Spa", "channelNumber": "73"},
            "deeptracks308": {"guid": "e3041d19-daa5-6517-8c73-41976582d1f9", "name": "Deep Tracks", "channelNumber": "308"},
            "80stop500551": {"guid": "6be4367a-f423-68eb-1a5e-76ef11a8970e", "name": "80s on 8 Top 500", "channelNumber": "551"},
            "pettyburiedtreasure711": {"guid": "f95497ef-39c0-66fd-5749-f6c7b6f768b9", "name": "Petty's Buried Treasure", "channelNumber": "711"}
        })

        # Load SiriusXM channel data and derive sorted GUIDs
        self.load_siriusxm_channel_data()
        self.sorted_siriusxm_guids = sorted(
            [chan.get("channelGuid") for chan in self.siriusxm_channels if chan.get("channelGuid")],
            key=lambda g: next((int(c.get("channelNumber", 9999)) for c in self.siriusxm_channels if c.get("channelGuid") == g), 9999)
        )

        # Misc device maps used elsewhere
        self.device_zone_ips = {}
        self.parsed_zone_group_state_by_ip = {}
        self._eval_coord_dev_by_ip = {}        # coordinator ip → Indigo device (rebuilt by refresh/zgt)
        self.soco_by_dev = {}

        # Guard: self.soco_devices_by_uuid may not exist at init time
        if hasattr(self, "soco_devices_by_uuid"):
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                uuid = dev.states.get("uuid")
                if not uuid:
                    continue
                soco = self.soco_devices_by_uuid.get(uuid)
                if soco:
                    self.soco_by_dev[dev.id] = soco

        # ✅ Rebuild uuid_to_indigo_device mapping
        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            soco = self.soco_devices.get(dev.address)
            ## Will set group_name here break things or fix early on issues? DT
            group_name = dev.states.get("GROUP_Name") or self.group_name_by_device_id.get(dev.id, "?")
            #self.logger.warning(f"⚠️ I set Group_Name early on to initialize for Londonmark script: Name= '{group_name}' Address= '{dev.address}'")            
            if soco:
                uid = self.safe_uid(dev.address, soco)  # probe-gated; no repeated timeouts on offline players
                if uid:
                    self.uuid_to_indigo_device[uid] = dev
                else:
                    self.logger.debug(f"UUID for '{dev.name}' not yet resolvable (player offline?) — will map later")



    ############################################################################################
    ### Ensure MP3s are visible in action dialog after reload
    ############################################################################################
    def getActionConfigUiValues(self, pluginAction, typeId, devId):
        try:
            self.logger.debug(f"🎛️ getActionConfigUiValues called for action type: {typeId}")
            self.getSoundFiles()  # Refresh MP3 list every time UI loads
            return pluginAction.props, indigo.Dict()
        except Exception as e:
            self.logger.error(f"❌ Error in getActionConfigUiValues: {e}")
            return pluginAction.props, indigo.Dict()






        self.getSoundFiles()



    def getSoundFilesList(self, filter="", valuesDict=None, typeId="", targetId=0):
        try:
            if not hasattr(self, 'Sound_Files') or not self.Sound_Files:
                self.getSoundFiles()
            return [(f, f) for f in sorted(self.Sound_Files)]
        except Exception as e:
            self.logger.error(f"❌ Error in getSoundFilesList(): {e}")
            return []


    ### End of Initialization


    ############################################################################################
    ### Actiondirect List Processing
    ############################################################################################

    def actionDirect(self, pluginAction, action_id_override=None):

        try:
            #self.logger.warning("🧪 [LOG 0] Entered actionDirect")

            # Normalize simplified override names into internal action IDs
            action_map = {
                "Play": "actionPlay",
                "TogglePlay": "actionTogglePlay",
                "Pause": "actionPause",
                "Stop": "actionStop",
                "Next": "actionNext",
                "Previous": "actionPrevious",
                "MuteToggle": "actionMuteToggle",
                "MuteOn": "actionMuteOn",
                "MuteOff": "actionMuteOff",
                "Volume": "actionVolume",
                "VolumeUp": "actionVolumeUp",
                "VolumeDown": "actionVolumeDown",
                "BassUp": "actionBassUp",
                "BassDown": "actionBassDown",
                "TrebleUp": "actionTrebleUp",
                "TrebleDown": "actionTrebleDown",
                "setStandalone": "setStandalone",
                "actionsetStandalone": "setStandalone",
                "setStandalones": "setStandalones",
                "actionsetStandalones": "setStandalones",
                "addPlayerToZone": "actionZP_addPlayerToZone",
                "GroupMuteToggle": "actionGroupMuteToggle",
                "GroupMuteOn": "actionGroupMuteOn",
                "GroupMuteOff": "actionGroupMuteOff",
                "GroupVolumeUp": "actionGroupVolumeUp",
                "GroupVolumeDown": "actionGroupVolumeDown",
                "NightMode": "actionNightMode",
                "ZP_Pandora": "actionZP_Pandora",
                "ZP_SiriusXM": "actionZP_SiriusXM",
                "ZP_TV": "actionZP_TV",
                "ZP_DumpURI": "actionZP_DumpURI",
                "ChannelUp": "actionChannelUp",
                "ChannelDown": "actionChannelDown",
                "Q_ShuffleToggle": "actionQ_ShuffleToggle",
                "Q_Shuffle": "actionQ_Shuffle",
                "ZP_SonosFavorites": "ZP_SonosFavorites",
                "ZP_SonosRadio": "ZP_SonosRadio",
                "ZP_Container": "ZP_Container",
                "Q_RepeatToggle": "actionQ_RepeatToggle",
                # allow both public and "action..." forms (reverse mappings)
                "actionGroupMuteOff": "GroupMuteOff",
                "actionGroupMuteOn": "GroupMuteOn",
                "actionGroupMuteToggle": "GroupMuteToggle",
                "actionGroupVolume": "GroupVolume",
                "actionRelativeGroupVolume": "RelativeGroupVolume",
            }

            raw_key = action_id_override or pluginAction.pluginTypeId
            #self.logger.warning(f"🧪 [LOG 1] raw_key: {raw_key}")
            action_key = action_map.get(raw_key, raw_key)
            action_id = action_key
            #self.logger.warning(f"🧪 [LOG 2] action_id resolved to: {action_id}")

            # Dispatch handler mapping (global or device-aware)
            dispatch_table = {
                "SetSiriusXMChannel":        lambda p, d, z: self.handleAction_SetSiriusXMChannel(p, d, z),
                "actionZP_SiriusXM":         lambda p, d, z: self.handleAction_ZP_SiriusXM(p, d, z, p.props),
                "actionZP_Pandora":          lambda p, d, z: self.handleAction_ZP_Pandora(p, d, z, p.props),
                "actionChannelUp":           lambda p, d, z: self.handleAction_ChannelUp(p, d, z),
                "actionChannelDown":         lambda p, d, z: self.handleAction_ChannelDown(p, d, z),
                "actionZP_addPlayerToZone":  lambda p, d, z: self.handleAction_ZP_addPlayerToZone(p, d, z),
                "actionQ_Shuffle":           lambda p, d, z: self.handleAction_Q_Shuffle(p, d, z),
                "actionQ_Crossfade":         lambda p, d, z: self.handleAction_Q_Crossfade(p, d),
            }

            device_id = int(pluginAction.deviceId)
            #self.logger.warning(f"🧪 [LOG 3] pluginAction.deviceId: {device_id}")

            # === Global Actions (e.g., from Control Pages) ===
            if device_id == 0:
                #self.logger.warning(f"🧪 [LOG 3.5] Global action (deviceId = 0) detected: {action_id}")

                if action_id == "setStandalones":
                    self.logger.warning(f"I am going to set standalones from a state where they are grouped")
                    zones = []
                    for x in range(1, 13):
                        ivar = f'zp{x}'
                        val = pluginAction.props.get(ivar)
                        if val and val != "00000":
                            zones.append(val)

                    for item in zones:
                        try:
                            dev = indigo.devices[int(item)]
                            self.logger.info(f"🔁 Un-grouping device: {dev.name}")
                            if dev.states.get("GROUP_Coordinator") == "true":
                                self.SOAPSend(dev.pluginProps["address"], "/MediaRenderer", "/AVTransport",
                                              "BecomeCoordinatorOfStandaloneGroup", "")
                            self.SOAPSend(dev.pluginProps["address"], "/MediaRenderer", "/AVTransport",
                                          "SetAVTransportURI",
                                          f"<CurrentURI>x-rincon-queue:{dev.states['ZP_LocalUID']}#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                            #DT_Test
                            #self.logger.warning(f"Lets build group coordinator tracker directlly from SOCO UUID ... DT_Test")
                            self.refresh_group_topology_after_plugin_zone_change()
                            #self.refresh_all_group_states()
                            self._refresh_all_group_states_helper(reason="action direct?")

                            self.evaluate_and_update_grouped_states()
                        except Exception as e:
                            self.logger.error(f"❌ Failed to ungroup device {item}: {e}")
                    return

                else:
                    self.logger.error(f"❌ Global action_id '{action_id}' not handled")
                    return

            # === Device-Based Actions ===
            try:
                dev = indigo.devices[device_id]
                #self.logger.warning(f"🧪 [LOG 4] dev.name: {dev.name}, ID: {dev.id}")
            except KeyError:
                self.logger.error(f"❌ Device ID {device_id} not found in Indigo database")
                return

            # Determine coordinator device and IP (single calculation)
            coordinator_dev = self.getCoordinatorDevice(dev)
            coordinator_ip = coordinator_dev.pluginProps.get("address", "").strip()

            # Assign correct target IP
            zoneIP = coordinator_ip
            if coordinator_dev.id != dev.id:
                self.logger.debug(f"🔁 Redirecting control from slave {dev.name} to coordinator {coordinator_dev.name} at {zoneIP}")
            else:
                self.logger.debug(f"✅ {dev.name} is the coordinator — using direct control")

            # Seed Coordinator* vars so later branches are safe
            CoordinatorIP = coordinator_ip
            CoordinatorDev = coordinator_dev

            # Fast-path: dedicated handlers
            if action_id in dispatch_table:
                dispatch_table[action_id](pluginAction, dev, zoneIP)
                return

            # === Transport Actions ===
            if action_id in ("actionPlay", "Play"):
                self.plugin.debugLog("Sonos Action: Play")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                self.logger.info(f"▶️ Play sent to {coordinator_dev.name}")

                if dev.id != coordinator_dev.id:
                    dev.updateStateOnServer("ZP_STATE", "PLAYING")
                    self.safe_debug(f"🔁 Synced ZP_STATE from {coordinator_dev.name} → {dev.name}: PLAYING")
                return

            #DT Here  (helper must NOT chain into action dispatch)
            if dev.states["GROUP_Coordinator"] == "false":
                Coordinator = dev.states["GROUP_Name"]
                for idev in indigo.devices.iter("self.ZonePlayer"):
                    if idev.states["GROUP_Coordinator"] == "true" and idev.states["GROUP_Name"] == Coordinator:
                        CoordinatorIP = idev.pluginProps["address"]
                        CoordinatorDev = self.getCoordinatorDevice(dev)
                        break

            # === Start a NEW action dispatch chain (decoupled from the helper above) ===

            if action_id == "announcement":
                # Sanitize and normalize pluginAction.props['setting']
                raw_setting = pluginAction.props.get("setting") if pluginAction.props else None
                self.logger.debug(f"[🧪 pluginAction.props['setting']] Raw value: {raw_setting} ({type(raw_setting).__name__})")

                try:
                    if isinstance(raw_setting, int):
                        raw_setting = str(raw_setting)
                        self.logger.debug(f"[🔄] Converted integer 'setting' to string: {raw_setting}")
                    elif raw_setting is None:
                        self.logger.warning("[⚠️ WARN] pluginAction.props['setting'] is missing or None")
                        raw_setting = ""
                    elif not isinstance(raw_setting, str):
                        self.logger.warning(f"[⚠️ WARN] Unexpected 'setting' type: {type(raw_setting).__name__}")
                        raw_setting = str(raw_setting)

                    # Now split
                    if "||" in raw_setting:
                        zone_name, ip_addr = raw_setting.strip().split("||", 1)
                        self.logger.debug(f"[✅ Parsed setting] Zone = '{zone_name}', IP = '{ip_addr}'")
                    else:
                        zone_name = ip_addr = None
                        self.logger.error(f"[❌ INVALID] 'setting' does not contain expected '||' delimiter: {raw_setting}")

                except Exception as e:
                    self.logger.exception(f"[❌ Exception] Failed parsing 'setting': {e}")
                    zone_name = ip_addr = None

                # Log volume and file props
                volume = pluginAction.props.get("volume") if pluginAction.props else None
                file = pluginAction.props.get("file") if pluginAction.props else None

                self.logger.debug(f"[🔈 Volume Level] = {volume}")
                self.logger.debug(f"[🎵 File] = {file}")
                self.logger.debug(f"[🌐 Target IP] = {ip_addr}")
                return

            elif action_id in ("actionPause", "Pause"):
                self.plugin.debugLog("Sonos Action: Pause")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause", "")
                self.logger.info(f"⏸ Pause sent to {coordinator_dev.name}")

                if dev.id != coordinator_dev.id:
                    dev.updateStateOnServer("ZP_STATE", "PAUSED_PLAYBACK")
                    self.safe_debug(f"🔁 Synced ZP_STATE from {coordinator_dev.name} → {dev.name}: PAUSED_PLAYBACK")
                return

            elif action_id in ("actionStop", "Stop"):
                self.plugin.debugLog("Sonos Action: Stop")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Stop", "")
                self.logger.info(f"⏹ Stop sent to {coordinator_dev.name}")

                if dev.id != coordinator_dev.id:
                    dev.updateStateOnServer("ZP_STATE", "STOPPED")
                    self.safe_debug(f"🔁 Synced ZP_STATE from {coordinator_dev.name} → {dev.name}: STOPPED")
                return

            elif action_id in ("actionTogglePlay", "TogglePlay"):
                self.plugin.debugLog("Sonos Action: Toggle Play")
                current_state = coordinator_dev.states.get("ZP_STATE", "").upper()

                if current_state == "PLAYING":
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause", "")
                    self.logger.info(f"⏸ TogglePlay → Pause sent to {coordinator_dev.name}")
                    new_state = "PAUSED_PLAYBACK"
                else:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                    self.logger.info(f"▶️ TogglePlay → Play sent to {coordinator_dev.name}")
                    new_state = "PLAYING"

                if dev.id != coordinator_dev.id:
                    dev.updateStateOnServer("ZP_STATE", new_state)
                    self.safe_debug(f"🔁 Synced ZP_STATE from {coordinator_dev.name} → {dev.name}: {new_state}")
                return

            # Mute Controls
            elif action_id in ("actionMuteToggle", "MuteToggle"):
                self.plugin.debugLog("Sonos Action: Mute Toggle")

                # dev.states["ZP_MUTE"] can be "0"/"1" or "true"/"false" (string) — normalize safely
                raw = dev.states.get("ZP_MUTE", 0)
                raw_s = str(raw).strip().lower()
                is_muted = raw_s in ("1", "true", "on", "yes")

                desired_mute = "0" if is_muted else "1"
                self.SOAPSend(
                    zoneIP,
                    "/MediaRenderer",
                    "/RenderingControl",
                    "SetMute",
                    f"<Channel>Master</Channel><DesiredMute>{desired_mute}</DesiredMute>"
                )

                indigo.server.log("ZonePlayer: %s, Mute %s" % (dev.name, "Off" if is_muted else "On"))
                return



            elif action_id in ("actionMuteOn", "MuteOn"):
                self.plugin.debugLog("Sonos Action: Mute On")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>1</DesiredMute>")
                indigo.server.log("ZonePlayer: %s, Mute On" % dev.name)
                return

            elif action_id in ("actionMuteOff", "MuteOff"):
                self.plugin.debugLog("Sonos Action: Mute Off")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute", "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
                indigo.server.log("ZonePlayer: %s, Mute Off" % dev.name)
                return

            # Group Mute Controls
            elif action_id in ("actionGroupMuteToggle", "GroupMuteToggle"):
                self.plugin.debugLog("Sonos Action: Group Mute Toggle")

                # parseCurrentMute(...) may return "0"/"1" or "true"/"false" — normalize safely
                gmute_raw = self.parseCurrentMute(
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupMute", "")
                )
                gmute_s = str(gmute_raw).strip().lower()
                group_is_muted = gmute_s in ("1", "true", "on", "yes")

                desired_group_mute = "0" if group_is_muted else "1"
                self.SOAPSend(
                    zoneIP,
                    "/MediaRenderer",
                    "/GroupRenderingControl",
                    "SetGroupMute",
                    f"<DesiredMute>{desired_group_mute}</DesiredMute>"
                )

                indigo.server.log("ZonePlayer Group: %s, Mute %s" % (dev.name, "Off" if group_is_muted else "On"))
                return


            elif action_id in ("actionGroupMuteOn", "GroupMuteOn"):
                self.plugin.debugLog("Sonos Action: Group Mute On")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>1</DesiredMute>")
                indigo.server.log("ZonePlayer Group: %s, Mute On" % dev.name)
                return

            elif action_id in ("actionGroupMuteOff", "GroupMuteOff"):
                self.plugin.debugLog("Sonos Action: Group Mute Off")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute", "<DesiredMute>0</DesiredMute>")
                indigo.server.log("ZonePlayer Group: %s, Mute Off" % dev.name)
                return

            # Group Volume Controls
            elif action_id in ("actionGroupVolume", "GroupVolume"):
                self.plugin.debugLog("Sonos Action: Group Volume")
                current_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                new_volume = int(eval(self.plugin.substitute(pluginAction.props.get("setting"))))
                if new_volume < 0 or new_volume > 100:
                    new_volume = current_volume
                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupVolume", f"<DesiredVolume>{new_volume}</DesiredVolume>")
                indigo.server.log(f"ZonePlayer Group: {dev.name}, Current Group Volume: {current_volume}, New Group Volume: {new_volume}")
                return

            elif action_id in ("actionRelativeGroupVolume", "RelativeGroupVolume"):
                self.plugin.debugLog("Sonos Action: Relative Group Volume")
                current_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                adjustment = pluginAction.props.get("setting")
                try:
                    new_volume = int(current_volume) + int(adjustment)
                except Exception:
                    new_volume = current_volume
                new_volume = max(0, min(new_volume, 100))
                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetRelativeGroupVolume", f"<Adjustment>{adjustment}</Adjustment>")
                indigo.server.log(f"ZonePlayer Group: {dev.name}, Current Group Volume: {current_volume}, New Group Volume: {new_volume}")
                return

            elif action_id in ("actionGroupVolumeDown", "GroupVolumeDown"):
                self.plugin.debugLog("Sonos Action: Group Volume Down")
                current_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                new_volume = max(0, int(current_volume) - 2)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetRelativeGroupVolume", "<Adjustment>-2</Adjustment>")
                indigo.server.log(f"ZonePlayer Group: {dev.name}, Current Group Volume: {current_volume}, New Group Volume: {new_volume}")
                return

            elif action_id in ("actionGroupVolumeUp", "GroupVolumeUp"):
                self.plugin.debugLog("Sonos Action: Group Volume Up")
                current_volume = self.parseCurrentVolume(self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", ""))
                new_volume = min(100, int(current_volume) + 2)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetRelativeGroupVolume", "<Adjustment>2</Adjustment>")
                indigo.server.log(f"ZonePlayer Group: {dev.name}, Current Group Volume: {current_volume}, New Group Volume: {new_volume}")
                return

            elif action_id in ("actionQ_Crossfade", "Q_Crossfade"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                mode = pluginAction.props.get("setting")
                if mode == 0:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetCrossfadeMode", "<CrossfadeMode>0</CrossfadeMode>")
                elif mode == 1:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetCrossfadeMode", "<CrossfadeMode>1</CrossfadeMode>")
                return

            elif action_id in ("actionQ_Repeat", "Q_Repeat"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                repeat = bool(int(pluginAction.props.get("setting")))
                repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                shuffle = self.boolConv(dev.states["Q_Shuffle"])
                if repeat == True:
                    PlayMode = self.QMode(repeat, False, shuffle)
                else:
                    PlayMode = self.QMode(repeat, repeat_one, shuffle)
                self.plugin.debugLog("Sonos Action: PlayMode %s" % PlayMode)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                return

            elif action_id in ("actionQ_RepeatOne", "Q_RepeatOne"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                repeat_one = bool(int(pluginAction.props.get("setting")))
                repeat = self.boolConv(dev.states["Q_Repeat"])
                shuffle = self.boolConv(dev.states["Q_Shuffle"])
                if repeat_one == True:
                    PlayMode = self.QMode(False, repeat_one, shuffle)
                else:
                    PlayMode = self.QMode(repeat, repeat_one, shuffle)
                self.plugin.debugLog("Sonos Action: PlayMode %s" % PlayMode)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                return

            elif action_id in ("actionQ_RepeatToggle", "Q_RepeatToggle"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                repeat = self.boolConv(dev.states["Q_Repeat"])
                repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                shuffle = self.boolConv(dev.states["Q_Shuffle"])
                if repeat == False and repeat_one == False:
                    PlayMode = self.QMode(True, False, shuffle)
                elif repeat == True and repeat_one == False:
                    PlayMode = self.QMode(False, True, shuffle)
                else:
                    PlayMode = self.QMode(False, False, shuffle)
                self.plugin.debugLog("Sonos Action: PlayMode %s" % PlayMode)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                return

            elif action_id in ("actionQ_Shuffle", "Q_Shuffle"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                shuffle = bool(int(pluginAction.props.get("setting")))
                repeat = self.boolConv(dev.states["Q_Repeat"])
                repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                PlayMode = self.QMode(repeat, repeat_one, shuffle)
                self.plugin.debugLog("Sonos Action: PlayMode %s" % PlayMode)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                return

            elif action_id in ("actionQ_ShuffleToggle", "Q_ShuffleToggle"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = CoordinatorIP
                repeat = self.boolConv(dev.states["Q_Repeat"])
                repeat_one = self.boolConv(dev.states["Q_RepeatOne"])
                shuffle = self.boolConv(dev.states["Q_Shuffle"])
                if shuffle == True:
                    PlayMode = self.QMode(repeat, repeat_one, False)
                else:
                    PlayMode = self.QMode(repeat, repeat_one, True)
                self.plugin.debugLog("Sonos Action: PlayMode %s" % PlayMode)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>"+PlayMode+"</NewPlayMode>")
                return

            elif action_id == "Q_Clear":
                self.SOAPSend(zoneIP, "/MediaRenderer", "/Queue", "RemoveAllTracks", "<QueueID>0</QueueID><UpdateID>0</UpdateID>")
                indigo.server.log("ZonePlayer: %s, Clear Queue" % dev.name)
                return

            elif action_id == "Q_Save":
                self.updateZoneTopology(dev)
                if dev.states["GROUP_Coordinator"] == "false":
                    self.plugin.debugLog("ZonePlayer: %s, Cannot Save Queue for Slave" % dev.name)
                else:
                    self.plugin.sleep(0.5)
                    PlaylistName = pluginAction.props.get("setting")
                    ZP  = self.parseBrowseNumberReturned(self.SOAPSend (zoneIP, "/MediaServer", "/ContentDirectory", "Browse", "<ObjectID>Q:0</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria>"))
                    if PlaylistName == "Indigo_" + dev.states['ZP_LocalUID']:
                        self.updateStateOnServer (dev, "Q_Number", ZP)
                    if int(ZP) > 0:
                        ObjectID = ""
                        for plist in Sonos_Playlists:
                            if plist[1] == PlaylistName:
                                ObjectID = plist[2]
                        AssignedObjectID = self.parseAssignedObjectID(self.SOAPSend (zoneIP, "/MediaRenderer", "/Queue", "SaveAsSonosPlaylist", "<QueueID>0</QueueID><Title>" + PlaylistName + "</Title><ObjectID>" + ObjectID + "</ObjectID>"))
                        if ObjectID == "":
                            ObjectID = AssignedObjectID
                        if PlaylistName.find(dev.states['ZP_LocalUID']) > -1:
                            self.updateStateOnServer (dev, "Q_ObjectID", ObjectID)

                        self.plugin.debugLog ("ZonePlayer: %s, Save Queue: %s" % (dev.name, PlaylistName))
                    else:
                        if PlaylistName == "Indigo_" + dev.states['ZP_LocalUID']:
                            ObjectID = ""
                            for plist in Sonos_Playlists:
                                if plist[1] == PlaylistName:
                                    ObjectID = plist[2]
                                    self.actionDirect(PA(dev.id, {"setting":ObjectID}), "CD_RemovePlaylist")
                            self.updateStateOnServer (dev, "Q_ObjectID", "")
                        self.plugin.debugLog ("ZonePlayer: %s, Nothing in Queue to Save" % dev.name)
                return

            elif action_id == "CD_RemovePlaylist":
                ObjectID = pluginAction.props.get("setting")
                for plist in Sonos_Playlists:
                    if plist[2] == ObjectID:
                        PlaylistName = plist[1]
                        self.SOAPSend (zoneIP, "/MediaServer", "/ContentDirectory", "DestroyObject", "<ObjectID>" + ObjectID + "</ObjectID>")
                indigo.server.log ("ZonePlayer: %s, Remove Playlist: %s" % (dev.name, PlaylistName))
                return

            elif action_id == "actionBassUp":
                current = int(dev.states.get("ZP_BASS", 0))
                newVal = max(min(current + 1, 10), -10)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetBass",
                              f"<DesiredBass>{newVal}</DesiredBass>")
                self.logger.info(f"🔊 Bass increased on {dev.name}: {current} → {newVal}")
                self.refresh_transport_state(zoneIP)
                return

            elif action_id == "actionBassDown":
                current = int(dev.states.get("ZP_BASS", 0))
                newVal = max(min(current - 1, 10), -10)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetBass",
                              f"<DesiredBass>{newVal}</DesiredBass>")
                self.logger.info(f"🔉 Bass decreased on {dev.name}: {current} → {newVal}")
                self.refresh_transport_state(zoneIP)
                return

            elif action_id == "actionTrebleUp":
                current = int(dev.states.get("ZP_TREBLE", 0))
                newVal = max(min(current + 1, 10), -10)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetTreble",
                              f"<DesiredTreble>{newVal}</DesiredTreble>")
                self.logger.info(f"🎶 Treble increased on {dev.name}: {current} → {newVal}")
                self.refresh_transport_state(zoneIP)
                return

            elif action_id == "actionTrebleDown":
                current = int(dev.states.get("ZP_TREBLE", 0))
                newVal = max(min(current - 1, 10), -10)
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetTreble",
                              f"<DesiredTreble>{newVal}</DesiredTreble>")
                self.logger.info(f"🎵 Treble decreased on {dev.name}: {current} → {newVal}")
                self.refresh_transport_state(zoneIP)
                return
        
            elif action_id == "actionVolume":
                self.logger.warning(f"[Debug] Received action_id: '{action_id}'")
                self.plugin.debugLog("Sonos Action: Volume")
                current_volume = dev.states["ZP_VOLUME"]
                new_volume = int(eval(self.plugin.substitute(pluginAction.props.get("setting"))))
                if new_volume < 0 or new_volume > 100:
                    new_volume = current_volume
                self.SOAPSend (zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume", "<Channel>Master</Channel><DesiredVolume>"+str(new_volume)+"</DesiredVolume>")
                indigo.server.log(u"ZonePlayer: %s, Current Volume: %s, New Volume: %s" % (dev.name, current_volume, new_volume))
                return

            elif action_id == "actionVolumeUp":
                self.safe_debug("🧪 Matched action_id == actionVolumeUp")

                # Pull volume from coordinator (not the slave!)
                current = int(coordinator_dev.states.get("ZP_VOLUME_MASTER", 0))
                new_volume = min(100, current + 5)

                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume",
                              f"<Channel>Master</Channel><DesiredVolume>{new_volume}</DesiredVolume>")

                self.logger.info(f"🔊 Volume UP sent to {coordinator_dev.name}: {current} → {new_volume}")

                # If this was initiated from a slave, update its visible state to match
                if dev.id != coordinator_dev.id:
                    dev.updateStateOnServer("ZP_VOLUME_MASTER", new_volume)
                    self.safe_debug(f"🔁 Synced ZP_VOLUME_MASTER from {coordinator_dev.name} → {dev.name}")
                return

            elif action_id == "actionVolumeDown":
                self.safe_debug("🧪 Matched action_id == actionVolumeDown")

                current = int(coordinator_dev.states.get("ZP_VOLUME_MASTER", 0))
                new_volume = max(0, current - 5)

                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume",
                              f"<Channel>Master</Channel><DesiredVolume>{new_volume}</DesiredVolume>")

                self.logger.info(f"🔉 Volume DOWN sent to {coordinator_dev.name}: {current} → {new_volume}")

                if dev.id != coordinator_dev.id:
                    dev.updateStateOnServer("ZP_VOLUME_MASTER", new_volume)
                    self.safe_debug(f"🔁 Synced ZP_VOLUME_MASTER from {coordinator_dev.name} → {dev.name}")
                return

            elif action_id == "actionMuteToggle":
                self.safe_debug("🧪 Matched action_id == actionMuteToggle")

                # Get mute state from coordinator, not slave
                raw_state = coordinator_dev.states.get("ZP_MUTE", "unknown")
                mute_state = str(raw_state).lower() == "true"

                mute_val = "0" if mute_state else "1"
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute",
                              f"<Channel>Master</Channel><DesiredMute>{mute_val}</DesiredMute>")

                self.logger.info(f"🎚 Mute TOGGLE sent to {coordinator_dev.name}: {'Off' if mute_state else 'On'}")

                # Optionally update the slave state immediately
                if dev.id != coordinator_dev.id:
                    new_state = "false" if mute_state else "true"
                    dev.updateStateOnServer("ZP_MUTE", new_state)
                    self.safe_debug(f"🔁 Synced ZP_MUTE from {coordinator_dev.name} → {dev.name}: {new_state}")
                return

            elif action_id == "actionMuteOn":
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute",
                              "<Channel>Master</Channel><DesiredMute>1</DesiredMute>")
                self.logger.info(f"🔇 Mute ON for {dev.name}")
                self.refresh_transport_state(zoneIP)
                return

            elif action_id == "actionMuteOff":
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute",
                              "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
                self.logger.info(f"🔊 Mute OFF for {dev.name}")
                self.refresh_transport_state(zoneIP)
                return

            elif action_id == "actionStop":
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Stop", "<InstanceID>0</InstanceID>")
                self.logger.info(f"⏹️ Stop triggered for {dev.name}")
                return

            elif action_id == "actionNext":
                uri = dev.states.get("ZP_CurrentTrackURI", "") or dev.states.get("ZP_AVTransportURI", "")
                self.safe_debug(f"🧪 Checking for SiriusXM stream in URI: {uri}")
                if "sirius" in uri.lower() or "x-sonosapi-" in uri.lower():
                    self.logger.info(f"📻 Detected SiriusXM stream — calling channelUpOrDown(up) for {dev.name}")
                    self.channelUpOrDown(dev, direction="up")
                    return
                else:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Next", "<InstanceID>0</InstanceID>")
                    self.logger.info(f"⏭️ Next track for {dev.name}")
                    return

            elif action_id == "actionPrevious":
                uri = dev.states.get("ZP_CurrentTrackURI", "") or dev.states.get("ZP_AVTransportURI", "")
                self.safe_debug(f"🧪 Checking for SiriusXM stream in URI: {uri}")
                if "sirius" in uri.lower() or "x-sonosapi-" in uri.lower():
                    self.logger.info(f"📻 Detected SiriusXM stream — calling channelUpOrDown(down) for {dev.name}")
                    self.channelUpOrDown(dev, direction="down")
                    return
                else:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Previous", "<InstanceID>0</InstanceID>")
                    self.logger.info(f"⏮️ Previous track for {dev.name}")
                    return

            elif action_id == "actionTogglePlay":
                state = dev.states.get("ZP_STATE", "STOPPED").upper()
                if state in ("STOPPED", "PAUSED_PLAYBACK"):
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                    self.logger.info(f"▶️ Play for {dev.name}")
                else:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause", "<Speed>1</Speed>")
                    self.logger.info(f"⏸ Pause for {dev.name}")
                return

            #####################################################################################################
            ### Start of action direct statements added code for action command support of favorites and volume
            #####################################################################################################

            elif action_id == "ZP_SonosFavorites":
                setting = pluginAction.props.get("setting")
                for uri in Sonos_Favorites:
                    if uri[4] == setting:
                        l2p=uri[0]
                        break
                mode = pluginAction.props.get("mode")
                if mode == "":
                    mode = "Play Now"  # (a stray `return` here used to abort the action when mode was empty)
                if uri_radio in l2p:
                    self.actionDirect (PA(dev.id, {"setting":l2p}), "ZP_RT_FavStation")
                    return
                elif uri_pandora in l2p:
                    setting = l2p[l2p.find(":")+1:l2p.find("?")]
                    self.actionDirect (PA(dev.id, {"setting":setting}), "ZP_Pandora")
                    return
                elif uri_siriusxm in l2p and "channel-linear" in l2p:
                    # True SiriusXM favourites carry channel-linear:<guid>. Plain
                    # x-sonosapi-hls: is a generic HLS scheme (Sonos Radio HD, Apple
                    # Music radio, …) and must NOT be routed to the SiriusXM handler.
                    setting = urllib.parse.unquote(l2p[l2p.find(":")+1:l2p.find("?")])
                    self.actionDirect (PA(dev.id, {"setting":setting}), "ZP_SiriusXM")
                    return
                elif uri_siriusxm in l2p or uri_sonos_http in l2p:
                    # Generic streaming favourite — play it with its stored URI and
                    # DIDL metadata via the Sonos Radio path.
                    self.actionDirect (PA(dev.id, {"setting":l2p}), "ZP_SonosRadio")
                    return
                elif uri_spotify in l2p:
                    self.actionDirect (PA(dev.id, {"setting":l2p, "mode":mode}), "ZP_Container")
                    return                
                elif uri_container in l2p or uri_jffs in l2p or uri_playlist in l2p or uri_file in l2p:
                    self.actionDirect (PA(dev.id, {"setting":l2p, "mode":mode}), "ZP_Container")
                    return
                elif uri_sonos_radio in l2p:
                    self.actionDirect (PA(dev.id, {"setting":l2p}), "ZP_SonosRadio")
                    return
                else:
                    indigo.server.log ("I do not know what to do with Favorite: %s" % l2p)
                    return

            elif action_id =="ZP_SonosRadio":
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = coordinator_dev.pluginProps.get("address", "").strip()
                l2p = pluginAction.props.get("setting")
                for title in Sonos_Favorites:
                    if title[0] == l2p:
                        pTitle = self.cleanString(title[1]).encode('ascii', 'xmlcharrefreplace')
                        URI = title[3]
                        MD = title[2]
                        break
                self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>"+URI+"</CurrentURI><CurrentURIMetaData>"+MD+"</CurrentURIMetaData>")
                self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                indigo.server.log ("ZonePlayer: %s, Play Radio: %s" % (dev.name, pTitle))
                return

            elif action_id == "ZP_RT_FavStation":
                # Restored from the original plugin — this branch was lost in a refactor,
                # leaving the "Play RadioTime Favorite Station" action (and radio-URI
                # favorites forwarded from ZP_SonosFavorites) logging
                # "Unknown or unsupported action: ZP_RT_FavStation" and doing nothing.
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = coordinator_dev.pluginProps.get("address", "").strip()
                if zoneIP:
                    l2p = pluginAction.props.get("setting", "").replace("&", "&amp;")
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>"+l2p+"</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" xmlns:r=\"urn:schemas-rinconnetworks-com:metadata-1-0/\" xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\"&gt;&lt;item id=\"-1\" parentID=\"-1\" restricted=\"true\"&gt;&lt;dc:title&gt;RADIO&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;&lt;desc id=\"cdudn\" nameSpace=\"urn:schemas-rinconnetworks-com:metadata-1-0/\"&gt;SA_RINCON65031_&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData>")
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                    indigo.server.log ("ZonePlayer: %s, Play RadioTime Station" % dev.name)
                else:
                    self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP RT FavStation' not actioned as Zone IP cannot be resolved!")
                return

            elif action_id == "ZP_Container":
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = coordinator_dev.pluginProps.get("address", "").strip()
                    dev_src_LocalUID = coordinator_dev.states['ZP_LocalUID']
                    #dev_src_LocalUID = CoordinatorDev.states['ZP_LocalUID']
                else:
                    dev_src_LocalUID = dev.states['ZP_LocalUID']                
                l2p = pluginAction.props.get("setting")
                mode = pluginAction.props.get("mode")
                #(uri_header, uri_detail) = l2p.split(':')
                for title in Sonos_Favorites:
                    if title[0] == l2p:
                        pTitle = self.cleanString(title[1]).encode('ascii', 'xmlcharrefreplace')
                        MD = title[2]
                        break

                # SONOS api change for Favorites?
                l2p = l2p.replace("&", "&amp;")

                if mode == "Play Now":
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev_src_LocalUID)+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                    track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData>"+MD+"</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Seek", "<Unit>TRACK_NR</Unit><Target>"+track_pos+"</Target>")
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                elif mode == "Play Next":
                    #current_track = self.parseCurrentTrack(dev, self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "GetPositionInfo", ""))
                    current_track = dev.states['ZP_CurrentTrack']
                    indigo.server.log(current_track)
                    track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData>"+MD+"</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>"+str(int(current_track)+1)+"</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                elif mode == "Add To Queue":
                    track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData>"+MD+"</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                elif mode == "Replace Queue":
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-rincon-queue:"+str(dev_src_LocalUID)+"#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "RemoveAllTracksFromQueue", "")
                    track_pos = self.parseFirstTrackNumberEnqueued(dev, self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "AddURIToQueue", "<EnqueuedURI>"+l2p+"</EnqueuedURI><EnqueuedURIMetaData>"+MD+"</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>1</EnqueueAsNext>"))
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Seek", "<Unit>TRACK_NR</Unit><Target>"+track_pos+"</Target>")
                    self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                indigo.server.log ("ZonePlayer: %s, Play: %s" % (dev.name, pTitle))
                return

            elif action_id == "ZP_LineIn":
                setting = pluginAction.props.get("setting")
                if not setting:
                    self.logger.warning(f"⚠️ No Line-In source selected for {dev.name}")
                    return
                try:
                    dev_src = indigo.devices[int(setting)]
                except Exception as e:
                    self.logger.error(f"❌ Invalid Line-In source device '{setting}': {e}")
                    return
                dev_src_LocalUID = dev_src.states.get('ZP_LocalUID')
                if not dev_src_LocalUID:
                    self.logger.error(f"❌ Selected Line-In source '{dev_src.name}' has no LocalUID; cannot switch.")
                    return
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI",
                              f"<CurrentURI>x-rincon-stream:{dev_src_LocalUID}</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                self.logger.info(f"🔊 {dev.name}: switched to Line-In source '{dev_src.states.get('ZP_ZoneName', dev_src.name)}'")
                return

            ############################################################################################
            #### end of added code for action command support of favorites and volume
            ############################################################################################
            elif action_id == "addPlayersToZone":
                self.logger.warning(f"✅ Entering addPlayersToZone - This is more multiple players")

                zones = []
                x = 1
                while x <= 12:
                    ivar = 'zp' + str(x)
                    if pluginAction.props.get(ivar) not in ["", None, "00000"]:
                        zones.append(pluginAction.props.get(ivar))
                    x = x + 1

                # NEW: resolve coordinator from the action's target (this handler treats `dev` as the coordinator)
                coord_dev = dev
                coord_ip  = (coord_dev.pluginProps.get("address", "") or "").strip()
                coord_uid = str(coord_dev.states.get('ZP_LocalUID', '')).strip()
                coord_name = coord_dev.name

                if not coord_uid or not coord_ip:
                    self.logger.error(f"❌ addPlayersToZone: missing coordinator UID/IP for {coord_dev.name}")
                    return

                # NEW: ensure coordinator is snapped to coord=true / grouped=true / name=<coord>
                try:
                    self._update_group_coord(coord_dev, "true", reason="addPlayersToZone(snap) coordinator")
                except Exception:
                    coord_dev.updateStateOnServer("GROUP_Coordinator", "true")
                coord_dev.updateStateOnServer("Grouped", True)                 # boolean
                coord_dev.updateStateOnServer("GROUP_Name", coord_name)

                # NEW: optional: start a small suppression window so evaluator won’t immediately undo snaps
                try:
                    if not hasattr(self, "_suppress_eval_until"):
                        self._suppress_eval_until = {}
                    self._suppress_eval_until[coord_dev.id] = time.time() + 2.0
                except Exception:
                    pass

                for item in zones:
                    indigo.server.log("add zone to group: %s" % item)
                    dev_dest = indigo.devices[int(item)]

                    # Skip if user accidentally included the coordinator in the list
                    if dev_dest.id == coord_dev.id:
                        self.logger.debug("⏭️ Skipping coordinator in join list")
                        continue

                    dest_ip  = (dev_dest.pluginProps.get("address", "") or "").strip()
                    dest_uid = str(dev_dest.states.get('ZP_LocalUID', '')).strip()

                    if not dest_ip or not dest_uid:
                        self.logger.warning(f"⚠️ addPlayersToZone: missing IP/UID for {dev_dest.name}; skipping")
                        continue

                    # Tell the JOINER to join the COORDINATOR
                    self.SOAPSend(
                        dest_ip,
                        "/MediaRenderer",
                        "/AVTransport",
                        "SetAVTransportURI",
                        f"<CurrentURI>x-rincon:{coord_uid}</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>"
                    )

                    # NEW: snap Indigo states for the joiner immediately
                    try:
                        self._update_group_coord(dev_dest, "false", reason="addPlayersToZone(snap) joiner")
                    except Exception:
                        dev_dest.updateStateOnServer("GROUP_Coordinator", "false")
                    dev_dest.updateStateOnServer("Grouped", True)              # boolean
                    dev_dest.updateStateOnServer("GROUP_Name", coord_name)

                    # NEW: suppression window for the joiner as well
                    try:
                        if not hasattr(self, "_suppress_eval_until"):
                            self._suppress_eval_until = {}
                        self._suppress_eval_until[dev_dest.id] = time.time() + 2.0
                    except Exception:
                        pass

                    # (optional) tiny pause helps the stack keep up when adding many at once
                    time.sleep(0.1)

                    #self.refresh_all_group_states()
                    # CHANGED: keep your helper call but it’s usually better *after* the loop to avoid churn.
                    self._refresh_all_group_states_helper(reason="add player to zone")

                #self.refresh_all_group_states()
                # CHANGED: keep your existing end-of-loop refresh; this is the important one
                self._refresh_all_group_states_helper(reason="add player to zone at end after all looped ????")

                # NEW: propagate artwork once the group is formed
                try:
                    self.propagate_artwork_to_slaves(coord_dev)
                except Exception as e:
                    self.logger.debug(f"artwork propagation after addPlayersToZone failed: {e}")

                # NEW: quick targeted reconcile so UI reflects final truth without waiting
                try:
                    self.evaluate_and_update_grouped_states(coord_dev)
                    for item in zones:
                        try:
                            self.evaluate_and_update_grouped_states(indigo.devices[int(item)])
                        except Exception:
                            pass
                except Exception as e:
                    self.logger.debug(f"post-add reconcile failed: {e}")

                self.logger.debug(f"✅ tried refresh at end of 1st add to set base cache ???? ")
                return




            elif action_id == "setStandalone":
                indigo.server.log(f"🔀 Request to remove zone from group: {dev.name}")

                coordinator_dev = self.getCoordinatorDevice(dev)
                coordinator_ip  = coordinator_dev.pluginProps.get("address", "").strip()
                coordinator_uid = coordinator_dev.states.get("ZP_LocalUID", "").strip()

                if not coordinator_ip or not coordinator_uid:
                    self.logger.error(f"❌ Cannot resolve IP or UID for coordinator device: {coordinator_dev.name}")
                    return

                # NEW: resolve the leaver (this action's target) explicitly
                leaver_dev = dev
                leaver_ip  = (leaver_dev.pluginProps.get("address", "") or "").strip()
                leaver_uid = str(leaver_dev.states.get("ZP_LocalUID", "")).strip()
                if not leaver_ip or not leaver_uid:
                    self.logger.error(f"❌ Missing IP/UID for leaver device: {leaver_dev.name}")
                    return

                try:
                    # Send ungrouping command
                    # ORIGINAL (kept for context):
                    # self.SOAPSend(
                    #     coordinator_ip,
                    #     "/MediaRenderer",
                    #     "/AVTransport",
                    #     "BecomeCoordinatorOfStandaloneGroup",
                    #     ""
                    # )
                    #
                    # NEW: Tell the LEAVER to become standalone (Sonos expects the call on the leaver)
                    self.SOAPSend(
                        leaver_ip,
                        "/MediaRenderer",
                        "/AVTransport",
                        "BecomeCoordinatorOfStandaloneGroup",
                        ""
                    )

                    # Give Sonos a moment to act; we’ll still verify via live SoCo below
                    time.sleep(0.4)

                    # Set playback queue on the appropriate device
                    # ORIGINAL logic kept: use the target device's (leaver's) queue
                    target_uid = leaver_dev.states.get("ZP_LocalUID", "").strip()
                    if not target_uid:
                        self.logger.error(f"❌ Missing ZP_LocalUID for {leaver_dev.name}")
                        return

                    # ORIGINAL (kept for context):
                    # self.SOAPSend(
                    #     coordinator_ip,
                    #     "/MediaRenderer",
                    #     "/AVTransport",
                    #     "SetAVTransportURI",
                    #     f"<CurrentURI>x-rincon-queue:{target_uid}#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>"
                    # )
                    #
                    # NEW: apply the queue on the LEAVER (now standalone)
                    self.SOAPSend(
                        leaver_ip,
                        "/MediaRenderer",
                        "/AVTransport",
                        "SetAVTransportURI",
                        f"<CurrentURI>x-rincon-queue:{target_uid}#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>"
                    )

                    # ─────────────────────────────────────────────────────────────
                    # NEW: Read LIVE SoCo topology for both devices to decide Grouped
                    # ─────────────────────────────────────────────────────────────
                    def _live_group_state(ip):
                        soco = self.soco_by_ip.get(ip)
                        grp  = getattr(soco, "group", None) if soco else None
                        if not grp:
                            return (False, None, None)  # treat as standalone unknown
                        members = list(getattr(grp, "members", []) or [])
                        coord   = getattr(grp, "coordinator", None)
                        uid     = getattr(soco, "uid", None)
                        is_coord = (uid is not None and coord and uid == getattr(coord, "uid", None))
                        grouped  = (len(members) >= 2)
                        return (grouped, is_coord, getattr(coord, "player_name", "") if coord else "")
                    
                    # Small converge loop (max ~1.25s) so we don’t race the UI
                    converge_deadline = time.time() + 1.25
                    leaver_grouped = None
                    coord_grouped  = None
                    while time.time() < converge_deadline:
                        lg_grouped, lg_is_coord, lg_name = _live_group_state(leaver_ip)
                        cg_grouped, cg_is_coord, cg_name = _live_group_state(coordinator_ip)
                        if lg_grouped is not None and cg_grouped is not None:
                            # If leaver shows 1-member (grouped False) or we’ve hit the deadline, break
                            if lg_grouped is False or time.time() > converge_deadline - 0.2:
                                leaver_grouped = lg_grouped
                                coord_grouped  = cg_grouped
                                break
                        time.sleep(0.1)
                    if leaver_grouped is None or coord_grouped is None:
                        # Fallback if SoCo wasn’t available: assume sane defaults
                        leaver_grouped = False
                        # Heuristic: if coordinator had at least 2 before, may still be grouped
                        coord_grouped  = True

                    # ─────────────────────────────────────────────────────────────
                    # Snap Indigo states immediately (booleans), using tracer for coord
                    # ─────────────────────────────────────────────────────────────
                    try:
                        self._update_group_coord(leaver_dev, "true", reason="setStandalone(snap)")
                    except Exception:
                        leaver_dev.updateStateOnServer("GROUP_Coordinator", "true")
                    leaver_dev.updateStateOnServer("Grouped", bool(leaver_grouped))  # CHANGED: boolean
                    leaver_dev.updateStateOnServer("GROUP_Name", leaver_dev.name)

                    try:
                        self._update_group_coord(coordinator_dev, "true", reason="setStandalone(snap)")
                    except Exception:
                        coordinator_dev.updateStateOnServer("GROUP_Coordinator", "true")
                    coordinator_dev.updateStateOnServer("Grouped", bool(coord_grouped))  # CHANGED: boolean
                    coordinator_dev.updateStateOnServer("GROUP_Name", coordinator_dev.name)

                    # ─────────────────────────────────────────────────────────────
                    # NEW: prime caches so evaluator doesn’t “re-group” stale members
                    # ─────────────────────────────────────────────────────────────
                    try:
                        # Remove leaver from coordinator bucket
                        if coordinator_dev.name in self.evaluated_group_members_by_coordinator:
                            self.evaluated_group_members_by_coordinator[coordinator_dev.name] = [
                                d for d in self.evaluated_group_members_by_coordinator[coordinator_dev.name]
                                if d.id != leaver_dev.id
                            ]
                        # Place leaver in its own singleton bucket
                        self.evaluated_group_members_by_coordinator[leaver_dev.name] = [leaver_dev]
                    except Exception as e:
                        self.logger.debug(f"cache prime (evaluated_group_members_by_coordinator) failed: {e}")

                    try:
                        # Best-effort prune in zone_group_state_cache
                        for g_uid, g_data in (self.zone_group_state_cache or {}).items():
                            mems = g_data.get("members", [])
                            new_mems = []
                            for m in mems:
                                if isinstance(m, dict):
                                    if str(m.get("uuid", "")).strip() != leaver_uid:
                                        new_mems.append(m)
                                else:
                                    if str(m).strip() != leaver_uid:
                                        new_mems.append(m)
                            g_data["members"] = new_mems
                    except Exception as e:
                        self.logger.debug(f"cache prime (zone_group_state_cache) failed: {e}")

                    # NEW: brief suppression so the next evaluator pass won’t undo snaps
                    try:
                        if not hasattr(self, "_suppress_eval_until"):
                            self._suppress_eval_until = {}
                        now_ts = time.time()
                        self._suppress_eval_until[leaver_dev.id]      = now_ts + 2.0
                        self._suppress_eval_until[coordinator_dev.id] = now_ts + 2.0
                    except Exception:
                        pass

                    #self.refresh_all_group_states()
                    self._refresh_all_group_states_helper(reason="Set Standalone")

                    # NEW: propagate artwork on the reduced group (optional, safe)
                    try:
                        coord_dev_lookup = self.ip_to_indigo_device.get(coordinator_ip)
                        if coord_dev_lookup:
                            self.propagate_artwork_to_slaves(coord_dev_lookup)
                    except Exception as e:
                        self.logger.debug(f"artwork propagation after setStandalone failed: {e}")

                    # NEW: quick targeted reconcile (asks evaluator to recheck these two)
                    try:
                        self.evaluate_and_update_grouped_states(leaver_dev)
                        self.evaluate_and_update_grouped_states(coordinator_dev)
                    except Exception as e:
                        self.logger.debug(f"post-standalone reconcile failed: {e}")

                    self.logger.info(f"✅ {leaver_dev.name} ungrouped and reassigned queue")

                except Exception as e:
                    self.logger.error(f"❌ Failed to set {dev.name} standalone: {e}")
                return





            elif action_id == "ZP_LIST":
                self.actionZP_LIST(pluginAction, dev)
                return

            ############################################################################################
            # Restored action branches — these actions were offered in Actions.xml but their
            # handlers were lost in a refactor, so they all fell through to "Unknown or
            # unsupported action". Semantics follow the original implementation, which matches
            # SoCo / Home Assistant's Sonos integration (SetBass/SetTreble clamp to ±10,
            # night mode via RenderingControl SetEQ, sleep timer via ConfigureSleepTimer,
            # queue via x-rincon-queue, TV input via x-sonos-htastream spdif).
            ############################################################################################

            elif action_id in ("actionBass", "Bass"):
                setting = pluginAction.props.get("setting")
                try:
                    new_bass = max(-10, min(10, int(setting)))
                except (TypeError, ValueError):
                    self.logger.error(f"❌ Invalid bass value '{setting}' for {dev.name} (expected -10..10)")
                    return
                current_bass = dev.states.get("ZP_BASS", "0")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetBass", f"<DesiredBass>{new_bass}</DesiredBass>")
                self.logger.info(f"ZonePlayer: {dev.name}, Current Bass: {current_bass}, New Bass: {new_bass}")
                return

            elif action_id in ("actionTreble", "Treble"):
                setting = pluginAction.props.get("setting")
                try:
                    new_treble = max(-10, min(10, int(setting)))
                except (TypeError, ValueError):
                    self.logger.error(f"❌ Invalid treble value '{setting}' for {dev.name} (expected -10..10)")
                    return
                current_treble = dev.states.get("ZP_TREBLE", "0")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetTreble", f"<DesiredTreble>{new_treble}</DesiredTreble>")
                self.logger.info(f"ZonePlayer: {dev.name}, Current Treble: {current_treble}, New Treble: {new_treble}")
                return

            elif action_id in ("actionNightMode", "NightMode"):
                setting = pluginAction.props.get("setting")
                mode = 1 if setting in (True, "true", "True", 1, "1", "on") else 0
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetEQ", f"<EQType>NightMode</EQType><DesiredValue>{mode}</DesiredValue>")
                self.logger.info(f"ZonePlayer: {dev.name}, Night Mode: {bool(mode)}")
                return

            # --- HA-parity soundbar/EQ controls (RenderingControl SetEQ, same EQ types SoCo uses) ---

            elif action_id in ("actionSpeechEnhancement", "SpeechEnhancement"):
                setting = pluginAction.props.get("setting")
                mode = 1 if setting in (True, "true", "True", 1, "1", "on") else 0
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetEQ", f"<EQType>DialogLevel</EQType><DesiredValue>{mode}</DesiredValue>")
                self.logger.info(f"ZonePlayer: {dev.name}, Speech Enhancement: {bool(mode)}")
                return

            elif action_id in ("actionAudioDelay", "AudioDelay"):
                setting = pluginAction.props.get("setting")
                try:
                    delay = max(0, min(5, int(setting)))
                except (TypeError, ValueError):
                    self.logger.error(f"❌ Invalid audio delay '{setting}' for {dev.name} (expected 0..5)")
                    return
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetEQ", f"<EQType>AudioDelay</EQType><DesiredValue>{delay}</DesiredValue>")
                self.logger.info(f"ZonePlayer: {dev.name}, Audio Delay: {delay}")
                return

            elif action_id in ("actionSurroundEnable", "SurroundEnable"):
                setting = pluginAction.props.get("setting")
                mode = 1 if setting in (True, "true", "True", 1, "1", "on") else 0
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetEQ", f"<EQType>SurroundEnable</EQType><DesiredValue>{mode}</DesiredValue>")
                self.logger.info(f"ZonePlayer: {dev.name}, Surround Speakers: {'enabled' if mode else 'disabled'}")
                return

            elif action_id in ("actionSurroundLevel", "SurroundLevel"):
                setting = pluginAction.props.get("setting")
                try:
                    level = max(-15, min(15, int(setting)))
                except (TypeError, ValueError):
                    self.logger.error(f"❌ Invalid surround level '{setting}' for {dev.name} (expected -15..15)")
                    return
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetEQ", f"<EQType>SurroundLevel</EQType><DesiredValue>{level}</DesiredValue>")
                self.logger.info(f"ZonePlayer: {dev.name}, Surround Level (TV): {level}")
                return

            elif action_id in ("actionMusicSurroundLevel", "MusicSurroundLevel"):
                setting = pluginAction.props.get("setting")
                try:
                    level = max(-15, min(15, int(setting)))
                except (TypeError, ValueError):
                    self.logger.error(f"❌ Invalid music surround level '{setting}' for {dev.name} (expected -15..15)")
                    return
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetEQ", f"<EQType>MusicSurroundLevel</EQType><DesiredValue>{level}</DesiredValue>")
                self.logger.info(f"ZonePlayer: {dev.name}, Surround Level (Music): {level}")
                return

            elif action_id in ("actionMusicFullVolume", "MusicFullVolume"):
                setting = pluginAction.props.get("setting")
                mode = 1 if setting in (True, "true", "True", 1, "1", "on") else 0  # 1 = full volume, 0 = ambient
                self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetEQ", f"<EQType>SurroundMode</EQType><DesiredValue>{mode}</DesiredValue>")
                self.logger.info(f"ZonePlayer: {dev.name}, Music on Surrounds: {'full volume' if mode else 'ambient'}")
                return

            elif action_id in ("actionZP_Queue", "ZP_Queue"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = coordinator_dev.pluginProps.get("address", "").strip()
                    dev_src_LocalUID = coordinator_dev.states['ZP_LocalUID']
                else:
                    dev_src_LocalUID = dev.states['ZP_LocalUID']
                if zoneIP and dev_src_LocalUID:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", f"<CurrentURI>x-rincon-queue:{dev_src_LocalUID}#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                    indigo.server.log("ZonePlayer: %s, Play Queue" % dev.name)
                else:
                    self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP Queue' not actioned as Zone IP cannot be resolved!")
                return

            elif action_id in ("actionZP_sleepTimer", "ZP_sleepTimer"):
                if dev.states["GROUP_Coordinator"] == "false":
                    zoneIP = coordinator_dev.pluginProps.get("address", "").strip()
                if zoneIP:
                    duration = pluginAction.props.get("setting", "")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "ConfigureSleepTimer", f"<NewSleepTimerDuration>{duration}</NewSleepTimerDuration>")
                    self.logger.info(f"ZonePlayer: {dev.name}, Sleep Timer set to: {duration or 'off'}")
                else:
                    self.logger.warning(f"ZonePlayer: {dev.name}, 'ZP Sleep Timer' not actioned as Zone IP cannot be resolved!")
                return

            elif action_id in ("actionZP_TV", "ZP_TV"):
                local_uid = str(dev.states.get('ZP_LocalUID', '')).strip()
                if not local_uid:
                    self.logger.error(f"❌ {dev.name} has no ZP_LocalUID; cannot switch to TV input.")
                    return
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>x-sonos-htastream:"+local_uid+":spdif</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" xmlns:r=\"urn:schemas-rinconnetworks-com:metadata-1-0/\" xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\"&gt;&lt;item id=\"spdif-input\" parentID=\"0\" restricted=\"false\"&gt;&lt;dc:title&gt;"+local_uid+"&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioItem&lt;/upnp:class&gt;&lt;res protocolInfo=\"spdif\"&gt;x-sonos-htastream:"+local_uid+":spdif&lt;/res&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData>")
                self.logger.info(f"📺 {dev.name}: switched to TV input")
                return

            elif action_id in ("actionZP_DumpURI", "ZP_DumpURI"):
                MediaInfo = self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "GetMediaInfo", "")
                PositionInfo = self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "GetPositionInfo", "")
                self.logger.info(f"ZonePlayer: {zoneIP}, {dev.name}")
                self.logger.info(f"MediaInfo: {MediaInfo}")
                self.logger.info(f"PositionInfo: {PositionInfo}")
                return

            # If it gets this far, action was not handled
            self.logger.warning(f"⚠️ Unknown or unsupported action: {action_id}")
            return

        except Exception as e:
            self.logger.error(f"❌ actionDirect exception: {e}")








    ############################################################################################
    ### Handleaction definitions
    ############################################################################################



    def old_handleAction_ZP_addPlayerToZone(self, pluginAction, dev, zoneIP):
        try:
            dev_dest = indigo.devices[int(pluginAction.props.get("setting"))]
            target_uid = str(dev.states.get('ZP_LocalUID', '')).strip()
            target_ip = dev_dest.pluginProps.get("address", "").strip()

            self.logger.warning(f"🔗 Requested: Add {dev.name} to group with {dev_dest.name}")
            self.logger.warning(f"🔍 UID={target_uid}, IP={target_ip}")

            if not target_uid or not target_ip:
                self.logger.error(f"❌ Missing required UID or IP for joining zone: UID={target_uid}, IP={target_ip}")
            else:
                self.logger.info(f"➕ Adding {dev.name} to group led by {dev_dest.name} @ {target_ip}")
                self.SOAPSend(
                    target_ip,
                    "/MediaRenderer",
                    "/AVTransport",
                    "SetAVTransportURI",
                    f"<CurrentURI>x-rincon:{target_uid}</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>"
                )
            self.refresh_all_group_states()
        except Exception as e:
            self.logger.error(f"❌ actionZP_addPlayerToZone failed: {e}")


    def old2_handleAction_ZP_addPlayerToZone(self, pluginAction, dev, zoneIP):
        """
        ALT semantics:
          - 'Device' (dev)        → JOINER (the one that will join a group)
          - 'Zone'   (dev_coord)  → COORDINATOR (leader of the group)
        """
        try:
            # Coordinator is chosen in the popup
            dev_coord = indigo.devices[int(pluginAction.props.get("setting"))]   # coordinator
            dev_join  = dev                                                     # joiner (selected Device)

            coord_uid = str(dev_coord.states.get('ZP_LocalUID', '')).strip()
            joiner_ip = dev_join.pluginProps.get("address", "").strip()

            self.logger.debug("🧪 ADD PLAYER TO ZONE DEBUG (Device=JOINER)")
            self.logger.debug(f"   Coordinator: {dev_coord.name}, ip={dev_coord.pluginProps.get('address','?')}, uid={coord_uid}")
            self.logger.debug(f"   Joiner     : {dev_join.name}, ip={joiner_ip}, uid={dev_join.states.get('ZP_LocalUID','?')}")
            self.logger.debug(f"   SOAP target_ip={joiner_ip}, x-rincon={coord_uid}")

            if not coord_uid or not joiner_ip:
                self.logger.error(f"❌ Missing values: coord_uid='{coord_uid}', joiner_ip='{joiner_ip}'")
                return

            # Tell the JOINER to join the COORDINATOR
            self.SOAPSend(
                joiner_ip,
                "/MediaRenderer",
                "/AVTransport",
                "SetAVTransportURI",
                f"<CurrentURI>x-rincon:{coord_uid}</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>"
            )


            self.logger.debug(f"[addPlayer snap] Setting {dev_coord.name} as Coord=true, {dev_join.name} as Coord=false")




            # Snap Indigo states to expected truth immediately
            self.logger.debug(f"[addPlayer snap] Setting {dev_coord.name} as Coord=true, {dev_join.name} as Coord=false")

            # ⬇️ use wrapper so the write is traced
            self._update_group_coord(dev_coord, "true",  reason="addPlayerToZone(snap)")
            dev_coord.updateStateOnServer("Grouped", True)
            dev_coord.updateStateOnServer("GROUP_Name", dev_coord.name)

            self._update_group_coord(dev_join,  "false", reason="addPlayerToZone(snap)")
            dev_join.updateStateOnServer("Grouped", True)
            dev_join.updateStateOnServer("GROUP_Name", dev_coord.name)


            # Snap Indigo states to expected truth immediately

            #dev_coord.updateStateOnServer("GROUP_Coordinator", "true")
            #dev_coord.updateStateOnServer("Grouped", True)
            #dev_coord.updateStateOnServer("GROUP_Name", dev_coord.name)

            #dev_join.updateStateOnServer("GROUP_Coordinator", "false")
            #dev_join.updateStateOnServer("Grouped", True)
            #dev_join.updateStateOnServer("GROUP_Name", dev_coord.name)

            # ✅ Align vars for artwork propagation
            coord_ip  = dev_coord.pluginProps.get("address", "").strip()
            coord_dev = self.ip_to_indigo_device.get(coord_ip)

            self.propagate_artwork_to_slaves(coord_dev)

            self.logger.info(f"🏷 Coordinator → {dev_coord.name}, Member → {dev_join.name}")



        except Exception as e:
            self.logger.error(f"❌ actionZP_addPlayerToZone failed: {e}")






    def handleAction_ZP_addPlayerToZone(self, pluginAction, dev, zoneIP):
        """
        ALT semantics:
          - 'Device' (dev)        → JOINER (the one that will join a group)
          - 'Zone'   (dev_coord)  → COORDINATOR (leader of the group)
        """
        try:
            # Coordinator is chosen in the popup
            dev_coord = indigo.devices[int(pluginAction.props.get("setting"))]   # coordinator
            dev_join  = dev                                                     # joiner (selected Device)

            coord_uid = str(dev_coord.states.get('ZP_LocalUID', '')).strip()
            joiner_ip = dev_join.pluginProps.get("address", "").strip()

            self.logger.debug("🧪 ADD PLAYER TO ZONE DEBUG (Device=JOINER)")
            self.logger.debug(f"   Coordinator: {dev_coord.name}, ip={dev_coord.pluginProps.get('address','?')}, uid={coord_uid}")
            self.logger.debug(f"   Joiner     : {dev_join.name}, ip={joiner_ip}, uid={dev_join.states.get('ZP_LocalUID','?')}")
            self.logger.debug(f"   SOAP target_ip={joiner_ip}, x-rincon={coord_uid}")

            if not coord_uid or not joiner_ip:
                self.logger.error(f"❌ Missing values: coord_uid='{coord_uid}', joiner_ip='{joiner_ip}'")
                return

            # Tell the JOINER to join the COORDINATOR
            self.SOAPSend(
                joiner_ip,
                "/MediaRenderer",
                "/AVTransport",
                "SetAVTransportURI",
                f"<CurrentURI>x-rincon:{coord_uid}</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>"
            )

            self.logger.debug(f"[addPlayer snap] Setting {dev_coord.name} as Coord=true, {dev_join.name} as Coord=false")

            # ---------------------------------------------------------------------
            # Snap Indigo states to expected truth immediately
            # ---------------------------------------------------------------------
            self.logger.debug(f"[addPlayer snap] Setting {dev_coord.name} as Coord=true, {dev_join.name} as Coord=false")

            try:
                # Prefer coordinator's friendly group name (fallback to device name)
                coord_ip   = (dev_coord.pluginProps.get("address", "") or "").strip()
                coord_soco = self.soco_by_ip.get(coord_ip)
                if coord_soco and getattr(coord_soco, "group", None) and getattr(coord_soco.group, "coordinator", None):
                    group_friendly = getattr(coord_soco.group.coordinator, "player_name", None) or dev_coord.states.get("GROUP_Name") or dev_coord.name
                else:
                    group_friendly = dev_coord.states.get("GROUP_Name") or dev_coord.name

                # ⬇️ use canonical writer so guards/tracing apply
                self._set_group_states(
                    dev_coord,
                    grouped=True,
                    is_coord=True,
                    group_name=group_friendly,
                )
                self._set_group_states(
                    dev_join,
                    grouped=True,
                    is_coord=False,
                    group_name=group_friendly,
                )

                # -----------------------------------------------------------------
                # Prime caches so the first evaluate pass can't flip Grouped back
                # -----------------------------------------------------------------
                try:
                    # 1) evaluated_group_members_by_coordinator
                    self.evaluated_group_members_by_coordinator = getattr(self, "evaluated_group_members_by_coordinator", {}) or {}
                    self.evaluated_group_members_by_coordinator.setdefault(group_friendly, [])
                    for d in (dev_coord, dev_join):
                        if all(x.id != d.id for x in self.evaluated_group_members_by_coordinator[group_friendly]):
                            self.evaluated_group_members_by_coordinator[group_friendly].append(d)

                    # 2) zone_group_state_cache: ensure coordinator+members are represented
                    self.zone_group_state_cache = getattr(self, "zone_group_state_cache", {}) or {}
                    grp_uid = None
                    if coord_soco and getattr(coord_soco, "group", None):
                        grp_uid = getattr(coord_soco.group, "uid", None)
                    cache_key = grp_uid or group_friendly
                    entry = self.zone_group_state_cache.setdefault(cache_key, {"coordinator": None, "members": []})

                    if coord_soco and getattr(coord_soco, "uid", None):
                        entry["coordinator"] = coord_soco.uid

                    def _ensure_member(dev_obj):
                        ip = (dev_obj.pluginProps.get("address", "") or "").strip()
                        soco = self.soco_by_ip.get(ip)
                        uuid = getattr(soco, "uid", None)
                        name = dev_obj.states.get("GROUP_Name") or dev_obj.name
                        # Store as dicts; evaluator handles dict members
                        if uuid and not any((m.get("uuid") if isinstance(m, dict) else m) == uuid for m in entry["members"]):
                            entry["members"].append({"uuid": uuid, "ip": ip, "name": name})

                    _ensure_member(dev_coord)
                    _ensure_member(dev_join)
                except Exception as cache_e:
                    self.logger.debug(f"addPlayer snapshot cache prime failed: {cache_e}")

            except Exception as snap_e:
                self.logger.debug(f"addPlayer snapshot grouped write failed: {snap_e}")

            # Snap Indigo states to expected truth immediately

            #dev_coord.updateStateOnServer("GROUP_Coordinator", "true")
            #dev_coord.updateStateOnServer("Grouped", True)
            #dev_coord.updateStateOnServer("GROUP_Name", dev_coord.name)

            #dev_join.updateStateOnServer("GROUP_Coordinator", "false")
            #dev_join.updateStateOnServer("Grouped", True)
            #dev_join.updateStateOnServer("GROUP_Name", dev_coord.name)

            # ✅ Align vars for artwork propagation
            coord_ip  = dev_coord.pluginProps.get("address", "").strip()
            coord_dev = self.ip_to_indigo_device.get(coord_ip)

            self.propagate_artwork_to_slaves(coord_dev)

            self.logger.info(f"🏷 Coordinator → {dev_coord.name}, Member → {dev_join.name}")

            # Optional but recommended: reconcile immediately so nothing flips back on the next tick
            try:
                self.evaluate_and_update_grouped_states(dev=dev_coord)
            except Exception as e:
                self.logger.debug(f"post-add evaluate failed: {e}")

        except Exception as e:
            self.logger.error(f"❌ actionZP_addPlayerToZone failed: {e}")









    def safe_debug(self, message):
        try:
            if self.logger.isEnabledFor(logging.DEBUG):
                try:
                    # Force the message to safe UTF-8
                    if isinstance(message, bytes):
                        message = message.decode("utf-8", errors="replace")
                    elif not isinstance(message, str):
                        message = str(message)

                    message = message.encode('utf-8', errors='replace').decode('utf-8', errors='replace')

                    self.logger.debug(message)
                except Exception as inner_e:
                    try:
                        # Try logging something minimal if formatting fails
                        self.logger.warning(f"⚠️ Failed to log debug message safely: {inner_e}")
                    except Exception:
                        pass
        except Exception:
            pass  # Absolute last resort: don't let even logging crash



    def refresh_transport_state(self, zone_ip):
        """
        Refresh the transport state for a given zone IP by querying the current state
        and updating relevant Indigo device states (ZP_STATE, etc.).
        This helps reestablish correct state after volume or mute changes that cause Sonos to misreport sources.
        """
        try:
            speaker = self.getSoCoDeviceByIP(zone_ip)
            if not speaker:
                self.logger.warning(f"⚠️ Cannot refresh transport state — no SoCo device found for {zone_ip}")
                return

            state = speaker.get_current_transport_info().get("current_transport_state", "").upper()
            dev = next((d for d in indigo.devices.iter("self") if d.address == zone_ip), None)

            if dev:
                dev.updateStateOnServer("ZP_STATE", state)
                dev.updateStateOnServer("State", state)
                self.logger.debug(f"🔄 Refreshed transport state for {dev.name}: {state}")
            else:
                self.logger.warning(f"⚠️ No Indigo device matched to IP {zone_ip} during refresh")

        except Exception as e:
            self.logger.error(f"❌ refresh_transport_state failed for {zone_ip}: {e}")





    def handleAction_ZP_Pandora(self, pluginAction, dev, zoneIP, props):
        try:
            station_id = pluginAction.props.get("setting") or pluginAction.props.get("channelSelector")
            self.logger.debug(f"🧪 handleAction_ZP_Pandora() called — device: {dev.name} | zoneIP: {zoneIP}")
            self.logger.debug(f"🪪 Extracted Pandora station ID: {station_id}")

            if not station_id:
                self.logger.warning(f"⚠️ No Pandora station ID provided for device ID {dev.id}")
                return

            global Sonos_Pandora
            if not Sonos_Pandora:
                self.logger.warning("⚠️ Sonos_Pandora is empty — attempting fallback reload...")
                self.logger.warning(f"🔍 Pandora enabled: {self.Pandora} | Email: {self.PandoraEmailAddress} | Password: {'***' if self.PandoraPassword else '(empty)'}")
                if self.Pandora and self.PandoraEmailAddress and self.PandoraPassword:
                    Sonos_Pandora = []  # 🔄 Force clear to ensure overwrite
                    self.getPandora(self.PandoraEmailAddress, self.PandoraPassword, self.PandoraNickname)
                else:
                    self.logger.warning("⚠️ Pandora credentials incomplete — skipping reload.")

            self.safe_debug(f"🧾 Known Sonos_Pandora entries: {Sonos_Pandora}")
            self.safe_debug(f"🧾 Known Sonos_Pandora IDs: {[s[0] for s in Sonos_Pandora]}")

            # Retry lookup after fallback
            matching_station = next((s for s in Sonos_Pandora if s[0] == station_id), None)
            if not matching_station:
                self.logger.warning(f"⚠️ Unknown Pandora station ID: {station_id}")
                return

            station_name = matching_station[1]
            nickname = matching_station[3] or ""

            uri = f"x-sonosapi-radio:ST%3a{station_id}?sid=236&flags=8296&sn=1"
            metadata = f"""<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/"
                                       xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/"
                                       xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/"
                                       xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">
                <item id="100c2068ST%3a{station_id}" parentID="10fe2064myStations" restricted="true">
                    <dc:title>{station_name}</dc:title>
                    <upnp:class>object.item.audioItem.audioBroadcast.#station</upnp:class>
                    <r:description>My Stations</r:description>
                    <desc id="cdudn" nameSpace="urn:schemas-rinconnetworks-com:metadata-1-0/">
                        SA_RINCON60423_X_#Svc60423-0-Token
                    </desc>
                </item>
            </DIDL-Lite>"""

            self.logger.info(f"📻 Sending {dev.name} to Pandora station: {station_name} ({station_id})")

            soco_dev = self.soco_by_ip.get(zoneIP)
            if not soco_dev:
                self.logger.warning(f"⚠️ soco_device is None for zoneIP {zoneIP}")
                return

            soco_dev.avTransport.SetAVTransportURI([
                ('InstanceID', 0),
                ('CurrentURI', uri),
                ('CurrentURIMetaData', metadata),
            ])
            soco_dev.play()

        except Exception as e:
            self.logger.error(f"❌ handleAction_ZP_Pandora failed for device ID {dev.id}: {e}")







    def handleAction_SetSiriusXMChannel(self, pluginAction, dev, zoneIP):
        try:
            #self.safe_debug(f"🔍 This is the channelselector at handleAction_SetSiriusXMChannel: {channelSelector})")
            #self.safe_debug(f"🔍 This is the channelselector at handleAction_SetSiriusXMChannel: {channel})")
            channel_id = pluginAction.props.get("channelSelector", "")
            #self.safe_debug(f"🪪 handleAction_SetSiriusXMChannel() called for device {dev.name} at {zoneIP}")
            self.safe_debug(f"🔍 pluginAction.props: {pluginAction.props}")
            self.safe_debug(f"🔍 Extracted channel_id: '{channel_id}'")

            if not channel_id:
                self.logger.error("❌ No channel ID provided from control page (pluginAction.props[\"channelSelector\"] was empty)")
                return

            channel = self.siriusxm_id_map.get(channel_id)
            if not channel:
                self.logger.error(f"❌ Channel ID '{channel_id}' not found in siriusxm_id_map.")
                self.safe_debug(f"🧪 Current siriusxm_id_map keys: {list(self.siriusxm_id_map.keys())[:10]}... ({len(self.siriusxm_id_map)} total)")
                return

            cname = f"{channel.get('channelNumber')} - {channel.get('name')}"
            guid = channel.get("guid")

            self.logger.warning(f"📡 Sending SiriusXM channel: {cname} (GUID: {guid}) to zone: {zoneIP}")
            self.sendSiriusXMChannel(zoneIP, guid, cname)

        except Exception as e:
            self.logger.error(f"❌ handleAction_SetSiriusXMChannel() failed: {e}")


 

    def handleAction_ZP_SiriusXM(self, pluginAction, dev, zoneIP, props):
        try:
            guid = pluginAction.props.get("channelSelector")
            if not guid:
                # Forwarded from a Sonos Favorite: props carry the URI fragment in
                # "setting" (e.g. "channel-linear:<guid>") rather than a channelSelector.
                setting = pluginAction.props.get("setting", "") or ""
                m = re.search(r'channel-linear[:%3a]+([0-9a-fA-F\-]{16,})', setting, re.IGNORECASE)
                if m:
                    guid = m.group(1)
                    self.logger.debug(f"📻 Resolved SiriusXM GUID {guid} from favorite URI fragment")
            if not guid:
                self.logger.warning(f"⚠️ No SiriusXM GUID provided for device ID {dev.id}")
                return

            channel = self.siriusxm_guid_map.get(guid)
            if not channel:
                self.logger.warning(f"⚠️ Unknown channel GUID: {guid} — falling back to generic title")
                title = f"SiriusXM {guid}"
                album_art = None
            else:
                title = f"CH {channel.get('channel_number', '?')} - {channel.get('title', 'Unknown')}"
                album_art = channel.get("albumArtURI", None)

            uri, metadata = self.build_siriusxm_uri_and_metadata(guid, title, album_art)

            self.logger.info(f"📻 Sending {dev.name} to SiriusXM: {title} ({guid})")

            soco_dev = self.get_soco_device(zoneIP)  # cache first, direct SoCo(ip) fallback
            if not soco_dev:
                self.logger.warning(f"⚠️ soco_device is None for zoneIP {zoneIP}")
                return

            soco_dev.avTransport.SetAVTransportURI([
                ('InstanceID', 0),
                ('CurrentURI', uri),
                ('CurrentURIMetaData', metadata),
            ])
            soco_dev.play()

            self.last_siriusxm_guid_by_dev[dev.id] = guid

        except Exception as e:
            self.logger.error(f"❌ handleAction_ZP_SiriusXM failed for device ID {dev.id}: {e}")


    def handleAction_TestHardcodedYachtRock(self, pluginAction, dev, zoneIP):
        self.sendSiriusXMChannel(zoneIP,
            "9150cc82-af5c-3be3-d170-0e81d87375a8",  # GUID
            "CH 15 - Yacht Rock Radio"
        )




    def handleAction_ZP_setStandalone(self, pluginAction, dev, zoneIP):
        try:
            self.logger.info(f"📤 Attempting to make {dev.name} standalone...")

            from soco import SoCo
            import time

            soco_dev = SoCo(zoneIP)

            # Log group composition
            group = soco_dev.group
            member_names = [m.player_name for m in group.members]
            self.logger.info(f"🧩 {dev.name} is grouped with: {member_names}")

            # If this device is the coordinator and has other members, break the group
            if soco_dev.is_coordinator and len(group.members) > 1:
                self.logger.info(f"🔁 {dev.name} is coordinator and has other members — breaking group.")
                try:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "BecomeCoordinatorOfStandaloneGroup", "")
                    time.sleep(0.5)
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed BecomeCoordinatorOfStandaloneGroup SOAP call: {e}")
                self.logger.info(f"✅ ZonePlayer: {dev.name} is now standalone.")
                return  # ✅ Exit early to avoid SetAVTransportURI error

            # (Optional) Check URI to confirm if still grouped via x-rincon
            current_uri = dev.states.get("ZP_CurrentTrackURI", "")
            if current_uri.startswith("x-rincon:"):
                self.logger.info(f"ℹ️ {dev.name} still grouped via URI {current_uri}, skipping queue setup.")
                return

            self.logger.info(f"✅ ZonePlayer: {dev.name} is already standalone.")

        except Exception as e:
            self.logger.error(f"❌ Exception in handleAction_ZP_setStandalone: {e}")


    def handleAction_ChannelUp(self, pluginAction, dev, props):
        self.channelUpOrDown(dev, direction="up")

    def handleAction_ChannelDown(self, pluginAction, dev, props):
        self.channelUpOrDown(dev, direction="down")
 
    def handleAction_Q_Crossfade(self, pluginAction, dev):
        try:
            from soco import SoCo

            zone_ip = dev.address
            crossfade_enabled = pluginAction.props.get("setting", False)
            crossfade_bool = bool(crossfade_enabled in ["true", "True", True])

            self.logger.warning(f"🔁 Setting crossfade on {dev.name} ({zone_ip}) to {crossfade_bool}")

            speaker = SoCo(zone_ip)
            speaker.cross_fade = crossfade_bool

            self.logger.info(f"✅ Crossfade set to {crossfade_bool} on {dev.name}")

            # Optionally update Indigo state if you track it
            dev.updateStateOnServer("Q_Crossfade", "true" if crossfade_bool else "false")

        except Exception as e:
            self.logger.error(f"❌ Failed to set crossfade on {dev.name}: {e}")


    def handleAction_Q_Shuffle(self, pluginAction, dev, zoneIP):
        try:
            setting = pluginAction.props.get("setting", False)
            if isinstance(setting, str):
                setting = setting.lower() in ["true", "1", "yes"]

            play_mode = "SHUFFLE_NOREPEAT" if setting else "NORMAL"

            self.logger.warning(f"🔀 Setting shuffle on {dev.name} ({zoneIP}) to {play_mode}")

            current_uri = dev.states.get("ZP_CurrentTrackURI", "") or dev.states.get("ZP_AVTransportURI", "")
            self.safe_debug(f"🔍 Current URI for shuffle check: {current_uri}")

            if not self.isShuffleSupported(current_uri):
                self.logger.warning(f"⚠️ Skipping SetPlayMode on {dev.name} — unsupported stream type: {current_uri}")
                return

            try:
                self.SOAPSend(
                    zoneIP,
                    "/MediaRenderer",
                    "/AVTransport",
                    "SetPlayMode",
                    f"<InstanceID>0</InstanceID><NewPlayMode>{play_mode}</NewPlayMode>"
                )
                self.logger.info(f"✅ Shuffle set to {play_mode} on {dev.name}")
            except Exception as e:
                if "errorCode>712" in str(e):
                    self.logger.warning(f"⚠️ Shuffle not supported on current stream for {dev.name} (UPnP error 712)")
                else:
                    raise  # re-raise other errors

        except Exception as e:
            self.logger.error(f"❌ handleAction_Q_Shuffle failed for {dev.name}: {e}")



    def isShuffleSupported(self, uri):
        unsupported_prefixes = [
            "x-sonosapi-radio:",  # Pandora
            "x-sonosapi-hls:",    # SiriusXM
            "x-sonos-htastream:", # TV
            "x-rincon-mp3radio:"  # TuneIn or raw streams
        ]
        return not any(uri.startswith(pfx) for pfx in unsupported_prefixes)

    ### End of Handleaction definitions


    ############################################################################################
    ### General methods / functions  that can be called in the SonosPlugin Class
    ############################################################################################



    def _devices(self):
        """Return the Indigo devices collection, preferring self.devices if present."""
        try:
            return self.devices if self.devices is not None else indigo.devices
        except Exception:
            return indigo.devices


    def actionQ_Shuffle(self, pluginAction, dev):
        try:
            setting = pluginAction.props.get("setting", False)
            if isinstance(setting, str):
                setting = setting.lower() == "true"

            zoneIP = dev.address
            self.logger.warning(f"🔀 Setting shuffle on {dev.name} ({zoneIP}) to {setting}")

            self.SOAPSend(
                zoneIP,
                "/MediaRenderer",
                "/AVTransport",
                "SetPlayMode",
                f"<NewPlayMode>{'SHUFFLE' if setting else 'NORMAL'}</NewPlayMode>"
            )

            dev.updateStateOnServer("Q_Shuffle", setting)
            self.logger.info(f"✅ Shuffle set to {setting} on {dev.name}")

        except Exception as e:
            self.logger.error(f"❌ Failed to set shuffle: {e}")



    def getZonePlayerByName(self, name):
        for zp in self.ZonePlayers:
            if zp.player_name == name:
                return zp
        self.logger.warning(f"⚠️ getZonePlayerByName(): No matching player found for name: {name}")
        return None



    def normalize_channel_dict(self, ch: XMChannel, streamUrl=None, albumArtURI=None, guidStreamValid=False):
        try:
            # Use only known-safe attributes
            chan_number_raw = getattr(ch, "channel_number", None) or ""
            chan_number_str = str(chan_number_raw).strip()

            try:
                chan_number_int = int(chan_number_str)
            except ValueError:
                self.logger.warning(f"🚫 Skipping malformed channel: {ch.name} — channel_number = '{chan_number_str}'")
                chan_number_int = None

            return {
                "id": ch.id,
                "guid": ch.guid,
                "channelNumber": chan_number_int,
                "channel_number": chan_number_int,  # for sorting
                "channel_number_str": chan_number_str,  # for diagnostics
                "name": ch.name,
                "shortDescription": ch.short_description,
                "longDescription": ch.long_description,
                "category": ch.category_name,
                "isFavorite": ch.is_favorite,
                "streamUrl": streamUrl,
                "albumArtURI": albumArtURI,
                "guidStreamValid": guidStreamValid,
                "fallbackStreamValid": bool(streamUrl),
                "channelType": getattr(ch, "channel_type", "audio"),
            }

        except Exception as e:
            self.logger.error(f"❌ normalize_channel_dict failed for channel {getattr(ch, 'name', 'UNKNOWN')}: {e}")
            return {}


    def load_siriusxm_channel_data(self):
        self.logger.info("🧪 ENTERED load_siriusxm_channel_data()")

        import os
        import json
        from sxm import SXMClient, RegionChoice, XMChannel

        def patched_from_dict(data):
            category_name = ""
            if "categories" in data and "categories" in data["categories"]:
                category_list = data["categories"]["categories"]
                if category_list and isinstance(category_list, list):
                    category_name = category_list[0].get("name", "")
            return XMChannel(
                id=data.get("id") or data.get("channelId", ""),
                name=data.get("name", ""),
                channel_number=data.get("channelNumber") or data.get("xmChannelNumber", ""),
                guid=data.get("guid") or data.get("channelGuid", ""),
                short_description=data.get("shortDescription", ""),
                long_description=data.get("longDescription", ""),
                category_name=category_name,
                is_favorite=data.get("isFavorite", False),
            )

        XMChannel.from_dict = staticmethod(patched_from_dict)

        cache_path = os.path.join(indigo.server.getInstallFolderPath(), "Preferences", "Plugins", "siriusxm_channel_cache.json")
        self.logger.info("📂 Checking for SiriusXM channel cache...")

        sxm_username = self.pluginPrefs.get("SiriusXMID", "").strip()
        sxm_password = self.pluginPrefs.get("SiriusXMPassword", "").strip()

        if not sxm_username or not sxm_password:
            self.logger.warning("⚠️ SiriusXM credentials not provided in plugin preferences")
            return

        # Always initialize the client
        self.siriusxm = SXMClient(username=sxm_username, password=sxm_password, region=RegionChoice.US)

        # ✅ Load cache if present
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    self.siriusxm_channels = json.load(f)
                self.logger.info(f"📦 Loaded existing SiriusXM channel cache — {len(self.siriusxm_channels)} channels")

                # 🔍 Debug first few entries
                self.safe_debug("🧪 Dumping first 5 SiriusXM cache entries for inspection:")
                for i, ch in enumerate(self.siriusxm_channels[:5]):
                    self.safe_debug(f"  📦 [{i}] Type: {type(ch)} — Value: {repr(ch)}")

                # ✅ Validate all entries are dicts
                invalid_entries = [i for i, ch in enumerate(self.siriusxm_channels) if not isinstance(ch, dict)]
                if invalid_entries:
                    self.logger.error(f"🚨 SiriusXM cache is corrupted — invalid entries at indexes: {invalid_entries}")
                    self.siriusxm_channels = []
                    self.refreshSiriusXMChannelCache()
                    return

                self.logger.info("⏭️ Skipping live SiriusXM fetch — enriching cached data.")
                self.fetch_and_enrich_channels()
                self.logger.info("✅ EXITING load_siriusxm_channel_data() (cache mode)")
                return

            except Exception as e:
                self.logger.warning(f"⚠️ Cache exists but failed to load: {e}")
                self.logger.info("🔁 Proceeding with live fetch due to cache failure.")

        # ✅ Live fetch if no cache or failed
        try:
            if not self.siriusxm.authenticate():
                self.logger.error("❌ SiriusXM authentication failed.")
                return

            self.logger.info("✅ SiriusXM login successful — fetching channel list...")
            self.fetch_and_enrich_channels()

            # 💾 Save updated cache
            self.logger.info("💾 Saving SiriusXM channel cache...")
            try:
                with open(cache_path, "w") as f:
                    json.dump(self.siriusxm_channels, f, indent=2)
                self.logger.info(f"✅ Cache saved: {cache_path}")
            except Exception as e:
                self.logger.error(f"❌ Failed to save SiriusXM cache: {e}")

        except Exception as e:
            self.logger.error(f"💥 SiriusXM init error: {e}")

        self.logger.info("✅ EXITING load_siriusxm_channel_data() (live mode)")




    def query_siriusxm_channel(self, query):
        """
        Query channel by number (int/str), name (case-insensitive), or ID.
        Returns dict with channel info or None.
        """
        for ch in self.siriusxm_channels:
            if str(ch["channelNumber"]) == str(query):
                return ch
            if ch["name"].lower() == str(query).lower():
                return ch
            if ch["id"] == query:
                return ch
        return None



    def load_siriusxm_cache(self):
        cache_path = os.path.join(indigo.server.getInstallFolderPath(), "Preferences", "Plugins", "siriusxm_channel_cache.json")

        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    self.siriusxm_channels = json.load(f)
                self.safe_debug(f"📦 Loaded SiriusXM channel cache from {cache_path} — {len(self.siriusxm_channels)} channels")
                return True
            except Exception as e:
                self.logger.error(f"❌ Failed to load SiriusXM channel cache: {e}")
                return False
        else:
            self.logger.info("📭 No SiriusXM channel cache found — will fetch live data.")
            return False



    def save_siriusxm_cache(self):
        cache_path = os.path.join(indigo.server.getInstallFolderPath(), "Preferences", "Plugins", "sxm_channels_cache.json")
        try:
            with open(cache_path, "w") as f:
                json.dump(self.siriusxm_channels, f, indent=2)
            self.logger.info(f"💾 SiriusXM cache saved to {cache_path}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save SiriusXM cache: {e}")



    def load_siriusxm_cache(self):
        cache_path = os.path.join(indigo.server.getInstallFolderPath(), "Preferences", "Plugins", "sxm_channels_cache.json")
        try:
            with open(cache_path, "r") as f:
                self.siriusxm_channels = json.load(f)
            self.logger.info(f"📂 Loaded SiriusXM channels from cache ({len(self.siriusxm_channels)} channels)")
            return True
        except Exception as e:
            self.logger.warning(f"⚠️ Could not load SiriusXM cache: {e}")
            return False




    def refreshSiriusXMChannelCache(self):
        self.logger.info("🔄 Refreshing SiriusXM channel cache from API...")
        self.fetch_and_enrich_channels()
        self.save_siriusxm_cache()




    def enrich_channel_with_stream(self, channel):
        guid = channel.get("guid")
        if not guid:
            self.logger.warning("No GUID found for channel; cannot fetch stream.")
            return None

        metadata = self.get_chan_parms_by_guid(guid)
        if metadata and "stream" in metadata:
            channel["streamUrl"] = metadata["stream"]
            channel["albumArtURI"] = metadata.get("art", "")
            channel["guidStreamValid"] = True
            channel["channelType"] = "GUID"
            return channel
        else:
            channel["guidStreamValid"] = False
            return None


    ############################################################################################
    ### Nenu Specific Action Processing Methods
    ############################################################################################

    ### Nenu Specific Action - Test tuning hardcoded to the "Grateful Dead" station.

    def menutestSiriusXMChannelChange(self, valuesDict=None):
        try:
            test_device_id = 125081577  # Sonos CR device

            if test_device_id not in indigo.devices:
                self.logger.error(f"❌ Device ID {test_device_id} not found.")
                return

            dev = indigo.devices[test_device_id]
            zoneIP = dev.pluginProps.get("address", None)
            if not zoneIP:
                self.logger.error(f"❌ Device {dev.name} has no IP address.")
                return

            soco_dev = SoCoDevice(zoneIP)

            uri = "x-sonosapi-hls:channel-linear:067801cb-bb3f-1707-dd21-d77e06bb27c0?sid=37&flags=8232&sn=3"

            metadata = (
                '<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" '
                'xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" '
                'xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" '
                'xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">'
                '<item id="10092020" parentID="10092020" restricted="true">'
                '<dc:title>SiriusXM Channel Test</dc:title>'
                '<upnp:class>object.item.audioItem.audioBroadcast</upnp:class>'
                '<desc id="cdudn" nameSpace="urn:schemas-rinconnetworks-com:metadata-1-0/">'
                'SA_RINCON65031_</desc>'
                '</item>'
                '</DIDL-Lite>'
            )

            self.logger.info(f"🎯 Changing channel via GUID only...")
            self.safe_debug(f"🛰 URI: {uri}")
            self.safe_debug(f"📦 Metadata:\n{metadata}")

            soco_dev.avTransport.SetAVTransportURI([
                ('InstanceID', 0),
                ('CurrentURI', uri),
                ('CurrentURIMetaData', metadata),
            ])
            soco_dev.play()

            self.logger.info(f"✅ Changed {dev.name} to SiriusXM test channel")

        except Exception as e:
            self.logger.error(f"❌ Channel change failed: {e}")


    ### End - Nenu Specific Action - Test tuning hardcoded to the "Grateful Dead" station.


    # ✅ Diagnostic method to verify parsed channel entries - Not real sure what this is doing ?????

    ### End - Nenu Specific Action - Diagnostic method to verify parsed channel entries

    ### Nenu Specific Action - Dump the channel cache to the log.
    def dump_siriusxm_channels_to_log(self):
        if not self.siriusxm_channels:
            self.logger.warning("📭 SiriusXM channel list is empty — nothing to dump.")
            return

        self.safe_debug(f"📦 Dumping new format {len(self.siriusxm_channels)} SiriusXM channels to log...")

        for i, ch in enumerate(self.siriusxm_channels):
            channel_number = ch.get("channelNumber", "—")
            name = ch.get("name", "—")
            cid = ch.get("id", "—")
            guid = ch.get("guid", "—")
            stream = ch.get("streamUrl", "—")
            art = ch.get("albumArtURI", "—")
            short = ch.get("shortDescription", "—")
            long_desc = ch.get("longDescription", "—")
            cat = ch.get("category", "—")
            guid_ok = ch.get("guidStreamValid", False)
            fallback_ok = ch.get("fallbackStreamValid", False)
            ch_type = ch.get("channelType", "—")
            is_fav = ch.get("isFavorite", False)

            self.logger.info(f"🔎 [{i:03}] #{channel_number:<4} | {name:<30} | ID: {cid:<10} | GUID: {guid}")
            self.logger.info(f"     ↳ Category: {cat} | Type: {ch_type} | Fav: {is_fav}")
            self.logger.info(f"     ↳ Short Desc: {short}")
            self.logger.info(f"     ↳ Stream: {stream}")
            self.logger.info(f"     ↳ Album Art: {art}")
            self.logger.info(f"     ↳ Stream OK: G={guid_ok} F={fallback_ok}")
            self.logger.info(f"     ↳ Long Desc: {long_desc}")

        self.logger.info("✅ Channel dump complete.")

    ### End - Nenu Specific Action - Dump the channel cache to the log.


    ### Nenu Specific Action - Delete and relaod the channel cache.
 
    def DeleteandDefine_SiriusXMCache(self):
        try:
            cache_path = os.path.join(indigo.server.getInstallFolderPath(), "Preferences", "Plugins", "siriusxm_channel_cache.json")

            if os.path.exists(cache_path):
                os.remove(cache_path)
                self.logger.info("🗑 Deleted SiriusXM channel cache.")
            else:
                self.logger.info("🗃 SiriusXM channel cache not found — nothing to delete.")

            self.logger.info("🔄 Reloading SiriusXM channel data...")
            self.load_siriusxm_channel_data()
            self.logger.info("✅ Reloaded SiriusXM channel data.")

        except Exception as e:
            self.logger.error(f"❌ Error during SiriusXM cache reset: {e}")

    ### End - Nenu Specific Action - Delete and relaod the channel cache.

    ############################################################################################
    ### Nenu Specific Action Processing Methods
    ############################################################################################

    def get_chan_parms_3_way(self, chan):
        try:
            if not isinstance(chan, dict):
                self.logger.error(f"❌ get_chan_parms_3_way(): Expected dict, got {type(chan)} | Value: {chan}")
                return {
                    "id": None,
                    "guid": None,
                    "channelNumber": None,
                    "name": str(chan),
                    "streamUrl": None,
                    "albumArtURI": None,
                    "guidStreamValid": False,
                    "fallbackStreamValid": False,
                    "channelType": "unknown"
                }

            chan_id = str(chan.get("id", "")).strip()
            guid = str(chan.get("guid", "")).strip()
            number = str(chan.get("channelNumber", "")).strip()
            name = str(chan.get("name", "")).strip()

            self.safe_debug(f"🔍 get_chan_parms_3_way() → {name} | GUID={guid} | ID={chan_id}")

            # Ensure SiriusXM session is initialized
            if not self.siriusxm:
                self.logger.warning("🔑 Initializing SiriusXM session for stream lookup...")
                self.siriusxm = SXMClient(
                    self.pluginPrefs.get("SiriusXMID", ""),
                    self.pluginPrefs.get("SiriusXMPassword", ""),
                    region=RegionChoice.US
                )
                if not self.siriusxm.authenticate():
                    self.logger.error("❌ SiriusXM authentication failed")
                    return {
                        "id": chan_id,
                        "guid": guid,
                        "channelNumber": number,
                        "name": name,
                        "streamUrl": None,
                        "albumArtURI": None,
                        "guidStreamValid": False,
                        "fallbackStreamValid": False,
                        "channelType": chan.get("channelType", "unknown")
                    }

            # Primary: Try to get stream via GUID
            stream_url = self.siriusxm.get_playlist(guid)
            guid_valid = stream_url is not None

            # 🛡️ Sanity check: stream_url must be a proper URL
            if isinstance(stream_url, str):
                if "#EXTM3U" in stream_url or "AAC_Data/" in stream_url:
                    self.logger.warning(f"⚠️ Stream URL for '{name}' appears to be raw playlist data — skipping GUID stream")
                    stream_url = None
                    guid_valid = False
                elif len(stream_url) > 1000:
                    self.logger.warning(f"⚠️ Stream URL for '{name}' too long ({len(stream_url)} chars) — skipping GUID stream")
                    stream_url = None
                    guid_valid = False

            # Fallback: Use legacy field if GUID failed
            fallback_url = chan.get("streamUrl")
            fallback_valid = fallback_url is not None and not guid_valid
            resolved_url = stream_url or fallback_url

            # Album Art fallback: use existing or try to extract from images
            album_art = chan.get("albumArtURI")
            if not album_art and "images" in chan and isinstance(chan["images"], dict):
                images_list = chan["images"].get("images", [])
                if images_list and isinstance(images_list, list):
                    album_art = images_list[0].get("url", "")

            return {
                "id": chan_id,
                "guid": guid,
                "channelNumber": number,
                "name": name,
                "streamUrl": resolved_url,
                "albumArtURI": album_art,
                "guidStreamValid": guid_valid,
                "fallbackStreamValid": fallback_valid,
                "channelType": chan.get("channelType", "audio")
            }

        except Exception as e:
            self.logger.error(f"❌ get_chan_parms_3_way() error: {e}")
            return {
                "id": None,
                "guid": None,
                "channelNumber": None,
                "name": str(chan),
                "streamUrl": None,
                "albumArtURI": None,
                "guidStreamValid": False,
                "fallbackStreamValid": False,
                "channelType": "unknown"
            }



    def fetch_and_enrich_channels(self):
        from datetime import datetime
        from sxm import XMChannel

        start_time = datetime.now()
        self.logger.info(f"🦪 ENTERED fetch_and_enrich_channels() at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        self.Sonos_SiriusXM = []
        enriched_channels = []

        is_cache_mode = bool(self.siriusxm_channels)
        if is_cache_mode:
            self.logger.info(f"📱 Enriching {len(self.siriusxm_channels)} cached SiriusXM channels — skipping get_channels()")
            channels = [XMChannel.from_dict(ch) for ch in self.siriusxm_channels if isinstance(ch, dict)]
        else:
            self.siriusxm_channels = []
            try:
                raw_channels = self.siriusxm.get_channels() or []
                channels = [XMChannel.from_dict(ch) for ch in raw_channels if isinstance(ch, dict)]
                self.logger.info(f"📱 Retrieved {len(channels)} raw SiriusXM channels")
            except Exception as e:
                self.logger.error(f"💥 Failed to retrieve channels: {e}")
                return

        for idx, ch in enumerate(channels):
            streamUrl = None
            albumArtURI = None
            guidStreamValid = False

            chan_number_raw = ch.channel_number or ch.displayChannelNumber or ""
            chan_number_str = str(chan_number_raw).strip()

            try:
                chan_number_int = int(chan_number_str)
            except ValueError:
                self.logger.warning(f"❌ Skipping malformed channel at index {idx}: {ch.name} — channel_number = '{chan_number_str}'")
                continue

            chan = self.normalize_channel_dict(ch, streamUrl, albumArtURI, guidStreamValid)
            chan["channel_number"] = chan_number_int
            chan["channel_number_str"] = chan_number_str

            enriched_channels.append(chan)

            # ✅ Legacy-compatible format using GUID in [1]
            entry = [
                chan_number_int,                    # 0: Channel number
                chan.get("guid", ch.guid),          # 1: GUID used by Sonos stream URL
                chan.get("name", ch.name),          # 2: Display name
                chan.get("id", ch.id),              # 3: Optional ID (for reference)
                chan.get("name", ch.name)           # 4: Duplicate name (legacy compatibility)
            ]
            self.Sonos_SiriusXM.append(entry)

            if idx < 5:
                self.safe_debug(f"📦 Enriched Channel [{idx}]: {entry} (type: {type(entry)})")

        enriched_channels.sort(key=lambda c: c.get("channel_number", 9999))
        self.siriusxm_channels = enriched_channels

        self.logger.info("🔁 Building fast lookup maps for ID and GUID...")
        self.siriusxm_id_map = {c[3]: c for c in self.Sonos_SiriusXM if c[3]}   # from [3] = channel ID
        self.siriusxm_guid_map = {c[1]: c for c in self.Sonos_SiriusXM if c[1] and '-' in c[1]}  # from [1] = GUID

        # Debugging: Dump sample keys
        self.logger.debug(f"📝 Sample ID map keys: {list(self.siriusxm_id_map.keys())[:5]}")
        self.logger.debug(f"📝 Sample GUID map keys: {list(self.siriusxm_guid_map.keys())[:5]}")
        self.logger.debug(f"✅ Maps built: {len(self.siriusxm_id_map)} IDs, {len(self.siriusxm_guid_map)} GUIDs")

        end_time = datetime.now()
        elapsed = (end_time - start_time).total_seconds()
        self.logger.info(f"✅ EXITING fetch_and_enrich_channels() at {end_time.strftime('%Y-%m-%d %H:%M:%S')} (elapsed: {elapsed:.1f} sec)")



    def getSiriusXM(self, channelInfo):
        """
        Returns full SiriusXM streaming parameters from a resolved channel dict.
        """
        if not channelInfo:
            return None

        chan_id = channelInfo.get("id")
        chan_num = channelInfo.get("channelNumber")
        name = channelInfo.get("name")
        stream_url = channelInfo.get("streamUrl")

        if not stream_url:
            self.logger.warning(f"❌ SiriusXM channel {name} (ID {chan_id}) has no stream URL.")
            return None

        return {
            "channelId": chan_id,
            "channelNumber": chan_num,
            "name": name,
            "streamUrl": stream_url
        }


    def func_switch(self, chanRef):
        """
        Looks up a SiriusXM channel by its ID and returns its metadata dict.
        """
        if not isinstance(chanRef, str):
            self.logger.error(f"❌ func_switch: Expected str channel ID, got {type(chanRef)} | Value: {chanRef}")
            return None

        chan_data = next((ch for ch in self.siriusxm_channels if ch.get("id") == chanRef), None)

        if not chan_data:
            self.logger.warning(f"🔁 func_switch: No match found for ID '{chanRef}'")
            return None

        return chan_data  # Already dict


    def getSiriusXMChannelList(self, filter="", valuesDict=None, typeId="", targetId=0):
        list_entries = []

        if not self.Sonos_SiriusXM:
            self.logger.warning("⚠️ SiriusXM channel list is empty. Cannot build UI list.")
            return []

        self.logger.warning(f"🧪 getSiriusXMChannelList CALLED with {len(self.Sonos_SiriusXM)} entries")

        for idx, entry in enumerate(self.Sonos_SiriusXM):
            try:
                channel_number = entry[0]
                channel_id = entry[1]
                channel_name = entry[2]

                if not channel_id or not channel_name:
                    self.logger.warning(f"⚠️ Skipping invalid channel entry at index {idx}: {entry}")
                    continue

                label = f"CH {channel_number} - {channel_name}"
                list_entries.append((channel_id, label))

                if idx < 5:
                    self.logger.warning(f"🧾 UI Entry [{idx}]: ID={channel_id} | Label={label}")

            except Exception as e:
                self.logger.error(f"❌ Error processing UI entry at index {idx}: {e} — Raw: {entry}")

        # Sort by channel number (first field)
        sorted_entries = sorted(list_entries, key=lambda x: int(x[1].split()[1]) if x[1].split()[1].isdigit() else 9999)
        self.logger.info(f"✅ Built {len(sorted_entries)} SiriusXM dropdown entries for Indigo UI")
        return sorted_entries
        

    def sendStreamToZone(self, zoneIP, stream_url, stream_title=""):
        try:
            zone = self.zone_by_ip.get(zoneIP)
            if not zone:
                self.logger.warning(f"Sonos: No zone found for IP {zoneIP}")
                return

            zone.play_uri(uri=stream_url, title=stream_title)
            self.logger.info(f"Sonos: Stream '{stream_title}' sent to zone {zoneIP}")

        except Exception as e:
            self.logger.error(f"Sonos: Failed to send stream to {zoneIP} - {e}")


    def old_actionZP_SiriusXM(self, pluginAction, dev):
        self.logger.debug("🪪 Entered plugin.py::actionZP_SiriusXM")

        props = pluginAction.props
        self.logger.debug(f"🧪 Raw pluginAction.props: {props}")

        channel_id = props.get("channelSelector") or props.get("channel", "").strip()
        self.safe_debug(f"🧪 Extracted channel ID: '{channel_id}'")

        # Lookup from legacy-format maps
        chan = self.siriusxm_guid_map.get(channel_id) or self.siriusxm_id_map.get(channel_id)

        if not chan:
            self.logger.warning(f"⚠️ SiriusXM: Channel ID '{channel_id}' not found in known maps.")
            return

        self.safe_debug(f"🔎 Channel structure: {chan} (type: {type(chan)})")

        # Legacy channel structure: [number, id, name, id, name]
        try:
            channel_guid = chan[1] if "-" in chan[1] else None  # Must be a GUID
            channel_name = chan[2]

            if not channel_guid:
                self.logger.warning(f"⚠️ Cannot send SiriusXM channel — GUID missing for ID '{channel_id}'")
                return

            zoneIP = dev.address
            self.logger.info(f"📡 Sending SiriusXM channel '{channel_name}' with GUID '{channel_guid}' to {zoneIP}")

            self.sendSiriusXMChannel(zoneIP, channel_guid, channel_name)

        except Exception as e:
            self.logger.error(f"❌ Exception during SiriusXM channel playback: {e}")



    def actionZP_SiriusXM(self, pluginAction, dev):
        self.logger.debug("🪪 Entered plugin.py::actionZP_SiriusXM")

        props = pluginAction.props
        self.logger.debug(f"🧪 Raw pluginAction.props: {props}")

        channel_id = props.get("channelSelector") or props.get("channel", "").strip()
        self.safe_debug(f"🧪 Extracted channel ID: '{channel_id}'")

        # Lookup from legacy-format maps
        chan = self.siriusxm_guid_map.get(channel_id) or self.siriusxm_id_map.get(channel_id)

        if not chan:
            self.logger.warning(f"⚠️ SiriusXM: Channel ID '{channel_id}' not found in known maps.")
            return

        self.safe_debug(f"🔎 Channel structure: {chan} (type: {type(chan)})")

        # ─────────────────────────────────────────────────────────────
        # NEW: Route to the *live* SoCo group coordinator when grouped.
        # This avoids race conditions where Indigo still shows the
        # joiner as coordinator due to demotion vetoes.
        # ─────────────────────────────────────────────────────────────
        target_ip = None
        target_dev = dev  # default

        try:
            # Try live SoCo first
            dev_ip = (dev.pluginProps.get("address", "") or "").strip()
            soco = self.soco_by_ip.get(dev_ip) if dev_ip else None
            live_coord = getattr(getattr(soco, "group", None), "coordinator", None) if soco else None
            live_coord_ip = getattr(live_coord, "ip_address", None)
            live_coord_name = getattr(live_coord, "player_name", None)

            if live_coord_ip:
                # If device is in a group and isn’t the live coordinator, route to live coord
                if not soco or (getattr(soco, "uid", None) != getattr(live_coord, "uid", None)):
                    target_ip = live_coord_ip
                    # Map to Indigo device if we can (for logging/artwork etc.), otherwise IP is enough
                    mapped = self.ip_to_indigo_device.get(live_coord_ip)
                    if mapped:
                        target_dev = mapped
                    self.logger.info(
                        f"🔁 SiriusXM request on '{dev.name}' "
                        f"→ routing by live SoCo to coordinator '{live_coord_name}' @ {live_coord_ip}"
                    )
                else:
                    # Caller is already the live coordinator
                    target_ip = dev_ip
                    target_dev = dev
                    self.logger.debug(
                        f"🧭 SiriusXM: '{dev.name}' is live coordinator per SoCo; using {dev_ip}"
                    )
            else:
                # Fall back to Indigo states if SoCo is unavailable
                grouped_flag = str(dev.states.get("Grouped", "")).strip().lower()
                is_coord_str = str(dev.states.get("GROUP_Coordinator", "")).strip().lower()
                is_grouped   = (grouped_flag == "true" or grouped_flag is True)
                is_coord     = (is_coord_str == "true" or is_coord_str is True)

                if is_grouped and not is_coord:
                    coord_dev = self.getCoordinatorDevice(dev)
                    if coord_dev:
                        target_dev = coord_dev
                        target_ip = (coord_dev.pluginProps.get("address", "") or "").strip()
                        self.logger.info(
                            f"🔁 SiriusXM request on grouped slave '{dev.name}' "
                            f"→ rerouting (state fallback) to coordinator '{coord_dev.name}' @ {target_ip}"
                        )
                if not target_ip:
                    target_ip = dev_ip
                    self.logger.warning(
                        f"⚠️ SiriusXM: live SoCo unavailable for '{dev.name}', and coordinator resolution "
                        f"by state fallback incomplete; using {dev_ip} (may break group)"
                    )
        except Exception as e:
            # Ultimate fallback: use the caller’s IP
            target_ip = (dev.pluginProps.get("address", "") or "").strip()
            self.logger.debug(f"SiriusXM coordinator routing failed, using {target_ip}: {e}")

        # Legacy channel structure: [number, id, name, id, name]
        try:
            channel_guid = chan[1] if "-" in chan[1] else None  # Must be a GUID
            channel_name = chan[2]

            if not channel_guid:
                self.logger.warning(f"⚠️ Cannot send SiriusXM channel — GUID missing for ID '{channel_id}'")
                return

            self.logger.info(
                f"📡 Sending SiriusXM channel '{channel_name}' with GUID '{channel_guid}' to {target_ip}"
            )
            self.sendSiriusXMChannel(target_ip, channel_guid, channel_name)

        except Exception as e:
            self.logger.error(f"❌ Exception during SiriusXM channel playback: {e}")




            


    def actionZP_LIST(self, pluginAction, dev):
        try:
            self.safe_debug(f"🧪 actionZP_LIST: pluginAction.props = {pluginAction.props}")

            # 🔍 Pull selected value from Indigo UI props
            val = pluginAction.props.get("ZP_LIST") or pluginAction.props.get("setting")

            # 🛠 Harden type of selected value
            if isinstance(val, str):
                raw_val = val.strip()
            elif isinstance(val, int):
                raw_val = str(val)
            else:
                self.logger.warning(f"[BAD PROP] ZP_LIST/setting is not string or int: {val} ({type(val).__name__})")
                return

            if not raw_val:
                self.logger.error(f"❌ actionZP_LIST: No playlist selected for {dev.name}")
                return

            # ✅ Now safe to use `raw_val` in logic (e.g., split or comparison)
            self.logger.info(f"▶️ ZP_LIST Action Triggered for {dev.name}: Selected = {raw_val}")
            # You can continue processing `raw_val` as needed here...

        except Exception as e:
            self.logger.error(f"❌ Exception in actionZP_LIST for {dev.name}: {e}")





            zoneIP = dev.pluginProps.get("address")
            if not zoneIP:
                self.logger.error(f"❌ actionZP_LIST: No IP address configured for {dev.name}")
                return

            # 🔍 Look up matching SoCo device
            soco_device = self.soco_by_ip.get(zoneIP)
            if not soco_device:
                self.logger.warning(f"⚠️ get_soco_device: IP {zoneIP} not found in soco_by_ip. Performing fallback discovery.")
                soco_device = self.get_soco_device(zoneIP)

            if not soco_device:
                self.logger.error(f"❌ actionZP_LIST: Could not locate SoCo device for IP {zoneIP}")
                return

            # 🔍 Retrieve Sonos playlist matching the selected title or ID
            playlists = soco_device.get_sonos_playlists()
            playlist_obj = None
            for pl in playlists:
                if raw_val in (pl.title, getattr(pl, "item_id", "")):
                    playlist_obj = pl
                    break

            if not playlist_obj:
                self.logger.error(f"❌ actionZP_LIST: Playlist object not found for '{raw_val}'")
                return

            self.logger.info(f"🎶 Queuing playlist '{playlist_obj.title}' on {dev.name}")

            # 🧼 Clear existing queue
            soco_device.clear_queue()

            # ➕ Add playlist to queue
            soco_device.add_to_queue(playlist_obj)

            # 🔁 Optionally enable repeat/shuffle
            soco_device.repeat = False
            soco_device.shuffle = False

            # ▶️ Start playback from beginning of queue
            soco_device.play_from_queue(0)

            self.logger.info(f"✅ Playlist '{playlist_obj.title}' started on {dev.name}")

        except Exception as e:
            self.logger.error(f"❌ actionZP_LIST: Failed to start playlist on {dev.name}: {e}")



    def get_model_name(self, soco_device):
        try:
            model_name = getattr(soco_device, "model_name", "").strip()
            if not model_name or model_name.lower() == "unknown":
                speaker_info = soco_device.get_speaker_info()
                model_name = speaker_info.get("model_name", "unknown")
            return model_name
        except Exception as e:
            self.logger.warning(f"⚠️ Could not retrieve model name: {e}")
            return "unknown"



    def reinitialize_and_rebuild_group_state(self):
        """
        Rebuild group state using logic similar to initial deviceStartComm load.
        This avoids plugin state drift after dynamic grouping/ungrouping.
        """
        self.logger.warning("🔄 Forcing reinitialization of group topology and plugin group states...")

        try:
            from soco import SoCo

            # ✅ Ensure all required plugin dictionaries are initialized
            if not hasattr(self, "zone_group_state_cache"):
                self.zone_group_state_cache = {}
            if not hasattr(self, "device_by_uuid"):
                self.device_by_uuid = {}
            if not hasattr(self, "uuid_to_soco"):
                self.uuid_to_soco = {}
            if not hasattr(self, "soco_devices"):
                self.soco_devices = {}
            if not hasattr(self, "parsed_zone_group_state_by_ip"):
                self.parsed_zone_group_state_by_ip = {}
            if not hasattr(self, "soco_by_ip"):
                self.soco_by_ip = {}
            if not hasattr(self, "ip_to_indigo_device"):
                self.ip_to_indigo_device = {}

            # 🔄 Clear all cached group state and mapping structures
            self.zone_group_state_cache.clear()
            self.device_by_uuid.clear()
            self.uuid_to_soco.clear()
            self.soco_devices.clear()
            self.parsed_zone_group_state_by_ip.clear()
            self.soco_by_ip.clear()
            self.ip_to_indigo_device.clear()

            # 🔁 Reinitialize SoCo and Indigo device bindings
            for dev in indigo.devices.iter("self"):
                ip = dev.address
                if not ip:
                    self.logger.warning(f"⚠️ Device {dev.name} has no IP — skipping")
                    continue

                try:
                    soco_device = SoCo(ip)
                    self.soco_by_ip[ip] = soco_device
                    self.ip_to_indigo_device[ip] = dev
                    self.logger.info(f"✅ Reinitialized SoCo for {dev.name} ({ip})")

                    # UID mapping
                    zp_uid = soco_device.uid
                    self.device_by_uuid[zp_uid] = dev
                    self.uuid_to_soco[zp_uid] = soco_device
                    self.soco_devices[zp_uid] = soco_device
                    self.logger.info(f"🔁 Bound {dev.name} to UUID {zp_uid}")

                except Exception as e:
                    self.logger.warning(f"❌ Failed to initialize SoCo for {dev.name} at {ip}: {e}")
                    continue

            # ⏬ Refresh zone group topology and populate group cache
            self.refresh_group_topology_after_plugin_zone_change()
            #self.refresh_all_group_states()
            self._refresh_all_group_states_helper(reason="Reinitialize and rebuild group states")

            self.evaluate_and_update_grouped_states()

            # 🔍 Confirm cache population
            if not self.zone_group_state_cache:
                self.logger.warning("🚫 zone_group_state_cache is still empty — group topology may not have been fetched.")
            else:
                self.logger.info(f"📊 zone_group_state_cache populated with {len(self.zone_group_state_cache)} group(s).")

            # ✅ Re-evaluate plugin logical grouped state




            self.logger.warning("✅ Reinitialization and group state rebuild complete.")

        except Exception as e:
            self.logger.error(f"❌ Failed to reinitialize group state: {e}")


    ############################################################################################
    ### Hellper methods for announce http server processing and checks
    ############################################################################################


    def getLocalIP(self):
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"


    def get_announce_http_config(self):
        """Read announcement HTTP config from prefs with safe fallbacks."""
        prefs = self.pluginPrefs or {}
        ip = (
            prefs.get("http_server") or
            prefs.get("httpServer") or
            prefs.get("httpServerIP") or
            prefs.get("http_ip") or
            ""  # empty means bind all interfaces on start; Sonos should use a reachable IP in URLs
        )

        # Port: default 8889
        try:
            port = int(prefs.get("http_port") or prefs.get("httpPort") or 8889)
        except Exception:
            port = 8889

        # Root path for announcement audio files
        root = prefs.get("SoundFilePath") or getattr(self, "SoundFilePath", "")
        if not root:
            root = indigo.server.getInstallFolderPath() + "/AudioFiles"

        return ip, port, root


    def ensure_announcement_http_server(self):
        if getattr(self, "_announce_httpd", None):
            self.logger.debug("📢 Announcement HTTP server already running")
            return True  # return True so startup can log it's running

        try:
            import http.server, socketserver, threading, os, http.client

            ip, port, root = self.get_announce_http_config()
            os.makedirs(root, exist_ok=True)
            # Remember the root actually being served — announcement builders must
            # write their audio here (prefs may change after the server started).
            self._announce_http_root = root

            class AnnouncementHandler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=root, **kwargs)
                def _mark_fetch(self):
                    # Record who pulled from us — the announcement flow checks this
                    # to detect players that can't reach the server (VLAN/firewall).
                    try:
                        self.server.parent_plugin._announce_last_fetch[self.client_address[0]] = time.time()
                    except Exception:
                        pass
                def do_GET(self):
                    self._mark_fetch()
                    super().do_GET()
                def do_HEAD(self):
                    self._mark_fetch()
                    super().do_HEAD()
                def log_message(self, fmt, *args):
                    try:
                        self.server.parent_logger.debug(f"[ANN HTTP] {self.client_address[0]} " + fmt % args)
                    except Exception:
                        pass

            class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
                allow_reuse_address = True

            # Prefer the explicit IP from config; if "ALL" or empty, bind to all interfaces.
            bind_host = (ip or "").strip()
            if bind_host.upper() == "ALL":
                bind_host = ""  # INADDR_ANY

            # Create & start server
            self._announce_httpd = ThreadedTCPServer((bind_host, port), AnnouncementHandler)
            self._announce_httpd.parent_logger = self.logger
            self._announce_httpd.parent_plugin = self
            if not hasattr(self, "_announce_last_fetch"):
                self._announce_last_fetch = {}

            t = threading.Thread(target=self._announce_httpd.serve_forever, daemon=True)
            t.start()
            self._announce_http_thread = t

            # Record what we actually bound (for diagnostics)
            try:
                bound_host, bound_port = self._announce_httpd.server_address  # ('0.0.0.0', 8889) or (ip, port)
            except Exception:
                bound_host, bound_port = (bind_host or "0.0.0.0", port)

            # Remember bound info
            self._announce_bound_host = bound_host
            self._announce_bound_port = bound_port
            self._announce_http_port = int(bound_port)

            # Determine a *publish* host for URIs (never loopback/0.0.0.0)
            def _is_bad(h: str) -> bool:
                return (not h) or h in ("0.0.0.0", "localhost", "::1") or str(h).startswith("127.")

            # Preference: explicit HTTPServer pref → selected interface IP → bound host if routable
            candidates = [
                (str(getattr(self, "HTTPServer", "")).strip() or None),
                (str(getattr(self, "selectedInterfaceIP", "")).strip() or None),
                (None if _is_bad(bound_host) else bound_host),
            ]
            publish_host = next((h for h in candidates if h and not _is_bad(h)), None)

            # Persist publish host for announcement URI builder
            self.announce_bind_ip = publish_host or ""

            # Log start
            self.logger.info(
                f"📢 Announcement HTTP server started on http://{bound_host or '0.0.0.0'}:{bound_port}/ serving {root}"
            )

            # Warn if we don’t yet have a safe publish host
            if not self.announce_bind_ip:
                self.logger.warning("⚠️ No safe LAN IP available to publish for announcements (loopback/0.0.0.0).")
            else:
                self.logger.info(f"✅ Announcement HTTP publish host: {self.announce_bind_ip}:{self._announce_http_port}")

                # Quick self-test (HEAD /) so we know Sonos can reach it by IP:PORT
                try:
                    conn = http.client.HTTPConnection(self.announce_bind_ip, self._announce_http_port, timeout=2.5)
                    conn.request("HEAD", "/")
                    resp = conn.getresponse()
                    self.logger.info(f"🧪 Announcement server self-test: {resp.status} {resp.reason}")
                    conn.close()
                except Exception as e:
                    self.logger.warning(
                        f"⚠️ Announcement server self-test failed on {self.announce_bind_ip}:{self._announce_http_port} → {e}"
                    )

            return True

        except OSError as e:
            self.logger.error(f"❌ Failed to start Announcement HTTP server (port in use?): {e}")
            return False
        except Exception as e:
            self.logger.exception(f"❌ Unexpected error starting Announcement HTTP server: {e}")
            return False





    ############################################################################################
    ### Refresh Cache both Indigo and anything we add on
    ############################################################################################

    def old_refresh_all_group_states_helper(self, reason: str = ""):
        """
        Canonical helper for refreshing and aligning all Sonos group states.
        Always call this instead of refresh_all_group_states() directly.

        Steps:
          1. Run refresh_all_group_states() to rebuild caches from SoCo.
          2. Apply evaluated truth back into Indigo device states so
             Grouped / GROUP_Coordinator / GROUP_Name stay consistent.

        Args:
            reason (str): Optional context for logging (e.g. 'startup', 'addPlayerToZone').
        """
        try:
            if reason:
                self.logger.warning(f"🔁 _refresh_all_group_states_helper begin — reason='{reason}'")

            # 1) Recompute (does not write to Indigo yet)
            self.refresh_all_group_states()

            # 2) Push evaluated truth into Indigo device states
            if hasattr(self, "apply_grouped_flags_from_eval"):
                self.apply_grouped_flags_from_eval()
            else:
                self.logger.warning(
                    "⚠️ apply_grouped_flags_from_eval() not found; "
                    "cannot align Grouped/Coordinator/Name states."
                )

            if reason:
                self.logger.warning(f"✅ _refresh_all_group_states_helper end — reason='{reason}'")

        except Exception as e:
            self.logger.error(f"❌ _refresh_all_group_states_helper failed: {e}")


    def old_2_refresh_all_group_states_helper(self, reason: str = ""):
        """
        Canonical helper: recompute + write evaluated group truth back to Indigo.
        Call this everywhere instead of refresh_all_group_states() directly.
        """
        try:
            if reason:
                self.logger.debug(f"🔁 refresh-all begin — {reason}")

            # 1) Recompute caches from SoCo
            self.refresh_all_group_states()

            groups = getattr(self, "zone_group_state_cache", {}) or {}
            ip2dev = getattr(self, "ip_to_indigo_device", {}) or {}
            soco_by_ip = getattr(self, "ip_to_soco_device", {}) or {}
            touched = set()

            # 2) Apply to all devices seen in groups
            for _, payload in groups.items():
                members = payload.get("members", []) or []
                if not members:
                    continue

                coord_row = next((m for m in members if m.get("coordinator", False)), members[0])
                coord_ip  = (coord_row.get("ip") or coord_row.get("location") or "").strip()
                coord_dev = ip2dev.get(coord_ip)

                # non-bonded count → grouped eval
                non_bonded_ips = []
                for m in members:
                    ip = (m.get("ip") or m.get("location") or "").strip()
                    name_lc = (m.get("zone_name") or m.get("name") or "").lower()
                    if ip and not any(k in name_lc for k in ("sub", "left", "right", "surround")):
                        non_bonded_ips.append(ip)
                grouped_eval = (len(set(non_bonded_ips)) > 1)

                group_name = coord_dev.name if coord_dev else (coord_row.get("name") or "Group")

                # coordinator
                if coord_dev:
                    coord_dev.updateStateOnServer("GROUP_Coordinator", "true")
                    coord_dev.updateStateOnServer("Grouped", True if grouped_eval else False)
                    coord_dev.updateStateOnServer("GROUP_Name", group_name)
                    touched.add(coord_dev.id)

                # members
                for m in members:
                    m_ip = (m.get("ip") or m.get("location") or "").strip()
                    if not m_ip or m_ip == coord_ip:
                        continue
                    m_dev = ip2dev.get(m_ip)
                    if not m_dev:
                        continue
                    m_dev.updateStateOnServer("GROUP_Coordinator", "false")
                    m_dev.updateStateOnServer("Grouped", True if grouped_eval else False)
                    m_dev.updateStateOnServer("GROUP_Name", group_name)
                    touched.add(m_dev.id)

            # 3) Anything not touched this pass = standalone
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                if dev.id in touched:
                    continue
                soco = soco_by_ip.get((dev.address or "").strip())
                is_coord_live = False
                try:
                    is_coord_live = bool(getattr(soco, "is_coordinator", False)) if soco else False
                except Exception:
                    pass
                dev.updateStateOnServer("Grouped", False)
                dev.updateStateOnServer("GROUP_Coordinator", "true" if is_coord_live else "false")
                dev.updateStateOnServer("GROUP_Name", dev.name)

            if reason:
                self.logger.debug(f"✅ refresh-all end — {reason}")



            # --- FINAL RECONCILE: make every Indigo device match live SoCo truth ---
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                ip = (dev.address or "").strip()
                soco = self.ip_to_soco_device.get(ip)

                live_coord = False
                live_grouped = False
                live_group_name = dev.name

                if soco and self._ip_probe_ok(ip):  # offline player: is_coordinator/.group would block in network timeouts
                    # coordinator truth
                    try:
                        live_coord = bool(getattr(soco, "is_coordinator", False))
                    except Exception:
                        live_coord = False

                    # grouped truth (non-bonded members > 1)
                    try:
                        g = soco.group
                        if g:
                            nonbond = 0
                            for m in (g.members or []):
                                nm = (getattr(m, "player_name", "") or "").lower()
                                if not any(k in nm for k in ("sub", "left", "right", "surround")):
                                    nonbond += 1
                            live_grouped = (nonbond > 1)
                            if getattr(g, "coordinator", None):
                                live_group_name = getattr(g.coordinator, "player_name", live_group_name) or live_group_name
                    except Exception:
                        pass

                # current stored values
                cur_coord   = dev.states.get("GROUP_Coordinator", "false")
                cur_grouped = dev.states.get("Grouped", False)
                cur_gname   = dev.states.get("GROUP_Name", dev.name)

                # normalize for compare
                norm_cur_coord   = (str(cur_coord).lower() == "true")
                norm_cur_grouped = bool(cur_grouped)

                # log diffs (only when change)
                if norm_cur_coord != live_coord or norm_cur_grouped != live_grouped or cur_gname != live_group_name:
                    self.logger.warning(
                        f"[reconcile] {dev.name} "
                        f"Coord {norm_cur_coord}->{live_coord}  "
                        f"Grouped {norm_cur_grouped}->{live_grouped}  "
                        f"Name '{cur_gname}'->'{live_group_name}'"
                    )

                # write back SoCo truth
                dev.updateStateOnServer("GROUP_Coordinator", "true" if live_coord else "false")
                dev.updateStateOnServer("Grouped", True if live_grouped else False)
                dev.updateStateOnServer("GROUP_Name", live_group_name)


            



        except Exception as e:
            self.logger.error(f"❌ _refresh_all_group_states_helper failed: {e}")


    def old_3__refresh_all_group_states_helper(self, reason: str = ""):
        """
        Canonical helper: recompute + write evaluated group truth back to Indigo.
        Call this everywhere instead of refresh_all_group_states() directly.
        """
        try:
            if reason:
                self.logger.debug(f"🔁 refresh-all begin — {reason}")

            # 1) Recompute caches from SoCo
            self.refresh_all_group_states()

            groups = getattr(self, "zone_group_state_cache", {}) or {}
            ip2dev = getattr(self, "ip_to_indigo_device", {}) or {}
            soco_by_ip = getattr(self, "ip_to_soco_device", {}) or {}
            touched = set()

            # 2) Apply to all devices seen in groups
            for _, payload in groups.items():
                members = payload.get("members", []) or []
                if not members:
                    continue

                coord_row = next((m for m in members if m.get("coordinator", False)), members[0])
                coord_ip  = (coord_row.get("ip") or coord_row.get("location") or "").strip()
                coord_dev = ip2dev.get(coord_ip)

                # non-bonded count → grouped eval
                non_bonded_ips = []
                for m in members:
                    ip = (m.get("ip") or m.get("location") or "").strip()
                    name_lc = (m.get("zone_name") or m.get("name") or "").lower()
                    if ip and not any(k in name_lc for k in ("sub", "left", "right", "surround")):
                        non_bonded_ips.append(ip)
                grouped_eval = (len(set(non_bonded_ips)) > 1)

                group_name = coord_dev.name if coord_dev else (coord_row.get("name") or "Group")

                # coordinator
                if coord_dev:
                    # ✅ write real booleans
                    coord_dev.updateStateOnServer("GROUP_Coordinator", True)
                    coord_dev.updateStateOnServer("Grouped", True if grouped_eval else False)
                    coord_dev.updateStateOnServer("GROUP_Name", group_name)
                    touched.add(coord_dev.id)

                # members
                for m in members:
                    m_ip = (m.get("ip") or m.get("location") or "").strip()
                    if not m_ip or m_ip == coord_ip:
                        continue
                    m_dev = ip2dev.get(m_ip)
                    if not m_dev:
                        continue
                    # ✅ write real booleans
                    m_dev.updateStateOnServer("GROUP_Coordinator", False)
                    m_dev.updateStateOnServer("Grouped", True if grouped_eval else False)
                    m_dev.updateStateOnServer("GROUP_Name", group_name)
                    touched.add(m_dev.id)

            # 3) Anything not touched this pass = standalone
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                if dev.id in touched:
                    continue
                soco = soco_by_ip.get((dev.address or "").strip())
                is_coord_live = False
                try:
                    is_coord_live = bool(getattr(soco, "is_coordinator", False)) if soco else False
                except Exception:
                    pass
                # ✅ write real booleans
                dev.updateStateOnServer("Grouped", False)
                dev.updateStateOnServer("GROUP_Coordinator", True if is_coord_live else False)
                dev.updateStateOnServer("GROUP_Name", dev.name)

            if reason:
                self.logger.debug(f"✅ refresh-all end — {reason}")

            # --- FINAL RECONCILE: make every Indigo device match live SoCo truth ---
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                ip = (dev.address or "").strip()
                soco = self.ip_to_soco_device.get(ip)

                live_coord = False
                live_grouped = False
                live_group_name = dev.name

                if soco and self._ip_probe_ok(ip):  # offline player: is_coordinator/.group would block in network timeouts
                    # coordinator truth
                    try:
                        live_coord = bool(getattr(soco, "is_coordinator", False))
                    except Exception:
                        live_coord = False

                    # grouped truth (non-bonded members > 1)
                    try:
                        g = soco.group
                        if g:
                            nonbond = 0
                            for m in (g.members or []):
                                nm = (getattr(m, "player_name", "") or "").lower()
                                if not any(k in nm for k in ("sub", "left", "right", "surround")):
                                    nonbond += 1
                            live_grouped = (nonbond > 1)
                            if getattr(g, "coordinator", None):
                                live_group_name = getattr(g.coordinator, "player_name", live_group_name) or live_group_name
                    except Exception:
                        pass

                # current stored values
                cur_coord   = dev.states.get("GROUP_Coordinator", False)
                cur_grouped = dev.states.get("Grouped", False)
                cur_gname   = dev.states.get("GROUP_Name", dev.name)

                # normalize for compare
                norm_cur_coord   = (str(cur_coord).lower() == "true") if isinstance(cur_coord, str) else bool(cur_coord)
                norm_cur_grouped = (str(cur_grouped).lower() == "true") if isinstance(cur_grouped, str) else bool(cur_grouped)

                # log diffs (only when change)
                if norm_cur_coord != live_coord or norm_cur_grouped != live_grouped or cur_gname != live_group_name:
                    self.logger.warning(
                        f"[reconcile] {dev.name} "
                        f"Coord {norm_cur_coord}->{live_coord}  "
                        f"Grouped {norm_cur_grouped}->{live_grouped}  "
                        f"Name '{cur_gname}'->'{live_group_name}'"
                    )

                # ✅ write back SoCo truth as real booleans
                dev.updateStateOnServer("GROUP_Coordinator", True if live_coord else False)
                dev.updateStateOnServer("Grouped", True if live_grouped else False)
                dev.updateStateOnServer("GROUP_Name", live_group_name)

            # --- SAFETY SWEEP: coerce any lingering string states to booleans ---
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                g = dev.states.get("Grouped", None)
                if isinstance(g, str):
                    gs = g.strip().lower()
                    if gs in ("true", "false"):
                        dev.updateStateOnServer("Grouped", True if gs == "true" else False)
                        self.logger.warning(f"🧹 coerced Grouped '{g}' → {gs == 'true'} for {dev.name} [{reason}]")
                c = dev.states.get("GROUP_Coordinator", None)
                if isinstance(c, str):
                    cs = c.strip().lower()
                    if cs in ("true", "false"):
                        dev.updateStateOnServer("GROUP_Coordinator", True if cs == "true" else False)
                        self.logger.warning(f"🧹 coerced GROUP_Coordinator '{c}' → {cs == 'true'} for {dev.name} [{reason}]")

        except Exception as e:
            self.logger.error(f"❌ _refresh_all_group_states_helper failed: {e}")








    # at top of file (once)
    import inspect

    def _refresh_all_group_states_helper(self, reason: str = ""):
        """
        Canonical helper: recompute + write evaluated group truth back to Indigo.
        Call this everywhere instead of refresh_all_group_states() directly.
        """
        try:
            # Identify the immediate caller (function and line), forensics-friendly.
            try:
                _frm = inspect.stack()[1]
                _caller = f"{_frm.function}:{_frm.lineno}"
            except Exception:
                _caller = "<?>"

            if reason:
                self.logger.debug(f"🔁 refresh-all begin — {reason} (caller={_caller})")

            # 1) Recompute caches from SoCo
            self.refresh_all_group_states()

            groups     = getattr(self, "zone_group_state_cache", {}) or {}
            ip2dev     = getattr(self, "ip_to_indigo_device", {}) or {}
            soco_by_ip = getattr(self, "ip_to_soco_device", {}) or {}
            touched    = set()

            # quick snapshot of group keys/count
            self.logger.debug(f"[refresh] groups_seen={len(groups)} ip→dev={len(ip2dev)} soco_by_ip={len(soco_by_ip)}")

            # --- HARD GUARD: never write when inputs are empty (startup/teardown race) ---
            if not groups or not ip2dev or not soco_by_ip:
                self.logger.debug(
                    "[refresh] SKIP writes — insufficient data "
                    f"(groups={len(groups)} ip→dev={len(ip2dev)} soco_by_ip={len(soco_by_ip)} "
                    f"reason='{reason}' caller={_caller})"
                )
                if reason:
                    self.logger.debug(f"✅ refresh-all end — {reason} (skipped)")
                return
            # ------------------------------------------------------------------------------

            # 2) Apply to all devices seen in groups
            for gid, payload in groups.items():
                members = payload.get("members", []) or []
                if not members:
                    self.logger.debug(f"[refresh] group {gid}: no members; skipping")
                    continue

                # identify coordinator row/IP
                coord_row = next((m for m in members if m.get("coordinator", False)), members[0])
                coord_ip  = (coord_row.get("ip") or coord_row.get("location") or "").strip()
                coord_dev = ip2dev.get(coord_ip)

                # detail each member row (debug)
                for m in members:
                    mi  = (m.get("ip") or m.get("location") or "").strip()
                    mnm = (m.get("zone_name") or m.get("name") or "")
                    isc = bool(m.get("coordinator", False))
                    isb = any(k in mnm.lower() for k in ("sub", "left", "right", "surround"))
                    self.logger.debug(f"[group] gid={gid} member ip={mi} name='{mnm}' coord={isc} bonded={isb}")

                # non-bonded count → grouped eval
                non_bonded_ips = []
                for m in members:
                    ip = (m.get("ip") or m.get("location") or "").strip()
                    nm = (m.get("zone_name") or m.get("name") or "").lower()
                    if ip and not any(k in nm for k in ("sub", "left", "right", "surround")):
                        non_bonded_ips.append(ip)
                grouped_eval = (len(set(non_bonded_ips)) > 1)
                self.logger.debug(f"[group] gid={gid} eval non_bonded={len(set(non_bonded_ips))} → Grouped={grouped_eval}")

                # derive *room/group* name from SoCo first (not device title)
                group_name = (
                    (coord_row.get("name") or "").strip()
                    or (coord_row.get("zone_name") or "").strip()
                    or ((coord_dev.states.get("GROUP_Name", "") or "").strip() if coord_dev else "")
                    or (coord_dev.name if coord_dev else "Group")
                )
                self.logger.debug(
                    f"[group-name] gid={gid} coord_ip={coord_ip} "
                    f"computed_group_name='{group_name}' "
                    f"(row.name='{coord_row.get('name')}', zone_name='{coord_row.get('zone_name')}')"
                )

                # coordinator (write via canonical setter)
                if coord_dev:
                    self._set_group_states(coord_dev, grouped=grouped_eval, is_coord=True, group_name=group_name)
                    touched.add(coord_dev.id)
                else:
                    # A Sonos player with no matching Indigo device (e.g. never added) is
                    # normal — warn once per IP instead of on every topology evaluation.
                    if not hasattr(self, "_warned_unmapped_coord_ips"):
                        self._warned_unmapped_coord_ips = set()
                    if coord_ip not in self._warned_unmapped_coord_ips:
                        self._warned_unmapped_coord_ips.add(coord_ip)
                        self.logger.warning(
                            f"[group] ⚠️ coord_dev missing for coord_ip={coord_ip} — no Indigo device "
                            f"maps to this player (further occurrences logged at debug level)")
                    else:
                        self.logger.debug(f"[group] coord_dev missing for coord_ip={coord_ip}")

                # members (including bonded) mirror grouped/name; only coord has is_coord=true
                for m in members:
                    m_ip = (m.get("ip") or m.get("location") or "").strip()
                    if not m_ip:
                        self.logger.warning(f"[group] ⚠️ member missing IP in gid={gid}")
                        continue
                    m_dev = ip2dev.get(m_ip)
                    if not m_dev or (coord_dev and m_dev.id == coord_dev.id):
                        continue
                    self._set_group_states(m_dev, grouped=grouped_eval, is_coord=False, group_name=group_name)
                    touched.add(m_dev.id)

            # 3) Anything not touched this pass = standalone (not grouped)
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                if dev.id in touched:
                    continue
                ip = (dev.address or "").strip()
                soco = soco_by_ip.get(ip)
                is_coord_live = False
                try:
                    is_coord_live = bool(getattr(soco, "is_coordinator", False)) if soco else False
                except Exception:
                    pass
                # keep prior GROUP_Name if set; else fallback to device name
                fallback_name = (dev.states.get("GROUP_Name", "") or "").strip() or dev.name
                self._set_group_states(dev, grouped=False, is_coord=is_coord_live, group_name=fallback_name)

            if reason:
                self.logger.debug(f"✅ refresh-all end — {reason}")

            # Optional reconciliation with live SoCo (left as-is)
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                ip = (dev.address or "").strip()
                soco = soco_by_ip.get(ip)

                live_coord = False
                live_grouped = False
                live_group_name = dev.name

                if soco:
                    try:
                        live_coord = bool(getattr(soco, "is_coordinator", False))
                    except Exception:
                        live_coord = False
                    try:
                        g = soco.group
                        if g:
                            nonbond = 0
                            for m in (g.members or []):
                                nm = (getattr(m, "player_name", "") or "").lower()
                                if not any(k in nm for k in ("sub", "left", "right", "surround")):
                                    nonbond += 1
                            live_grouped = (nonbond > 1)
                            if getattr(g, "coordinator", None):
                                gn = getattr(g.coordinator, "player_name", "") or ""
                                if gn:
                                    live_group_name = gn
                    except Exception:
                        pass

                self._set_group_states(dev, grouped=live_grouped, is_coord=live_coord, group_name=live_group_name)

        except Exception as e:
            self.logger.error(f"❌ _refresh_all_group_states_helper failed: {e}")






    ############################################################################################
    ### Dump Groups To Log by master coordinator
    ############################################################################################


    def dump_by_master(self):
        """
        Dumps the ZoneGroupState parsed group data as seen from the Sonos perspective (zone_group_state_cache).
        """
        if not hasattr(self, "zone_group_state_cache") or not self.zone_group_state_cache:
            self.logger.warning("🚫 No zone group data available to dump.")
            return

        self.logger.info("\n📦 Dumping Sonos / SOCO view of grouped devices to the log...")
        devices_in_parsed_groups = set()

        for group_id, group_data in self.zone_group_state_cache.items():
            if not isinstance(group_data, dict):
                self.logger.warning(f"⚠️ Skipping invalid group_data for '{group_id}' (expected dict, got {type(group_data)})")
                continue

            members = group_data.get("members", [])
            if not members:
                continue

            # 👉 Skip "synthetic" groups that have no coordinator flagged
            has_coordinator = False
            try:
                for _m in members:
                    if isinstance(_m, dict):
                        if bool(_m.get("coordinator", False)):
                            has_coordinator = True
                            break
                    elif isinstance(_m, int):
                        _dev = indigo.devices.get(_m)
                        if _dev and _dev.states.get("GROUP_Coordinator", "false") == "true":
                            has_coordinator = True
                            break
            except Exception:
                pass

            if not has_coordinator:
                # These are usually bonded-only injections (e.g., subs/surrounds) without a coordinator.
                # We skip them to avoid duplicate-looking groups like:
                #   ['Office','Office']  and then  ['Sonos Office Play5 Left','Sonos Office Play5 Right']
                self.logger.debug(f"🧹 Skipping non-coordinator (synthetic) group cache entry: {group_id}")
                continue

            member_rows = []
            device_names_in_group = []

            for member in members:
                try:
                    if isinstance(member, dict):
                        name = member.get("name", "?")                     # Sonos room name
                        ip = member.get("ip", "?")
                        bonded = member.get("bonded", False)
                        is_coordinator = member.get("coordinator", False)
                        indigo_dev = self.ip_to_indigo_device.get(ip)
                        indigo_dev = indigo.devices.get(indigo_dev) if isinstance(indigo_dev, int) else indigo_dev
                        indigo_name = indigo_dev.name if indigo_dev else "(unmapped)"
                        indigo_id = indigo_dev.id if indigo_dev else "-"
                        grouped_state = indigo_dev.states.get("Grouped", "?") if indigo_dev else "?"
                    elif isinstance(member, int):
                        dev = indigo.devices.get(member)
                        if not dev:
                            self.logger.debug(f"⚠️ Could not resolve injected device ID {member}")
                            continue

                        # 🔧 Keep display name consistent with Sonos room/group naming
                        name = dev.states.get("GROUP_Name", dev.name)       # show room/group name here
                        ip = dev.address if dev.address else "?"
                        bonded = "sub" in dev.name.lower()
                        is_coordinator = (dev.states.get("GROUP_Coordinator", "false") == "true")
                        indigo_name = dev.name                               # still show Indigo device name in its own column
                        indigo_id = dev.id
                        grouped_state = dev.states.get("Grouped", "?")
                    else:
                        self.logger.warning(f"⚠️ Skipping invalid member in group '{group_id}': {member}")
                        continue

                    role = "Master (Coordinator)" if is_coordinator else "Slave"
                    plugin_grouped = "true" if grouped_state in (True, "true") else "false"

                    device_names_in_group.append(name)
                    if isinstance(member, dict) and indigo_dev:
                        devices_in_parsed_groups.add(indigo_dev.id)
                    elif isinstance(member, int):
                        devices_in_parsed_groups.add(indigo_id)

                    self.logger.debug(
                        f"🔍 Adding member row: name={name}, ip={ip}, role={role}, "
                        f"indigo={indigo_name}, bonded={bonded}, grouped={grouped_state}, plugin_state={plugin_grouped}"
                    )

                    member_rows.append({
                        "Device Name": name,
                        "IP Address": ip,
                        "Role": role,
                        "Indigo Device": indigo_name,
                        "Indigo ID": indigo_id,
                        "Bonded": str(bonded),
                        "Grouped": str(grouped_state),
                        "Plugin State": plugin_grouped
                    })

                except Exception as e:
                    self.logger.warning(f"⚠️ Skipping invalid member in group '{group_id}': {e}")
                    continue

            col_widths = [30, 20, 25, 30, 10, 8, 8, 10]
            total_width = sum(col_widths) + len(col_widths) - 1

            self.logger.info("")
            self.logger.info(f"🧑‍💻 Devices in group (ZonePlayerUUIDsInGroup): {device_names_in_group}")
            self.logger.info("{:<30} {:<20} {:<25} {:<30} {:<10} {:<8} {:<8} {:<10}".format(
                "Device Name", "IP Address", "Role", "Indigo Device", "Indigo ID",
                "Bonded", "Grouped", "Plugin State"
            ))
            self.logger.info("=" * total_width)

            for row in member_rows:
                self.logger.info("{:<30} {:<20} {:<25} {:<30} {:<10} {:<8} {:<8} {:<10}".format(
                    row["Device Name"], row["IP Address"], row["Role"],
                    row["Indigo Device"], str(row["Indigo ID"]), row["Bonded"],
                    row["Grouped"], row["Plugin State"]
                ))




    ############################################################################################
    ### Dump Groups To Log by logical group
    ############################################################################################

    def old_dump_by_logical_group(self):
        """
        Dumps the plugin-evaluated logical group state summary.
        """
        if not hasattr(self, "evaluated_group_members_by_coordinator") or not self.evaluated_group_members_by_coordinator:
            self.logger.warning("🚫 No plugin-evaluated group info available.")
            return

        self.logger.info("\n🔍 Evaluated Grouped Logic Summary (plugin-level view):")

        # Absolute column widths for fixed starts
        DEVICE_W  = 33  # prefix + name cell (you said this already lines up fine)
        ROLE_W    = 27
        BONDED_W  = 12
        GROUPED_W = 20
        GNAME_W   = 22
        TOTAL_W   = DEVICE_W + ROLE_W + BONDED_W + GROUPED_W + GNAME_W

        # Small helper to pad (or truncate) any cell to an exact width
        def _pad(cell: str, width: int) -> str:
            s = cell if cell is not None else ""
            if len(s) < width:
                s = s + (" " * (width - len(s)))
            else:
                s = s[:width]
            return s

        # Header
        self.logger.info("")
        header = (
            _pad("Device Name", DEVICE_W) +
            _pad("Role",        ROLE_W) +
            _pad("Bonded",      BONDED_W) +
            _pad("Logical Group", GROUPED_W) +
            _pad("Group Name",  GNAME_W)
        )
        self.logger.info(header)
        self.logger.info("=" * TOTAL_W)
        self.logger.info("")

        for coordinator_name, dev_list in sorted(self.evaluated_group_members_by_coordinator.items()):
            self.logger.info(f"🎧 Group: {coordinator_name}")
            self.logger.info("-" * TOTAL_W)

            for indigo_dev in sorted(dev_list, key=lambda d: d.name.lower()):
                # 🔬 Drift check (diagnostic only; no behavior change)
                try:
                    live_dev = indigo.devices[indigo_dev.id]
                    cached_g = indigo_dev.states.get("Grouped", "?")
                    live_g   = live_dev.states.get("Grouped", "?")
                    if cached_g != live_g:
                        self.logger.warning(
                            f"🧪 Drift: {indigo_dev.name} cached_Grouped='{cached_g}' "
                            f"current_Grouped='{live_g}' cached_obj_id={id(indigo_dev)} live_obj_id={id(live_dev)}"
                        )
                except Exception:
                    pass

                # Coordinator vs slave
                is_coord = indigo_dev.states.get("GROUP_Coordinator", "false") == "true"
                role = "Master (Coordinator)" if is_coord else "Slave"

                # Bonded detection (prefer states, else name heuristic)
                bonded_state = (
                    indigo_dev.states.get("GROUP_Bonded", None) or
                    indigo_dev.states.get("Bonded",       None)
                )
                if isinstance(bonded_state, str):
                    bonded_bool = (bonded_state.lower() == "true")
                elif isinstance(bonded_state, bool):
                    bonded_bool = bonded_state
                else:
                    name_lc = indigo_dev.name.lower()
                    bonded_bool = any(t in name_lc for t in ("sub", "left", "right", "surround"))

                bonded_display = "🎯 True" if bonded_bool else "◻️ False"

                # Grouped display
                grouped = indigo_dev.states.get("Grouped", "?")
                grouped_display = (
                    "✅ true" if grouped in (True, "true") else
                    "❌ false" if grouped in (False, "false") else
                    f"❓ {grouped}"
                )

                # Group name
                group_name = indigo_dev.states.get("GROUP_Name") or self.group_name_by_device_id.get(indigo_dev.id, "?")

                # Name prefix — coordinator vs non-coordinator
                # (You said name column lines up, so we leave it alone.)
                name_prefix = "🔹 " if is_coord else "▫️ "
                name_cell = f"{name_prefix}{indigo_dev.name}"

                # ✅ Visual correction: when the row is a SLAVE, nudge ALL subsequent columns
                # (Role / Bonded / Evaluated / Group Name) 1 space to the RIGHT so their
                # starting character matches the coordinator rows exactly.
                slave_offset = " " if not is_coord else ""

                # Build the fixed-width row by concatenation (absolute starts)
                line = (
                    _pad(name_cell, DEVICE_W) +
                    _pad(slave_offset + role,           ROLE_W)   +
                    _pad(slave_offset + bonded_display, BONDED_W) +
                    _pad(slave_offset + grouped_display,GROUPED_W)+
                    _pad(slave_offset + group_name,     GNAME_W)
                )
                self.logger.info(line)

            self.logger.info("")



    def dump_by_logical_group(self):
        """
        Dumps the plugin-evaluated logical group state summary.
        """
        if not hasattr(self, "evaluated_group_members_by_coordinator") or not self.evaluated_group_members_by_coordinator:
            self.logger.warning("🚫 No plugin-evaluated group info available.")
            return

        self.logger.info("\n🔍 Evaluated Grouped Logic Summary (plugin-level view):")

        # Absolute column widths for fixed starts
        DEVICE_W  = 33  # prefix + name cell (you said this already lines up fine)
        ROLE_W    = 27
        BONDED_W  = 12
        GROUPED_W = 20
        GNAME_W   = 22
        TOTAL_W   = DEVICE_W + ROLE_W + BONDED_W + GROUPED_W + GNAME_W

        # Small helper to pad (or truncate) any cell to an exact width
        def _pad(cell: str, width: int) -> str:
            s = cell if cell is not None else ""
            if len(s) < width:
                s = s + (" " * (width - len(s)))
            else:
                s = s[:width]
            return s

        # Header
        self.logger.info("")
        header = (
            _pad("Device Name", DEVICE_W) +
            _pad("Role",        ROLE_W) +
            _pad("Bonded",      BONDED_W) +
            _pad("Logical Group", GROUPED_W) +
            _pad("Group Name",  GNAME_W)
        )
        self.logger.info(header)
        self.logger.info("=" * TOTAL_W)
        self.logger.info("")

        for coordinator_name, dev_list in sorted(self.evaluated_group_members_by_coordinator.items()):
            self.logger.info(f"🎧 Group: {coordinator_name}")
            self.logger.info("-" * TOTAL_W)

            for indigo_dev in sorted(dev_list, key=lambda d: d.name.lower()):
                # 🔬 Drift check (diagnostic only; no behavior change)
                try:
                    live_dev = indigo.devices[indigo_dev.id]
                    cached_g = indigo_dev.states.get("Grouped", "?")
                    live_g   = live_dev.states.get("Grouped", "?")
                    if cached_g != live_g:
                        self.logger.debug(
                            f"🧪 Drift: {indigo_dev.name} cached_Grouped='{cached_g}' "
                            f"current_Grouped='{live_g}' cached_obj_id={id(indigo_dev)} live_obj_id={id(live_dev)}"
                        )
                except Exception:
                    live_dev = indigo_dev  # fall back to cached if lookup fails

                # 🔎 STATE TRACE (exact line you requested)
                dev = live_dev  # alias so the format matches your snippet verbatim
                try:
                    self.logger.debug(
                        f"[state-trace] {dev.name}: Grouped={repr(dev.states.get('Grouped'))} "
                        f"type={type(dev.states.get('Grouped')).__name__} "
                        f"Coord={repr(dev.states.get('GROUP_Coordinator'))}"
                    )
                except Exception:
                    pass

                # Coordinator vs slave
                is_coord = indigo_dev.states.get("GROUP_Coordinator", "false") == "true"
                role = "Master (Coordinator)" if is_coord else "Slave"

                # Bonded detection (prefer states, else name heuristic)
                bonded_state = (
                    indigo_dev.states.get("GROUP_Bonded", None) or
                    indigo_dev.states.get("Bonded",       None)
                )
                if isinstance(bonded_state, str):
                    bonded_bool = (bonded_state.lower() == "true")
                elif isinstance(bonded_state, bool):
                    bonded_bool = bonded_state
                else:
                    name_lc = indigo_dev.name.lower()
                    bonded_bool = any(t in name_lc for t in ("sub", "left", "right", "surround"))

                bonded_display = "🎯 True" if bonded_bool else "◻️ False"

                # Grouped display
                grouped = indigo_dev.states.get("Grouped", "?")
                grouped_display = (
                    "✅ true" if grouped in (True, "true") else
                    "❌ false" if grouped in (False, "false") else
                    f"❓ {grouped}"
                )

                # Group name
                group_name = indigo_dev.states.get("GROUP_Name") or self.group_name_by_device_id.get(indigo_dev.id, "?")

                # Name prefix — coordinator vs non-coordinator
                # (You said name column lines up, so we leave it alone.)
                name_prefix = "🔹 " if is_coord else "▫️ "
                name_cell = f"{name_prefix}{indigo_dev.name}"

                # ✅ Visual correction: when the row is a SLAVE, nudge ALL subsequent columns
                # (Role / Bonded / Evaluated / Group Name) 1 space to the RIGHT so their
                # starting character matches the coordinator rows exactly.
                slave_offset = " " if not is_coord else ""

                # Build the fixed-width row by concatenation (absolute starts)
                line = (
                    _pad(name_cell, DEVICE_W) +
                    _pad(slave_offset + role,           ROLE_W)   +
                    _pad(slave_offset + bonded_display, BONDED_W) +
                    _pad(slave_offset + grouped_display,GROUPED_W)+
                    _pad(slave_offset + group_name,     GNAME_W)
                )
                self.logger.info(line)

            self.logger.info("")











    ############################################################################################
    ### Dump Groups To Log by inventory
    ############################################################################################

    def dump_by_inventory(self):
        """
        Dumps a full audit of all Sonos Indigo devices including grouping, coordinator, bonded status,
        and plugin-evaluated group coordinator.
        """
        self.logger.info("\n📋 Full Indigo Device Audit Across All Indigo Registered Sonos Devices:")

        # Updated columns with Indigo ID and Group Coord
        audit_cols = [32, 15, 10, 12, 8, 14, 10, 10, 10, 32]
        audit_total_width = sum(audit_cols)
        audit_fmt = "{:<32} {:<15} {:<10} {:<12} {:<8} {:<14} {:<10} {:<10} {:<10} {:<32}"

        self.logger.info("")
        self.logger.info(audit_fmt.format(
            "Device Name", "IP Address", "Grouped", "Coordinator", "Bonded",
            "Group", "XML", "Evaluated", "Indigo ID", "Group Coord"
        ))
        self.logger.info("=" * audit_total_width)

        # Devices seen in XML-parsed group data
        devices_in_parsed_groups = set()
        if hasattr(self, "zone_group_state_cache"):
            for group in self.zone_group_state_cache.values():
                for member in group.get("members", []):
                    if isinstance(member, dict):
                        ip = member.get("ip")
                        dev = self.ip_to_indigo_device.get(ip)
                        if isinstance(dev, indigo.Device):
                            devices_in_parsed_groups.add(dev.id)
                        elif isinstance(dev, int):
                            devices_in_parsed_groups.add(dev)

        # Devices in plugin-evaluated groups
        devices_in_evaluated = set()
        coord_by_device_id = {}
        if hasattr(self, "evaluated_group_members_by_coordinator"):
            for devs in self.evaluated_group_members_by_coordinator.values():
                coordinator = None
                for dev in devs:
                    if dev.states.get("GROUP_Coordinator", "false") == "true":
                        coordinator = dev.name
                        break
                for dev in devs:
                    devices_in_evaluated.add(dev.id)
                    coord_by_device_id[dev.id] = coordinator or "(unknown)"

        # Iterate over all Indigo Sonos devices
        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            name = dev.name
            ip = dev.address if hasattr(dev, "address") else dev.states.get("ip", "?")
            grouped = dev.states.get("Grouped", "?")

            # 🟢 Use live SoCo state to determine coordinator
            soco = self.ip_to_soco_device.get(ip)
            if soco:
                try:
                    coordinator = "True" if soco.is_coordinator else "False"
                except Exception as e:
                    self.logger.debug(f"Coordinator check failed for {dev.name} ({ip}): {e}")
                    coordinator = "?"
            else:
                self.logger.debug(f"No SoCo object found for {dev.name} ({ip})")
                coordinator = "?"

            # Group name truncation
            group_name = dev.states.get("GROUP_Name", "?")
            if len(group_name) > 12:
                group_name = group_name[:12] + "…"

            bonded = "sub" in name.lower() or "surround" in name.lower() or "left" in name.lower() or "right" in name.lower()
            in_xml = "Yes" if dev.id in devices_in_parsed_groups else "No"
            in_eval = "Yes" if dev.id in devices_in_evaluated else "No"

            # Group coordinator truncation
            group_coord = coord_by_device_id.get(dev.id, "-")
            if len(group_coord) > 12:
                group_coord = group_coord[:12] + "…"

            self.logger.info(audit_fmt.format(
                name, ip, str(grouped), coordinator,
                "Yes" if bonded else "No", group_name, in_xml, in_eval,
                str(dev.id), group_coord
            ))

        self.logger.info("")






    ############################################################################################
    ### Dump Groups To Log - All three
    ############################################################################################
    def dump_groups_to_log(self):
        """
        Wrapper method to dump full Sonos group state using all perspectives:
        1. dump_by_master()        — Sonos-derived ZoneGroupState from XML
        2. dump_by_logical_group() — Plugin-evaluated group logic
        3. dump_by_inventory()     — Full inventory audit of all Sonos Indigo devices
        """
        self.logger.info("🗂️ Starting full group state dump (Sonos + Plugin view)...")

        # Run evaluation first so we have fresh plugin-evaluated states
        self.evaluate_and_update_grouped_states()

        # 🔍 Pre-check — log each device's current Grouped state from Indigo
        #self.logger.warning("⚠️ Pre-dump: Current Indigo device 'Grouped' values (post evaluation):")
        #for dev in indigo.devices.iter("self"):
        #    grouped_val = dev.states.get("Grouped", None)
        #    self.logger.warning(f"   {dev.name} — Grouped = {grouped_val!r}")

        full_separator = "─" * 179

        self.logger.info("\n" + full_separator + "\n")
        self.dump_by_master()

        self.logger.info("\n" + full_separator + "\n")
        self.dump_by_inventory()
        self.logger.info("\n" + full_separator + "\n")

        self.logger.info("\n" + full_separator + "\n")
        self.dump_by_logical_group()

        self.logger.info("✅ Group state dump complete.")






    ############################################################################################
    ### End - Dump Groups To Log
    ############################################################################################



    def _compute_announce_publish_host(self):
        # Don’t publish loopback/any.
        def _ok(h):
            return h and h not in ("localhost", "0.0.0.0", "::1") and not str(h).startswith("127.")
        # Preference order: explicit pref → selected interface → bound host if routable
        candidates = [
            (getattr(self, "HTTPServer", "") or "").strip(),
            (getattr(self, "selectedInterfaceIP", "") or "").strip(),
            (getattr(self, "_announce_bound_host", "") or "").strip(),
        ]
        for h in candidates:
            if _ok(h):
                return h
        return ""





    def refresh_all_group_states(self):
        """
        Refresh and evaluate current Sonos zone groups using the SoCo .group property.
        """
        self.logger.debug("🔁 Entering Refresh_all_group_states")
        self.logger.debug("🔁 Forcing group topology refresh and evaluation using SoCo group objects...")

        groups = {}
        seen_members = set()

        # NEW: build a coordinator-by-IP map for downstream use (e.g., evaluate_and_update_grouped_states)
        # Ensure the instance attribute exists and start from it (in case other paths populated it)
        if not hasattr(self, "_eval_coord_dev_by_ip") or not isinstance(getattr(self, "_eval_coord_dev_by_ip"), dict):
            self._eval_coord_dev_by_ip = {}
        _eval_coord_dev_by_ip = {}  # fresh build each pass

        # NEW: also track grouped state per coordinator IP (purely plugin logical; optional)
        if not hasattr(self, "_eval_grouped_by_coord_ip") or not isinstance(getattr(self, "_eval_grouped_by_coord_ip"), dict):
            self._eval_grouped_by_coord_ip = {}
        _eval_grouped_by_coord_ip = {}

        # ─────────────────────────────────────────────────────────────────────────────
        # PASS 1: Walk every SoCo group and record coordinator→IP→Indigo device mapping
        # ─────────────────────────────────────────────────────────────────────────────
        for loop_ip, soco in self.soco_by_ip.items():
            try:
                if not self._ip_probe_ok(loop_ip):
                    continue  # offline player — .group would block in a network timeout
                group = soco.group
                if not group or not group.coordinator:
                    continue

                coord = group.coordinator
                coord_ip = (getattr(coord, "ip_address", "") or "").strip()
                if not coord_ip:
                    coord_ip = (loop_ip or "").strip()

                if not coord_ip:
                    self.logger.warning(f"[coord-skip] Missing coordinator IP for group uid={getattr(coord, 'uid', '(unknown)')}")
                    continue

                # Map coordinator IP → Indigo device (IP-only policy)
                indigo_dev = self.ip_to_indigo_device.get(coord_ip)
                _eval_coord_dev_by_ip[coord_ip] = indigo_dev

                # DEBUG/WARN so we can see it happening
                #self.logger.warning(f"🌐 PASS1 mapped coordinator: uid={getattr(coord,'uid',None)} ip={coord_ip} dev={(indigo_dev.name if indigo_dev else '(none)')}")

            except Exception as e:
                self.logger.warning(f"⚠️ Failed PASS1 mapping for {loop_ip}: {e}")

        # ─────────────────────────────────────────────────────────────────────────────
        # PASS 2: Build groups cache (include ALL members, including subs)
        #        NOTE: decide Grouped ONCE per coordinator after the loop to avoid
        #        flip-flops when the same group is seen multiple times in this pass.
        # ─────────────────────────────────────────────────────────────────────────────
        coord_nonbonded_max = {}  # coord_ip -> max(non_bonded_count) seen across loop iterations

        for loop_ip, soco in self.soco_by_ip.items():
            try:
                if not self._ip_probe_ok(loop_ip):
                    continue  # offline player — .group would block in a network timeout
                group = soco.group
                if not group or not group.coordinator:
                    continue

                group_id = group.coordinator.uid
                if group_id not in groups:
                    groups[group_id] = {
                        "coordinator": group.coordinator.uid,
                        "members": [],
                    }

                # Count members (non-bonded vs bonded purely informational)
                non_bonded_count = 0

                for member in group.members:
                    member_uuid = member.uid
                    if member_uuid in seen_members:
                        continue
                    seen_members.add(member_uuid)

                    zone_name = (member.player_name or "").lower()

                    # IP-only: always get an IP; fall back to loop ip if needed
                    member_ip = (getattr(member, "ip_address", "") or "").strip()
                    if not member_ip:
                        member_ip = (loop_ip or "").strip()

                    is_coord = (str(member_uuid) == str(group.coordinator.uid))
                    is_bonded = any(k in zone_name for k in ("sub", "left", "right", "surround"))

                    groups[group_id]["members"].append({
                        "uuid": member_uuid,
                        "location": member_ip,
                        "zone_name": zone_name,
                        "name": member.player_name,
                        "ip": member_ip,
                        # Use UUID equality, not object identity, to mark coordinator
                        "coordinator": is_coord,
                        "bonded": is_bonded
                    })

                    if not is_bonded:
                        non_bonded_count += 1

                    # DEBUG/WARN row so we can watch exactly what we add
                    #self.logger.warning(
                    #    f"🧩 PASS2 add member: group={group_id} name='{member.player_name}' "
                    #    f"ip={member_ip} uuid={member_uuid} coord={is_coord} bonded={is_bonded}"
                    #)

                # Record the strongest view of non-bonded count per coordinator IP during this pass.
                coord_ip = (getattr(group.coordinator, "ip_address", "") or loop_ip or "").strip()
                if coord_ip:
                    prev = coord_nonbonded_max.get(coord_ip, 0)
                    # take the max to avoid later partial/filtered iterations downgrading the count
                    coord_nonbonded_max[coord_ip] = max(prev, non_bonded_count)

                    # (moved final grouped decision to a separate finalize step below)

            except Exception as e:
                self.logger.warning(f"⚠️ Failed PASS2 building for {loop_ip}: {e}")

        # FINALIZE grouped decision once per coordinator IP (prevents true→false overwrite)
        for coord_ip, nb_count in coord_nonbonded_max.items():
            grouped_val = "true" if nb_count > 1 else "false"
            _eval_grouped_by_coord_ip[coord_ip] = grouped_val
            #self.logger.warning(f"📏 PASS2 grouped decision (final): coord_ip={coord_ip} non_bonded={nb_count} → {grouped_val}")

        # Persist results to the instance
        self.zone_group_state_cache = groups
        self._eval_coord_dev_by_ip = _eval_coord_dev_by_ip
        self._eval_grouped_by_coord_ip = _eval_grouped_by_coord_ip

        # Final visibility
        self.logger.debug(f"💾 zone_group_state_cache groups={len(groups)} coord_ip_map={len(_eval_coord_dev_by_ip)}")
        self.logger.debug("🔁 Exiting Refresh_all_group_states")
        #self.evaluate_and_update_grouped_states()












    def Old_b4_delete_get_all_zone_groups(self):
        """Fetch and apply the latest zone group topology across all devices."""
        self.logger.warning("🔁 Initiating full group topology refresh...")

        updated = False
        for soco in self.soco_by_ip.values():
            try:
                #topology = soco.zoneGroupTopology
                topology = soco.zoneGroupTopology.to_xml_string()
                self.zone_group_state_cache = self.parse_zone_group_state(topology)
                self.logger.debug(f"📦 Zone group state updated from {soco.ip_address}")
                updated = True
                break  # Successfully fetched topology from one active player
            except Exception as e:
                self.logger.warning(f"⚠️ Could not fetch group topology from {soco.ip_address}: {e}")

        if not updated:
            self.logger.error("❌ Failed to update zone group state from any device")
            return

        # Re-evaluate all known Indigo devices
        self.logger.warning("🔍 Re-evaluating all Indigo Sonos devices with updated group state...")
        for dev in indigo.devices.iter("self"):
            try:
                self.refresh_group_topology_after_plugin_zone_change()
                #self.evaluate_and_update_grouped_states(dev)
            except Exception as e:
                self.logger.error(f"❌ Error re-evaluating group state for {dev.name}: {e}")

        # Optional debug dump
        if hasattr(self, "dump_groups_to_log"):
            self.dump_groups_to_log()




    ############################################################################################
    ### SiriusXM Generic Channel Changer and helpers based on only needing a GUID
    ############################################################################################

    def channelUpOrDown(self, dev, direction):
        import re


        # --- bootstrap cache so first XM hop works even after cold start ---
        if not hasattr(self, "last_known_sxm_channel"):
            self.last_known_sxm_channel = {}

        # Try to seed from current device state if this zone isn't cached yet
        zoneIP = dev.pluginProps.get("address")
        if zoneIP and zoneIP not in self.last_known_sxm_channel:
            # 1) Parse "CH N - Name" from ZP_STATION if available
            try:
                st = dev.states.get("ZP_STATION", "") or ""
                m = re.search(r"\bCH\s+(\d{1,4})\b", st, re.IGNORECASE)
                if m:
                    self.last_known_sxm_channel[zoneIP] = int(m.group(1))
            except Exception:
                pass

            # 2) If still unknown, try to pull GUID from current URI and map to a channel number
            if zoneIP not in self.last_known_sxm_channel:
                try:
                    uri = (dev.states.get("ZP_CurrentTrackURI", "") or
                           dev.states.get("ZP_AVTransportURI", "") or "")
                    # look for "...channel-linear:<guid>..."
                    gm = re.search(r"channel-linear[:%3a]([0-9a-fA-F-]{16,})", uri)
                    if gm and getattr(self, "siriusxm_channels", None):
                        guid = gm.group(1).lower()
                        ch = next((c for c in self.siriusxm_channels
                                   if str(c.get("guid", "")).lower() == guid), None)
                        if ch and ch.get("channel_number") is not None:
                            try:
                                self.last_known_sxm_channel[zoneIP] = int(str(ch["channel_number"]).strip())
                            except Exception:
                                pass
                except Exception:
                    pass
                

        self.logger.info(f"📝 Determining next SiriusXM channel (using cached value)...")

        try:
            zoneIP = dev.pluginProps.get("address")
            if not zoneIP:
                self.logger.warning(f"⚠️ Device {dev.name} has no IP address configured.")
                return

            if not hasattr(self, "last_known_sxm_channel"):
                self.logger.warning(f"⚠️ No last known SiriusXM channel cache exists.")
                return

            current_channel_number = self.last_known_sxm_channel.get(zoneIP)
            if current_channel_number is None:
                self.logger.warning(f"⚠️ No cached SiriusXM channel for zone {zoneIP}. Cannot proceed.")
                return

            self.safe_debug(f"🔍 Cached current channel number: {current_channel_number}")

            # Clean, normalize, and validate channel list
            valid_channels = []
            for ch in self.siriusxm_channels:
                raw_ch_num = ch.get("channel_number")
                if raw_ch_num is None:
                    self.logger.warning(f"🚫 Skipping malformed channel (missing number): {ch.get('name')}")
                    continue
                try:
                    clean_ch_num = int(str(raw_ch_num).strip())

                    # ⛳ Minimal guard to avoid 19xx “team” feeds that can 402 on SetAVTransportURI
                    if not (1 <= clean_ch_num <= 999):
                        continue  # ← added filter; everything else remains unchanged

                    ch["channel_number"] = clean_ch_num  # Normalize in-place as int
                    valid_channels.append(ch)
                except Exception:
                    self.logger.warning(f"🚫 Skipping malformed channel: {ch.get('name')} — channel_number = {repr(raw_ch_num)}")
                    self.safe_debug(f"⤵️ Raw channel object: {ch}")

            if not valid_channels:
                self.logger.error("❌ No valid SiriusXM channels found for navigation.")
                return

            # Sort by channel_number
            sorted_channels = sorted(valid_channels, key=lambda c: c["channel_number"])

            # Log all valid channels
            self.safe_debug("📋 Dumping all known SiriusXM channels (sorted):")
            for ch in sorted_channels:
                self.safe_debug(f" - CH {ch['channel_number']} | {ch.get('name')} | GUID: {ch.get('guid')}")

            # Find current index
            current_index = next(
                (i for i, ch in enumerate(sorted_channels)
                 if ch["channel_number"] == current_channel_number),
                None
            )

            # If current channel isn't in the list (or cache got stale), clamp to edge per direction
            if current_index is None:
                if direction == "up":
                    current_index = -1  # so +1 lands at 0 below
                else:
                    current_index = 0   # so -1 wraps to last below

            # Compute initial next/prev candidate with wrap
            if direction == "up":
                next_index = (current_index + 1) % len(sorted_channels)
            else:
                next_index = (current_index - 1 + len(sorted_channels)) % len(sorted_channels)

            # Robust selection: skip malformed/unplayable entries and avoid infinite loops
            attempts = 0
            chosen = None
            idx = next_index
            while attempts < len(sorted_channels):
                cand = sorted_channels[idx]
                cand_num = cand.get("channel_number")
                cand_guid = cand.get("guid")
                if cand_guid and isinstance(cand_num, int):
                    chosen = cand
                    break
                # advance in requested direction with wrap
                if direction == "up":
                    idx = (idx + 1) % len(sorted_channels)
                else:
                    idx = (idx - 1 + len(sorted_channels)) % len(sorted_channels)
                attempts += 1

            if not chosen:
                self.logger.error("❌ Could not find a valid next/previous SiriusXM channel to tune.")
                return

            next_channel = chosen
            next_guid = next_channel.get("guid")

            self.logger.info(
                f"🔀 Switching {direction} from CH {current_channel_number} to "
                f"CH {next_channel['channel_number']} - {next_channel.get('name')}"
            )

            # Send the next channel
            self.sendSiriusXMChannel(zoneIP, next_guid, next_channel.get("name"))

        except Exception as e:
            self.logger.error(f"❌ Failed to switch channel {direction} for {dev.name}: {e}")




    def _is_benign_upnp_402(self, err_obj) -> bool:
        """
        Returns True if the exception looks like the known-benign UPnP 402 'Invalid Args'
        we see when sending custom SiriusXM URIs. These often still succeed.
        """
        try:
            s = str(err_obj) if err_obj is not None else ""
            return ("UPnPError" in s) and ("402" in s or "Invalid Args" in s or "errorCode>402<" in s)
        except Exception:
            return False


    def SiriusXMChannelChanger(self, dev, guid):
        try:
            zoneIP = dev.pluginProps.get("address")
            if not zoneIP:
                self.logger.error(f"❌ No IP address found for device {dev.name}")
                return

            if not guid:
                self.logger.warning(f"⚠️ No SiriusXM GUID provided for device {dev.name}")
                return

            # 🔍 Lookup channel info by GUID
            channel = next((ch for ch in self.siriusxm_channels if ch.get("guid") == guid), None)
            if not channel:
                self.logger.warning(f"⚠️ No SiriusXM channel found for GUID: {guid}")
                return

            ch_number = channel.get("channel_number", "?")
            ch_name = channel.get("name", "Unknown")
            album_art = channel.get("albumArtURI", "")
            title = f"CH {ch_number} - {ch_name}"
            uri = f"x-sonosapi-hls:channel-linear:{guid}?sid=37&flags=8232&sn=3"

            metadata = (
                '<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" '
                'xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" '
                'xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" '
                'xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">'
                '<item id="10092020" parentID="10092020" restricted="true">'
                f'<dc:title>{title}</dc:title>'
                '<upnp:class>object.item.audioItem.audioBroadcast</upnp:class>'
                '<desc id="cdudn" nameSpace="urn:schemas-rinconnetworks-com:metadata-1-0/">'
                'SA_RINCON65031_</desc>'
                '</item>'
                '</DIDL-Lite>'
            )

            self.logger.info(f"📻 Switching {dev.name} to SiriusXM: {title}")
            self.safe_debug(f"🛰 URI: {uri}")
            self.safe_debug(f"📦 Metadata:\n{metadata}")

            # ✅ Use cached SoCo object
            soco_dev = self.soco_by_ip.get(zoneIP)
            if not soco_dev:
                from soco import SoCo
                soco_dev = SoCo(zoneIP)
                self.soco_by_ip[zoneIP] = soco_dev

            # 🎯 Attempt SetAVTransportURI with error handling
            try:
                soco_dev.avTransport.SetAVTransportURI([
                    ('InstanceID', 0),
                    ('CurrentURI', uri),
                    ('CurrentURIMetaData', metadata),
                ])
                time.sleep(0.5)
                soco_dev.play()

            except Exception as upnp_err:
                # --- inserted: treat UPnP 402 "Invalid Args" as benign for custom SXM URIs ---
                err = str(upnp_err) if upnp_err is not None else ""
                is_402 = (
                    "UPnPError" in err and (
                        "402" in err or
                        "Invalid Args" in err or
                        "errorCode>402<" in err
                    )
                )
                if is_402:
                    # Log once per device at debug (or comment this out to be completely silent)
                    seen = getattr(self, "_saw_sxm_402", set())
                    if dev.id not in seen:
                        self.logger.debug(f"⚠️ Trapped benign UPnP 402 for {dev.name}; continuing without error.")
                        seen.add(dev.id)
                        self._saw_sxm_402 = seen
                    # Nudge playback; many players already applied the URI
                    try:
                        soco_dev.play()
                    except Exception as play_err:
                        self.logger.debug(f"⏯️ Post-402 play retry hiccup on {dev.name}: {play_err}")
                    return  # Skip further state updates on this pass; transport will typically proceed
                # --- end inserted 402 guard ---

                # (existing error logging retained for non-402 cases)
                self.logger.error(f"❌ UPNP Error: {upnp_err}")
                self.logger.error(f"❌ Offending Command -> zoneIP: {zoneIP}, URI: {uri}")
                self.logger.error(f"📦 Metadata Sent:\n{metadata}")
                if "UPnPError" in str(upnp_err) and "402" in str(upnp_err):
                    self.logger.warning(f"⚠️ Sonos rejected the SiriusXM stream due to invalid arguments (UPnP 402). Check URI/metadata formatting.")
                return  # Skip further state updates on failure

            # ✅ Update states after success
            if "channel_number" in channel and "name" in channel:
                channel_number = channel["channel_number"]
                channel_name = channel["name"]
                dev.updateStateOnServer("ZP_STATION", f"CH {channel_number} - {channel_name}")
                self.safe_debug(f"📝 Updated ZP_STATION to CH {channel_number} - {channel_name}")

            self.logger.info(f"✅ Successfully changed {dev.name} to {title}")

            # 💾 Save last known SiriusXM channel
            if not hasattr(self, "last_known_sxm_channel"):
                self.last_known_sxm_channel = {}

            try:
                clean_ch_num = int(str(channel.get("channel_number", 0)).strip())
                # NOTE: key by zoneIP so channelUpOrDown() can read it (it looks up by IP)
                self.last_known_sxm_channel[zoneIP] = clean_ch_num
                self.logger.info(f"💾 Saved last known SiriusXM channel {clean_ch_num} for zone {zoneIP}")
            except Exception:
                self.logger.warning(f"⚠️ Could not parse and save channel_number for {dev.name}")

        except Exception as e:
            self.logger.error(f"❌ SiriusXMChannelChanger failed for {dev.name}: {e}")







    def _cache_sxm_channel(self, dev=None, zoneIP=None, channel_number=None):
        """
        Save last-known SiriusXM channel using both dev.id and IP keys (when available).
        Keeps compatibility with code that reads either key.
        """
        if channel_number is None:
            return
        try:
            ch = int(str(channel_number).strip())
        except Exception:
            return

        if not hasattr(self, "last_known_sxm_channel") or not isinstance(self.last_known_sxm_channel, dict):
            self.last_known_sxm_channel = {}

        if dev is not None:
            # by device id
            try:
                self.last_known_sxm_channel[dev.id] = ch
            except Exception:
                pass
            # by IP (if we can get it)
            try:
                ip = (dev.pluginProps.get("address") or getattr(dev, "address", None) or "").strip()
                if ip:
                    self.last_known_sxm_channel[ip] = ch
            except Exception:
                pass
        elif zoneIP:
            self.last_known_sxm_channel[zoneIP] = ch



    def _get_cached_sxm_channel(self, dev=None, zoneIP=None):
        """
        Retrieve last-known SiriusXM channel; prefer dev.id, then IP.
        Returns int or None.
        """
        d = getattr(self, "last_known_sxm_channel", None)
        if not isinstance(d, dict):
            return None

        # by device id
        if dev is not None and dev.id in d:
            return d[dev.id]

        # by IP
        ip = None
        try:
            ip = zoneIP or (dev.pluginProps.get("address") if dev else None) or (getattr(dev, "address", None) if dev else None)
        except Exception:
            ip = zoneIP

        if ip in d:
            return d[ip]

        return None


                

    ############################################################################################


    def query_siriusxm_channel(self, channel_name_or_id):
        sxm_user = self.pluginPrefs.get("sirius_user", "")
        sxm_pass = self.pluginPrefs.get("sirius_pass", "")
        if not sxm_user or not sxm_pass:
            self.logger.error("SiriusXM credentials are not set in plugin preferences")
            return

        sxm = SiriusXM(username=sxm_user, password=sxm_pass, logger=self.logger)
        if not sxm.authenticate():
            self.logger.error("SiriusXM login failed")
            return

        result = sxm.get_channel(channel_name_or_id)
        if result:
            self.logger.info(f"🎵 Found SiriusXM channel: {result['name']} ({result['siriusChannelNumber']})")
        else:
            self.logger.warning(f"No matching SiriusXM channel found for: {channel_name_or_id}")


    def parse_siriusxm_guid_from_uri(self, uri):
        if not uri:
            return None

        try:
            # Decode percent-encoded parts
            decoded_uri = urllib.parse.unquote(uri)

            # Look for the pattern after 'channel-linear:'
            match = re.search(r'channel-linear:([a-f0-9\-]+)', decoded_uri, re.IGNORECASE)
            if match:
                return match.group(1)
        except Exception as e:
            self.logger.error(f"❌ Error parsing SiriusXM GUID from URI: {e}")

        return None

    def parse_siriusxm_guid_from_uri(self, uri):
        try:
            if "x-sonosapi-hls:channel-linear:" in uri:
                after_prefix = uri.split("x-sonosapi-hls:channel-linear:")[1]
                guid = after_prefix.split("?")[0]
                return guid.strip().lower()
        except Exception as e:
            self.logger.error(f"❌ Failed to parse GUID from URI: {uri} — {e}")
        return None


    def is_valid_guid(self, guid):
        import re
        return bool(re.fullmatch(
            r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}",
            guid, re.IGNORECASE
        ))



    def extract_siriusxm_guid(self, uri: str) -> str:
        try:
            self.safe_debug(f"🧪 extract_siriusxm_guid() input: {uri}")
            # Match both formats:
            # - x-sonosapi-hls:channel-linear:<guid>
            # - x-sonosapi-hls:<guid>
            match = re.search(
                r"x-sonosapi-hls:(?:channel-linear:)?([a-f0-9\-]{36})", uri, re.IGNORECASE
            )
            if match:
                guid = match.group(1)
                self.safe_debug(f"✅ Parsed SiriusXM GUID: {guid}")
                return guid

            self.logger.warning(f"⚠️ Could not parse SiriusXM GUID from URI: {uri}")
        except Exception as e:
            self.logger.error(f"❌ extract_siriusxm_guid() exception: {e}")
        return ""




    def sendSiriusXMChannel(self, zoneIP, channel_guid, channel_name):
        """
        Compatibility wrapper: resolve Indigo device from zoneIP and delegate to SiriusXMChannelChanger().
        Keeps existing call sites working while unifying the logic in one place.
        """
        try:
            self.logger.info("🔁 Entered sendSiriusXMChannel()")

            if not zoneIP:
                self.logger.error("❌ No zoneIP provided for sendSiriusXMChannel")
                return
            if not channel_guid:
                self.logger.warning(f"⚠️ No SiriusXM GUID provided for zone {zoneIP}")
                return

            # Resolve Indigo device by IP
            dev = None
            cached = self.ip_to_indigo_device.get(zoneIP)
            if isinstance(cached, indigo.Device):
                dev = cached
            elif isinstance(cached, int):
                dev = indigo.devices.get(cached)

            if not dev:
                # If we can’t resolve, fall back to SoCo directly but still use RAW payloads + 402 suppression
                self.logger.warning(f"⚠️ Could not resolve Indigo device for {zoneIP}; falling back to direct send.")
                # Build a fake, lightweight device-like shim with minimal props needed
                class _Shim:
                    name = f"(IP {zoneIP})"
                    pluginProps = {"address": zoneIP}
                    def updateStateOnServer(*args, **kwargs): pass
                    id = f"ip:{zoneIP}"
                return self.SiriusXMChannelChanger(_Shim, channel_guid)

            # Delegate to the single source of truth
            return self.SiriusXMChannelChanger(dev, channel_guid)

        except Exception as e:
            self.logger.error(f"❌ Failed to send SiriusXM channel {channel_name}: {e}")



    def actionChannelUp(self, pluginAction, dev):
        self.safe_debug(f"⚡ Action received: actionChannelUp for device ID {dev.id}")

        currentURI = dev.states.get("ZP_CurrentTrackURI", "")
        guid = self.parse_siriusxm_guid_from_uri(currentURI)

        if not guid:
            self.logger.warning(f"⚠️ Could not parse current SiriusXM content ID from URI: {currentURI}")
            return

        try:
            # Sort by numeric channelNumber
            guidList = sorted(
                self.siriusxm_guid_map.keys(),
                key=lambda g: int(self.siriusxm_guid_map[g].get("channelNumber", 9999))
            )

            currentIndex = guidList.index(guid)
            nextIndex = (currentIndex + 1) % len(guidList)
            nextGuid = guidList[nextIndex]
            nextChan = self.siriusxm_guid_map[nextGuid]
            channelNum = nextChan.get("channelNumber", "???")
            channelName = nextChan.get("title", "Unknown")

        except Exception as e:
            self.logger.warning(f"⚠️ ChannelUp lookup failed from {guid} — {e}")
            return

        self.logger.info(f"🔁 ChannelUp: {guid} → {nextGuid} ({channelNum}) - {channelName}")
        pluginAction.props["setting"] = nextGuid
        self.actionZP_SiriusXM(pluginAction, dev)
           

    def actionChannelDown(self, pluginAction, dev):
        self.safe_debug(f"⚡ Action received: actionChannelDown for device ID {dev.id}")

        currentURI = dev.states.get("ZP_CurrentTrackURI", "")
        guid = self.parse_siriusxm_guid_from_uri(currentURI)

        if not guid:
            self.logger.warning(f"⚠️ Could not parse current SiriusXM content ID from URI: {currentURI}")
            return

        try:
            # Sort by numeric channelNumber
            guidList = sorted(
                self.siriusxm_guid_map.keys(),
                key=lambda g: int(self.siriusxm_guid_map[g].get("channelNumber", 9999))
            )

            currentIndex = guidList.index(guid)
            prevIndex = (currentIndex - 1) % len(guidList)
            prevGuid = guidList[prevIndex]
            prevChan = self.siriusxm_guid_map[prevGuid]
            channelNum = prevChan.get("channelNumber", "???")
            channelName = prevChan.get("title", "Unknown")

        except Exception as e:
            self.logger.warning(f"⚠️ ChannelDown lookup failed from {guid} — {e}")
            return

        self.logger.info(f"🔁 ChannelDown: {guid} → {prevGuid} ({channelNum}) - {channelName}")
        pluginAction.props["setting"] = prevGuid
        self.actionZP_SiriusXM(pluginAction, dev)



    def get_current_uri_for_zone(self, zoneIP):
        try:
            soco_device = self.soco_by_ip.get(zoneIP)
            if soco_device is None:
                self.logger.warning(f"⚠️ soco_device is None for zoneIP {zoneIP}")
                return None

            transport_info = soco_device.avTransport.GetMediaInfo([('InstanceID', 0)])
            uri = transport_info.get('CurrentURI', None)

            if not uri:
                self.logger.warning(f"⚠️ get_current_uri_for_zone() say's - No URI available to parse for device at {zoneIP}")
            return uri

        except Exception as e:
            self.logger.error(f"❌ get_current_uri_for_zone() failed for zoneIP {zoneIP}: {e}")
            return None


    def get_next_siriusxm_guid(self, current_guid):
        if not self.sorted_siriusxm_guids:
            self.logger.warning("⚠️ SiriusXM GUID list is empty.")
            return None
        try:
            i = self.sorted_siriusxm_guids.index(current_guid)
            return self.sorted_siriusxm_guids[(i + 1) % len(self.sorted_siriusxm_guids)]
        except ValueError:
            self.logger.warning(f"⚠️ Current GUID {current_guid} not found. Returning first.")
            return self.sorted_siriusxm_guids[0]

    def get_prev_siriusxm_guid(self, current_guid):
        if not self.sorted_siriusxm_guids:
            self.logger.warning("⚠️ SiriusXM GUID list is empty.")
            return None
        try:
            i = self.sorted_siriusxm_guids.index(current_guid)
            return self.sorted_siriusxm_guids[(i - 1) % len(self.sorted_siriusxm_guids)]
        except ValueError:
            self.logger.warning(f"⚠️ Current GUID {current_guid} not found. Returning last.")
            return self.sorted_siriusxm_guids[-1]




###############################################################################################################################

    def exception_handler(self, exception_error_message, log_failing_statement):
        filename, line_number, method, statement = traceback.extract_tb(sys.exc_info()[2])[-1]
        module = filename.split('/')
        log_message = f"'{exception_error_message}' in module '{module[-1]}', method '{method} [{self.globals[PLUGIN_INFO][PLUGIN_VERSION]}]'"
        if log_failing_statement:
            log_message = log_message + f"\n   Failing statement [line {line_number}]: '{statement}'"
        else:
            log_message = log_message + f" at line {line_number}"
        self.logger.error(log_message)








############################################################################################
### Action annoucement processing
############################################################################################

    def actionAnnouncement(self, pluginAction, action):
        #self.logger.error(f"[ANNOUNCE TOP] action={action!r}")
        #self.logger.error(f"[ANNOUNCE TOP PROPS] {dict(pluginAction.props or {})}")
        self.logger.debug(f"[ANNOUNCE ENTRY] action={action!r} props_present={pluginAction.props is not None}")
        if pluginAction.props:
            self.logger.debug(f"[ANNOUNCE PROPS] keys={sorted(pluginAction.props.keys())}")
            self.logger.debug(f"[ANNOUNCE PROPS SAMPLE] ZonePlayer={pluginAction.props.get('ZonePlayer')!r} "
                             f"zp1={pluginAction.props.get('zp1')!r} "
                             f"source={pluginAction.props.get('source')!r} "
                             f"sound_file={pluginAction.props.get('sound_file')!r} "
                             f"level={pluginAction.props.get('level')!r}")

        # Comment out or early-return before doing anything
        # self.logger.warning("🔕 Skipping announcement test — isolating plugin failure.")
        # return

        #indigo.server.log("did i hit 3 ????", type="Sonos PY Plugin Msg: 6778: ")
        global SavedState
        global actionBusy

        actionBusy = 1

        # ---- safer volume parse (preserves existing assignment semantics) ----
        try:
            _raw_vol = (pluginAction.props or {}).get("zp_volume")
            zp_volume = int(self.plugin.substitute(_raw_vol or "20"))
        except Exception:
            zp_volume = 20

        # Preserve existing group structure if Group Coordinator Only is selected in action
        try:
            gc_only = bool((pluginAction.props or {}).get("gc_only"))
        except Exception:
            gc_only = False

        # need this until group announcement actions are merged
        if action == "announcement":
            gc_only = False

        # --- build AnnouncementZones robustly (accepts bools or strings) ---
        AnnouncementZones = []

        def _is_true(v):
            s = str(v).strip().lower()
            return (v is True) or (s in ("true", "1", "yes", "on"))

        # helper: add zone if props value looks like a valid Indigo device id
        def _add_zone_if_valid(val):
            try:
                if val not in ("", None, "00000"):
                    dev_id = int(val)
                    _ = indigo.devices[dev_id]  # raises if invalid
                    AnnouncementZones.append(dev_id)
            except Exception as e:
                self.logger.error(f"❌ Invalid zone selection '{val}': {e}")

        # Special handling: for announcementMP3 we don't need to hunt for the group coordinator here.
        skip_gc_resolve = (action == "announcementMP3")

        if gc_only is False:
            # collect zp1..zp12
            try:
                for x in range(1, 13):
                    ivar = f"zp{x}"
                    _add_zone_if_valid((pluginAction.props or {}).get(ivar))
            except Exception as e:
                self.logger.error(f"❌ Failed building AnnouncementZones: {e}")
        else:
            # Resolve coordinator from zp1 or from bound device — unless we are skipping for announcementMP3
            dev = None

            # If skipping GC resolve (announcementMP3), just seed the list with zp1 or bound device and move on.
            if skip_gc_resolve:
                try:
                    anchor = (pluginAction.props or {}).get("zp1")
                    if anchor not in ("", None, "00000"):
                        dev = indigo.devices[int(anchor)]
                except Exception:
                    dev = None

                if dev is None:
                    try:
                        if action and hasattr(action, "deviceId") and action.deviceId:
                            dev = indigo.devices[action.deviceId]
                    except Exception:
                        dev = None

                if dev:
                    AnnouncementZones.append(dev.id)
                else:
                    self.logger.debug("[GC] announcementMP3: no zp1 or bound device to seed AnnouncementZones")
            else:
                # Original GC resolution path
                try:
                    anchor = (pluginAction.props or {}).get("zp1")
                    if anchor not in ("", None, "00000"):
                        dev = indigo.devices[int(anchor)]
                except Exception as e:
                    self.logger.error(f"❌ gc_only set but zp1 invalid: {e}")

                if dev is None:
                    # fall back to the device the action is bound to
                    try:
                        if action and hasattr(action, "deviceId") and action.deviceId:
                            dev = indigo.devices[action.deviceId]
                    except Exception:
                        pass

                if not dev:
                    self.logger.error("❌ gc_only is set but no valid zp1 or bound device was provided.")
                else:
                    if _is_true(dev.states.get("GROUP_Coordinator")):
                        AnnouncementZones.append(dev.id)
                    else:
                        # if selected ZonePlayer is not master of a group, find the master
                        coordinator_group = dev.states.get("GROUP_Name", "")
                        resolved = False
                        for idev in indigo.devices.iter("self.ZonePlayer"):
                            if _is_true(idev.states.get("GROUP_Coordinator")) and idev.states.get("GROUP_Name") == coordinator_group:
                                AnnouncementZones.append(idev.id)
                                resolved = True
                                break
                        if not resolved:
                            # Fallback: if we couldn’t resolve, at least target the chosen device so the action can run
                            # (demoted to debug to avoid noisy logs during announcements)
                            self.logger.debug(
                                f"[GC] Could not resolve group coordinator for '{dev.name}' "
                                f"(group '{coordinator_group}'). Using selected device."
                            )
                            AnnouncementZones.append(dev.id)

        self.logger.debug(f"🔎 gc_only={gc_only} | AnnouncementZones={AnnouncementZones}")



        # =========================================================================================
        # Announcement (FILE / LINE-IN) input normalization + target resolution
        # =========================================================================================
        if action == "announcement":
            try:
                props = pluginAction.props or {}

                # --- read panel fields (cover common variants) ---
                zone_sel = (
                    props.get("zp1")
                    or props.get("zoneplayer")
                    or props.get("ZonePlayer")
                    or props.get("deviceId")
                    or props.get("player")
                    or props.get("zone")
                )

                # Volume field on this dialog is "level" (fallbacks preserved)
                raw_vol = props.get("level", props.get("volume", props.get("zp_volume", 20)))
                try:
                    zp_volume = int(str(raw_vol).strip())
                except Exception:
                    self.logger.debug(f"[ANNOUNCE] Bad volume '{raw_vol}' ({type(raw_vol).__name__}); defaulting to 20")
                    zp_volume = 20

                # Source (e.g., "File" or "Line-In")
                source = props.get("source", "").strip() if isinstance(props.get("source"), str) else props.get("source")

                # Sound file name (for File source)
                file_name_prop = props.get("sound_file", props.get("file", ""))
                sound_file = file_name_prop.strip() if isinstance(file_name_prop, str) else ""

                # Line-In source device (device id string) when Source == "Line-In"
                zp_input = props.get("zp_input")

                # --- resolve target device from ZonePlayer selection (to get IP) ---
                dev_target = None
                if zone_sel not in (None, "", "00000"):
                    try:
                        dev_target = indigo.devices[int(zone_sel)]
                    except Exception:
                        # if it's not an id, try by name
                        try:
                            for d in indigo.devices.iter("self.ZonePlayer"):
                                if d.name == str(zone_sel) or d.states.get("ZP_ZoneName") == str(zone_sel):
                                    dev_target = d
                                    break
                        except Exception:
                            pass

                # Fallback: if nothing explicitly selected, use first computed AnnouncementZones entry
                if not dev_target and AnnouncementZones:
                    try:
                        dev_target = indigo.devices[int(AnnouncementZones[0])]
                    except Exception:
                        pass

                # Extract IP address from the resolved device
                zone_ip = ""
                if dev_target:
                    zone_ip = (dev_target.pluginProps.get("address") or dev_target.address or "").strip()

                # --- LOG exactly what we got/resolved ---
                self.logger.debug(
                    f"[ANNOUNCE INPUT] props_keys={list(props.keys())} | "
                    f"ZoneSel={zone_sel!r} → Device={(dev_target.name if dev_target else None)!r} "
                    f"(ID={(dev_target.id if dev_target else None)!r}) IP={zone_ip!r} | "
                    f"Source={source!r} File={sound_file!r} Volume={zp_volume}"
                )

                # Guardrails: must have a target and IP
                if not dev_target or not zone_ip:
                    self.logger.error("❌ Could not resolve target ZonePlayer IP from action props. Aborting announcement.")
                    actionBusy = 0
                    return

                # ========================= NEW: snapshot only the target =========================
                try:
                    self.logger.info(f"[STATE SAVE] Snapshotting target before announcement: "
                                     f"id={dev_target.id}, ip={zone_ip}, name={dev_target.name}")
                    # Prefer filtered snapshot if your actionStates supports it:
                    self.actionStates(pluginAction, "saveStates", only_device_ids=[dev_target.id])
                except TypeError:
                    # Older signature without only_device_ids – fall back to full snapshot
                    self.logger.warning("[STATE SAVE] actionStates() has no 'only_device_ids' param; saving all devices.")
                    self.actionStates(pluginAction, "saveStates")
                except Exception as e:
                    self.logger.error(f"[STATE SAVE] Failed to snapshot target device state: {e}")
                # ======================= END NEW BLOCK (kept rest unchanged) ======================

                # -----------------------------------------------------------------------------
                # Existing FILE / LINE-IN execution logic – unchanged except for using zone_ip,
                # zp_volume, sound_file, and zp_input we normalized above.
                # -----------------------------------------------------------------------------

                # FILE-based announcement
                if str(source).lower() == "file":
                    # Validate file name early
                    if not sound_file:
                        self.logger.error("❌ Missing Sound File for File source. Aborting.")
                        actionBusy = 0
                        return

                    if not AnnouncementZones:
                        AnnouncementZones = [dev_target.id]

                    # Begin playback loop (your existing structure preserved)
                    for item in AnnouncementZones:
                        try:
                            dev = indigo.devices[int(item)]

                            # Only act on the resolved target IP
                            if dev.address and dev.address.strip() != zone_ip:
                                self.logger.debug(f"[SKIP] Device '{dev.name}' IP '{dev.address}' does not match target '{zone_ip}'")
                                continue

                            self.logger.info(f"[SEND] Sending FILE announcement '{sound_file}' to '{dev.name}' at {zone_ip}")

                            # Make standalone if required for URI change
                            if dev.states.get('GROUP_Coordinator') == "false":
                                self.logger.debug(f"[GROUP] '{dev.name}' is not coordinator — breaking from group...")
                                self.SOAPSend(zone_ip, "/MediaRenderer", "/AVTransport", "BecomeCoordinatorOfStandaloneGroup", "")

                            # Set volume
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/RenderingControl", "SetVolume",
                                          f"<Channel>Master</Channel><DesiredVolume>{zp_volume}</DesiredVolume>")

                            # Unmute
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/RenderingControl", "SetMute",
                                          "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")

                            # TODO: Set AVTransportURI for your http_server + file path (your existing code)
                            # self.SOAPSend(zone_ip, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", ...)

                            # Play
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")

                        except Exception as e:
                            self.logger.error(f"[ERROR] Exception while sending FILE announcement to device {item}: {e}")

                # LINE-IN announcement
                elif str(source).lower() in ("line-in", "linein", "line_in"):
                    # Resolve source device (Line-In)
                    try:
                        dev_src = indigo.devices[int(zp_input)]
                        dev_src_LocalUID = dev_src.states['ZP_LocalUID']
                        self.logger.debug(f"[SOURCE] Line-In UID: {dev_src_LocalUID} ({dev_src.name})")
                    except Exception as e:
                        self.logger.error(f"❌ Invalid or missing zp_input for Line-In announcement: {e}")
                        actionBusy = 0
                        return

                    if dev_src.states.get('ZP_AIName', "") == "":
                        self.logger.warning("❌ No Line-In available on selected source device.")
                        actionBusy = 0
                        return

                    if not AnnouncementZones:
                        AnnouncementZones = [dev_target.id]

                    # Begin playback loop
                    for item in AnnouncementZones:
                        try:
                            dev = indigo.devices[int(item)]

                            # Only act on the resolved target IP
                            if dev.address and dev.address.strip() != zone_ip:
                                self.logger.debug(f"[SKIP] Device '{dev.name}' IP '{dev.address}' does not match target '{zone_ip}'")
                                continue

                            self.logger.info(f"[SEND] Sending Line-In announcement to '{dev.name}' at IP {zone_ip}")

                            # If member of group, make standalone (required for URI change)
                            if dev.states.get('GROUP_Coordinator') == "false":
                                self.logger.debug(f"[GROUP] '{dev.name}' is not coordinator — breaking from group...")
                                self.SOAPSend(zone_ip, "/MediaRenderer", "/AVTransport", "BecomeCoordinatorOfStandaloneGroup", "")

                            # Change to Line-In
                            self.plugin.debugLog(f"🔊 Playing LineIn: {dev_src.states.get('ZP_AIName', '[Unknown]')}")
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/AVTransport", "SetAVTransportURI",
                                          f"<CurrentURI>x-rincon-stream:{dev_src_LocalUID}</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>")

                            # Set volume
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/RenderingControl", "SetVolume",
                                          f"<Channel>Master</Channel><DesiredVolume>{zp_volume}</DesiredVolume>")

                            # Unmute
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/RenderingControl", "SetMute",
                                          "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")

                            # Play
                            self.SOAPSend(zone_ip, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")

                        except Exception as e:
                            self.logger.error(f"[ERROR] Exception while sending Line-In announcement to device {item}: {e}")

                else:
                    # Unknown/unsupported source type
                    self.logger.error(f"❌ Unsupported announcement source: {source!r}")
                    actionBusy = 0
                    return

            except Exception as e:
                self.logger.error(f"[FATAL] Announcement handler crashed: {e}")
                actionBusy = 0
                return

        elif action == "announcementMP3":
            # ---- normalize props & log what the UI actually sent ----
            props = pluginAction.props or {}
            #self.logger.error(f"[MP3 RAW PROPS] {dict(props)}")
            # ---- normalize props & log what the UI actually sent ----
            props = pluginAction.props or {}

            # Source (e.g., "TTS" or "File"); normalize gently
            source_raw = props.get("ttsORfile") or props.get("source")
            source = (source_raw.strip().lower() if isinstance(source_raw, str) else None)

            # Sound file (when using File source)
            #sf_raw = props.get("sound_file") or props.get("file") or ""
            #sound_file = sf_raw.strip() if isinstance(sf_raw, str) else ""
            mp3_candidates = {
                k: v for k, v in props.items()
                if "file" in str(k).lower()
                or "sound" in str(k).lower()
                or ".mp3" in str(v).lower()
                or ".aiff" in str(v).lower()
            }
            #self.logger.error(f"[MP3 FILE CANDIDATES] {mp3_candidates}")

            sf_raw = (
                props.get("sound_file")
                or props.get("soundFile")
                or props.get("SoundFile")
                or props.get("sound")
                or props.get("audioFile")
                or props.get("announcementFile")
                or props.get("file")
                or ""
            )
            sound_file = sf_raw.strip() if isinstance(sf_raw, str) else ""
            # If source not provided but a file is present, assume "file"
            if not source and sound_file:
                source = "file"
            # Default to "file" if still unknown
            source = source or "file"

            # Volume (accept int or str; fall back to 20)
            raw_level = props.get("level", props.get("volume", props.get("zp_volume", 20)))
            try:
                zp_volume = int(str(raw_level).strip())
            except Exception:
                self.logger.warning(f"[WARN] Invalid volume {raw_level!r} — defaulting to 20")
                zp_volume = 20

            # Clamp volume to 0–100
            if zp_volume < 0 or zp_volume > 100:
                self.logger.warning(f"[WARN] Volume out of range ({zp_volume}); clamping to 0–100")
                zp_volume = max(0, min(100, zp_volume))

            # gc_only (play on already-grouped coordinator only) if present
            gc_only = bool(props.get("gc_only", False))

            # Log what we’ll use
            self.logger.debug(
                f"[ANNOUNCE INPUT] source={source.upper()} file={sound_file!r} volume={zp_volume} "
                f"gc_only={gc_only} zp1={props.get('zp1')!r}"
            )

            # ===== determine target device/IP from built AnnouncementZones =====
            if not AnnouncementZones:
                self.logger.error("❌ AnnouncementZones is empty — no zone selected for MP3 playback.")
                return

            try:
                GM = indigo.devices[int(AnnouncementZones[0])]
                zoneIP = (GM.pluginProps.get("address") or GM.address or "").strip()
                if not zoneIP:
                    self.logger.error(f"❌ No IP address found in pluginProps for device {GM.name}.")
                    return
                self.logger.debug(f"[ANNOUNCE TARGET] device={GM.name} id={GM.id} ip={zoneIP}")
            except Exception as e:
                self.logger.error(f"❌ Failed to resolve announcement zone device or IP: {e}")
                return

            # ===== build/prepare the announcement audio asset =====
            # Every engine must write into the root the 8889 announce server
            # actually serves, and the duration probe below must read that same
            # file — the TTS engines used to write to the plugin CWD (served as
            # 404) and the probe read the CWD too, so a stale CWD file's length
            # truncated File announcements at the wrong duration.
            announce_root = (getattr(self, "_announce_http_root", "")
                             or self.get_announce_http_config()[2] or ".")
            try:
                if source == "tts":
                    announcement = self.plugin.substitute(props.get("setting"), validateOnly=False)
                    zp_language = props.get("language")
                    tts = gTTS(text=announcement, lang=zp_language)
                    tts.save(os.path.join(announce_root, 'announcement.mp3'))
                    s_announcement = "announcement.mp3"
                    tts_delay = 0

                elif source == "ivona":
                    announcement = self.plugin.substitute(props.get("IVONA_setting"), validateOnly=False)
                    v = pyvona.pyvona.create_voice(self.IVONAaccessKey, self.IVONAsecretKey)
                    v.codec = 'mp3'
                    v.voice_name = IVONAVoices[int(props.get("IVONA_voice"))][1]
                    v.sentence_break = int(props.get("IVONA_sentence_break"))
                    v.speech_rate = props.get("IVONA_speech_rate")
                    v.fetch_voice(announcement, os.path.join(announce_root, 'announcement'))
                    s_announcement = "announcement.mp3"
                    tts_delay = 0.5
                    self.plugin.sleep(0.5)  # allow file creation

                elif source == "polly":
                    announcement = self.plugin.substitute(props.get("POLLY_setting"), validateOnly=False)
                    client = boto3.client('polly', aws_access_key_id=self.PollyaccessKey,
                                          aws_secret_access_key=self.PollysecretKey, region_name='us-east-1')
                    response = client.synthesize_speech(OutputFormat='mp3', Text=announcement, VoiceId=props.get("POLLY_voice"))
                    if "AudioStream" in response:
                        with closing(response["AudioStream"]) as stream:
                            data = stream.read()
                            with open(os.path.join(announce_root, "announcement.mp3"), "wb") as f:
                                f.write(data)
                    s_announcement = "announcement.mp3"
                    tts_delay = 0.5

                elif source == "apple":
                    announcement = self.plugin.substitute(props.get("APPLE_setting"), validateOnly=False)
                    apple_voice = (props.get("APPLE_voice") or "").strip()
                    # Older configs stored NSSpeechSynthesizer ids
                    # (com.apple.voice.compact.en-US.Samantha) — resolve to the
                    # plain voice name `say` expects.
                    if apple_voice.startswith("com.apple."):
                        resolved = None
                        try:
                            attrs = NSSpeechSynthesizer.attributesForVoice_(apple_voice) or {}
                            resolved = attrs.get("VoiceName")
                        except Exception:
                            resolved = None
                        apple_voice = resolved or apple_voice.rsplit(".", 1)[-1]
                    wav_path = os.path.join(announce_root, "announcement.wav")
                    try:
                        if os.path.exists(wav_path):
                            os.remove(wav_path)
                    except Exception:
                        pass
                    # NSSpeechSynthesizer is deprecated and renders SILENCE for many
                    # modern voices — the `say` CLI is synchronous and voice-complete.
                    # Output WAV 44.1kHz/16-bit: say's AIFF output is actually an
                    # AIFF-C container, which Sonos rejects ("not encoded correctly");
                    # WAVE at 44.1k verified playing on a real player.
                    import subprocess
                    cmd = ["/usr/bin/say", "-o", wav_path, "--data-format=LEI16@44100"]
                    if apple_voice:
                        cmd += ["-v", apple_voice]
                    cmd.append(announcement)
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                    if result.returncode != 0 and apple_voice:
                        self.logger.warning(
                            f"⚠️ Apple voice {apple_voice!r} failed ({(result.stderr or '').strip()}) — "
                            f"retrying with the system default voice")
                        result = subprocess.run(["/usr/bin/say", "-o", wav_path,
                                                 "--data-format=LEI16@44100", announcement],
                                                capture_output=True, text=True, timeout=60)
                    if result.returncode != 0 or not os.path.isfile(wav_path) or os.path.getsize(wav_path) == 0:
                        self.logger.error(f"❌ Apple speech synthesis failed: {(result.stderr or 'no output').strip()}")
                        return
                    s_announcement = "announcement.wav"
                    tts_delay = 0.5

                elif source == "microsoft":
                    announcement = self.plugin.substitute(props.get("MICROSOFT_setting"), validateOnly=False)
                    language = props.get("MICROSOFT_voice")
                    statinfo = self.MicrosoftTranslate(announcement, language,
                                                       out_path=os.path.join(announce_root, "announcement.mp3"))
                    s_announcement = "announcement.mp3"
                    tts_delay = 0.5
                    if statinfo is False:
                        self.plugin.errorLog("Microsoft Translate Error")
                        return

                else:
                    # File source (default)
                    fname = sound_file
                    if not fname:
                        self.logger.error("❌ No sound file selected in 'sound_file'.")
                        return

                    src = os.path.join(self.SoundFilePath or "", fname)
                    if not os.path.isfile(src):
                        self.logger.error(f"❌ Sound file not found: {src}")
                        return

                    # IMPORTANT:
                    # The announcement HTTP server serves from announce_root,
                    # so write announcement.mp3 there, not the plugin working directory.
                    dst = os.path.join(announce_root, "announcement.mp3")



                    try:
                        import shutil

                        if os.path.exists(dst):
                            os.remove(dst)

                        shutil.copyfile(src, dst)

                        self.logger.info(
                            f"[ANNOUNCE COPY] {os.path.basename(src)} → announcement.mp3 "
                            f"({os.path.getsize(src)} bytes)"
                        )

                    except Exception as e:
                        self.logger.error(f"❌ Failed to prepare announcement file: {e}")
                        return



                    announcement = f"FILE [{fname}]"
                    s_announcement = "announcement.mp3"
                    tts_delay = 0

                indigo.server.log("Announcement: %s, Volume: %s" % (announcement, zp_volume))

            except Exception as e:
                self.logger.error(f"❌ Error while preparing announcement audio: {e}")
                return




            # helper: coerce any value to an int, or None if not possible
            def _as_int(v):
                try:
                    return int(str(v).strip())
                except Exception:
                    return None

            # ===== SoCo Snapshot capture (preferred save/restore path) =====
            # Same mechanism Home Assistant's Sonos integration uses. Selectable
            # via plugin config; falls back to the legacy flow when disabled or
            # when no snapshot could be captured.
            def _pref_true(v, default=True):
                if v is None:
                    return default
                return (v is True) or (str(v).strip().lower() in ("true", "1", "yes", "on"))

            use_snapshot = _pref_true(self.plugin.pluginPrefs.get("useSocoSnapshot"), default=True)
            announce_snapshots = []
            if use_snapshot:
                try:
                    from soco.snapshot import Snapshot
                    # IPs of announcement zones — used to spot original group
                    # members OUTSIDE the announcement (they need merging back).
                    ann_ips = set()
                    for _zid in AnnouncementZones:
                        try:
                            _zd = indigo.devices[int(_zid)]
                            ann_ips.add((_zd.pluginProps.get("address") or _zd.address or "").strip())
                        except Exception:
                            pass
                    for item in AnnouncementZones:
                        try:
                            _dev = indigo.devices[int(item)]
                            _ip = (_dev.pluginProps.get("address") or _dev.address or "").strip()
                            if not _ip or not self._ip_probe_ok(_ip):
                                self.logger.debug(f"[ANNOUNCE SNAP] skip {_dev.name}: offline/no IP")
                                continue
                            _soco = self.soco_by_ip.get(_ip) or SoCo(_ip)
                            try:
                                snap = Snapshot(_soco)
                                snap.snapshot()
                            except Exception as snap_error:
                                self.logger.debug(
                                    f"[ANNOUNCE SNAP] full snapshot failed for {_dev.name} "
                                    f"({snap_error}) — capturing volume/mute only")
                                snap = _VolumeOnlySnap(_soco)
                            # Never restore a leftover announcement URL from a previous
                            # run (mirrors the legacy flow's "announcement." guard).
                            if "/announcement." in str(getattr(snap, "media_uri", "") or ""):
                                snap.media_uri = ""
                            # Record the zone's ORIGINAL coordinator so restore can
                            # rebuild the exact pre-announcement grouping — and, when
                            # this zone coordinates a group, any members OUTSIDE the
                            # announcement (they get orphaned into a remnant group
                            # when the coordinator is pulled away).
                            orig_coord = None
                            orig_members = []
                            try:
                                grp = _soco.group
                                grp_coord = getattr(grp, "coordinator", None) if grp else None
                                if grp_coord is not None and \
                                        getattr(grp_coord, "uid", None) != getattr(_soco, "uid", None):
                                    orig_coord = grp_coord
                                elif grp is not None:
                                    for m in list(getattr(grp, "members", []) or []):
                                        try:
                                            if getattr(m, "uid", None) != getattr(_soco, "uid", None) \
                                                    and (m.ip_address or "").strip() not in ann_ips:
                                                orig_members.append(m)
                                        except Exception:
                                            continue
                            except Exception as topo_error:
                                self.logger.debug(f"[ANNOUNCE SNAP] group lookup failed for {_dev.name}: {topo_error}")
                            announce_snapshots.append((_dev, snap, _soco, orig_coord, orig_members))
                            self.logger.debug(
                                f"[ANNOUNCE SNAP] captured {_dev.name}"
                                + (f" (slave of {getattr(orig_coord, 'player_name', '?')})" if orig_coord
                                   else f" (coordinator/standalone, outside members: {len(orig_members)})"))
                        except Exception as e:
                            self.logger.warning(f"[ANNOUNCE SNAP] snapshot failed for zone {item}: {e}")
                    if not announce_snapshots:
                        self.logger.warning("[ANNOUNCE SNAP] no snapshots captured — using legacy save/restore")
                        use_snapshot = False
                except Exception as e:
                    self.logger.warning(f"[ANNOUNCE SNAP] SoCo snapshot unavailable — using legacy save/restore: {e}")
                    use_snapshot = False
                    announce_snapshots = []

            # ===== legacy state capture (only when SoCo Snapshot is off/failed) =====
            if not use_snapshot:
                # --- capture current playback state for quick restore (target device only) ---
                prev = {
                    "uri": "", "meta": "", "pos": "00:00:00", "vol": None,
                    "state": "UNKNOWN",             # NEW: transport state
                    "mute": None,                   # NEW: device mute (0/1)
                    "per_dev_vol": {}, "per_dev_mute": {},  # NEW: per-device mutes
                    "group_vol": None, "group_mute": None   # existing + group mute now meaningful
                }
                try:
                    self.logger.debug(f"[ANNOUNCE SAVE] snapshot begin for {GM.name} @ {zoneIP}")
                    mi = self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "GetMediaInfo", "")
                    prev["meta"] = self.parseDirty(mi, "<CurrentURIMetaData>", "</CurrentURIMetaData>") or ""
                    prev["uri"]  = self.parseDirty(mi, "<CurrentURI>", "</CurrentURI>") or ""
                    pi = self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "GetPositionInfo", "")
                    try:
                        prev["pos"] = self.parseRelTime(GM, pi) or "00:00:00"
                    except Exception as e:
                        self.logger.debug(f"[ANNOUNCE SAVE] parseRelTime failed: {e}")
                        try:
                            rel = self.parseDirty(pi, "<RelTime>", "</RelTime>") or ""
                            prev["pos"] = rel if rel.count(":") == 2 else "00:00:00"
                        except Exception:
                            prev["pos"] = "00:00:00"

                    # NEW: Transport state (PLAYING/PAUSED_PLAYBACK/STOPPED)
                    try:
                        ti = self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "GetTransportInfo", "")
                        prev["state"] = (self.parseDirty(ti, "<CurrentTransportState>", "</CurrentTransportState>") or "UNKNOWN").strip()
                    except Exception as e:
                        self.logger.debug(f"[ANNOUNCE SAVE] GetTransportInfo failed: {e}")

                    # Volume + mute on target device
                    try:
                        gv = self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "GetVolume",
                                           "<Channel>Master</Channel>")
                        prev["vol"] = _as_int(self.parseCurrentVolume(gv))
                    except Exception as e:
                        self.logger.debug(f"[ANNOUNCE SAVE] GetVolume failed: {e}")
                        prev["vol"] = None

                    # NEW: device mute
                    try:
                        gm_xml = self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "GetMute",
                                               "<Channel>Master</Channel>")
                        prev["mute"] = _as_int(self.parseCurrentMute(gm_xml))  # expect 0/1
                    except Exception as e:
                        self.logger.debug(f"[ANNOUNCE SAVE] GetMute failed: {e}")
                        prev["mute"] = None

                    self.logger.debug(f"[ANNOUNCE SAVE] uri={prev['uri']!r} pos={prev['pos']} vol={prev['vol']} "
                                      f"state={prev['state']} mute={prev['mute']}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to snapshot current state prior to announcement: {e}")

                # --- capture volumes/mutes we will overwrite (per-device or group) ---
                try:
                    if gc_only is False:
                        # Per-device snapshot
                        snap_cnt = 0
                        for item in AnnouncementZones:
                            try:
                                _dev = indigo.devices[int(item)]
                                _ip = (_dev.pluginProps.get("address") or _dev.address or "").strip()
                                if not _ip:
                                    self.logger.debug(f"[ANNOUNCE SAVE] skip {_dev.name}: no IP")
                                    continue
                                # volume
                                gv = self.SOAPSend(_ip, "/MediaRenderer", "/RenderingControl", "GetVolume",
                                                   "<Channel>Master</Channel>")
                                v_raw = self.parseCurrentVolume(gv)
                                v = _as_int(v_raw)
                                prev["per_dev_vol"][_dev.id] = v
                                # NEW: mute
                                gm_xml = self.SOAPSend(_ip, "/MediaRenderer", "/RenderingControl", "GetMute",
                                                       "<Channel>Master</Channel>")
                                m = _as_int(self.parseCurrentMute(gm_xml))
                                prev["per_dev_mute"][_dev.id] = m
                                snap_cnt += 1
                                self.logger.debug(f"[ANNOUNCE SAVE] captured {_dev.name} vol={v} mute={m}")
                            except Exception as e:
                                self.logger.debug(f"[ANNOUNCE SAVE] capture failed for device {item}: {e}")
                        self.logger.debug(f"[ANNOUNCE SAVE] per-device volumes/mutes captured: {snap_cnt} → "
                                          f"{prev['per_dev_vol']} / {prev['per_dev_mute']}")
                    else:
                        # Group snapshot (coordinator only)
                        try:
                            gv = self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupVolume", "")
                            prev["group_vol"] = _as_int(self.parseCurrentVolume(gv))
                        except Exception as e:
                            self.logger.debug(f"[ANNOUNCE SAVE] GetGroupVolume failed: {e}")
                            prev["group_vol"] = None
                        try:
                            gm = self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "GetGroupMute", "")
                            prev["group_mute"] = _as_int(self.parseCurrentMute(gm))
                        except Exception as e:
                            self.logger.debug(f"[ANNOUNCE SAVE] GetGroupMute failed: {e}")
                            prev["group_mute"] = None
                        self.logger.debug(f"[ANNOUNCE SAVE] group_vol={prev['group_vol']} group_mute={prev['group_mute']}")
                except Exception as e:
                    self.logger.debug(f"[ANNOUNCE SAVE] Volume/mute snapshot failed (continuing): {e}")

            self.logger.debug("[ANNOUNCE STEP] snapshot complete; entering (re)group")

            # ===== (re)group if needed =====
            try:
                if gc_only is False:
                    # set standalone
                    self.plugin.debugLog("Announcement: set standalone")
                    for item in AnnouncementZones:
                        dev = indigo.devices[int(item)]
                        self.actionDirect(PA(dev.id), "setStandalone")

                    # add announcement zones to group (ensure 'setting' is a string)
                    # addPlayerToZone semantics: bound device = JOINER, 'setting' = COORDINATOR,
                    # so each additional zone joins GM's group (GM stays coordinator).
                    self.plugin.debugLog("Announcement: add announcement zones to group")
                    itemcount = 0
                    for item in AnnouncementZones:
                        dev = indigo.devices[int(item)]
                        if itemcount > 0:
                            self.actionDirect(PA(dev.id, {'setting': str(GM.id)}), "addPlayerToZone")
                        itemcount += 1
                else:
                    # Nothing to split here; just ensure transport is stopped on GM
                    try:
                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Stop", "")
                        self.logger.debug("[ANNOUNCE] Stop before announcement sent")
                    except Exception as e:
                        self.logger.debug(f"[ANNOUNCE] Stop before announcement failed (continuing): {e}")
            except Exception:
                # Non-fatal: don’t abort the announcement if grouping hiccups
                self.logger.exception("❌ Announcement pre-playback grouping step failed (continuing)")

            self.logger.debug("[ANNOUNCE STEP] (re)group done; entering volume set")

            # ===== set volume (per device or group) =====
            self.plugin.debugLog("Announcement: set volume")
            if gc_only is False:
                # Per-device: set RenderingControl volume + unmute on each selected ZP
                for item in AnnouncementZones:
                    dev = indigo.devices[int(item)]
                    ip = (dev.pluginProps.get("address") or dev.address or "").strip()
                    if not ip:
                        self.logger.debug(f"[ANNOUNCE VOL] skip {dev.name}: no IP")
                        continue
                    self.logger.debug(f"[ANNOUNCE VOL] {dev.name} → {zp_volume}")
                    # Set volume
                    self.SOAPSend(ip, "/MediaRenderer", "/RenderingControl", "SetVolume",
                                  f"<Channel>Master</Channel><DesiredVolume>{zp_volume}</DesiredVolume>")
                    # Unmute
                    self.SOAPSend(ip, "/MediaRenderer", "/RenderingControl", "SetMute",
                                  "<Channel>Master</Channel><DesiredMute>0</DesiredMute>")
            else:
                # Group: SetGroupVolume + SetGroupMute on the coordinator only
                self.logger.debug(f"[ANNOUNCE VOL] GROUP → {zp_volume}")
                try:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupVolume",
                                  f"<DesiredVolume>{zp_volume}</DesiredVolume>")
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute",
                                  "<DesiredMute>0</DesiredMute>")
                except Exception as e:
                    self.logger.warning(f"[ANNOUNCE VOL] group volume/mute set failed (continuing): {e}")

            self.logger.debug("[ANNOUNCE STEP] volume set; entering audio probe")

            # ===== inspect the audio to time playback =====
            count = 0
            success = 0
            audio = None
            while count < 5 and success == 0:
                try:
                    if "mp3" in s_announcement:
                        audio = MP3(os.path.join(announce_root, s_announcement))
                    elif "wav" in s_announcement:
                        audio = WAVE(os.path.join(announce_root, s_announcement))
                    elif "aiff" in s_announcement:
                        audio = AIFF(os.path.join(announce_root, s_announcement))
                    success = 1
                except Exception as e:
                    self.logger.debug(f"[ANNOUNCE] audio probe failed (try {count+1}/5): {e}")
                    self.plugin.sleep(0.5)
                    count += 1

            if success == 1 and audio is not None:
                indigo.server.log("Announcement Length: %s" % audio.info.length)

                # Ensure announcement URI components are valid
                try:
                    # 1) Ensure our lightweight 8889 server is up (no-ops if already started)
                    try:
                        self.ensure_announcement_http_server()
                    except Exception as _srv_e:
                        self.logger.error(f"❌ Announcement HTTP server not available: {_srv_e}")
                        return

                    # 2) Decide which host to publish to the Sonos player
                    def _usable_host(h: str) -> bool:
                        h = (h or "").strip()
                        if not h:
                            return False
                        lo = ("localhost", "127.0.0.1", "::1")
                        return h not in lo and not h.startswith("127.") and h != "0.0.0.0"

                    candidates = [
                        (self.HTTPServer or "").strip(),
                        (getattr(self, "announce_bind_ip", "") or "").strip(),
                        (getattr(self, "selectedInterfaceIP", "") or "").strip(),
                    ]
                    http_server = next((h for h in candidates if _usable_host(h)), "")
                    self.logger.debug(f"[ANNOUNCE URI] host candidates={candidates} -> chosen={http_server!r}")

                    if not http_server:
                        self.logger.error("❌ No usable HTTP server IP found (refusing to use loopback/0.0.0.0).")
                        return

                    # 3) Choose a port: prefs → actual server port → 8889
                    http_port = (str(self.HTTPStreamingPort).strip()
                                 if getattr(self, "HTTPStreamingPort", None) not in (None, "", 0)
                                 else str(getattr(self, "_announce_http_port", "") or ""))
                    if not http_port:
                        http_port = "8889"  # final fallback

                    # 4) Ensure we have a file name prepared by earlier code
                    announcement_file = s_announcement or ""
                    if not announcement_file:
                        self.logger.error("❌ Announcement file not prepared.")
                        return

                    # 5) Build and send
                    #announcement_uri = f"http://{http_server}:{http_port}/{announcement_file}"
                    import time
                    announcement_uri = f"http://{http_server}:{http_port}/{announcement_file}?t={int(time.time() * 1000)}"
                    soap_payload = (
                        f"<CurrentURI>{announcement_uri}</CurrentURI>"
                        f"<CurrentURIMetaData></CurrentURIMetaData>"
                    )
                    self.logger.info(f"[ANNOUNCE URI] {announcement_uri}")
                    uri_set_time = time.time()
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", soap_payload)

                except Exception as e:
                    self.logger.error(f"❌ Exception building announcement URI: {e}")
                    return

                # turn off queue repeat
                try:
                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetPlayMode", "<NewPlayMode>NORMAL</NewPlayMode>")
                except Exception as e:
                    self.logger.warning(f"⚠️ Could not set play mode to NORMAL: {e}")

                self.plugin.sleep(1)

                # Play announcement
                self.logger.debug("[ANNOUNCE] Play announcement")
                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")

                # Fetch watchdog: the player must PULL the file from our HTTP
                # server. If no request has arrived a couple of seconds after
                # Play, nothing will ever sound (player sits in TRANSITIONING) —
                # almost always a firewall/VLAN rule blocking speaker → server.
                # Diagnose loudly instead of failing silently.
                total_wait = tts_delay + audio.info.length
                self.plugin.sleep(min(2.0, total_wait))
                fetches = getattr(self, "_announce_last_fetch", {}) or {}
                if fetches.get(zoneIP, 0.0) < uri_set_time:
                    self.logger.error(
                        f"❌ {GM.name} never fetched the announcement from {announcement_uri} — "
                        f"the player cannot reach this Mac on port {http_port}. Check that your "
                        f"firewall/VLAN rules allow {zoneIP} → {http_server}:{http_port}/tcp.")
                if total_wait > 2.0:
                    self.plugin.sleep(total_wait - 2.0)

                # --- restore previous playback (best-effort) ---
                if use_snapshot:
                    self._restore_announcement_snapshots(announce_snapshots)
                else:
                    try:
                        self.logger.debug(f"[ANNOUNCE RESTORE] begin; gc_only={gc_only} "
                                          f"dev_vols={prev.get('per_dev_vol')} group_vol={prev.get('group_vol')} "
                                          f"uri={prev.get('uri')!r} pos={prev.get('pos')} vol={prev.get('vol')} "
                                          f"state={prev.get('state')} mute={prev.get('mute')}")

                        had_prior_uri = bool(prev.get("uri")) and "announcement." not in (prev.get("uri") or "")

                        if had_prior_uri:
                            restore_payload = (f"<CurrentURI>{prev['uri']}</CurrentURI>"
                                               f"<CurrentURIMetaData>{prev['meta']}</CurrentURIMetaData>")
                            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", restore_payload)
                            self.plugin.sleep(0.3)  # settle

                            if prev.get("pos") and prev["pos"].count(":") == 2 and prev["pos"] != "00:00:00":
                                try:
                                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Seek",
                                                  f"<Unit>REL_TIME</Unit><Target>{prev['pos']}</Target>")
                                    self.logger.debug(f"[ANNOUNCE RESTORE] Seek to {prev['pos']}")
                                except Exception as e:
                                    self.logger.debug(f"[ANNOUNCE RESTORE] Seek failed (continuing): {e}")
                        else:
                            self.logger.debug("[ANNOUNCE RESTORE] No prior URI captured; skipping URI restore")

                        # ========== RESTORE VOLUME + MUTE EXACTLY ==========
                        if gc_only:
                            restore_gv = prev.get("group_vol")
                            if isinstance(restore_gv, int):
                                try:
                                    self.logger.debug(f"[ANNOUNCE RESTORE] Restoring GROUP volume → {restore_gv}")
                                    self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupVolume",
                                                  f"<DesiredVolume>{restore_gv}</DesiredVolume>")
                                except Exception as e:
                                    self.logger.debug(f"[ANNOUNCE RESTORE] Group volume restore failed: {e}")
                            if prev.get("group_mute") in (0, 1):
                                try:
                                    self.logger.debug(f"[ANNOUNCE RESTORE] Restoring GROUP mute → {prev['group_mute']}")
                                    self.SOAPSend(zoneIP, "/MediaRenderer", "/GroupRenderingControl", "SetGroupMute",
                                                  f"<DesiredMute>{prev['group_mute']}</DesiredMute>")
                                except Exception as e:
                                    self.logger.debug(f"[ANNOUNCE RESTORE] Group mute restore failed: {e}")
                        else:
                            for item in AnnouncementZones:
                                try:
                                    _dev = indigo.devices[int(item)]
                                    _ip = (_dev.pluginProps.get("address") or _dev.address or "").strip()
                                    if not _ip:
                                        continue
                                    pv = prev["per_dev_vol"].get(_dev.id, None)
                                    pm = prev["per_dev_mute"].get(_dev.id, None)
                                    if isinstance(pv, int):
                                        self.logger.debug(f"[ANNOUNCE RESTORE] { _dev.name } volume → {pv}")
                                        self.SOAPSend(_ip, "/MediaRenderer", "/RenderingControl", "SetVolume",
                                                      f"<Channel>Master</Channel><DesiredVolume>{pv}</DesiredVolume>")
                                    if pm in (0, 1):
                                        self.logger.debug(f"[ANNOUNCE RESTORE] { _dev.name } mute → {pm}")
                                        self.SOAPSend(_ip, "/MediaRenderer", "/RenderingControl", "SetMute",
                                                      f"<Channel>Master</Channel><DesiredMute>{pm}</DesiredMute>")
                                except Exception as e:
                                    self.logger.debug(f"[ANNOUNCE RESTORE] per-device restore failed for {item}: {e}")

                            if isinstance(prev.get("vol"), int):
                                try:
                                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetVolume",
                                                  f"<Channel>Master</Channel><DesiredVolume>{prev['vol']}</DesiredVolume>")
                                except Exception:
                                    pass
                            if prev.get("mute") in (0, 1):
                                try:
                                    self.SOAPSend(zoneIP, "/MediaRenderer", "/RenderingControl", "SetMute",
                                                  f"<Channel>Master</Channel><DesiredMute>{prev['mute']}</DesiredMute>")
                                except Exception:
                                    pass
                        # ========== /RESTORE VOLUME + MUTE EXACTLY ==========

                        # Only resume transport to the *previous* state
                        state = (prev.get("state") or "UNKNOWN").upper()
                        if had_prior_uri:
                            if state == "PLAYING":
                                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                                self.logger.debug("[ANNOUNCE RESTORE] Resumed PLAYING")
                            elif state in ("PAUSED_PLAYBACK", "PAUSED"):
                                try:
                                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause", "")
                                    self.logger.debug("[ANNOUNCE RESTORE] Restored PAUSED")
                                except Exception:
                                    try:
                                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")
                                        self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause", "")
                                        self.logger.debug("[ANNOUNCE RESTORE] Pause via Play→Pause fallback")
                                    except Exception as e:
                                        self.logger.debug(f"[ANNOUNCE RESTORE] Pause fallback failed: {e}")
                            elif state == "STOPPED":
                                try:
                                    self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Stop", "")
                                    self.logger.debug("[ANNOUNCE RESTORE] Restored STOPPED")
                                except Exception as e:
                                    self.logger.debug(f"[ANNOUNCE RESTORE] Stop failed: {e}")
                        else:
                            try:
                                self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Stop", "")
                                self.logger.debug("[ANNOUNCE RESTORE] No prior URI → STOP")
                            except Exception:
                                pass

                    except Exception as e:
                        self.logger.warning(f"⚠️ Failed to restore previous playback after announcement: {e}")
            else:
                self.plugin.errorLog("Unable to read MP3/AIFF file. Announcement aborted.")



                


                
    def MicrosoftTranslateAuth(self):
        authUrl = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13/'
        scopeUrl = 'http://api.microsofttranslator.com'
        grantType = 'client_credentials'

        postdata = {'grant_type':grantType, 'scope':scopeUrl, 'client_id':self.MSTranslateClientID, 'client_secret':self.MSTranslateClientSecret}
        response = requests.post(authUrl, data=postdata, timeout=15)

        if response.status_code == 200:
            content = json.loads (response.content)
            return (content['access_token'])
        else:
            self.plugin.errorLog("[%s] Cannot authenticate to Microsoft Translate" % time.asctime())
            return (False)

    def MicrosoftTranslateLanguages(self):
        accessToken = self.MicrosoftTranslateAuth()
        if accessToken == False:
            return (False)

        scopeUrl = 'http://api.microsofttranslator.com'
        headers = {'Content-Type':'text/xml', 'Authorization':'Bearer ' + accessToken}
        url = scopeUrl + '/V2/Http.svc/GetLanguagesForSpeak'
        response = requests.get(url, headers=headers, timeout=15)

        langCodes = []
        Languages = ET.fromstring(response.content)
        for lang in Languages:
            langCodes.append(lang.text)
        languageCodes = str(langCodes).replace("'",'"')

        #self.myLocale = self.getLocale()
        #if self.myLocale == None:
        self.myLocale = 'en'

        url = scopeUrl + '/V2/Ajax.svc/GetLanguageNames?locale=' + self.myLocale + '&languageCodes=' + languageCodes
        response = requests.post(url, headers=headers, timeout=15)

        name_code = dict(zip(langCodes, eval(response.content)))
        indigo.server.log("Loaded Microsoft Translate Voices... [%s]" % len(name_code))

        return (name_code)

    def MicrosoftTranslate(self, announcement, language, out_path='announcement.mp3'):
        authUrl = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13/'
        scopeUrl = 'http://api.microsofttranslator.com'
        speakUrl = 'http://api.microsofttranslator.com/V2/Http.svc/Speak'
        grantType = 'client_credentials'

        accessToken = self.MicrosoftTranslateAuth()
        if accessToken == False:
            return (False)

        headers = {'Content-Type':'audio/mp3', 'Authorization':'Bearer ' + accessToken}
        url = speakUrl + '?text=' + announcement + '&language=' + language + '&format=audio/mp3&options=MaxQuality'

        with open (out_path, 'wb') as handle:
            response = requests.get(url, headers=headers, stream=True, timeout=15)

            if response.ok:
                for block in response.iter_content(1024):
                    handle.write(block)
                return (True)
            else:
                return (False)

    def getReferencePlayerIP(self):
        return soco.discover().pop().ip_address





############################################################################################
### End - Action annoucement processing
############################################################################################



    ######################################################################################
    # Plugin Preferences
    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        try:
            if not userCancelled:
                self.safe_debug(f"[{time.asctime()}] Getting plugin preferences.")

                # ✅ Apply prefs FIRST before referencing them
                self.plugin.pluginPrefs.update(valuesDict)
                try:
                    self.plugin.debug = self.plugin.pluginPrefs["showDebugInLog"]
                except Exception as exception_error:
                    self.plugin.debug = False

                try:
                    self.plugin.xmlDebug = self.plugin.pluginPrefs["showXMLInLog"]
                except Exception as exception_error:
                    self.plugin.xmlDebug = False

                try:
                    self.plugin.eventsDebug = self.plugin.pluginPrefs["showEventsInLog"]
                except Exception as exception_error:
                    self.plugin.eventsDebug = False

                try:
                    self.plugin.stateUpdatesDebug = self.plugin.pluginPrefs["showStateUpdatesInLog"]
                except Exception as exception_error:
                    self.plugin.stateUpdatesDebug = False

                rootZPIP = self.plugin.pluginPrefs.get("rootZPIP", "auto")
                if self.rootZPIP != rootZPIP:
                    self.rootZPIP = rootZPIP
                    if self.rootZPIP == 'auto':
                        self.rootZPIP = self.getReferencePlayerIP()
                        self.logger.info(f"Using Reference ZonePlayer IP: {self.rootZPIP}")
                    if self.rootZPIP is not None:
                        self.getSonosFavorites()
                        self.getPlaylistsDirect()
                        self.getRT_FavStationsDirect()
                        # Retrieve Sonos Device ID for Music API
                        url = "http://" + self.rootZPIP + ":1400/status/zp"
                        response = requests.get(url, timeout=5)
                        if response.ok:
                            root = ET.fromstring(response.content)
                            self.SonosDeviceID = root.findtext('.//SerialNumber')
                        else:
                            self.logger.error(f"[{time.asctime()}] Cannot retrieve SerialNumber from Root ZonePlayer: {self.rootZPIP}")
                    else:
                        self.logger.error(f"[{time.asctime()}] Reference ZonePlayer IP address invalid.")

                try:
                    self.EventProcessor = self.plugin.pluginPrefs["EventProcessor"]
                except Exception as exception_error:
                    self.EventProcessor = "SoCo"

                try:
                    self.EventIP = self.plugin.pluginPrefs["EventIP"]
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] Could not retrieve Event Listener IP address.")

                try:
                    self.EventCheck = self.plugin.pluginPrefs["EventCheck"]
                except Exception as exception_error:
                    self.EventCheck = 60
                    self.logger.error(f"[{time.asctime()}] Could not retrieve Event Check Interval; setting to 60 seconds.")

                try:
                    self.SubscriptionCheck = self.plugin.pluginPrefs["SubscriptionCheck"]
                except Exception as exception_error:
                    self.SubscriptionCheck = 15
                    self.logger.error(f"[{time.asctime()}] Could not retrieve Subscription Check Interval; setting to 15 seconds.")

                try:
                    http_ip = self.plugin.pluginPrefs.get("HTTPStreamingIP")
                    http_port = self.plugin.pluginPrefs.get("HTTPStreamingPort")

                    if (self.HTTPStreamingIP != http_ip) or (self.HTTPStreamingPort != http_port):
                        self.HTTPStreamingIP = http_ip
                        self.HTTPStreamingPort = http_port

                        # Tear down the existing streamer (if any) before spawning a new one,
                        # otherwise the next bind() fails with EADDRINUSE on port 8888.
                        self.HTTPStreamerOn = False
                        if getattr(self, "httpd", None):
                            try:
                                self.httpd.server_close()
                            except Exception:
                                pass
                            self.httpd = None

                        v = Thread(target=self.HTTPStreamer)
                        v.setDaemon(True)
                        v.start()
                except Exception as exception_error:
                    import traceback
                    self.logger.error(f"[{time.asctime()}] HTTPStreamer not functioning: {exception_error}")
                    self.safe_debug(traceback.format_exc())


                try:
                    new_path = self.plugin.pluginPrefs.get("SoundFilePath", "").strip()
                    if not new_path:
                        new_path = indigo.server.getInstallFolderPath() + "/AudioFiles"

                    self.SoundFilePath = new_path
                    self.logger.info(f"🔁 Reloading sound files from: {self.SoundFilePath}")
                    self.getSoundFiles()
                except Exception as exception_error:
                    self.logger.error(f"[{time.asctime()}] ❌ Could not process SoundFilePath: {exception_error}")



                self.processServicePrefs()

                self.logger.info(f"[{time.asctime()}] Processed plugin preferences.")
                return True

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def processServicePrefs(self):
        """Load/refresh streaming-service and TTS credentials from pluginPrefs.

        Called from closedPrefsConfigUi and from startup() — the original plugin
        loaded these at startup via closedPrefsConfigUi(None, None); without a
        startup call the TTS keys stay None until the config dialog is re-saved
        (e.g. Polly announcements fail with "Unable to locate credentials").
        """
        try:
            if (self.Pandora != self.plugin.pluginPrefs['Pandora']) or \
                    (self.PandoraEmailAddress != self.plugin.pluginPrefs['PandoraEmailAddress']) or \
                    (self.PandoraPassword != self.plugin.pluginPrefs['PandoraPassword']) or \
                    (self.PandoraNickname != self.plugin.pluginPrefs['PandoraNickname']):
                self.Pandora = self.plugin.pluginPrefs['Pandora']
                self.PandoraEmailAddress = self.plugin.pluginPrefs['PandoraEmailAddress']
                self.PandoraPassword = self.plugin.pluginPrefs['PandoraPassword']
                self.PandoraNickname = self.plugin.pluginPrefs['PandoraNickname']
                if self.Pandora:
                    self.getPandora(self.PandoraEmailAddress, self.PandoraPassword, self.PandoraNickname)
        except Exception as exception_error:
            self.logger.error(f"[{time.asctime()}] Could not retrieve Pandora credentials.")

        try:
            if (self.Pandora2 != self.plugin.pluginPrefs['Pandora2']) or \
                    (self.PandoraEmailAddress2 != self.plugin.pluginPrefs['PandoraEmailAddress2']) or \
                    (self.PandoraPassword2 != self.plugin.pluginPrefs['PandoraPassword2']) or \
                    (self.PandoraNickname2 != self.plugin.pluginPrefs['PandoraNickname2']):
                self.Pandora2 = self.plugin.pluginPrefs['Pandora2']
                self.PandoraEmailAddress2 = self.plugin.pluginPrefs['PandoraEmailAddress2']
                self.PandoraPassword2 = self.plugin.pluginPrefs['PandoraPassword2']
                self.PandoraNickname2 = self.plugin.pluginPrefs['PandoraNickname2']
                if self.Pandora2:
                    self.getPandora(self.PandoraEmailAddress2, self.PandoraPassword2, self.PandoraNickname2)
        except Exception as exception_error:
            self.logger.error(f"[{time.asctime()}] Could not retrieve secondary Pandora credentials.")

        try:
            if (self.SiriusXM != self.plugin.pluginPrefs['SiriusXM']) or \
                    (self.SiriusXMID != self.plugin.pluginPrefs['SiriusXMID']) or \
                    (self.SiriusXMPassword != self.plugin.pluginPrefs['SiriusXMPassword']):
                self.SiriusXM = self.plugin.pluginPrefs['SiriusXM']
                self.SiriusXMID = self.plugin.pluginPrefs['SiriusXMID']
                self.SiriusXMPassword = self.plugin.pluginPrefs['SiriusXMPassword']
                if self.SiriusXM:
                    self.getSiriusXM()
        except Exception as exception_error:
            self.logger.error(f"[{time.asctime()}] Could not retrieve SiriusXM parameters.")

        try:
            if (self.IVONA != self.plugin.pluginPrefs['IVONA']) or \
                    (self.IVONAaccessKey != self.plugin.pluginPrefs['IVONAaccessKey']) or \
                    (self.IVONAsecretKey != self.plugin.pluginPrefs['IVONAsecretKey']):
                self.IVONA = self.plugin.pluginPrefs['IVONA']
                if self.IVONA:
                    self.IVONAaccessKey = self.plugin.pluginPrefs['IVONAaccessKey']
                    self.IVONAsecretKey = self.plugin.pluginPrefs['IVONAsecretKey']
                if self.IVONA:
                    self.IVONAVoices()
        except Exception as exception_error:
            self.logger.error(f"[{time.asctime()}] Could not retrieve IVONA parameters.")

        try:
            polly_pref   = self.plugin.pluginPrefs.get('Polly', False)
            polly_access = self.plugin.pluginPrefs.get('PollyaccessKey', '')
            polly_secret = self.plugin.pluginPrefs.get('PollysecretKey', '')
            if (self.Polly != polly_pref) or \
                    (self.PollyaccessKey != polly_access) or \
                    (self.PollysecretKey != polly_secret):
                self.Polly = polly_pref
                if self.Polly:
                    self.PollyaccessKey = polly_access
                    self.PollysecretKey = polly_secret
                    self.PollyVoices()
        except Exception as exception_error:
            self.logger.error(f"[{time.asctime()}] Could not retrieve Polly parameters: {exception_error}")

        try:
            if (self.MSTranslate != self.plugin.pluginPrefs['MSTranslate']) or \
                    (self.MSTranslateClientID != self.plugin.pluginPrefs['MSTranslateClientID']) or \
                    (self.MSTranslateClientSecret != self.plugin.pluginPrefs['MSTranslateClientSecret']):
                self.MSTranslate = self.plugin.pluginPrefs['MSTranslate']
                if self.MSTranslate:
                    self.MSTranslateClientID = self.plugin.pluginPrefs['MSTranslateClientID']
                    self.MSTranslateClientSecret = self.plugin.pluginPrefs['MSTranslateClientSecret']
                if self.MSTranslate:
                    self.MSTranslateVoices = self.MicrosoftTranslateLanguages()
        except Exception as exception_error:
            self.logger.error(f"[{time.asctime()}] Could not retrieve MSTranslate parameters.")




###############################################################################################################################


    def getSonosFavorites(self):
        try:
            global Sonos_Favorites
            Sonos_Favorites = []
            res = self.restoreString(self.SOAPSend(self.rootZPIP, "/MediaServer", "/ContentDirectory", "Browse", "<ObjectID>FV:2</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria>"), 1)
            Favorites = ET.fromstring(res)
            for Favorite in Favorites.findall('.//{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}item'):
                e_id = Favorite.attrib['id']
                e_res_clean = Favorite.findtext('.//{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}res')
                e_res = self.restoreString(e_res_clean, 0)
                e_title = self.restoreString(Favorite.findtext('.//{http://purl.org/dc/elements/1.1/}title'), 0)
                e_resMD = Favorite.findtext('.//{urn:schemas-rinconnetworks-com:metadata-1-0/}resMD')
                Sonos_Favorites.append((e_res, e_title, e_resMD, e_res_clean, e_id))
                self.safe_debug(f"\tSonos Favorites: {e_id}, {e_title}, {e_res}")
            self.logger.info(f"Loaded Sonos Favorites... [{len(Sonos_Favorites)}]")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement


    ############################################################################################
    ### Define all of your action processing in this block
    ############################################################################################
        
    def actionTogglePlay(self, indigo_device):
        zoneIP = indigo_device.address
        transport_state = indigo_device.states.get("ZP_STATE", "STOPPED").upper()

        self.safe_debug(f"🎛 ZP_STATE for {indigo_device.name} (from Indigo): {transport_state}")

        # If ZP_STATE looks unreliable, fall back to querying SoCo directly
        if transport_state not in ("PLAYING", "PAUSED_PLAYBACK", "STOPPED"):
            soco_device = self.findDeviceByIP(zoneIP)
            if soco_device:
                try:
                    transport_info = soco_device.get_current_transport_info()
                    transport_state = transport_info.get("current_transport_state", "STOPPED").upper()
                    self.safe_debug(f"🎛 ZP_STATE for {indigo_device.name} (from SoCo): {transport_state}")
                except Exception as e:
                    self.logger.warning(f"⚠️ SoCo state fetch failed for {indigo_device.name}: {e}")
                    transport_state = "STOPPED"

        # Execute based on state
        if transport_state == "PLAYING":
            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause",
                          "<InstanceID>0</InstanceID><Speed>1</Speed>")
            self.logger.info(f"⏸ Pause triggered for {indigo_device.name}")
        else:
            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play",
                          "<InstanceID>0</InstanceID><Speed>1</Speed>")
            self.logger.info(f"▶️ Play triggered for {indigo_device.name}")

    def actionVolumeUp(self, indigo_device):
        try:
            discovered = soco.discover()
            soco_device = soco.SoCo(indigo_device.address)
            current_vol = soco_device.volume
            soco_device.volume = min(current_vol + 5, 100)
            self.logger.info(f"🔊 Volume UP for {indigo_device.name}: {current_vol} → {soco_device.volume}")
        except Exception as e:
            self.logger.error(f"❌ actionVolumeUp error for {indigo_device.name}: {e}")

    def actionVolumeDown(self, indigo_device):
        try:
            discovered = soco.discover()
            soco_device = soco.SoCo(indigo_device.address)
            current_vol = soco_device.volume
            soco_device.volume = max(current_vol - 5, 0)
            self.logger.info(f"🔉 Volume DOWN for {indigo_device.name}: {current_vol} → {soco_device.volume}")
        except Exception as e:
            self.logger.error(f"❌ actionVolumeDown error for {indigo_device.name}: {e}")


    def actionNext(self, indigo_device):
        try:
            zoneIP = indigo_device.address
            current_uri = indigo_device.states.get("ZP_CurrentTrackURI", "")

            if "x-sonosapi-hls:channel-linear" in current_uri:
                self.logger.info(f"📻 SiriusXM detected on {indigo_device.name} — calling ChannelUp directly")
                self.channelUpOrDown(indigo_device, direction="up")
            else:
                soco_device = soco.SoCo(zoneIP)
                soco_device.next()
                self.logger.info(f"⏭️ Skipped to NEXT track on {indigo_device.name}")
        except Exception as e:
            self.logger.error(f"❌ actionNext error for {indigo_device.name}: {e}")



    def actionPrevious(self, indigo_device):
        try:
            zoneIP = indigo_device.address
            current_uri = indigo_device.states.get("ZP_CurrentTrackURI", "")

            if "x-sonosapi-hls:channel-linear" in current_uri:
                self.logger.info(f"📻 SiriusXM detected on {indigo_device.name} — calling ChannelDown directly")
                self.channelUpOrDown(indigo_device, direction="down")
            else:
                soco_device = soco.SoCo(zoneIP)
                soco_device.previous()
                self.logger.info(f"⏮️ Went to PREVIOUS track on {indigo_device.name}")
        except Exception as e:
            self.logger.error(f"❌ actionPrevious error for {indigo_device.name}: {e}")

    def _get_any_reachable_soco(self):
        """Return a SoCo instance for any currently-reachable player, or None."""
        for ip, sd in list((getattr(self, "soco_by_ip", {}) or {}).items()):
            if self.is_host_reachable(ip, timeout=1.0):
                return sd
        # Fall back to configured Indigo device addresses
        for idev in indigo.devices.iter("self.ZonePlayer"):
            ip = (idev.pluginProps.get("address") or idev.address or "").strip()
            if ip and self.is_host_reachable(ip, timeout=1.0):
                return self.get_soco_device(ip)
        return None

    def getSonosAlarmsList(self, filter="", valuesDict=None, typeId="", targetId=0):
        """Dynamic list of native Sonos alarms for the Set Alarm On/Off action."""
        try:
            from soco.alarms import get_alarms
            soco_dev = self._get_any_reachable_soco()
            if soco_dev is None:
                return [("none", "No reachable Sonos player found")]
            alarms = get_alarms(soco_dev)
            entries = []
            for a in sorted(alarms, key=lambda x: str(x.start_time)):
                zone_name = getattr(getattr(a, "zone", None), "player_name", "?")
                recurrence = getattr(a, "recurrence", "") or "once"
                state = "enabled" if a.enabled else "disabled"
                entries.append((str(a.alarm_id), f"{a.start_time} — {zone_name} — {recurrence} — {state}"))
            return entries or [("none", "No Sonos alarms configured")]
        except Exception as e:
            self.logger.error(f"❌ getSonosAlarmsList failed: {e}")
            return [("none", "Error loading alarms — see log")]

    def actionSonosAlarm(self, pluginAction):
        """Enable / disable / toggle a native Sonos alarm (HA-parity feature)."""
        try:
            from soco.alarms import get_alarms
            alarm_id = pluginAction.props.get("alarmId")
            operation = pluginAction.props.get("operation", "toggle")
            volume_raw = (pluginAction.props.get("volume") or "").strip()

            if not alarm_id or alarm_id == "none":
                self.logger.warning("⚠️ No Sonos alarm selected in action config.")
                return

            soco_dev = self._get_any_reachable_soco()
            if soco_dev is None:
                self.logger.error("❌ No reachable Sonos player — cannot modify alarms.")
                return

            alarm = next((a for a in get_alarms(soco_dev) if str(a.alarm_id) == str(alarm_id)), None)
            if alarm is None:
                self.logger.error(f"❌ Sonos alarm '{alarm_id}' no longer exists — re-select it in the action config.")
                return

            if operation == "enable":
                alarm.enabled = True
            elif operation == "disable":
                alarm.enabled = False
            else:
                alarm.enabled = not alarm.enabled

            volume_note = ""
            if volume_raw:
                try:
                    alarm.volume = max(0, min(100, int(volume_raw)))
                    volume_note = f", volume {alarm.volume}"
                except (TypeError, ValueError):
                    self.logger.warning(f"⚠️ Ignoring invalid alarm volume '{volume_raw}' (expected 0-100)")

            alarm.save()
            zone_name = getattr(getattr(alarm, "zone", None), "player_name", "?")
            self.logger.info(f"⏰ Sonos alarm {alarm.start_time} ({zone_name}) → {'enabled' if alarm.enabled else 'disabled'}{volume_note}")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def actionPandoraThumbs(self, pluginAction, action):
        """Pandora Thumbs Up / Thumbs Down — restored from the original plugin
        (plugin.py forwarded here but the method was lost in a refactor)."""
        try:
            dev = indigo.devices[pluginAction.deviceId]
            zoneIP = dev.pluginProps["address"]

            if dev.states["GROUP_Coordinator"] == "false":
                Coordinator = dev.states["GROUP_Name"]
                for idev in indigo.devices.iter("self.ZonePlayer"):
                    if idev.states["GROUP_Coordinator"] == "true" and idev.states["GROUP_Name"] == Coordinator:
                        zoneIP = idev.pluginProps["address"]
                        dev = indigo.devices[idev.id]
                        break

            if uri_pandora in dev.states["ZP_CurrentURI"]:
                (x, y) = dev.states["ZP_CurrentURI"].split(':')
                (stationId, z) = y.split('?')
                PandoraStation = None
                PandoraEmailAddress = None
                for item in Sonos_Pandora:
                    if item[0] == stationId:
                        PandoraStation = item[1]
                        PandoraEmailAddress = item[2]
                        break
                if PandoraEmailAddress is None:
                    self.logger.error(f"Pandora station {stationId} not found in station list; cannot send feedback.")
                    return
                trackToken = self.parsePandoraToken(dev.states["ZP_CurrentTrackURI"])

                if PandoraEmailAddress == self.PandoraEmailAddress:
                    PandoraPassword = self.PandoraPassword
                elif PandoraEmailAddress == self.PandoraEmailAddress2:
                    PandoraPassword = self.PandoraPassword2
                else:
                    self.logger.error(f"No Pandora credentials match account '{PandoraEmailAddress}'.")
                    return

                pandora = Pandora()
                pandora.authenticate(PandoraEmailAddress, PandoraPassword)

                if action == "thumbs_up":
                    thumbAction = "Thumbs Up"
                    feedback = True
                else:
                    thumbAction = "Thumbs Down"
                    feedback = False

                try:
                    thumb_status = pandora.add_feedback(stationId, trackToken, feedback)
                    partist = thumb_status['artistName']
                    ptrack = thumb_status['songName']
                    if action == "thumbs_down":
                        self.actionDirect(PA(dev.id), "Next")
                    self.logger.info(f"{thumbAction} for station: {PandoraStation}, artist: {partist}, track: {ptrack} on ZonePlayer: {dev.name}")
                except Exception:
                    self.logger.error(f"Unable to {thumbAction} track on ZonePlayer: {dev.name}")

            else:
                self.logger.error(f"Pandora not actively playing on ZonePlayer: {dev.name}")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def actionStates(self, pluginAction, action, only_device_ids=None):
        #indigo.server.log("did i hit 2 ????", type="Sonos PY Plugin Msg: 6778: ")
        global SavedState

        if action == "saveStates":
            SavedState = []
            # normalize a set (or None for all)
            scope = set(only_device_ids) if only_device_ids else None

            for dev in indigo.devices.iter("self.ZonePlayer"):
                if dev.enabled and dev.pluginProps["model"] != SONOS_SUB:
                    if scope and dev.id not in scope:
                        continue  # 🔕 skip non-target devices during announcement

                    # --- these two calls were creating the UPNP noise ---
                    try:
                        ZP_CurrentURIMetaData = self.parseDirty(
                            self.SOAPSend(dev.pluginProps["address"],
                                          "/MediaRenderer", "/AVTransport",
                                          "GetMediaInfo", "", context="SAVE"),
                            "<CurrentURIMetaData>", "</CurrentURIMetaData>")
                    except Exception as e:
                        self.logger.warning(f"⚠️ Failed GetMediaInfo for {dev.name} ({dev.pluginProps['address']}): {e}")
                        ZP_CurrentURIMetaData = ""

                    try:
                        rel_time = self.parseRelTime(
                            dev,
                            self.SOAPSend(dev.pluginProps["address"],
                                          "/MediaRenderer", "/AVTransport",
                                          "GetPositionInfo", "", context="SAVE"))
                    except Exception as e:
                        self.logger.warning(f"⚠️ Failed GetPositionInfo for {dev.name} ({dev.pluginProps['address']}): {e}")
                        rel_time = "00:00:00"

                    SavedState.append((
                        dev.states['ZP_LocalUID'],
                        dev.states['Q_Crossfade'],
                        dev.states['Q_Repeat'],
                        dev.states['Q_Shuffle'],
                        dev.states['ZP_MUTE'],
                        dev.states['ZP_STATE'],
                        dev.states['ZP_VOLUME'],
                        dev.states['ZP_CurrentURI'],
                        ZP_CurrentURIMetaData,
                        dev.states['ZP_CurrentTrack'],
                        dev.states['GROUP_Coordinator'],
                        "",  # ZP (unused as before)
                        rel_time,
                        dev.states['ZonePlayerUUIDsInGroup']
                    ))

        elif action == "restoreStates":
            pass




    def actionStop(self, indigo_device):
        try:
            discovered = soco.discover()
            soco_device = soco.SoCo(indigo_device.address)
            soco_device.stop()
            self.logger.info(f"⏹️ STOPPED playback on {indigo_device.name}")
        except Exception as e:
            self.logger.error(f"❌ actionStop error for {indigo_device.name}: {e}")



    ############################### End of Action Processing Block ###############################



    def startup(self):
        self.logger.info("🔌 Sonos Plugin Starting Up...")


        # at plugin start
        self._startup_warmup = True


        # Default image path in case artwork is missing from the stream
        #DEFAULT_ARTWORK_PATH = '/Library/Application Support/Perceptive Automation/images/Sonos/default_artwork copy.jpg'

        # Ensure that the artwork folder exists for saving images
        ARTWORK_FOLDER = "/Library/Application Support/Perceptive Automation/images/Sonos/"
        os.makedirs(ARTWORK_FOLDER, exist_ok=True)

        # check for sound file?
        self.SoundFilePath = self.pluginPrefs.get("SoundFilePath", "")
        self.logger.debug(f"🔧 Loaded SoundFilePath from prefs: {self.SoundFilePath}")

        if not self.SoundFilePath:
            self.SoundFilePath = indigo.server.getInstallFolderPath() + "/AudioFiles"
            self.logger.info(f"⚠️ Falling back to default SoundFilePath: {self.SoundFilePath}")

        # Cleanup old art before starting the server to reduce storage size and keep things tidy
        self.cleanup_old_artwork()
        self.logger.debug(f"🖼️ Updated artwork 5")

        # Function to start the HTTP server and serve images
        def start_http_server():
            try:
                import http.server
                import socketserver
                import threading

                # Set the artwork folder to be served
                artwork_folder = "/Library/Application Support/Perceptive Automation/images/Sonos/"
                port = 8888

                # Handler class to serve files from the specified artwork folder
                class ArtworkHandler(http.server.SimpleHTTPRequestHandler):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, directory=artwork_folder, **kwargs)

                # Pre-create a TCPServer that can reuse the socket
                class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
                    allow_reuse_address = True

                # Create and start the server
                httpd = ThreadedTCPServer(("", port), ArtworkHandler)
                server_thread = threading.Thread(target=httpd.serve_forever)
                server_thread.daemon = True
                server_thread.start()

                print(f"🚀 Mini HTTP server started on http://localhost:{port}/ serving {artwork_folder}")

            except Exception as e:
                print(f"DT - Failed to start mini HTTP server: {e}")

        # Start the HTTP server
        start_http_server()

        # start the announce http server - DT
        ip, port, root = self.get_announce_http_config()
        self.logger.info(f"📢 Announcement HTTP config → ip='{ip or 'ALL'}', port={port}, root='{root}'")

        # Ensure SoundFilePath points at the folder we intend to serve (keep your earlier choice if set)
        if not self.SoundFilePath:
            self.SoundFilePath = root
        try:
            os.makedirs(self.SoundFilePath, exist_ok=True)
        except Exception as e:
            self.logger.error(f"❌ Could not create SoundFilePath '{self.SoundFilePath}': {e}")

        # Persist the streaming port (from config; always an int)
        try:
            self.HTTPStreamingPort = int(port)
        except Exception:
            self.HTTPStreamingPort = 8889  # last-ditch default

        # --- Pick a publishable HTTP host (never loopback / 0.0.0.0) before server start ---
        def _usable_host(h: str) -> bool:
            if not h:
                return False
            h = h.strip()
            if h in ("localhost", "0.0.0.0", "::1"):
                return False
            if h.startswith("127."):
                return False
            return True

        try:
            # Candidate order:
            #  1) Existing self.HTTPServer (if safe)
            #  2) Interface on target Sonos subnet (if discoverable)
            #  3) selectedInterfaceIP from earlier discovery
            publish_host = (getattr(self, "HTTPServer", "") or "").strip()

            if not _usable_host(publish_host):
                best_on_subnet = None
                try:
                    # Reuse your subnet-aware scanner if present
                    best_on_subnet = self.find_sonos_interface_ip(getattr(self, "targetSonosSubnet", None))
                except Exception:
                    best_on_subnet = None

                if _usable_host(best_on_subnet):
                    publish_host = best_on_subnet
                else:
                    selected_ip = (str(getattr(self, "selectedInterfaceIP", "")).strip() or "")
                    if _usable_host(selected_ip):
                        publish_host = selected_ip
                    else:
                        publish_host = ""  # let ensure_announcement_http_server() bind to all; we'll re-evaluate after

            # Set (or clear) the attribute now; we may refine it after bind
            self.HTTPServer = publish_host

            if _usable_host(self.HTTPServer):
                self.logger.info(f"🌐 Using {self.HTTPServer} as HTTPServer for announcements")
            else:
                self.logger.warning("⚠️ No safe LAN IP available yet for announcements; will re-evaluate after server start.")
        except Exception as e:
            self.logger.warning(f"⚠️ Unable to normalize HTTPServer at startup: {e}")

        # Bring up the announcement server and log conclusively
        try:
            started = self.ensure_announcement_http_server()
        except Exception as e:
            started = False
            self.logger.error(f"❌ Announcement HTTP server failed to start: {e}")

        # If ensure_announcement_http_server doesn't return a boolean, infer from attribute
        if started is None:
            started = bool(getattr(self, "_announce_httpd", None))

        if started:
            # If we still don't have a safe publish host, try to use what the server actually bound (if usable)
            try:
                bound_host = (getattr(self, "announce_bind_ip", "") or "").strip()
                if not _usable_host(self.HTTPServer) and _usable_host(bound_host):
                    self.HTTPServer = bound_host
                    self.logger.info(f"🌐 Announcement publish host updated to {self.HTTPServer} after server start")
            except Exception:
                pass

            self.logger.info(
                f"✅ Announcement HTTP server is running on "
                f"{(self.HTTPServer if _usable_host(self.HTTPServer) else '0.0.0.0')}:{self.HTTPStreamingPort}"
            )
        else:
            self.logger.error("❌ Announcement HTTP server is NOT running (see errors above)")

        # 📥 Continue normal Sonos initialization
        # Split into smaller guarded sections so later steps still run.

        # Load streaming-service/TTS credentials (Pandora, SiriusXM, IVONA, Polly,
        # MSTranslate) from pluginPrefs — the original plugin did this at startup
        # via closedPrefsConfigUi(None, None); without it Polly/IVONA keys remain
        # None until the config dialog is re-saved.
        try:
            self.processServicePrefs()
        except Exception as e:
            self.logger.error(f"❌ Failed to load service credentials from prefs (continuing): {e}")

        # Apple voices for the announcement UI — the original plugin loaded these
        # at startup; without this the APPLE_voice menu is empty and Apple Speech
        # announcements silently produce nothing.
        try:
            global NSVoices
            NSVoices = NSSpeechSynthesizer.availableVoices()
            self.logger.info(f"🗣️ Loaded Apple Voices.. [{len(NSVoices)}]")
        except Exception as e:
            self.logger.error(f"❌ Cannot load Apple Voices: {e}")

        # One-time heads-up when players live on a different subnet/VLAN than
        # this Mac — announcements and artwork are pulled BY the players FROM us.
        self._log_cross_vlan_firewall_advice()




###

        #self.soco_event_handler()

        # Ensure the cache exists before any dumps or evaluations
        self._seed_zone_group_cache_from_soco()

        # Now run the exact same pipeline you run after a ZGT change
        #self.refresh_group_topology_after_plugin_zone_change()
        #for dev in indigo.devices.iter("self"):
        #    self.updateZoneGroupStates(dev)

        self.evaluate_and_update_grouped_states()
        self._refresh_all_group_states_helper(reason="event handler")
        #self.refresh_all_group_states()
        self._seed_zone_group_cache_from_soco()        
        # Optional: emit your dumps
        #self.dump_group_state_to_log()
        #self.audit_all_sonos_devices()




###






        try:
            self.sorted_siriusxm_guids = sorted(self.siriusxm_guid_map.keys())
        except Exception as e:
            self.logger.error(f"❌ Failed to sort SiriusXM GUIDs: {e}")

        try:
            discovered = soco.discover()
            if discovered:
                for device in discovered:
                    self.soco_by_ip[device.ip_address] = device
            else:
                self.logger.warning("⚠️ SoCo discovery found no Sonos devices on the network (continuing)")
        except Exception as e:
            self.logger.error(f"❌ SoCo discovery failed (continuing): {e}")

        try:
            self.rootZPIP = self.plugin.pluginPrefs.get("rootZPIP", "auto")
            if self.rootZPIP == "auto":
                self.rootZPIP = self.getReferencePlayerIP()
                self.logger.info(f"✅ Using Reference ZonePlayer IP: {self.rootZPIP}")

            if not self.rootZPIP:
                self.logger.error("❌ rootZPIP is not set. Cannot fetch Sonos playlists.")
            elif not self.is_host_reachable(self.rootZPIP):
                self.logger.warning(f"📴 Reference ZonePlayer {self.rootZPIP} is unreachable — skipping playlists/favorites load at startup.")
            else:
                try:
                    self.getSonosFavorites()
                    self.getPlaylistsDirect()
                    self.getRT_FavStationsDirect()
                    self.safe_debug("📥 Sonos playlists, favorites, and radio stations loaded.")
                except Exception as e:
                    self.logger.error(f"❌ Failed loading playlists/favorites: {e}")
        except Exception as e:
            self.logger.error(f"❌ Reference player setup failed: {e}")

        try:
            self.logger.debug("🕒 Deferring SiriusXM test playback for 'Office' until runConcurrentThread()")
            self.logger.debug("🔧 Starting up Sonos Plugin...")
            self.build_ip_to_device_map()
            self.logger.debug("🔎 Performing post-startup audit of Sonos device group states...")
        except Exception as e:
            self.logger.error(f"❌ Device/IP map build failed (continuing): {e}")

        try:
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                # Resyncs the state list from Devices.xml if required states are missing
                dev = self.initialize_custom_states(dev) or dev

                group_coordinator = dev.states.get("GROUP_Coordinator", "n/a")
                #self.trace_me()
                group_name = dev.states.get("GROUP_Name", "n/a")
                Grouped = dev.states.get("Grouped", "n/a")
                # NOTE: we now run evaluate/elevate AFTER bootstrap so we just log here.
                self.logger.debug(f"📊 Device '{dev.name}': Coordinator={group_coordinator}, Group='{group_name}', Grouped={Grouped}")

        except Exception as e:
            self.logger.error(f"❌ Per-device initialization loop failed (continuing): {e}")







    def shutdown(self):
        try:
            self.logger.info("SonosPlugin shutdown initiated.")

            # ✅ Gracefully stop mini HTTP server
            if hasattr(self, "httpd") and self.httpd:
                try:
                    self.logger.info("🛑 Shutting down mini HTTP server...")
                    try:
                        self.httpd.shutdown()
                    except Exception as shutdown_error:
                        self.logger.warning(f"⚠️ First shutdown() attempt failed: {shutdown_error} — retrying...")

                        # 🛠 Try forcing socket close manually if shutdown failed
                        if hasattr(self.httpd, "socket") and self.httpd.socket:
                            try:
                                self.httpd.socket.close()
                                self.logger.warning("🛠 Forced socket close after failed shutdown attempt.")
                            except Exception as socket_close_error:
                                self.logger.error(f"❌ Failed to close server socket manually: {socket_close_error}")

                    try:
                        self.httpd.server_close()
                    except Exception as server_close_error:
                        self.logger.warning(f"⚠️ server_close() failed: {server_close_error}")

                    self.logger.info("✅ Mini HTTP server shut down cleanly.")
                except Exception as httpd_error:
                    self.logger.error(f"❌ Error during mini HTTP server shutdown: {httpd_error}")
                finally:
                    self.httpd = None  # ✅ Explicitly clear

            if hasattr(self, "server_thread") and self.server_thread:
                try:
                    self.logger.info("🛑 Waiting for mini HTTP server thread to finish...")
                    self.server_thread.join(timeout=5.0)
                    if self.server_thread.is_alive():
                        self.logger.warning("⚠️ Server thread still alive after join timeout.")
                    else:
                        self.logger.info("✅ Mini HTTP server thread terminated.")
                except Exception as thread_error:
                    self.logger.error(f"❌ Error waiting for mini HTTP server thread: {thread_error}")
                finally:
                    self.server_thread = None  # ✅ Explicitly clear

            # ✅ Stop SoCo Event Listener
            try:
                from soco.events import event_listener
                is_running = getattr(event_listener, "is_running", None)
                if callable(is_running):
                    if is_running():
                        event_listener.stop()
                        self.logger.info("✅ SoCo Event Listener stopped.")
                elif isinstance(is_running, bool):
                    if is_running:
                        event_listener.stop()
                        self.logger.info("✅ SoCo Event Listener stopped.")
                else:
                    self.logger.warning("⚠️ SoCo Event Listener not running or invalid.")
            except Exception as event_listener_error:
                self.logger.error(f"❌ Error shutting down SoCo Event Listener: {event_listener_error}")


            # ✅ Stop announce http server - DT

            try:
                if getattr(self, "_announce_httpd", None):
                    self._announce_httpd.shutdown()
                    self._announce_httpd.server_close()
                    self._announce_httpd = None
                    self.logger.info("📢 Announcement HTTP server stopped")
            except Exception as e:
                self.logger.warning(f"Failed to stop announcement HTTP server: {e}")




        except Exception as e:
            self.logger.error(f"❌ shutdown error: {e}")



    def bootstrap_group_state_from_startup(self):
        """
        Bring startup state to the same 'normalized' view we get after a ZoneGroupTopology change.
        This mirrors what your ZGT handler does (parse → cache → refresh → propagate).
        """

        try:
            # 1) Pick any known player IP to ask ZoneGroupTopology for the whole-house state
            any_ip = None
            for d in indigo.devices.iter("self.ZonePlayer"):
                ip = (d.pluginProps.get("address") or d.address or "").strip()
                if ip:
                    any_ip = ip
                    break

            if not any_ip:
                self.logger.warning("⚠️ bootstrap_group_state_from_startup: no device IPs available yet; skipping.")
                return

            # 2) Cold read of ZoneGroupState (same info you get via ZGT event)
            try:
                raw = self.SOAPSend(any_ip, "/ZoneGroupTopology", "/ZoneGroupTopology", "GetZoneGroupState", "")
                xml = self.parseDirty(raw, "<ZoneGroupState>", "</ZoneGroupState>") or ""
                if isinstance(xml, bytes):
                    xml = xml.decode("utf-8", errors="replace")
            except Exception as e:
                self.logger.error(f"❌ bootstrap_group_state_from_startup: GetZoneGroupState failed: {e}")
                return

            # 3) Parse and seed the cache exactly as in the ZGT handler
            try:
                parsed_groups = self.parse_zone_group_state(xml) or {}
                with self.zone_group_state_lock:
                    self.zone_group_state_cache = copy.deepcopy(parsed_groups)
                self.logger.info(f"💾 (startup) zone_group_state_cache seeded with {len(parsed_groups)} group(s)")
            except Exception as e:
                self.logger.error(f"❌ bootstrap_group_state_from_startup: parse_zone_group_state failed: {e}")
                return

            # 4) Run the same post-change normalization you use in ZGT path
            try:
                self.refresh_group_topology_after_plugin_zone_change()
            except Exception as e:
                self.logger.debug(f"bootstrap: refresh_group_topology_after_plugin_zone_change() failed (continuing): {e}")

            # Optional but recommended: these are used elsewhere (e.g., after setStandalones)
            try:
                self._refresh_all_group_states_helper(reason="bootstrap_group_state_from_startup")
                #self.refresh_all_group_states()
            except Exception as e:
                self.logger.debug(f"bootstrap: refresh_all_group_states() failed (continuing): {e}")

            try:
                self.evaluate_and_update_grouped_states()
            except Exception as e:
                self.logger.debug(f"bootstrap: evaluate_and_update_grouped_states() failed (continuing): {e}")

            # 5) Propagate group states to Indigo devices — this is exactly what your ZGT handler does
            try:
                self.logger.debug("📣 (startup) Propagating Grouped/Coordinator updates to all devices…")
                for dev in indigo.devices.iter("self"):
                    self.updateZoneGroupStates(dev)
            except Exception as e:
                self.logger.debug(f"bootstrap: updateZoneGroupStates propagation failed (continuing): {e}")

            # (Optional) If you want the same rich logs at startup:
            try:
                self.dump_group_state_to_log()
                self.audit_all_sonos_devices()
            except Exception as e:
                self.logger.debug(f"bootstrap: audit/dump skipped: {e}")

        except Exception as e:
            self.logger.error(f"❌ bootstrap_group_state_from_startup failed: {e}")





    def HTTPStreamer(self):
        try:
            HandlerClass = SimpleHTTPRequestHandler
            ServerClass = BaseHTTPServer.HTTPServer
            Protocol = "HTTP/1.0"

            if self.HTTPStreamingIP == "auto":
                try:
                    self.HTTPServer = socket.gethostbyname(socket.gethostname())
                except Exception as exception_error:
                    self.HTTPServer = None
                if self.HTTPServer is None:
                    d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    d.connect(("indigodomo.com", 80))
                    self.HTTPServer = d.getsockname()[0]
                    d.close()
            else:
                self.HTTPServer = self.HTTPStreamingIP

            server_address = ('0.0.0.0', int(self.HTTPStreamingPort))
            HandlerClass.protocol_version = Protocol
            self.httpd = ServerClass(server_address, HandlerClass)

            sa = self.httpd.socket.getsockname()
            self.logger.info(f"Serving HTTP Streamer on {self.HTTPServer} [{sa[0]}], port {sa[1]}")
            self.HTTPStreamerOn = True
            while self.HTTPStreamerOn:
                try:
                    self.httpd.handle_request()
                except Exception:
                    if not self.HTTPStreamerOn:
                        break  # intentional teardown via prefs reload
                    raise

        except Exception as exception_error:
            if self.HTTPStreamerOn:
                self.exception_handler(f"Cannot start HTTP Streamer on {self.HTTPServer}: {exception_error}", True)


    def _set_subscription_callback(self, sub, indigo_device, service_name):
        try:
            sub.callback = self.soco_event_handler
            self.soco_subs[indigo_device.id][service_name] = sub
            sid = getattr(sub, "sid", "no-sid")
            callback_name = getattr(sub.callback, "__name__", "no-callback")
            self.logger.info(f"🔔 Subscribed to {service_name} for {indigo_device.name} | SID: {sid}, Callback: {callback_name}")
        except Exception as e:
            self.logger.error(f"❌ Error in _set_subscription_callback for {indigo_device.name} [{service_name}]: {e}")


    def socoSubscribe(self, indigo_device, soco_device):
        from soco.events import event_listener

        self.safe_debug(f"🧪 socoSubscribe() ENTERED for {indigo_device.name} at {soco_device.ip_address}")

        # Confirm event listener status
        self.safe_debug(
            f"📡 SoCo Event Listener status: running={event_listener.is_running}, "
            f"address={getattr(event_listener, 'address', '?')}, "
            f"port={getattr(event_listener, 'port', '?')}"
        )

        # ✅ Use helper to get model name
        model_name = self.get_model_name(soco_device)
        self.logger.info(f"🧪 Model name for {indigo_device.name}: {model_name}")

        self.soco_subs[indigo_device.id] = {}
        self.soco_by_ip[indigo_device.address] = soco_device
        self.safe_debug(f"✅ soco_by_ip[{indigo_device.address}] stored with SoCo {soco_device.uid}")

        def _log_subscription_result(service_name, sub_obj):
            sid = getattr(sub_obj, "sid", None)
            if sid:
                self.logger.debug(f"🔒 {service_name} subscription confirmed for {indigo_device.name} | SID: {sid}")
            else:
                self.logger.error(f"❌ {service_name} subscription returned None SID for {indigo_device.name}")

        def _subscribe_with_retry(service_attr, service_name):
            try:
                # Determine suppression before subscribing
                is_coordinator = indigo_device.states.get("GROUP_Coordinator", False) in [True, "true", "True"]
                bonded_keywords = ["sub", "surround", "boost"]
                is_bonded = any(kw in model_name.lower() for kw in bonded_keywords)
                if not is_coordinator or is_bonded:
                    self.logger.debug(f"ℹ️ Skipping {service_name} subscription for {indigo_device.name} (bonded or non-coordinator)")
                    return

                self.logger.debug(f"🔔 Initiating subscription to {service_name} for {indigo_device.name}")
                sub_obj = getattr(soco_device, service_attr).subscribe(auto_renew=True, strict=True)
                _log_subscription_result(service_name, sub_obj)

                sid = getattr(sub_obj, "sid", None)
                if sid:
                    sub_obj.callback = self.soco_event_handler
                    self.soco_subs[indigo_device.id][service_name] = sub_obj
                    return

                # Retry once if SID is None
                self.logger.warning(f"🔁 Retrying {service_name} subscription for {indigo_device.name} after None SID...")
                sub_obj_retry = getattr(soco_device, service_attr).subscribe(auto_renew=True, strict=True)
                sid_retry = getattr(sub_obj_retry, "sid", None)
                if sid_retry:
                    self.logger.info(f"✅ {service_name} retry successful | SID: {sid_retry}")
                    sub_obj_retry.callback = self.soco_event_handler
                    self.soco_subs[indigo_device.id][service_name] = sub_obj_retry
                else:
                    self.logger.error(f"❌ Retry {service_name} still returned None SID for {indigo_device.name}")
            except Exception as e:
                self.logger.error(f"❌ Failed to subscribe to {service_name} for {indigo_device.name}: {e}")

        # AVTransport
        _subscribe_with_retry("avTransport", "AVTransport")

        # RenderingControl
        _subscribe_with_retry("renderingControl", "RenderingControl")

        # Optional AudioIn
        if model_name.lower().startswith("connect") or "port" in model_name.lower():
            try:
                self.logger.debug(f"🔔 Initiating subscription to AudioIn for {indigo_device.name}")
                ai_sub = soco_device.audioIn.subscribe(auto_renew=True, strict=True)
                _log_subscription_result("AudioIn", ai_sub)

                ai_sub.callback = self.soco_event_handler
                self.soco_subs[indigo_device.id]["AudioIn"] = ai_sub
                self.logger.info(f"✅ Subscribed to AudioIn | SID: {getattr(ai_sub, 'sid', 'N/A')}, Callback: {getattr(ai_sub.callback, '__name__', 'None')}")
            except Exception as e:
                self.logger.error(f"❌ Failed to subscribe to AudioIn: {e}")

        # ZoneGroupTopology
        try:
            self.logger.debug(f"🔔 Initiating subscription to ZoneGroupTopology for {indigo_device.name}")
            zgt_sub = soco_device.zoneGroupTopology.subscribe(auto_renew=True, strict=True)
            _log_subscription_result("ZoneGroupTopology", zgt_sub)

            zgt_sub.callback = self.soco_event_handler
            self.soco_subs[indigo_device.id]["ZoneGroupTopology"] = zgt_sub
            self.logger.debug(f"✅ Subscribed - Here !!!!! -  to ZoneGroupTopology | SID: {getattr(zgt_sub, 'sid', 'N/A')}, Callback: {getattr(zgt_sub.callback, '__name__', 'None')}")
        except Exception as e:
            self.logger.warning(f"⚠️ ZoneGroupTopology subscription failed for {indigo_device.name}: {e}")

        # Final Listener Check
        self.logger.debug(
            f"🛰 Listener running={event_listener.is_running}, "
            f"bound to {getattr(event_listener, 'address', '?')}:{getattr(event_listener, 'port', '?')}"
        )








    ############################################################################################
    ### Start Device communications
    ############################################################################################


    def is_host_reachable(self, ip, port=1400, timeout=2.0):
        """Quick TCP probe so offline players can't stall the dispatch thread.

        All Indigo UI callbacks (including opening config dialogs) are serviced
        on the same thread as deviceStartComm — a single unreachable player
        with a 10-20s (or unbounded) connect timeout freezes the whole plugin UI.
        """
        if not ip:
            return False
        try:
            with socket.create_connection((ip, port), timeout=timeout):
                return True
        except OSError:
            return False

    def _ip_probe_ok(self, ip, ttl=30.0, timeout=1.0):
        """Reachability check with a short negative cache (shared with the ZGT walk).

        A player that fails the probe is skipped for `ttl` seconds so hot loops
        (group evaluation, UID lookups, topology dumps) can't repeatedly hammer
        an offline player with 10-20s SoCo network timeouts — one dead device
        was enough to make Indigo log "timeout waiting for plugin response".
        """
        if not ip:
            return False
        if not hasattr(self, "_zgt_unreachable_until"):
            self._zgt_unreachable_until = {}
        now = time.time()
        if self._zgt_unreachable_until.get(ip, 0.0) > now:
            return False
        if self.is_host_reachable(ip, timeout=timeout):
            return True
        self._zgt_unreachable_until[ip] = now + ttl
        return False

    def safe_uid(self, ip, soco_dev):
        """Resolve a SoCo player's UID without repeated network timeouts.

        SoCo's .uid on a cold instance polls ZoneGroupState against the player's
        own IP — for an offline player that's a full network timeout on EVERY
        access. Resolution order: plugin cache → SoCo's own cache → the Indigo
        device's ZP_LocalUID state → (only if the host answers a 1s probe) the
        network. Returns None when unresolvable.
        """
        if not hasattr(self, "uid_by_ip"):
            self.uid_by_ip = {}
        uid = self.uid_by_ip.get(ip)
        if uid:
            return uid
        # SoCo caches _uid after any successful fetch (or when parsed from ZGT XML)
        cached = getattr(soco_dev, "_uid", None) if soco_dev is not None else None
        if cached:
            self.uid_by_ip[ip] = cached
            return cached
        # The Indigo device already knows its UID from a previous session
        idev = (getattr(self, "ip_to_indigo_device", {}) or {}).get(ip)
        if idev is not None:
            state_uid = (idev.states.get("ZP_LocalUID") or "").strip()
            if state_uid:
                self.uid_by_ip[ip] = state_uid
                return state_uid
        if soco_dev is None or not self._ip_probe_ok(ip):
            return None
        try:
            uid = soco_dev.uid
            if uid:
                self.uid_by_ip[ip] = uid
            return uid
        except Exception as e:
            self.logger.debug(f"safe_uid: could not fetch UID from {ip}: {e}")
            return None

    def retry_deferred_devices(self):
        """Retry startup for devices that were offline when deviceStartComm ran.

        Called periodically from plugin.py's runConcurrentThread.
        """
        deferred = getattr(self, "deferred_start_devices", None)
        if not deferred:
            return
        uid_to_ip = None  # lazy: at most one discovery sweep per retry pass
        for dev_id in list(deferred):
            try:
                dev = indigo.devices[dev_id]
            except KeyError:
                deferred.discard(dev_id)
                continue
            if not dev.enabled:
                deferred.discard(dev_id)
                continue
            if self.is_host_reachable(dev.address):
                self.logger.info(f"🔄 {dev.name} ({dev.address}) is reachable again — starting device.")
                deferred.discard(dev_id)
                try:
                    self.deviceStartComm(dev)
                except Exception as e:
                    self.logger.error(f"❌ Deferred deviceStartComm failed for {dev.name}: {e}")
                continue

            # Configured IP still dead — but the IP is not the player's identity
            # (forum t=28960): look for the same RINCON UID at a new address (DHCP
            # move) and heal the stored address so the device recovers without the
            # user deleting/recreating it or touching control pages.
            uid = (dev.states.get("ZP_LocalUID") or "").strip()
            if not uid:
                continue
            if uid_to_ip is None:
                uid_to_ip = self._discover_uid_to_ip()
            new_ip = uid_to_ip.get(uid, "")
            if new_ip and new_ip != dev.address:
                self.logger.info(
                    f"🩹 {dev.name} answered discovery at {new_ip} (configured {dev.address}) — "
                    f"updating device address; Indigo will restart the device.")
                try:
                    props = dev.pluginProps
                    props["address"] = new_ip
                    deferred.discard(dev_id)
                    dev.replacePluginPropsOnServer(props)
                except Exception as e:
                    self.logger.error(f"❌ Could not update address for {dev.name}: {e}")

    def _discover_uid_to_ip(self):
        """One SSDP sweep mapping live players' RINCON UIDs → current IPs.

        Used only from the deferred-retry path, throttled to one sweep per five
        minutes so a long-term-offline player doesn't keep the network busy with
        multicast discovery every 60s retry tick.
        """
        now = time.time()
        if now - getattr(self, "_last_heal_discovery", 0.0) < 300.0:
            return getattr(self, "_heal_uid_to_ip", {}) or {}
        self._last_heal_discovery = now
        mapping = {}
        try:
            found = soco.discover(timeout=5) or set()
        except Exception as e:
            self.logger.debug(f"self-heal discovery failed: {e}")
            found = set()
        for player in found:
            try:
                ip = player.ip_address
                self.soco_by_ip[ip] = player
                player_uid = self.safe_uid(ip, player)
                if player_uid:
                    mapping[player_uid] = ip
            except Exception:
                continue
        self._heal_uid_to_ip = mapping
        return mapping

    def _log_cross_vlan_firewall_advice(self):
        """Warn once at startup when Sonos players live on a different subnet.

        Announcements (tcp/8889) and album art (tcp/8888) are PULLED by the
        players from this Mac. A one-way LAN→VLAN firewall lets the plugin
        control players fine while their fetches back to us are silently
        dropped — announcements produce no audio (player stuck TRANSITIONING)
        and artwork stays blank. Uses a /24 heuristic, good enough for advice.
        """
        try:
            host = (getattr(self, "HTTPServer", "") or "").strip()
            if not host or host.count(".") != 3:
                return
            host_net = host.rsplit(".", 1)[0]
            announce_port = (getattr(self, "_announce_http_port", None)
                             or getattr(self, "HTTPStreamingPort", None) or 8889)
            other_nets = set()
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                ip = (dev.pluginProps.get("address") or dev.address or "").strip()
                if ip and ip.count(".") == 3 and ip.rsplit(".", 1)[0] != host_net:
                    other_nets.add(ip.rsplit(".", 1)[0] + ".0/24")
            if other_nets:
                nets = ", ".join(sorted(other_nets))
                self.logger.warning(
                    f"🧱 Sonos players found on {nets} — a different subnet/VLAN than this Mac ({host}). "
                    f"Announcements, album art AND event notifications all travel FROM the players TO "
                    f"this Mac, so your router/firewall must allow {nets} → {host} on "
                    f"tcp/{announce_port} (announcements), tcp/8888 (album art) and tcp/1400 "
                    f"(Sonos event notifications). Without tcp/1400 the players' state/group change "
                    f"events never arrive — subscriptions look confirmed but the plugin goes blind and "
                    f"group/playback states go stale, even though normal control keeps working.")
        except Exception as e:
            self.logger.debug(f"cross-VLAN advice check failed: {e}")

    def _restore_announcement_snapshots(self, announce_snapshots):
        """Restore group topology AND player state captured before an announcement.

        Phase 1 rebuilds the ORIGINAL grouping (soco Snapshot alone never does
        this — HA does it in its own speaker layer): zones that were slaves
        re-join their old coordinator, zones that were standalone leave the
        temporary announcement group. Phase 2 restores the soco Snapshots —
        full transport (URI/queue/position, resumes if it was playing) for
        original coordinators/standalone players, volume/mute for original
        slaves (their audio follows their re-joined coordinator).
        """
        # Phase 1 — rebuild original grouping.
        # Iterate REVERSED so temp-group members leave before the temp
        # coordinator (announce_snapshots is in AnnouncementZones order, GM
        # first). Do NOT consult soco's is_coordinator here: its cached topology
        # can lag the announcement regrouping and skip the unjoin entirely —
        # seen live: zones stayed grouped, then Phase 2 got UPnP 701 trying to
        # pause a still-slaved player. We put these zones into the temp group,
        # so unconditionally take them out; unjoin on an already-standalone
        # player is a harmless no-op.
        for _dev, snap, _soco, orig_coord, orig_members in reversed(announce_snapshots):
            try:
                if orig_coord is not None:
                    _soco.join(orig_coord)
                    self.logger.debug(
                        f"[ANNOUNCE SNAP] {_dev.name} re-joined its original group "
                        f"(coordinator {getattr(orig_coord, 'player_name', '?')})")
                else:
                    _soco.unjoin()
                    self.logger.debug(f"[ANNOUNCE SNAP] {_dev.name} standalone again (as before announcement)")
            except Exception as e:
                self.logger.warning(f"[ANNOUNCE SNAP] regroup failed for {_dev.name}: {e}")

        # Phase 1.5 — merge back ORIGINAL group members that were outside the
        # announcement: when their coordinator was pulled into the temp group,
        # Sonos re-formed them under an elected coordinator; re-join them so
        # the original group comes back exactly as it was.
        for _dev, snap, _soco, orig_coord, orig_members in announce_snapshots:
            for m in (orig_members or []):
                try:
                    m.join(_soco)
                    self.logger.debug(
                        f"[ANNOUNCE SNAP] {getattr(m, 'player_name', '?')} re-joined "
                        f"{_dev.name}'s restored group")
                except Exception as e:
                    self.logger.warning(
                        f"[ANNOUNCE SNAP] could not re-join {getattr(m, 'player_name', '?')} "
                        f"to {_dev.name}: {e}")

        # Let the topology settle before touching transports
        try:
            self.plugin.sleep(1.0)
        except Exception:
            time.sleep(1.0)

        # Phase 2 — player state; original coordinators/standalone first so their
        # streams are re-established before slave volume restores.
        ordered = sorted(announce_snapshots, key=lambda t: t[3] is not None)
        for _dev, snap, _soco, orig_coord, orig_members in ordered:
            try:
                snap.restore(fade=False)
                self.logger.debug(f"[ANNOUNCE SNAP] restored {_dev.name}")
            except Exception as e:
                self.logger.warning(f"[ANNOUNCE SNAP] restore failed for {_dev.name}: {e}")

        # Phase 3 — resync plugin group caches from LIVE topology. The temp
        # announcement group primed zone_group_state_cache and
        # evaluated_group_members_by_coordinator (addPlayerToZone snap-priming),
        # and soco's own group view can be frozen when event NOTIFYs can't reach
        # us (one-way VLAN firewall) — without a forced live /status/zp refresh
        # those ghosts keep resurrecting "grouped" device states after the
        # players are actually standalone again.
        try:
            self._last_topology_refresh = 0.0  # beat the 3s debounce
            self.evaluated_group_members_by_coordinator = {}
            self.refresh_group_topology_after_plugin_zone_change()
            self.logger.debug("[ANNOUNCE SNAP] post-restore live topology resync complete")
        except Exception as e:
            self.logger.debug(f"[ANNOUNCE SNAP] post-restore topology resync failed: {e}")

    def deviceStartComm(self, indigo_device):
        #self.logger.debug(f"🧪 deviceStartComm CALLED for {indigo_device.name}")

        try:
            self.logger.debug(f"🔌 Starting communication with Indigo device {indigo_device.name} ({indigo_device.address})")
            self.devices[indigo_device.id] = indigo_device

            # Ensure lookup maps exist
            if not hasattr(self, "soco_by_ip"):
                self.soco_by_ip = {}
            if not hasattr(self, "ip_to_indigo_device"):
                self.ip_to_indigo_device = {}
            if not hasattr(self, "uuid_to_indigo_device"):
                self.uuid_to_indigo_device = {}
            # --- NEW: ensure alternate SoCo map exists for helper consistency
            if not hasattr(self, "ip_to_soco_device"):
                self.ip_to_soco_device = {}

            # ✅ Ensure essential states exist before proceeding (resyncs state list from Devices.xml if needed)
            indigo_device = self.initialize_custom_states(indigo_device) or indigo_device
            self.devices[indigo_device.id] = indigo_device

            # 🚦 Fast reachability gate — an offline player must not stall the dispatch
            # thread (it also services all config dialogs) with long connect timeouts.
            if not hasattr(self, "deferred_start_devices"):
                self.deferred_start_devices = set()
            if not self.is_host_reachable(indigo_device.address):
                self.logger.warning(
                    f"📴 {indigo_device.name} ({indigo_device.address}) is unreachable — "
                    f"deferring startup for this device; will retry in background.")
                indigo_device.setErrorStateOnServer("offline")
                self.deferred_start_devices.add(indigo_device.id)
                return
            self.deferred_start_devices.discard(indigo_device.id)
            indigo_device.setErrorStateOnServer(None)  # clear any previous 'offline' flag

            # 🖼️ Preload ZP_ART with default placeholder if missing
            if not indigo_device.states.get("ZP_ART"):
                self.logger.debug(f"🖼️ Preloading ZP_ART with default placeholder for {indigo_device.name}")
                self.logger.debug(f"🖼️ Updated artwork 7")
                indigo_device.updateStateOnServer("ZP_ART", "/images/no_album_art.png")

            # Force plugin to use upgraded SoCo library
            import sys, os
            upgraded_path = os.path.join(os.path.dirname(__file__), "soco-upgraded")
            if upgraded_path not in sys.path:
                sys.path.insert(0, upgraded_path)

            import soco
            from soco import SoCo
            from soco.discovery import discover

            self.logger.debug(f"🧪 SoCo loaded from: {getattr(soco, '__file__', 'unknown')}")
            self.logger.debug(f"🧪 SoCo version: {getattr(soco, '__version__', 'unknown')}")

            # ♻️ Reuse the SoCo instance from startup discovery when available; otherwise
            # talk to the (known-reachable) player directly. The previous per-device
            # network discovery sweeps (2 × 5s each) only stalled the dispatch thread —
            # matching the discovery result by IP is equivalent to SoCo(ip) directly.
            soco_device = self.soco_by_ip.get(indigo_device.address)
            if soco_device is None:
                try:
                    soco_device = SoCo(indigo_device.address)
                    self.logger.debug(f"✅ Created SoCo for {indigo_device.name} at {indigo_device.address}")
                except Exception as e:
                    self.logger.error(f"❌ Direct SoCo init failed for {indigo_device.name}: {e}")
                    indigo_device.setErrorStateOnServer("error")
                    return

            # ✅ Always store in lookup maps
            self.soco_by_ip[indigo_device.address] = soco_device
            self.ip_to_indigo_device[indigo_device.address] = indigo_device
            # --- NEW: also store in the map used elsewhere in the helper paths
            self.ip_to_soco_device[indigo_device.address] = soco_device

            self.safe_debug(f"✅ soco_by_ip[{indigo_device.address}] stored with SoCo {getattr(soco_device, 'uid', 'unknown')}")

            # 🆔 Update ZP_LocalUID from SoCo
            try:
                zp_uid = soco_device.uid
                indigo_device.updateStateOnServer("ZP_LocalUID", value=zp_uid)
                self.logger.debug(f"🆔 Set ZP_LocalUID for {indigo_device.name}: {zp_uid}")
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to set ZP_LocalUID for {indigo_device.name}: {e}")

            # 🧠 ✅ Patch: ensure UUID maps back to Indigo device
            try:
                zp_uid = soco_device.uid
                if zp_uid:
                    self.logger.debug(f"🔁 Mapping UUID {zp_uid} to Indigo device: {indigo_device.name}")
                    self.uuid_to_indigo_device[zp_uid] = indigo_device
            except Exception as e:
                self.logger.error(f"❌ Failed to bind UUID to Indigo device in deviceStartComm: {e}")

            # 🧪 Log model name
            model_name = self.get_model_name(soco_device)
            self.logger.debug(f"🧪 Retrieved model_name for {indigo_device.name}: {model_name}")
            indigo_device.updateStateOnServer("ModelName", model_name)

            # --- NEW: immediate seed from live SoCo for this device (esp. for coordinators)
            try:
                if hasattr(self, "_soco_group_truth") and hasattr(self, "_set_group_states"):
                    is_coord, is_grouped, gname = self._soco_group_truth(soco_device)
                    self.logger.debug(f"[coord-seed] {indigo_device.name} ip={indigo_device.address} "
                                      f"live(coord={is_coord}, grouped={is_grouped}, name='{gname}')")
                    # Always perform a local seed write; group propagation happens later via helper
                    seed_name = gname or indigo_device.states.get("GROUP_Name", "").strip() or indigo_device.name
                    self._set_group_states(indigo_device, grouped=bool(is_grouped), is_coord=bool(is_coord), group_name=seed_name)

                    # --- NEW: startup-state probe after seed
                    self.logger.debug(
                        f"[startup-state] {indigo_device.name}: "
                        f"Grouped={indigo_device.states.get('Grouped')} "
                        f"GROUP_Coordinator={indigo_device.states.get('GROUP_Coordinator')} "
                        f"GROUP_Name='{indigo_device.states.get('GROUP_Name','')}'"
                    )

                    # --- NEW: if this device is coordinator, nudge artwork propagation early
                    if is_coord:
                        try:
                            self.propagate_artwork_to_slaves(indigo_device)
                        except Exception as _e:
                            self.logger.debug(f"⚠️ early propagate_artwork_to_slaves failed for {indigo_device.name}: {_e}")
            except Exception as e:
                self.logger.warning(f"⚠️ coord-seed failed for {indigo_device.name}: {e}")

            # 🚀 Start event listener if needed
            if not getattr(self, "event_listener_started", False):
                try:
                    from soco.events import event_listener
                    self.logger.info("🚀 Starting SoCo Event Listener...")
                    soco.config.EVENT_LISTENER_IP = self.find_sonos_interface_ip()
                    event_listener.start(any_zone=soco_device)
                    self.event_listener_started = True
                    self.logger.debug(f"✅ SoCo Event Listener running: {event_listener.is_running}")
                except Exception as e:
                    self.logger.error(f"❌ Failed to start SoCo Event Listener: {e}")

            # 🔔 Subscribe and update group state
            try:
                self.socoSubscribe(indigo_device, soco_device)
                self.updateZoneGroupStates(indigo_device)
            except Exception as e:
                self.logger.error(f"❌ socoSubscribe() or updateZoneGroupStates() failed for {indigo_device.name}: {e}")

            #self.initZones(indigo_device)
            self.initZones(indigo_device, soco_device)
            self.logger.debug(f"During start up - lets evaluate_and_update current grouped states - yes ????")
            self.refresh_group_topology_after_plugin_zone_change()
            #self.evaluate_and_update_grouped_states()

            for dev in indigo.devices.iter("self"):
                ip = dev.address
                if ip:
                    try:
                        soco_inst = SoCo(ip)
                        # keep both maps in sync
                        self.ip_to_soco_device[ip] = soco_inst
                        self.soco_by_ip[ip] = soco_inst
                    except Exception as e:
                        self.logger.warning(f"Failed to initialize SoCo for {ip}: {e}")

            # --- NEW: one safe post-discovery sweep when inputs are ready
            try:
                if hasattr(self, "_ready_for_group_refresh") and self._ready_for_group_refresh():
                    self.logger.debug("[post-discovery] inputs ready → running _refresh_all_group_states_helper('post-discovery')")
                    self._refresh_all_group_states_helper(reason="post-discovery")
                else:
                    groups_ct = len(getattr(self, "zone_group_state_cache", {}) or {})
                    ip2dev_ct = len(getattr(self, "ip_to_indigo_device", {}) or {})
                    soco_ct   = len(getattr(self, "ip_to_soco_device", {}) or {})
                    self.logger.debug(f"[post-discovery] not ready; groups={groups_ct} ip→dev={ip2dev_ct} soco_by_ip={soco_ct}")
            except Exception as e:
                self.logger.warning(f"⚠️ post-discovery refresh failed: {e}")

            # … Run a single shot of dump_groups_to_log once fter deviceStartComm for all devices completes (or a short timer)
            self._startup_warmup = False

            # Debounced, one-shot dump once everything settles
            self._schedule_one_shot_dump_groups(delay=8.0)

        except Exception as e:
            self.logger.error(f"✅ Error in deviceStartComm for {indigo_device.name}: {e}")









    ############################################################################################
    ### End of General Methods that can be called in the SonosPlugin Class
    ############################################################################################








    ######################################################################################
    # UI Validation
    def validatePrefsConfigUi(self, valuesDict):
        try:
            self.safe_debug("Validating Plugin Configuration")
            errorsDict = indigo.Dict()
            if valuesDict["rootZPIP"] == "":
                errorsDict["rootZPIP"] = "Please enter a reference ZonePlayer IP Address."
            if valuesDict["EventProcessor"] == "":
                errorsDict["EventProcessor"] = "Please select an Event Processsor."
            if valuesDict["EventIP"] == "":
                errorsDict["EventIP"] = "Please select an Event Listener IP Address."
            if valuesDict["EventCheck"] == "":
                errorsDict["EventCheck"] = "Please select an Event Check Interval."
            if valuesDict["SubscriptionCheck"] == "":
                errorsDict["SubscriptionCheck"] = "Please select an Subscription Check Interval."
            if valuesDict["HTTPStreamingIP"] == "":
                errorsDict["rootZPIP"] = "Please enter an HTTP Streaming IP Address."
            if valuesDict["HTTPStreamingPort"] == "":
                errorsDict["rootZPIP"] = "Please enter an HTTP Streaming Port."
            if valuesDict["Pandora"] == "True":
                if valuesDict["PandoraEmailAddress"] == "":
                    errorsDict["PandoraEmailAddress"] = "Please enter a Pandora Email Address."
                if valuesDict["PandoraPassword"] == "":
                    errorsDict["PandoraPassword"] = "Please enter a Pandora Password."
            if valuesDict["SiriusXM"] == "True":
                if valuesDict["SiriusXMID"] == "":
                    errorsDict["SiriusXMID"] = "Please enter a SiriusXM ID."
                if valuesDict["SiriusXMPassword"] == "":
                    errorsDict["SiriusXMPassword"] = "Please enter a SiriusXM Password."
            if valuesDict["IVONA"] == "True":
                if valuesDict["IVONAaccessKey"] == "":
                    errorsDict["IVONAaccessKey"] = "Please enter an IVONA Access Key."
                if valuesDict["IVONAsecretKey"] == "":
                    errorsDict["IVONAsecretKey"] = "Please enter an IVONA Secret Key."
            if valuesDict["Polly"] == "True":
                if valuesDict["PollyaccessKey"] == "":
                    errorsDict["PollyaccessKey"] = "Please enter a Polly Access Key."
                if valuesDict["PollysecretKey"] == "":
                    errorsDict["PollysecretKey"] = "Please enter a Polly Secret Key."
            if valuesDict["MSTranslate"] == "True":
                if valuesDict["MSTranslateClientID"] == "":
                    errorsDict["MSTranslateClientID"] = "Please enter a Microsoft Translate Client ID."
                if valuesDict["MSTranslateClientSecret"] == "":
                    errorsDict["MSTranslateClientSecret"] = "Please enter an Microsoft Translate Client Secret."

            if len(errorsDict) > 0:
                self.logger.error("\t Validation Errors")
                return False, valuesDict, errorsDict
            else:
                self.safe_debug("\t Validation Succesful")
                return True, valuesDict

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    ######################################################################################



    def _usable_host(self, h: str) -> bool:
        try:
            if not h:
                return False
            h = h.strip()
            if h in ("localhost", "0.0.0.0", "::1"):
                return False
            if h.startswith("127."):
                return False
            return True
        except Exception:
            return False


    def choose_publish_host(self, zone_ip: str | None = None) -> str | None:
        """
        Returns a LAN-reachable host/IP to publish in the announcement URI.
        Tries (in order):
          1) self.HTTPServer (if safe)
          2) self.selectedInterfaceIP (if safe)
          3) Interface on the same /24 as the target zone_ip (if provided)
          4) self.announce_bind_ip (if safe)
        """
        # Preferred explicit setting
        cand = (getattr(self, "HTTPServer", "") or "").strip()
        if self._usable_host(cand):
            return cand

        # Indigo-selected interface
        cand = (getattr(self, "selectedInterfaceIP", "") or "").strip()
        if self._usable_host(cand):
            return cand

        # Try to match the zone's /24 (very effective in mixed-interface hosts)
        if zone_ip:
            try:
                import ipaddress
                net = ipaddress.ip_network(zone_ip.rsplit(".", 1)[0] + ".0/24", strict=False)
                ip_on_subnet = self.find_sonos_interface_ip(str(net))
                if self._usable_host(ip_on_subnet):
                    return ip_on_subnet
            except Exception:
                pass

        # Last resort: whatever we recorded from the 8889 server bind
        cand = (getattr(self, "announce_bind_ip", "") or "").strip()
        if self._usable_host(cand):
            return cand

        return None





    def find_sonos_interface_ip(self, target_subnet=None):
        """
        Attempts to locate the first local interface IP that belongs to the
        target Sonos subnet. Uses `ifaddr` to enumerate adapters.

        Args:
            target_subnet (str): Optional subnet in CIDR notation.  
                                 Falls back to self.targetSonosSubnet or 192.168.80.0/24.

        Returns:
            str or None: The matching IPv4 address as a string, or None if not found.
        """
        try:
            import ipaddress, ifaddr

            # Decide which subnet to use
            subnet_to_use = target_subnet or getattr(self, "targetSonosSubnet", None) or "192.168.80.0/24"
            try:
                target_net = ipaddress.IPv4Network(subnet_to_use, strict=False)
            except Exception as e:
                self.logger.error(f"❌ Invalid subnet format '{subnet_to_use}': {e}")
                return None

            self.logger.info(f"🔍 Searching for interface IP on subnet {target_net}...")

            found_ip = None
            adapters = ifaddr.get_adapters()
            for adapter in adapters:
                for ip_obj in adapter.ips:
                    ip = ip_obj.ip
                    # Skip IPv6 or tuple addresses
                    if isinstance(ip, (list, tuple)):
                        continue
                    try:
                        ip_addr = ipaddress.IPv4Address(ip)
                    except ipaddress.AddressValueError:
                        continue

                    self.logger.debug(f"   🧪 Interface {adapter.nice_name} → IP {ip_addr}")
                    if ip_addr in target_net:
                        self.logger.info(f"   ✅ Selected interface '{adapter.nice_name}' with IP {ip_addr} (matches target subnet)")
                        found_ip = str(ip_addr)
                        return found_ip  # Return immediately on first match

            # 🔀 Routed-subnet fallback: no local interface sits directly on the Sonos
            # subnet (e.g. players on 192.168.30.0/24, this Mac on 192.168.1.0/24 with a
            # router in between). The players are still reachable — ask the OS which
            # source IP it would use to route to one and publish that instead.
            probe_ip = None
            for candidate_ip in list(getattr(self, "soco_by_ip", {}) or {}):
                probe_ip = candidate_ip
                break
            if probe_ip is None:
                try:
                    for idev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                        if idev.address:
                            probe_ip = idev.address
                            break
                except Exception:
                    pass
            if probe_ip is None:
                root_ip = getattr(self, "rootZPIP", None)
                if root_ip and root_ip != "auto":
                    probe_ip = root_ip
            if probe_ip is None:
                try:
                    probe_ip = str(next(target_net.hosts()))  # first host of the target subnet
                except Exception:
                    probe_ip = None

            if probe_ip:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                        s.connect((probe_ip, 1400))  # no packet sent — just resolves routing
                        found_ip = s.getsockname()[0]
                    self.logger.info(
                        f"   ✅ No interface directly on {target_net}; Sonos subnet appears routed — "
                        f"using source IP {found_ip} (via route to {probe_ip})")
                    return found_ip
                except Exception as e:
                    self.logger.debug(f"Routed-IP fallback via {probe_ip} failed: {e}")

            self.logger.warning(f"❌ No interface found on target Sonos subnet {target_net} (and no routed fallback available)")
            return None

        except Exception as e:
            self.logger.exception(f"❌ Exception in find_sonos_interface_ip: {e}")
            return None



            



#############################################################################################################################################################################################################
### Event Handler to process player controls and soco state changes and maintain current dynamic state updates
#############################################################################################################################################################################################################
    def soco_event_handler(self, event_obj):

        ## The first try block here can set variables and or log various things that need to be defined or checked ahead of the event processing loop
        try:
            soco_ip = getattr(getattr(event_obj, "soco", None), "ip_address", "(no soco)")
            soco_ref = getattr(event_obj, "soco", None)
            zone_ip = getattr(soco_ref, "ip_address", None)
            #self.logger.warning("📥 Raw Event Object Received:")
            #self.logger.warning(f"   ⤷ service: {getattr(event_obj.service, 'service_type', '?')}")
            #self.logger.warning(f"   ⤷ sid: {getattr(event_obj, 'sid', '?')}")
            #self.logger.warning(f"   ⤷ soco.ip: {soco_ip}")
            #self.logger.warning(f"   ⤷ variables: {event_obj.variables}")
            service_type = getattr(event_obj.service, "service_type", "").lower()
            # 👇 keep a lowercased copy ONLY for string checks; DO NOT use it for lookups
            sid_lc = (getattr(event_obj, "sid", "") or "").lower()
            sid_orig = getattr(event_obj, "sid", "")  # preserve original casing for mapping later
            zone_ip = getattr(getattr(event_obj, "soco", None), "ip_address", None)
        except Exception as log_err:
            self.logger.error(f"❌ Failed to log raw event object: {log_err}")



    #        # the following is a dectection and log event only to see if we can isolate
    #        if not zone_ip:
    #            self.logger.info(f"🔎 ZGT event with no source IP — likely a Sonos response to a command or an unsolicted subscription song change, subscription renewal or other Sonos system or app event.")
    #            #return
    #        else:
    #            self.logger.info(f"🔎 New check - ZoneGroupTopology event triggered by {zone_ip}")

        ######################################################################################################################################################################################################
        ### Zone Group Topology (ZGT) processing
        ######################################################################################################################################################################################################
        # Normalize a few things safely so we don't blow up on startup/discovery events
        service_type_lc = (str(service_type) if service_type is not None else "").lower()
        sid_lc = (str(getattr(event_obj, "sid", "")) or "").lower()
        vars_dict = getattr(event_obj, "variables", {}) or {}

        is_zgt_event = (
            "zonegrouptopology" in service_type_lc or
            "zonegrouptopology" in sid_lc or
            "zone_group_state" in vars_dict or
            "ZoneGroupState" in vars_dict
        )

        if is_zgt_event:
        #            self.logger.info(f"🔎 This is from - (if is_zgt_event) - logic - ZoneGroupTopology event from {zone_ip} missing ZoneGroupState")
        #            self.logger.info(f"🧪 9999 zgt event detected entering the event logic now...")
        #            self.logger.info(f"🔎 ZoneGroupTopology event triggered by {zone_ip}")
            zone_state_xml = (
                vars_dict.get("zone_group_state") or
                vars_dict.get("ZoneGroupState") or
                ""
            )

            if not zone_state_xml:
                self.logger.debug(f"🔎 This is from - (if not zone_state_xml) - logic - ZoneGroupTopology event from {zone_ip} missing ZoneGroupState")
            else:
                # Ensure XML is string, not bytes
                if isinstance(zone_state_xml, bytes):
                    try:
                        zone_state_xml = zone_state_xml.decode("utf-8", errors="replace")
                        self.logger.debug("🔧 zone_state_xml was bytes, decoded to UTF-8.")
                    except Exception as decode_err:
                        self.logger.error(f"❌ Failed to decode zone_group_state XML bytes: {decode_err}")
                        return

                try:
                    self.logger.debug(f"🧪 zgt event was detected entering the phase 2 try event logic now...")
                    parsed_groups = self.parse_zone_group_state(zone_state_xml)
                    if not parsed_groups:
                        self.logger.warning("⚠️ Parsed zone group data was empty.")
                    else:
                        #self.logger.warning(f"🧪 Parsed {len(parsed_groups)} group(s) from XML. Evaluating cache...")

                        def _normalized_group_snapshot(group_dict):
                            return json.dumps(group_dict, sort_keys=True)

                        incoming_snapshot = _normalized_group_snapshot(parsed_groups)
                        with self.zone_group_state_lock:
                            current_snapshot = _normalized_group_snapshot(self.zone_group_state_cache)

                            if incoming_snapshot == current_snapshot:
                                self.logger.debug("⏩ No group topology change detected — skipping re-evaluation.")
                                return

                            self.zone_group_state_cache = copy.deepcopy(parsed_groups)
                            self.logger.debug(f"💾 zone_group_state_cache updated 1 with {len(parsed_groups)} group(s)")

                        for group_id, data in parsed_groups.items():
                            for m in data["members"]:
                                bonded_flag = " (Bonded)" if m["bonded"] else ""
                                coord_flag = " (Coordinator)" if m["coordinator"] else ""
                                # self.logger.warning(f"   → {m['name']} @ {m['ip']}{bonded_flag}{coord_flag}")

                        #self.logger.info("📣 Calling evaluate_and_update_grouped_states() after ZoneGroupTopology change...")
                        self.refresh_group_topology_after_plugin_zone_change()
                        #self.evaluate_and_update_grouped_states()

                        self.logger.debug("📣 Propagating updated Grouped states to all devices...")
                        for dev in indigo.devices.iter("self"):
                            self.updateZoneGroupStates(dev)

                        # ─────────────────────────────────────────────────────────────
                        # ✅ After states are fresh, trigger artwork propagation
                        #    & drift check only once topology/states are bootstrapped.
                        #    Drift is computed using NON-BONDED members only.
                        # ─────────────────────────────────────────────────────────────
                        try:
                            # Ensure flag exists; only run the hook after we finished a full state push
                            if not hasattr(self, "_topology_bootstrapped"):
                                self._topology_bootstrapped = False

                            # ✅ Now that we've pushed the Grouped states, mark as bootstrapped
                            was_bootstrapped = self._topology_bootstrapped
                            self._topology_bootstrapped = True

                            # Run the artwork/drift pass; if this is the very first ever ZGT, it still runs now
                            coord_ip_map = getattr(self, "_eval_coord_dev_by_ip", {}) or {}
                            for coord_ip, coord_dev in coord_ip_map.items():
                                if not coord_dev:
                                    continue

                                # 🔄 Re-fetch to avoid stale reads
                                try:
                                    coord_dev_ref = indigo.devices[coord_dev.id]
                                except Exception:
                                    coord_dev_ref = coord_dev

                                grouped_flag = coord_dev_ref.states.get("Grouped", "false")

                                # Build SoCo member lists
                                soco = self.soco_by_ip.get(coord_ip)
                                all_member_ips, bonded_member_ips = [], []
                                try:
                                    if soco and getattr(soco, "group", None):
                                        for m in (soco.group.members or []):
                                            ip = (getattr(m, "ip_address", "") or "").strip()
                                            name_lc = (getattr(m, "player_name", "") or "").lower()
                                            if not ip:
                                                continue
                                            all_member_ips.append(ip)
                                            if ("sub" in name_lc or "left" in name_lc or "right" in name_lc or "surround" in name_lc):
                                                bonded_member_ips.append(ip)
                                except Exception:
                                    pass

                                non_bonded_ips = [ip for ip in all_member_ips if ip not in bonded_member_ips]
                                non_bonded_count = len(non_bonded_ips)

                                # 🧭 Completeness guard — if any non-bonded member lacks an Indigo device, don’t warn yet
                                unresolved = [ip for ip in non_bonded_ips if not self.ip_to_indigo_device.get(ip)]
                                if unresolved:
                                    self.logger.debug(
                                        f"⏳ Suppressing drift check for {coord_ip}: unresolved non-bonded members {unresolved}"
                                    )
                                    continue

                                if grouped_flag == "true":
                                    # Coordinator-centered propagation (no event object)
                                    try:
                                        self.update_album_artwork(event_obj=None, dev=coord_dev_ref, zone_ip=coord_ip)
                                    except Exception as art_err:
                                        self.logger.warning(f"⚠️ Artwork propagation skipped for {coord_dev_ref.name} ({coord_ip}): {art_err}")
#                               else:
#                                    # 🚫 Only warn when there is actual grouping beyond bonded members
#                                    if non_bonded_count < 2:
#                                        self.logger.info(
#                                            "⚠️ Grouped state drift detected 1 ZGT — This is ok during initialization - "
#                                            f"Indigo.Grouped={grouped_flag}, SoCo.non_bonded_members>1=True, "
#                                            f"coord_ip={coord_ip}, all_members={all_member_ips}, bonded={bonded_member_ips}"
#                                        )
                        except Exception as hook_err:
                            self.logger.debug(f"⚠️ Failed to invoke artwork propagation after ZGT: {hook_err}")

                        self.logger.debug("📣 DT added for testing - Propagating updated Grouped states to all devices...")
                        #self._bootstrap_now_from_zgt()
                        #self.evaluate_and_update_grouped_states()

                except Exception as e:
                    self.logger.error(f"❌ Failed to parse ZoneGroupState XML: {e}")
        #            self.logger.info(f"🧪 zgt event detected EXITING the event logic now...")




        try:
            service_type = getattr(event_obj.service, "service_type", "UNKNOWN")
            # 👇 keep the original SID here (no .lower()) so mapping by SID works
            sid = getattr(event_obj, "sid", "N/A")
            zone_ip = getattr(event_obj, "zone_ip", None)

            #self.logger.warning(f"📥 RAW EVENT RECEIVED — service: {service_type} | sid: {sid}")

            if not zone_ip and hasattr(event_obj, "soco"):
                zone_ip = getattr(event_obj.soco, "ip_address", None)

            indigo_device = None
            dev_id = None

            for dev_lookup_id, subs in self.soco_subs.items():
                if any(sub.sid == sid for sub in subs.values()):
                    indigo_device = indigo.devices[int(dev_lookup_id)]
                    dev_id = indigo_device.id
                    if not zone_ip:
                        zone_ip = indigo_device.address
                    break

            if not indigo_device:
                self.logger.debug(f"⚠️ Event received with unknown SID {sid}. Cannot map to Indigo device.")
                return

            #self.logger.debug(f"📡 Event received from {zone_ip} — SID={sid} | Service={service_type}")
            #self.logger.debug(f"📦 Event variables: {getattr(event_obj, 'variables', {})}")

            # 👇 Only treat GroupStateChanged as a ZGT hint; do NOT return here so other services still process.
            vars_dict = getattr(event_obj, "variables", {}) or {}
            if ("GroupStateChanged" in vars_dict or "groupstatechanged" in vars_dict) and "ZoneGroupTopology" in service_type:
                self.logger.info("🔄 GroupStateChanged (ZGT) present — triggering group state refresh (no early return)…")
                # optional: self.refresh_group_topology_after_plugin_zone_change()
                # fall through to allow transport/rendering updates to be handled

            if not zone_ip:
                zone_ip = "unknown"

            state_updates = {}

            self.safe_debug(f"🧪 Event handler fired! SID={getattr(event_obj, 'sid', 'N/A')} zone_ip={zone_ip} Type={type(event_obj)}")
            self.safe_debug(f"🧑‍💻 Full event variables: {getattr(event_obj, 'variables', {})}")


        ######################################################################################################################################################################################################
        ### Transport State processing
        ######################################################################################################################################################################################################

            def safe_call(val):
                try:
                    return val() if callable(val) else val
                except Exception:
                    return ""


            if "transport_state" in event_obj.variables:
                transport_state = event_obj.variables["transport_state"]
                transport_state_upper = transport_state.upper()
                state_updates["ZP_STATE"] = transport_state_upper
                indigo_device.updateStateOnServer(key="State", value=transport_state_upper)
                indigo_device.updateStateOnServer(key="ZP_STATE", value=transport_state_upper)
                self.logger.debug(f"🔄 Updated State and ZP_STATE from event: {transport_state_upper}")

            if not hasattr(self, "last_siriusxm_track_by_dev"):
                self.last_siriusxm_track_by_dev = {}
            if not hasattr(self, "last_siriusxm_artist_by_dev"):
                self.last_siriusxm_artist_by_dev = {}


            current_uri = (
                event_obj.variables.get("current_track_uri") or
                event_obj.variables.get("enqueued_transport_uri") or
                event_obj.variables.get("av_transport_uri")
            )

            uri_priority = [
                ("enqueued_transport_uri", event_obj.variables.get("enqueued_transport_uri", "")),
                ("av_transport_uri", event_obj.variables.get("av_transport_uri", "")),
                ("current_track_uri", event_obj.variables.get("current_track_uri", ""))
            ]

            if "volume" in event_obj.variables:
                vol = event_obj.variables["volume"]
                state_updates["ZP_VOLUME_MASTER"] = int(vol.get("Master", 0))
                state_updates["ZP_VOLUME_LF"] = int(vol.get("LF", 0))
                state_updates["ZP_VOLUME_RF"] = int(vol.get("RF", 0))
                state_updates["ZP_VOLUME"] = str(vol)

            if "mute" in event_obj.variables:
                mute_val = event_obj.variables["mute"]
                mute_state = mute_val.get("Master") if isinstance(mute_val, dict) else mute_val
                state_updates["ZP_MUTE"] = "true" if str(mute_state).strip() == "1" else "false"

            if "bass" in event_obj.variables:
                try:
                    state_updates["ZP_BASS"] = int(event_obj.variables["bass"])
                except Exception as e:
                    self.logger.warning(f"⚠️ Invalid bass value: {event_obj.variables['bass']} — {e}")

            if "treble" in event_obj.variables:
                try:
                    state_updates["ZP_TREBLE"] = int(event_obj.variables["treble"])
                except Exception as e:
                    self.logger.warning(f"⚠️ Invalid treble value: {event_obj.variables['treble']} — {e}")

            if state_updates:
                for k, v in state_updates.items():
                    self.safe_debug(f"🔄 Lightweight update → {k}: {v}")
                    indigo_device.updateStateOnServer(key=k, value=v)


        ######################################################################################################################################################################################################
        ### Refresh Group Membership - only if there are any_grouped = any
        ######################################################################################################################################################################################################


            try:
                any_grouped = any(
                    str(dev.states.get("Grouped", "")).lower() == "true"
                    for dev in indigo.devices.iter("self")
                    if dev.enabled
                )
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to evaluate 'Grouped' status across devices: {e}")
                any_grouped = False

            if any_grouped:
                soco_device = self.getSoCoDeviceByIP(indigo_device.address)
                if soco_device:
                    self.refresh_group_membership(indigo_device, soco_device)
                    #self.logger.info(f"🔁 Active group detected — forcing master/slave state updates for {indigo_device.name}")      
                    self.refresh_group_topology_after_plugin_zone_change()
                    #self.evaluate_and_update_grouped_states()
                else:
                    self.logger.warning(f"⚠️ Could not refresh group membership: No SoCo device for {indigo_device.name}")
            else:
                self.logger.debug("⏩ No active groups (Grouped=true) detected — skipping group refresh/state sync")



        ######################################################################################################################################################################################################
        ### Customized State Processing for things like SiriusXM, Pandora, Sonos, Apple, Etc.
        ######################################################################################################################################################################################################


            # Initialize helpers and flags early
            is_siriusxm = False
            is_pandora = False
            is_apple_music = False
            is_sonos_radio = False
            is_sonos = False
            detected_source = "Sonos"  # default fallback

            for name, uri in uri_priority:
                if "x-sonosapi-hls:channel-linear" in uri:
                    detected_source = "SiriusXM"
                    is_siriusxm = True
                    break
                elif "x-sonosapi-radio" in uri or "VC1%3a%3aST%3a%3aST%3a" in uri:
                    detected_source = "Pandora"
                    is_pandora = True
                    break
                elif "x-apple-music" in uri:
                    detected_source = "Apple Music"
                    is_apple_music = True
                    break
                elif "x-sonosapi-stream" in uri:
                    detected_source = "Sonos Radio"
                    is_sonos_radio = True
                    break
                elif "x-sonos-http:librarytrack" in uri:
                    detected_source = "Sonos"
                    is_apple_music = True
                    break

            if detected_source == "Sonos":
                is_sonos = True

            self.safe_debug(f"✅ Detected source: {detected_source}")
            state_updates["ZP_SOURCE"] = detected_source

            # === SiriusXM handling ===
            if is_siriusxm:
                meta = event_obj.variables.get("enqueued_transport_uri_meta_data") or event_obj.variables.get("av_transport_uri_meta_data")
                if meta:
                    try:
                        title_raw = safe_call(getattr(meta, "title", ""))
                        self.safe_debug(f"🔍 Raw SiriusXM title string: '{title_raw}'")

                        ch_part, name_part = "", ""
                        if " - " in title_raw:
                            ch_part, name_part = title_raw.split(" - ", 1)
                            ch_part = ch_part.strip()
                            name_part = name_part.strip()
                        else:
                            ch_part = title_raw.strip()
                            name_part = ""

                        state_updates["ZP_TRACK"] = ch_part or "Unknown Channel"
                        state_updates["ZP_STATION"] = ch_part or "Unknown Station"
                        state_updates["ZP_ARTIST"] = name_part or "Unknown Artist"
                        state_updates["ZP_ALBUM"] = ""

                        self.safe_debug(f"🎶 SiriusXM parsed → TRACK: '{state_updates['ZP_TRACK']}', ARTIST: '{state_updates['ZP_ARTIST']}', STATION: '{state_updates['ZP_STATION']}'")

                        self.last_siriusxm_track_by_dev[dev_id] = state_updates["ZP_TRACK"]
                        self.last_siriusxm_artist_by_dev[dev_id] = state_updates["ZP_ARTIST"]

                    except Exception as e:
                        self.logger.warning(f"⚠️ Failed to parse SiriusXM metadata: {e}")
                        fallback_track = self.last_siriusxm_track_by_dev.get(dev_id, "Unknown Channel")
                        fallback_artist = self.last_siriusxm_artist_by_dev.get(dev_id, "Unknown Artist")
                        state_updates["ZP_TRACK"] = fallback_track
                        state_updates["ZP_STATION"] = fallback_track
                        state_updates["ZP_ARTIST"] = fallback_artist
                        state_updates["ZP_ALBUM"] = ""

            # === Pandora handling ===
            if is_pandora and "enqueued_transport_uri_meta_data" in event_obj.variables:
                meta = event_obj.variables["enqueued_transport_uri_meta_data"]
                try:
                    station_title = safe_call(getattr(meta, "title", ""))
                    if station_title.endswith(" (My Station)"):
                        station_title = station_title.replace(" (My Station)", "").strip()
                    if station_title:
                        state_updates["ZP_STATION"] = station_title
                        self.safe_debug(f"📻 Extracted Pandora station name: {station_title}")

                    station_creator = safe_call(getattr(meta, "creator", ""))
                    if station_creator:
                        state_updates["ZP_CREATOR"] = station_creator
                        if "ZP_ARTIST" not in state_updates or not state_updates["ZP_ARTIST"]:
                            state_updates["ZP_ARTIST"] = station_creator
                        self.safe_debug(f"🎨 Extracted Pandora creator: {station_creator}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to parse Pandora metadata: {e}")

            #################################################################################################
            ### Is everything here and after a drop through that fires everytime? 
            #################################################################################################

            #################################################################################################
            ### Is everything here and after a drop through that fires everytime? 
            ### this refresh_group_mambership below seems to be the only call to refresh group membership - 
            ### perhaps we need to wrap this with test logic to only call if group is changed, seems to 
            ### happen now on every group trigger? This would also remove the extra art save.
            #################################################################################################

#            self.logger.info("Trapping here what fires after drop through from all other states assesment events")    

            # === General metadata ===
            if "current_track_meta_data" in event_obj.variables:
                meta = event_obj.variables["current_track_meta_data"]
                try:
                    meta_dict = meta.to_dict()
                    track_title = meta_dict.get("title", "")
                    track_album = meta_dict.get("album", "")
                    track_artist = meta_dict.get("artist", "")
                    track_creator = meta_dict.get("creator", "")

                    if track_title:
                        state_updates["ZP_TRACK"] = track_title
                    if track_album:
                        state_updates["ZP_ALBUM"] = track_album
                    if track_artist:
                        state_updates["ZP_ARTIST"] = track_artist
                    elif track_creator:
                        state_updates["ZP_ARTIST"] = track_creator
                    if track_creator:
                        state_updates["ZP_CREATOR"] = track_creator

                    # ✅ NEW: Capture and store all relevant URIs
                    current_uri = event_obj.variables.get("current_track_uri", "")
                    av_transport_uri = event_obj.variables.get("av_transport_uri", "")
                    enqueued_uri = event_obj.variables.get("enqueued_transport_uri", "")

                    state_updates["ZP_CurrentTrackURI"] = current_uri
                    state_updates["ZP_AVTransportURI"] = av_transport_uri
                    state_updates["ZP_EnqueuedURI"] = enqueued_uri

                    self.safe_debug(f"📡 Captured URIs — current: {current_uri}, av: {av_transport_uri}, enqueued: {enqueued_uri}")

                    self.safe_debug(f"🎵 General metadata parsed: title={track_title}, artist={track_artist}, creator={track_creator}, album={track_album}")

                except Exception as e:
                    self.logger.debug(f"⚠️ Failed to extract general metadata: {e}")

            # === Apply all collected state updates ===
            if state_updates:
                for k, v in state_updates.items():
                    self.safe_debug(f"🔄 Heavyweight update → {k}: {v}")
                    indigo_device.updateStateOnServer(key=k, value=v)


#### Do I need thois if it is firing from controller? Seems to fire with both if on but neither when off?

            # === Artwork block — moved here for coordination after states ===
            try:
                indigo_device = self.getIndigoDeviceFromEvent(event_obj)
                if indigo_device:
                    self.update_album_artwork(
                        event_obj=event_obj,
                        dev=indigo_device,
                        zone_ip=indigo_device.address.strip()
                    )
                    self.logger.debug(f"🖼️ Standalone - I am updating artwork here for {zone_ip} — after drop through from all other states assesment events")    
                else:
                    self.logger.debug("⚠️ Skipping artwork update — Indigo device could not be resolved from event")
            except Exception as e:
                self.logger.debug(f"⚠️ Failed to update album artwork: {e}")


            # === Coordinator logic ===
            is_master = False
            if indigo_device:
                try:
                    coordinator = self.getCoordinatorDevice(indigo_device)
                    is_master = (coordinator.address == indigo_device.address)
                except Exception as e:
                    self.logger.debug(f"⚠️ Could not determine coordinator for {indigo_device.name}: {e}")
            else:
                self.logger.debug("⚠️ Skipping coordinator check — indigo_device is None")


            if is_master:
                self.updateStateOnSlaves(indigo_device)
                #self.evaluate_and_update_grouped_states()            

        except Exception as e:
            self.logger.error(f"❌ Error in soco_event_handler: {e}")


#################################################################################################
### End of Event Handler
#################################################################################################






#################################################################################################
### Helpers
#################################################################################################

# Add at class init if you like, but helper guards handle None fine:
# self._dbg_last_write_coord = {}

    def _trace_group_coord_write(self, dev, new_value, reason=""):
        """
        Log *who* wrote GROUP_Coordinator, what they wrote, and where from.
        Also stash a stamp in plugin memory. Only write a device state if that
        key already exists on the device (Indigo won't accept ad-hoc keys).
        """
        try:
            import os, time, inspect
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            frame = inspect.stack()[2]  # caller of the wrapper below
            callsite = f"{os.path.basename(frame.filename)}:{frame.lineno} {frame.function}"
            stamp = f"{ts} → {new_value} [{reason}] @ {callsite}"

            # Keep a plugin-level record so we never lose the trace.
            if not hasattr(self, "_dbg_last_write_coord") or self._dbg_last_write_coord is None:
                self._dbg_last_write_coord = {}
            self._dbg_last_write_coord[dev.id] = stamp

            # Only attempt to update a device state if the key already exists on the device.
            # (Indigo rejects unknown state keys.)
            if "DBG_last_write_COORD" in dev.states:
                try:
                    dev.updateStateOnServer("DBG_last_write_COORD", stamp)
                except Exception as e:
                    # Don't spam errors; just note it in debug.
                    self.safe_debug(f"[TRACE] could not update DBG_last_write_COORD on {dev.name}: {e}")

            self.logger.debug(f"[TRACE] GROUP_Coordinator={new_value} on {dev.name} ← {stamp}")

        except Exception as e:
            self.safe_debug(f"[TRACE] failed to trace coord write for {getattr(dev,'name','?')}: {e}")


    def _update_group_coord(self, dev, coord_str, reason=""):
        """
        Single choke point for writing GROUP_Coordinator so we always trace who wrote it.
        coord_str must be the canonical string 'true' or 'false'.
        """
        try:
            self._trace_group_coord_write(dev, coord_str, reason)
        finally:
            dev.updateStateOnServer("GROUP_Coordinator", coord_str)


    def _audit_coord_drift(self, where=""):
        """
        Scan all Sonos devices and compare GROUP_Coordinator (Indigo) vs live SoCo.
        If there’s drift, log it loudly. (No device-state writes here.)
        """
        try:
            self.logger.warning(f"[AUDIT] Coordinator drift check start ({where})")
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                ip = (dev.address or "").strip()
                soco = (getattr(self, "ip_to_soco_device", {}) or {}).get(ip)
                is_coord_live = bool(getattr(soco, "is_coordinator", False)) if soco else None
                curr = str(dev.states.get("GROUP_Coordinator", "")).strip().lower()

                if is_coord_live is None:
                    self.logger.warning(f"[AUDIT] {dev.name}: no live SoCo; Indigo={curr}")
                    continue

                expected = "true" if is_coord_live else "false"
                if curr != expected:
                    last = None
                    try:
                        last = self._dbg_last_write_coord.get(dev.id)
                    except Exception:
                        last = "(no trace)"
                    self.logger.error(f"[AUDIT][DRIFT] {dev.name}: Indigo={curr} but SoCo={expected}. Last writer: {last}")
            self.logger.warning(f"[AUDIT] Coordinator drift check end ({where})")
        except Exception as e:
            self.logger.error(f"[AUDIT] audit failed: {e}")








    def old_soco_group_truth(self, soco_device):
        """
        Return (is_coord, is_grouped, group_name) from a live SoCo handle.
        - is_grouped: True if >1 non-bonded members in the SoCo group
        - group_name: coordinator player_name when available, otherwise device/row name
        """
        is_coord = False
        is_grouped = False
        group_name = ""

        try:
            if not soco_device:
                return (False, False, "")

            # coordinator flag
            try:
                is_coord = bool(getattr(soco_device, "is_coordinator", False))
            except Exception:
                is_coord = False

            # group topology
            g = None
            try:
                g = soco_device.group
            except Exception:
                g = None

            if g:
                # count non-bonded members to decide grouped=True|False
                nonbond = 0
                for m in (getattr(g, "members", []) or []):
                    nm = (getattr(m, "player_name", "") or "").lower()
                    if not any(k in nm for k in ("sub", "left", "right", "surround")):
                        nonbond += 1
                is_grouped = (nonbond > 1)

                # group name from the coordinator if present
                if getattr(g, "coordinator", None):
                    group_name = getattr(g.coordinator, "player_name", "") or ""

            # fallback group_name to the device's own player_name when blank
            if not group_name:
                try:
                    group_name = getattr(soco_device, "player_name", "") or ""
                except Exception:
                    group_name = ""

        except Exception as e:
            self.logger.debug(f"[soco-truth] failed: {e}")

        return (is_coord, is_grouped, group_name)





    def _soco_group_truth(self, soco):
        """
        Return (is_coord: bool, is_grouped: bool, group_name: str) from live SoCo.
        Bonded satellites (sub/left/right/surround) do not count toward grouping.
        """
        is_coord = False
        is_grouped = False
        group_name = ""
        if not soco:
            return is_coord, is_grouped, group_name
        try:
            is_coord = bool(getattr(soco, "is_coordinator", False))
        except Exception:
            is_coord = False
        try:
            g = soco.group
            if g:
                # coordinator name
                cn = getattr(getattr(g, "coordinator", None), "player_name", "") or ""
                if cn:
                    group_name = cn
                # grouped = non-bonded members > 1
                nonbond = 0
                bonded_seen = False                 # NEW
                for m in (g.members or []):
                    nm = (getattr(m, "player_name", "") or "").lower()
                    if any(k in nm for k in ("sub", "left", "right", "surround")):
                        bonded_seen = True         # NEW
                    else:
                        nonbond += 1
                is_grouped = (nonbond > 1)
                # NEW: bonded-only sets should not clear coordinator
                # e.g., stereo pair has nonbond==1 but is_coord should remain whatever SoCo says
                if bonded_seen and nonbond <= 1:
                    # leave is_coord as-is; do NOT derive from is_grouped
                    pass
            if not group_name:
                group_name = getattr(soco, "player_name", "") or group_name
        except Exception:
            pass
        return is_coord, is_grouped, group_name






    def _ready_for_group_refresh(self) -> bool:
        """
        Returns True when we have enough inputs to safely run _refresh_all_group_states_helper
        without clobbering states (i.e., seed/write passes won’t run with empty maps).
        """
        try:
            groups = getattr(self, "zone_group_state_cache", {}) or {}
            ip2dev = getattr(self, "ip_to_indigo_device", {}) or {}
            soco_by_ip = getattr(self, "ip_to_soco_device", None)
            if soco_by_ip is None:
                soco_by_ip = getattr(self, "soco_by_ip", {}) or {}
            ok = (len(groups) > 0) and (len(ip2dev) > 0) and (len(soco_by_ip) > 0)
            if not ok:
                # Normal transient state while devices are still starting — debug, not warning
                self.logger.debug(
                    f"[ready-probe] NOT READY for refresh: groups={len(groups)} ip→dev={len(ip2dev)} soco_by_ip={len(soco_by_ip)}"
                )
            else:
                self.logger.debug(
                    f"[ready-probe] READY for refresh: groups={len(groups)} ip→dev={len(ip2dev)} soco_by_ip={len(soco_by_ip)}"
                )
            return ok
        except Exception as e:
            self.logger.warning(f"[ready-probe] exception: {e}")
            return False




    # Add this tiny helper once (near other helpers)
    def _soco_group_truth(self, soco):
        """
        Return (is_coord: bool, is_grouped: bool, group_name: str) from live SoCo.
        Bonded satellites (sub/left/right/surround) do not count toward grouping.
        """
        is_coord = False
        is_grouped = False
        group_name = ""
        if not soco:
            return is_coord, is_grouped, group_name
        try:
            is_coord = bool(getattr(soco, "is_coordinator", False))
        except Exception:
            is_coord = False
        try:
            g = soco.group
            if g:
                # coordinator name
                cn = getattr(getattr(g, "coordinator", None), "player_name", "") or ""
                if cn:
                    group_name = cn
                # grouped = non-bonded members > 1
                nonbond = 0
                for m in (g.members or []):
                    nm = (getattr(m, "player_name", "") or "").lower()
                    if not any(k in nm for k in ("sub", "left", "right", "surround")):
                        nonbond += 1
                is_grouped = (nonbond > 1)
            # fallback to the player's own name if group_name is still empty
            if not group_name:
                group_name = getattr(soco, "player_name", "") or group_name
        except Exception:
            pass
        return is_coord, is_grouped, group_name



    def _topology_ready(self) -> bool:
        """
        Returns True when we have enough live objects to trust a fresh topology read.
        We consider it 'ready' if we have at least one SoCo object AND at least one
        IP→Indigo device mapping. You can tighten this if needed.
        """
        try:
            soco_by_ip = getattr(self, "soco_by_ip", {}) or {}
            ip2dev     = getattr(self, "ip_to_indigo_device", {}) or {}
            ready = bool(soco_by_ip) and bool(ip2dev)
            if not ready:
                self.logger.warning(
                    f"[topology] not ready (soco_by_ip={len(soco_by_ip)} ip→dev={len(ip2dev)})"
                )
            return ready
        except Exception as e:
            self.logger.warning(f"[topology] readiness check failed: {e}")
            return False






    def old_set_group_states(self, dev, *, grouped, is_coord, group_name):
        """
        Canonical writer for the 3 group states on an Indigo device:
          - Grouped (bool)
          - GROUP_Coordinator ("true"/"false" string)
          - GROUP_Name (string)

        NOTE:
        - Do NOT couple coordinator to Grouped; a bonded-only set may have Grouped=False
          while still being the coordinator of its bonded set.
        - Keep types consistent with existing UI/filters.
        """
        try:
            # Normalize incoming values
            new_grouped = bool(grouped)
            coord_str   = "true" if bool(is_coord) else "false"
            new_name    = (group_name or "").strip()

            # Current state snapshots
            prev_grouped = bool(dev.states.get("Grouped", False))
            prev_coord   = str(dev.states.get("GROUP_Coordinator", "")).strip().lower()
            prev_name    = (dev.states.get("GROUP_Name", "") or "").strip()

            # --- existing true→false veto with live SoCo check (unchanged) ---
            if prev_coord == "true" and coord_str == "false":
                try:
                    ip = (dev.address or "").strip()
                    soco = (getattr(self, "ip_to_soco_device", {}) or {}).get(ip)
                    live_is_coord = bool(getattr(soco, "is_coordinator", False)) if soco else None
                    if live_is_coord is True:
                        self.logger.debug(
                            f"[set-group]   veto coord flip on {dev.name}: attempted 'true'→'false' but live SoCo still reports coordinator"
                        )
                        coord_str = "true"
                    elif live_is_coord is None:
                        self.logger.debug(
                            f"[set-group]   veto coord flip on {dev.name}: no live SoCo available to verify; preserving 'true'"
                        )
                        coord_str = "true"
                except Exception as e:
                    self.logger.debug(f"[set-group]   veto coord flip on {dev.name}: check failed ({e}); preserving 'true'")
                    coord_str = "true"

            # --- bonded-leader safety (unchanged logic) ---
            if prev_coord == "true" and coord_str == "false" and ((prev_name == dev.name) or (new_name == dev.name)):
                self.logger.debug(f"[set-group][guard] Skip demote of {dev.name}: named group anchor (prev_name='{prev_name}', new_name='{new_name}')")
                coord_str = "true"

            # Coordinator
            if prev_coord != coord_str:
                self.logger.debug(f"[set-group]   Coord: '{prev_coord}' → '{coord_str}' on {dev.name}")
                # ⬇️ use tracer wrapper so we can see who wrote it
                self._update_group_coord(dev, coord_str, reason="_set_group_states")

            # Grouped
            if prev_grouped != new_grouped:
                self.logger.debug(f"[set-group]   Grouped: {prev_grouped} → {new_grouped} on {dev.name}")
                dev.updateStateOnServer("Grouped", new_grouped)

            # Group name
            if prev_name != new_name:
                self.logger.debug(f"[set-group]   Name: '{prev_name}' → '{new_name}' on {dev.name}")
                dev.updateStateOnServer("GROUP_Name", new_name)

            # Optional trace
            try:
                caller = getattr(self, "_who_called", lambda: "?")()
            except Exception:
                caller = "?"
            self.logger.debug(
                f"[coord-check] {dev.name} write coord={coord_str} (grouped={new_grouped}, name='{new_name}') via caller={caller}"
            )

        except Exception as e:
            self.logger.error(f"❌ _set_group_states failed for {dev.name}: {e}")






    def old2_set_group_states(self, dev, *, grouped, is_coord, group_name):
        """
        Canonical writer for the 3 group states on an Indigo device:
          - Grouped (bool)
          - GROUP_Coordinator ("true"/"false" string)
          - GROUP_Name (string)

        NOTE:
        - Do NOT couple coordinator to Grouped; a bonded-only set may have Grouped=False
          while still being the coordinator of its bonded set.
        - Keep types consistent with existing UI/filters.
        """
        try:
            # Normalize incoming values
            new_grouped = bool(grouped)
            coord_str   = "true" if bool(is_coord) else "false"
            new_name    = (group_name or "").strip()

            # Current state snapshots
            prev_grouped = bool(dev.states.get("Grouped", False))
            prev_coord   = str(dev.states.get("GROUP_Coordinator", "")).strip().lower()
            prev_name    = (dev.states.get("GROUP_Name", "") or "").strip()

            # --- existing true→false veto with live SoCo check (refined) ---
            if prev_coord == "true" and coord_str == "false":
                try:
                    # Resolve SoCo by IP (be tolerant of address storage)
                    ip = (getattr(dev, "address", None) or dev.pluginProps.get("address", "") or "").strip()
                    soco = (getattr(self, "ip_to_soco_device", {}) or {}).get(ip) or self.soco_by_ip.get(ip)

                    live_is_coord = bool(getattr(soco, "is_coordinator", False)) if soco else None

                    # NEW: if we can read the live group's coordinator uuid, check for a mismatch
                    live_group   = getattr(soco, "group", None) if soco else None
                    live_coord   = getattr(live_group, "coordinator", None) if live_group else None
                    live_coord_u = getattr(live_coord, "uid", None)
                    self_u       = getattr(soco, "uid", None)
                    uuid_mismatch = bool(live_coord_u and self_u and str(live_coord_u) != str(self_u))

                    if live_is_coord is True and not uuid_mismatch:
                        # SoCo still says we're the coordinator AND no uuid mismatch → keep "true"
                        self.logger.debug(
                            f"[set-group]   veto coord flip on {dev.name}: attempted 'true'→'false' but live SoCo still reports coordinator"
                        )
                        coord_str = "true"

                    elif live_is_coord is True and uuid_mismatch:
                        # NEW: SoCo says True but the group's coordinator uid is someone else → allow demotion
                        self.logger.debug(
                            f"[set-group]   allowing demotion on {dev.name}: SoCo is_coordinator=True but uuid mismatch "
                            f"(self={self_u}, group.coord={live_coord_u})"
                        )
                        # coord_str stays "false"

                    elif live_is_coord is None:
                        # CHANGED: if we cannot verify SoCo right now, DO NOT force 'true' — honor caller's demotion
                        self.logger.debug(
                            f"[set-group]   no live SoCo available for {dev.name}; honoring caller-requested demotion to 'false'"
                        )
                        # coord_str stays "false"

                    else:
                        # live_is_coord is False → demotion is safe
                        pass

                except Exception as e:
                    # CHANGED: on error, do NOT force-true; log and honor caller's demotion
                    self.logger.debug(f"[set-group]   SoCo check failed for {dev.name} ({e}); honoring demotion to 'false'")
                    # coord_str stays "false"

            # --- bonded-leader safety (unchanged logic) ---
            if prev_coord == "true" and coord_str == "false" and ((prev_name == dev.name) or (new_name == dev.name)):
                self.logger.debug(f"[set-group][guard] Skip demote of {dev.name}: named group anchor (prev_name='{prev_name}', new_name='{new_name}')")
                coord_str = "true"

            # Coordinator
            if prev_coord != coord_str:
                self.logger.debug(f"[set-group]   Coord: '{prev_coord}' → '{coord_str}' on {dev.name}")
                # ⬇️ use tracer wrapper so we can see who wrote it
                self._update_group_coord(dev, coord_str, reason="_set_group_states")

            # Grouped
            if prev_grouped != new_grouped:
                self.logger.debug(f"[set-group]   Grouped: {prev_grouped} → {new_grouped} on {dev.name}")
                dev.updateStateOnServer("Grouped", new_grouped)

            # Group name
            if prev_name != new_name:
                self.logger.debug(f"[set-group]   Name: '{prev_name}' → '{new_name}' on {dev.name}")
                dev.updateStateOnServer("GROUP_Name", new_name)

            # Optional trace
            try:
                caller = getattr(self, "_who_called", lambda: "?")()
            except Exception:
                caller = "?"
            self.logger.debug(
                f"[coord-check] {dev.name} write coord={coord_str} (grouped={new_grouped}, name='{new_name}') via caller={caller}"
            )

        except Exception as e:
            self.logger.error(f"❌ _set_group_states failed for {dev.name}: {e}")


    def _set_group_states(self, dev, *, grouped, is_coord, group_name):
        """
        Canonical writer for the 3 group states on an Indigo device:
          - Grouped (bool)
          - GROUP_Coordinator ("true"/"false" string)
          - GROUP_Name (string)

        NOTE:
        - Do NOT couple coordinator to Grouped; a bonded-only set may have Grouped=False
          while still being the coordinator of its bonded set.
        - Keep types consistent with existing UI/filters.
        """
        try:
            # Normalize incoming values
            new_grouped = bool(grouped)
            coord_str   = "true" if bool(is_coord) else "false"
            new_name    = (group_name or "").strip()

            # Current state snapshots
            prev_grouped = bool(dev.states.get("Grouped", False))
            prev_coord   = str(dev.states.get("GROUP_Coordinator", "")).strip().lower()
            prev_name    = (dev.states.get("GROUP_Name", "") or "").strip()

            # --- veto only if SoCo still reports coordinator (safety), no name-based vetoes ---
            if prev_coord == "true" and coord_str == "false":
                try:
                    ip   = (getattr(dev, "address", "") or "").strip()
                    soco = (getattr(self, "ip_to_soco_device", {}) or {}).get(ip)
                    live_is_coord = bool(getattr(soco, "is_coordinator", False)) if soco else None
                    if live_is_coord is True:
                        self.logger.debug(
                            f"[set-group]   veto coord flip on {dev.name}: attempted 'true'→'false' but live SoCo still reports coordinator"
                        )
                        coord_str = "true"   # preserve true (avoid clobber)
                    elif live_is_coord is None:
                        self.logger.debug(
                            f"[set-group]   veto coord flip on {dev.name}: no live SoCo available to verify; preserving 'true'"
                        )
                        coord_str = "true"
                except Exception as e:
                    self.logger.debug(f"[set-group]   veto coord flip on {dev.name}: check failed ({e}); preserving 'true'")
                    coord_str = "true"

            # --- co-promotion of Grouped when making/keeping a coordinator with >1 members ---
            # This only adjusts the local write; it does not forcibly rewire your evaluated logic.
            if coord_str == "true" and new_grouped is False:
                try:
                    ip   = (getattr(dev, "address", "") or "").strip()
                    soco = (getattr(self, "ip_to_soco_device", {}) or {}).get(ip)
                    grp  = getattr(soco, "group", None) if soco else None
                    members_live = list(getattr(grp, "members", [])) if grp else []
                    # more than 1 non-bonded member typically means "grouped"
                    if len(members_live) > 1:
                        self.logger.debug(f"[set-group][co-promote] live members={len(members_live)} → forcing Grouped=True on {dev.name}")
                        new_grouped = True
                except Exception:
                    # be quiet on failure – we'll allow later passes to reconcile
                    pass

            # Coordinator
            if prev_coord != coord_str:
                self.logger.debug(f"[set-group]   Coord: '{prev_coord}' → '{coord_str}' on {dev.name}")
                # use tracer wrapper if you have it, else write directly
                tracer = getattr(self, "_update_group_coord", None)
                if callable(tracer):
                    tracer(dev, coord_str, reason="_set_group_states")
                else:
                    dev.updateStateOnServer("GROUP_Coordinator", coord_str)

            # Grouped (boolean)
            if prev_grouped != new_grouped:
                self.logger.debug(f"[set-group]   Grouped: {prev_grouped} → {new_grouped} on {dev.name}")
                dev.updateStateOnServer("Grouped", new_grouped)

            # Group name
            if prev_name != new_name:
                self.logger.debug(f"[set-group]   Name: '{prev_name}' → '{new_name}' on {dev.name}")
                dev.updateStateOnServer("GROUP_Name", new_name)

            # Optional trace
            try:
                caller = getattr(self, "_who_called", lambda: "?")()
            except Exception:
                caller = "?"
            self.logger.debug(
                f"[coord-check] {dev.name} write coord={coord_str} (grouped={new_grouped}, name='{new_name}') via caller={caller}"
            )

        except Exception as e:
            self.logger.error(f"❌ _set_group_states failed for {dev.name}: {e}")









    def _schedule_one_shot_dump_groups(self, delay=6.0):
        """Debounce: schedule dump_groups_to_log() once, shortly after the *last* deviceStartComm."""
        # If we've already done the dump this startup, bail.
        if getattr(self, "_dump_groups_done", False):
            return

        import threading

        # Cancel any pending timer so we only run once after the "last" startComm finishes.
        t = getattr(self, "_dump_groups_timer", None)
        if t is not None:
            try:
                t.cancel()
            except Exception:
                pass

        def _run_once():
            try:
                self.dump_groups_to_log()
            except Exception as e:
                self.logger.error(f"❌ dump_groups_to_log failed: {e}")
            finally:
                # Mark as done so subsequent calls won't reschedule.
                self._dump_groups_done = True
                self._dump_groups_timer = None

        self._dump_groups_timer = threading.Timer(delay, _run_once)
        self._dump_groups_timer.daemon = True
        self._dump_groups_timer.start()


    def _post_zgt_check_grouped_and_propagate_art(self):
        """
        Run exactly after a ZGT change has been parsed and Indigo Grouped states have been updated.
        - Compare Indigo 'Grouped' (truth) vs SoCo non-bonded member count (>1)
        - Warn only if all non-bonded members are resolvable to Indigo devices (avoid startup noise)
        - If Grouped is 'true', trigger artwork propagation from each coordinator
        """
        try:
            coord_ip_map = getattr(self, "_eval_coord_dev_by_ip", {}) or {}
            for coord_ip, coord_dev in coord_ip_map.items():
                if not coord_dev:
                    continue

                # Re-fetch device to avoid stale cache
                try:
                    coord_dev_ref = indigo.devices[coord_dev.id]
                except Exception:
                    coord_dev_ref = coord_dev

                grouped_flag = coord_dev_ref.states.get("Grouped", "false")

                # Build SoCo member lists for this coordinator
                soco = self.soco_by_ip.get(coord_ip)
                if not soco or not getattr(soco, "group", None):
                    continue

                all_member_ips, bonded_member_ips = [], []
                try:
                    for m in (soco.group.members or []):
                        ip = (getattr(m, "ip_address", "") or "").strip()
                        name_lc = (getattr(m, "player_name", "") or "").lower()
                        if not ip:
                            continue
                        all_member_ips.append(ip)
                        if ("sub" in name_lc or "left" in name_lc or "right" in name_lc or "surround" in name_lc):
                            bonded_member_ips.append(ip)
                except Exception:
                    pass

                non_bonded_ips = [ip for ip in all_member_ips if ip not in bonded_member_ips]
                non_bonded_count = len(non_bonded_ips)

                # If any non-bonded member isn't mapped to an Indigo device yet, skip (no warning)
                unresolved = [ip for ip in non_bonded_ips if not self.ip_to_indigo_device.get(ip)]
                if unresolved:
                    # Keep this at DEBUG so you can see why a check was skipped during discovery
                    self.logger.debug(
                        f"⏳ Suppressing drift check for {coord_ip}: unresolved non-bonded members {unresolved}"
                    )
                    continue

                # If Indigo says grouped, do artwork propagation (no event)
                if grouped_flag == "true":
                    try:
                        self.update_album_artwork(event_obj=None, dev=coord_dev_ref, zone_ip=coord_ip)
                    except Exception as art_err:
                        self.logger.warning(f"⚠️ Artwork propagation skipped for {coord_dev_ref.name} ({coord_ip}): {art_err}")
                else:
                    # Only warn when there is actual grouping beyond bonded members
                    if non_bonded_count < 2:
                        self.logger.info(
                            "⚠️ Grouped state drift detected 2 Post-ZGT — This is ok during initialization - "
                            f"Indigo.Grouped={grouped_flag}, SoCo.non_bonded_members>1=True, "
                            f"coord_ip={coord_ip}, all_members={all_member_ips}, bonded={bonded_member_ips}"
                        )
        except Exception as e:
            self.logger.debug(f"⚠️ Post-ZGT grouped/artwork check failed: {e}")






    def _seed_zone_group_cache_from_soco(self):
        """
        Seed zone_group_state_cache from SoCo's group view so that "pre-change" dumps
        use the same truth as "post-change" (ZGT-event) processing.
        Safe to call multiple times; it only writes if it can build a snapshot.
        """
        try:
            # Find any SoCo instance to ask for groups
            any_dev = None
            if self.soco_by_ip:
                any_dev = next(iter(self.soco_by_ip.values()))
            else:
                # last resort – may be slower but ok at startup
                disc = soco.discover(timeout=2)  # short timeout
                if disc:
                    any_dev = next(iter(disc))

            if not any_dev:
                self.logger.debug("seed_cache: no SoCo device available yet; skip")
                return False

            # SoCo groups API – consistent across versions
            # any_dev.all_groups returns a set/list of ZoneGroup objects
            groups = getattr(any_dev, "all_groups", None)
            if callable(groups):
                groups = any_dev.all_groups()

            if not groups:
                self.logger.debug("seed_cache: any_dev.all_groups returned empty")
                return False

            # Build the same structure your ZGT parser returns
            # Expecting: { group_id: { "name": str, "members": [ {ip, name, uid, coordinator, bonded}, ... ] } }
            cache = {}
            for zg in groups:
                # zg.uid (group coordinator uid), zg.label (group name), zg.members (list of SoCo)
                group_id = getattr(zg, "uid", None) or getattr(zg, "coordinator", None)
                group_name = getattr(zg, "label", None) or getattr(zg, "name", None) or "Unknown Group"
                members = []
                for m in list(getattr(zg, "members", []) or []):
                    try:
                        # coordinator flag: compare to zg.coordinator (SoCo object) or zg.coordinator.uid
                        is_coord = False
                        try:
                            coord_obj = getattr(zg, "coordinator", None)
                            if coord_obj is not None:
                                is_coord = (coord_obj.uid == m.uid)
                        except Exception:
                            pass

                        # bonded: leave False here (you set it later in your evaluate_* path)
                        members.append({
                            "ip": m.ip_address,
                            "name": m.player_name,
                            "uid": m.uid,
                            "coordinator": bool(is_coord),
                            "bonded": False,
                        })
                    except Exception:
                        continue

                if members:
                    cache[group_id or group_name] = {"name": group_name, "members": members}

            if not cache:
                self.logger.debug("seed_cache: built empty cache; skip")
                return False

            import copy
            with self.zone_group_state_lock:
                self.zone_group_state_cache = copy.deepcopy(cache)

            self.logger.info(f"💾 Seeded zone_group_state_cache from SoCo with {len(cache)} group(s)")
            # Build coordinator map & grouped flags from current SoCo topology so early hooks don't see an empty map
            try:
                #self.refresh_all_group_states()
                self._refresh_all_group_states_helper(reason="_seed_zone_group_cache_from_soco")
                
            except Exception as e:
                self.logger.warning(f"⚠️ Initial group state refresh failed: {e}")
            return True

        except Exception as e:
            self.logger.debug(f"seed_cache: failed: {e}")
            return False





    def getSoCoDeviceByIP(self, ip_address):
        try:
            if not hasattr(self, "soco_device_cache"):
                self.soco_device_cache = {}

            #self.safe_debug(f"🔍 getSoCoDeviceByIP called for {ip_address}")

            if ip_address in self.soco_device_cache:
                self.safe_debug(f"✅ Found {ip_address} in soco_device_cache")
                return self.soco_device_cache[ip_address]

            # ♻️ Reuse the instance from startup discovery when available
            known = getattr(self, "soco_by_ip", {}).get(ip_address)
            if known is not None:
                self.soco_device_cache[ip_address] = known
                return known

            # Direct init by IP — equivalent to a discovery match, and it works across
            # routed subnets/VLANs where multicast discovery can never reach (previously
            # this ran a 5s discovery sweep and warned "No SoCo devices discovered" on
            # every cache miss in such setups).
            from soco import SoCo
            try:
                device = SoCo(ip_address)
                self.soco_device_cache[ip_address] = device
                self.safe_debug(f"✅ Direct SoCo init for {ip_address}")
                return device
            except Exception as init_error:
                self.logger.error(f"❌ Direct SoCo init failed in getSoCoDeviceByIP({ip_address}): {init_error}")
                return None

        except Exception as e:
            self.logger.error(f"❌ Error in getSoCoDeviceByIP: {e}")
            return None


        
    def getCoordinatorDevice(self, device):
        """
        Given an Indigo device, return the Indigo device object representing
        the group coordinator (master) for that device's group.
        If the device is the master or resolution fails, returns itself.
        """
        try:
            if not device:
                self.logger.error("❌ getCoordinatorDevice: device argument is None")
                return None

            zone_ip = device.address
            if not zone_ip:
                self.logger.error(f"❌ getCoordinatorDevice: device {device.name} has no IP address set")
                return device

            self.logger.debug(f"🔍 Looking up SoCo device for IP: {zone_ip}")
            soco_device = self.getSoCoDeviceByIP(zone_ip)

            if not soco_device:
                self.logger.warning(f"⚠️ getSoCoDeviceByIP({zone_ip}) returned None — treating {device.name} as its own coordinator.")
                if hasattr(self, "soco_device_cache"):
                    self.logger.debug(f"📋 Cached SoCo devices: {list(self.soco_device_cache.keys())}")
                else:
                    self.logger.debug("📋 No soco_device_cache attribute present.")
                return device  # fallback

            # Confirm group/coordinator exists
            group = getattr(soco_device, "group", None)
            if not group or not hasattr(group, "coordinator"):
                self.logger.warning(f"⚠️ SoCo device {zone_ip} has no group or coordinator info — using self.")
                return device

            coordinator = group.coordinator
            coordinator_ip = getattr(coordinator, "ip_address", None)
            if not coordinator_ip:
                self.logger.warning(f"⚠️ Coordinator IP is missing — falling back to self.")
                return device

            self.logger.debug(f"✅ Group coordinator IP for {device.name}: {coordinator_ip}")

            # Match to Indigo device
            for dev in indigo.devices.iter("self"):
                if dev.address == coordinator_ip:
                    self.logger.debug(f"✅ Found Indigo device for coordinator: {dev.name} ({coordinator_ip})")
                    return dev

            self.logger.warning(f"⚠️ No Indigo device matches coordinator IP {coordinator_ip}; defaulting to self.")
            return device

        except Exception as e:
            self.logger.error(f"❌ Exception in getCoordinatorDevice: {e}")
            return device





    def clear_device_states(self, indigo_device):
        try:
            state_defaults = {
                "ModelName": "",
                "SerialNumber": "",
                "ZP_INFO": "",
                "ZP_STATION": "",
                "ZP_VOLUME": "",
                "ZP_VOLUME_MASTER": 0,
                "ZP_VOLUME_LF": 0,
                "ZP_VOLUME_RF": 0,
                "ZP_MUTE": "false",
                "ZP_BASS": "0",
                "ZP_TREBLE": "0",
                "ZP_STATE": "",
                "ZP_ART": "",
                "ZP_TRACK": "",
                "ZP_DURATION": "",
                "ZP_RELATIVE": "",
                "ZP_ALBUM": "",
                "ZP_ARTIST": "",
                "ZP_SOURCE": "",                
                "ZP_CREATOR": "",
                "ZP_AIName": "",
                "ZP_AIPath": "",
                "ZP_CurrentURI": "",
                "ZP_ZoneName": "",
                "ZP_LocalUID": "",
                "ZP_NALBUM": "",
                "ZP_NARTIST": "",
                "ZP_NCREATOR": "",
                "ZP_NART": "",
                "ZP_NTRACK": "",
                "Q_Crossfade": False,
                "Q_Repeat": False,
                "Q_RepeatOne": False,
                "Q_Shuffle": False,
                "Q_Number": "",
                "Q_ObjectID": "",
                "GROUP_Coordinator": False,
                "GROUP_Name": "",
                "ZP_CurrentTrack": "",
                "ZP_CurrentTrackURI": "",
                "ZoneGroupID": "",
                "ZoneGroupName": "",
                "ZonePlayerUUIDsInGroup": "",
                "bootseq": 0,
                "alive": "",
            }

            for state_id, default_value in state_defaults.items():
                indigo_device.updateStateOnServer(state_id, default_value)

            self.logger.info(f"✅ Cleared all states for device '{indigo_device.name}'")

        except Exception as e:
            self.logger.error(f"❌ Failed to clear states for device '{indigo_device.name}': {e}")





    def soco_discover_and_subscribe(self):
        try:
            self.logger.info("🔍 Discovering Sonos devices on the network...")

            devices = soco.discover(timeout=5)  # Add a timeout to avoid blocking forever
            if not devices:
                self.logger.warning("❌ No Sonos devices discovered.")
                return

            self.logger.info(f"✅ Found {len(devices)} Sonos device(s). Subscribing to events...")

            # Clear and rebuild the device cache
            self.soco_by_ip = {}

            for device in devices:
                ip = device.ip_address
                name = device.player_name
                self.logger.info(f"   📻 Discovered {name} @ {ip}")

                # Cache the SoCo device by IP for later lookup
                self.soco_by_ip[ip] = device

                # Try to match to an Indigo device by IP
                matched_device = None
                for dev in indigo.devices.iter("self"):
                    if dev.address == ip:
                        matched_device = dev
                        break

                if matched_device:
                    self.safe_debug(f"   🔗 Matched to Indigo device {matched_device.name} (ID: {matched_device.id})")
                    self.socoSubscribe(matched_device, device)
                else:
                    self.logger.warning(f"⚠️ No Indigo device found matching IP {ip}")

        except Exception as e:
            self.logger.exception("❌ Error during Sonos device discovery and subscription")

            

    ######################################################################################
    # Utiliies






    def build_ip_to_device_map(self):
        self.ip_to_indigo_device = {
            dev.address.strip(): dev
            for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos")
        }



    PORT = 8888
    IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

    class SimpleImageHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=IMAGES_DIR, **kwargs)

    if __name__ == "__main__":
        with socketserver.TCPServer(("", PORT), SimpleImageHandler) as httpd:
            print(f"🎵 Mini Sonos Art Server serving at http://localhost:{PORT}")
            httpd.serve_forever()



    def cleanString(self, in_string):
        try:
            in_string = in_string.replace("&", "&amp;amp;")
            in_string = in_string.replace("'", "&apos;")
            return in_string

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def restoreString(self, in_string, filter):
        """
        Normalize Sonos strings safely from bytes/None and replace common entities.
        Always returns a str. (Note: parameter name 'filter' shadows the built-in.)
        """
        try:
            # Guard against None
            if in_string is None:
                return ""

            # Decode bytes -> str
            if isinstance(in_string, (bytes, bytearray)):
                try:
                    in_string = in_string.decode("utf-8", errors="ignore")
                except Exception:
                    in_string = in_string.decode("latin-1", errors="ignore")

            # Coerce other types to str (e.g., ints)
            if not isinstance(in_string, str):
                in_string = str(in_string)

            # 🔽 Your existing logic preserved
            in_string = in_string.replace("&amp;apos;", "'")
            if filter == 0:
                in_string = in_string.replace("&amp;amp;", "&")
                in_string = in_string.replace("&amp;", "&")
            in_string = in_string.replace("&quot;", "\"")
            in_string = in_string.replace("&lt;", "<")
            in_string = in_string.replace("&gt;", ">")
            in_string = in_string.replace("&apos;", "'")

            return in_string

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement
            # Fail-safe return to avoid propagating NoneType further
            try:
                return str(in_string) if in_string is not None else ""
            except Exception:
                return ""





#    def restoreString(self, in_string):
#        if in_string:
#            return in_string
#        return ""


    def shit_save_restoreString(self, in_string, _unused=None):
        if not in_string:
            self.logger.warning("⚠️ restoreString called with None or empty input.")
            return ""
        try:
            return in_string.replace("&amp;apos;", "'").replace("&amp;quot;", '"')
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to clean metadata string: {e}")
            return in_string










    def updateZoneGroupStates(self, dev):
        try:
            device_ip = dev.address.strip()
            soco_device = self.soco_by_ip.get(device_ip)
            if not soco_device:
                self.logger.warning(f"⚠️ No SoCo device found for IP {device_ip}")
                return

            group = soco_device.group
            coordinator = group.coordinator
            group_members = group.members

            group_id = group.uid
            #self.trace_me()               
            group_name = coordinator.player_name or "Unknown Group"
            member_uuids = [member.uid for member in group_members]

            bonded_model_types = ["sub", "surround", "sl"]
            coordinator_ip = coordinator.ip_address.strip()
            coord_indigo = self.ip_to_indigo_device.get(coordinator_ip)

            if not coord_indigo:
                self.logger.debug(f"⚠️ Could not resolve Indigo device for coordinator: {coordinator.player_name} ({coordinator_ip})")
                return

            # Get coordinator's actual grouped state from Indigo
            coord_grouped_state = str(coord_indigo.states.get("Grouped", "")).lower()
            is_grouped = (coord_grouped_state == "true")

            for member in group_members:
                member_ip = member.ip_address.strip()
                member_name = member.player_name or ""

                indigo_device = self.ip_to_indigo_device.get(member_ip)
                if not indigo_device:
                    self.logger.debug(f"Skipping update: No Indigo device found for IP {member_ip} ({member_name})")
                    continue

                is_coordinator = (coordinator_ip == member_ip)

                # Lookup model_name from cache to determine bonding
                cached_soco = self.soco_by_ip.get(member_ip)
                model_name = getattr(cached_soco, "model_name", "").lower() if cached_soco else ""
                is_bonded = any(bonded_type in model_name for bonded_type in bonded_model_types)

                # Apply coordinator's grouped state to all members
                new_grouped_state = "true" if is_grouped else "false"

                # Update Indigo states
                #self.trace_me()
                indigo_device.updateStateOnServer("ZP_ZoneName", member_name)
                indigo_device.updateStateOnServer("ZoneGroupID", group_id)
                indigo_device.updateStateOnServer("ZoneGroupName", group_name)
                indigo_device.updateStateOnServer("ZonePlayerUUIDsInGroup", ", ".join(member_uuids))

                if "GROUP_Coordinator" in indigo_device.states:
                    indigo_device.updateStateOnServer("GROUP_Coordinator", str(is_coordinator).lower())
                else:
                    self.logger.warning(f"⚠️ Device '{indigo_device.name}' missing 'GROUP_Coordinator' state — skipping.")

                if "GROUP_Name" in indigo_device.states:
                    indigo_device.updateStateOnServer("GROUP_Name", group_name)
                else:
                    self.logger.warning(f"⚠️ Device '{indigo_device.name}' missing 'GROUP_Name' state — skipping.")

                if "Grouped" in indigo_device.states:
                    indigo_device.updateStateOnServer("Grouped", new_grouped_state)
                else:
                    self.logger.warning(f"⚠️ Device '{indigo_device.name}' missing 'Grouped' state — skipping.")

                #self.logger.info(f"✅ Updated {indigo_device.name}: Coordinator={is_coordinator}, Grouped={new_grouped_state}, Bonded={is_bonded}")

        except Exception as e:
            self.logger.error(f"❌ Error updating zone group states for {dev.name}: {e}")







    def get_soco_by_uuid(self, uuid):
        # safe_uid resolves from cache / Indigo state and probe-gates any network
        # access — previously every call burned a 10s timeout per offline player.
        for ip, soco in list(self.soco_by_ip.items()):
            if self.safe_uid(ip, soco) == uuid:
                return soco
        self.logger.debug(f"🔍 No SoCo found for UUID {uuid}")
        return None





    def parse_zone_group_state(self, xml_data):
        import xml.etree.ElementTree as ET
        group_dict = {}

        #self.logger.warning("🛠 ENTERED parse_zone_group_state()")

        # Ensure xml_data is a str (not bytes)
        if isinstance(xml_data, bytes):
            try:
                xml_data = xml_data.decode("utf-8", errors="replace")
                self.logger.debug("🔧 XML data was bytes, decoded to UTF-8.")
            except Exception as decode_err:
                self.logger.error(f"❌ Failed to decode XML data: {decode_err}")
                return {}

        #self.logger.warning(f"📨 Incoming XML data length: {len(xml_data)}")
        #self.logger.warning(f"🔎 First 200 chars: {xml_data[:200]}")

        try:
            root = ET.fromstring(xml_data)
            for zg in root.findall(".//ZoneGroup"):
                coordinator = zg.get("Coordinator")
                group_id = zg.get("ID", coordinator)  # fallback to UUID if ID is missing
                members = []

                for member in zg.findall("ZoneGroupMember"):
                    zone_name = member.get("ZoneName", "")
                    if "sub" in zone_name.lower():
                        #self.logger.warning(f"🚫 Skipping bonded sub: {zone_name}")
                        continue  # skip Sub devices

                    uuid = member.get("UUID")
                    location = member.get("Location", "")
                    try:
                        ip = location.split("//")[1].split(":")[0] if location else "?"
                    except Exception:
                        ip = "?"

                    bonded = member.get("Invisible", "0") == "1"
                    members.append({
                        "uuid": uuid,
                        "name": zone_name,
                        "ip": ip,
                        "bonded": bonded,
                        "coordinator": (uuid == coordinator)
                    })

                if members:
                    group_dict[group_id] = {
                        "coordinator": coordinator,
                        "members": members
                    }

            #self.logger.warning(f"✅ Parsed {len(group_dict)} group(s) from ZoneGroupState.")
            for gid, group in group_dict.items():
                for m in group["members"]:
                    bonded = " (Bonded)" if m["bonded"] else ""
                    coordinator = " (Coordinator)" if m["coordinator"] else ""
                    #self.logger.warning(f"   → {m['name']} @ {m['ip']}{bonded}{coordinator}")

        except Exception as e:
            self.logger.error(f"❌ Failed to parse ZoneGroupState XML: {e}")
            return {}

        return group_dict






    def fetch_live_topology(self, ip):
        import xml.etree.ElementTree as ET
        import requests

        try:
            url = f"http://{ip}:1400/status/topology"
            resp = requests.get(url, timeout=3)
            resp.raise_for_status()
            tree = ET.fromstring(resp.content)

            groups = {}
            for zp in tree.findall(".//ZonePlayer"):
                uuid = zp.text.strip().replace("uuid:", "")
                name = zp.attrib.get("zoneName", "Unknown")
                coord = zp.attrib.get("coordinator", "false").lower() == "true"
                group = zp.attrib.get("group", "Unknown")
                ip = zp.attrib.get("location", "").split("//")[-1].split(":")[0]
                groups[uuid] = {
                    "name": name,
                    "ip": ip,
                    "group": group,
                    "is_coordinator": coord
                }

            return groups

        except Exception as e:
            self.logger.error(f"❌ fetch_live_topology({ip}) failed: {e}")
            return {}



    def rebuild_ip_to_device_map(self):
        #self.logger.warning("🔁 Rebuilding IP-to-Indigo device map...")
        self.ip_to_indigo_device = {}
        for dev in indigo.devices.iter("self"):
            ip = dev.pluginProps.get("address", "").strip()
            if ip:
                self.ip_to_indigo_device[ip] = dev


    def initialize_custom_states(self, dev):
        """Ensure required custom states exist on the device.

        States can only be defined in Devices.xml — updateStateOnServer() cannot
        create them (the server ignores the update and logs "state key ... not
        defined"). If a required key is missing, the device was created before
        the state was added to Devices.xml, so force Indigo to resync its state
        list with stateListOrDisplayStateIdChanged().

        Returns a refreshed copy of the device (or the original if no resync
        was needed), so callers can keep using an up-to-date state list.
        """
        if dev is None:
            self.logger.warning("🚫 initialize_custom_states called with None device!")
            return None

        required_keys = [
            "Grouped",
            "GROUP_Coordinator",
            "GROUP_Name",
            "ZonePlayerUUIDsInGroup",
            "ZP_LocalUID",
        ]

        missing_keys = [key for key in required_keys if key not in dev.states]
        if not missing_keys:
            return dev

        self.logger.info(f"🔧 State list for {dev.name} is missing {', '.join(missing_keys)} — resyncing from Devices.xml")
        dev.stateListOrDisplayStateIdChanged()
        dev = indigo.devices[dev.id]  # refresh local copy so it has the new state list

        still_missing = [key for key in missing_keys if key not in dev.states]
        if still_missing:
            self.logger.error(f"❌ States still missing on {dev.name} after resync: {', '.join(still_missing)} — check Devices.xml")
        else:
            self.logger.info(f"🛠 State list resynced for {dev.name}: added {', '.join(missing_keys)}")
        return dev








#################################################################################################
### Evaluate_and_update_grouped_states
#################################################################################################





    def evaluate_and_update_grouped_states(self, dev=None):
        now = time.time()
        if hasattr(self, "_last_group_eval") and now - self._last_group_eval < 3.0:
            return
        self._last_group_eval = now

        # Initialize required custom states
        if dev:
            self.logger.debug(f"⚙️ Evaluating group state for device: {dev.name}")
            dev = self.initialize_custom_states(dev) or dev
        else:
            self.logger.debug("⚙️ Evaluating group state for all Sonos devices...")
            for d in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                if d is not None:
                    self.initialize_custom_states(d)
                else:
                    self.logger.warning("🚫 Encountered None in device list — skipping.")

        bonded_names = ["sub"]
        seen_groups = set()

        #self.logger.info("🔄 Evaluating current group states 1 for all Sonos devices...")

        # 🧠 Reset evaluated group tracking cache
        self.evaluated_group_members_by_coordinator = {}

        for group_uid, group_data in self.zone_group_state_cache.items():
            coordinator_entry = group_data.get("coordinator")
            member_entries = group_data.get("members", [])

            self.logger.debug(f"🧪 Group ID: {group_uid} | Coordinator: {coordinator_entry} | Members: {len(member_entries)}")

            if group_uid in seen_groups:
                continue
            seen_groups.add(group_uid)

            # --- BEGIN: robust coordinator/members resolution (added) ---
            # Try to resolve coordinator by UUID via SoCo, but fall back to cached dict info if needed.
            coordinator_uuid = coordinator_entry.get("uuid") if isinstance(coordinator_entry, dict) else coordinator_entry
            coordinator = self.get_soco_by_uuid(coordinator_uuid)

            # Normalize members into a list of dicts with name/ip/bonded/is_coord and optional soco
            from types import SimpleNamespace
            norm_members = []
            ip_to_is_coord = {}

            for entry in member_entries:
                if isinstance(entry, dict):
                    m_uuid = entry.get("uuid")
                    m_ip   = entry.get("ip")
                    m_name = entry.get("name") or entry.get("zone_name") or ""
                    m_bond = bool(entry.get("bonded", False))
                    m_is_c = bool(entry.get("coordinator", False))
                else:
                    # legacy: bare UUID string
                    m_uuid = entry
                    m_ip, m_name, m_bond, m_is_c = None, "", False, False

                m_soco = None
                if m_uuid:
                    m_soco = self.get_soco_by_uuid(m_uuid)
                if (m_soco is None) and m_ip:
                    m_soco = self.soco_by_ip.get(m_ip)

                norm_members.append({
                    "uuid": m_uuid,
                    "ip": m_ip,
                    "name": m_name,
                    "bonded": m_bond,
                    "is_coord": m_is_c,
                    "soco": m_soco,
                })
                if m_ip:
                    ip_to_is_coord[m_ip] = m_is_c

            # If SoCo coordinator not found, try to pick the coordinator from members by cache flag
            if coordinator is None:
                for m in norm_members:
                    if m["is_coord"] and m["soco"] is not None:
                        coordinator = m["soco"]
                        break

            # Build the 'members' list as SoCo-like objects so the rest of your code can remain unchanged
            members = []
            for m in norm_members:
                if m["soco"] is not None:
                    members.append(m["soco"])
                else:
                    # lightweight proxy with .player_name and .ip_address
                    # NEW: include uid so later coordinator equality check works
                    members.append(SimpleNamespace(player_name=m["name"] or "", ip_address=m["ip"] or "", uid=m["uuid"]))
                    # (all other behavior unchanged)

            if not members:
                self.logger.warning(f"⚠️ Group {group_uid} has no resolvable members — skipping.")
                continue
            # --- END: robust coordinator/members resolution (added) ---

            # 🔍 Evaluate non-bonded members
            non_bonded_members = [
                m for m in members
                if not any(b in (m.player_name or "").lower() for b in bonded_names)
            ]
            unique_names = set((m.player_name or "").lower() for m in non_bonded_members)

            # ✅ Determine grouped status — TRUE only if more than one *non-bonded* member
            is_grouped = len(unique_names) > 1

            if not is_grouped:
                # If we didn't resolve a coordinator SoCo object, use the first member's name for logging
                base_name = coordinator.player_name if coordinator else (members[0].player_name if members else "(unknown)")
                self.logger.debug(f"🧩 Not grouped: {base_name} — fewer than 2 unique non-bonded members")

            # Prefer the coordinator’s friendly name if known, else first member name
            if coordinator:
                group_name = coordinator.player_name if is_grouped else members[0].player_name
            else:
                group_name = members[0].player_name

            # 🧠 Initialize tracking for this group
            if group_name not in self.evaluated_group_members_by_coordinator:
                self.logger.debug(f"📦 Initializing group entry for '{group_name}' in evaluated_group_members_by_coordinator")
                self.evaluated_group_members_by_coordinator[group_name] = []

            # -------- Single per-member loop (keeps all original behavior) --------
            for member in members:
                member_ip = (member.ip_address or "").strip()
                indigo_device = self.ip_to_indigo_device.get(member_ip)
                if not indigo_device:
                    #self.logger.warning(f"⚠️ No Indigo device found for {member.player_name} ({member_ip}) — skipping")
                    continue

                if dev and dev.id != indigo_device.id:
                    self.logger.debug(f"⏭ Skipping {indigo_device.name} due to dev filter (looking for ID {dev.id})")
                    continue

                expected_grouped = "true" if is_grouped else "false"

                # --- DEBUG PROBE: live-vs-uuid coordinator check (safe for proxies) ---
                try:
                    live_is_coord = bool(getattr(member, "is_coordinator", False))
                    m_uuid = getattr(member, "uid", None)
                    self.logger.debug(
                        f"coord_check name={member.player_name} "
                        f"m_uuid={m_uuid} "
                        f"coordinator_uuid={coordinator_uuid} "
                        f"live_is_coord={live_is_coord} "
                        f"expected_by_uuid={(str(m_uuid) == str(coordinator_uuid))}"
                    )
                except Exception:
                    pass
                # --- END DEBUG PROBE ---

                # --- changed: coordinator flag based on UUID equality (object identity can be unreliable) ---
                member_uuid = getattr(member, "uid", None)
                # NEW: normalize both sides to strings for reliable comparison
                expected_coord = "true" if (member_uuid is not None and coordinator_uuid is not None and str(member_uuid) == str(coordinator_uuid)) else "false"

                grouped_val = indigo_device.states.get("Grouped", "undefined")
                coord_val = indigo_device.states.get("GROUP_Coordinator", "undefined")
                name_val = indigo_device.states.get("GROUP_Name", "")

                # Update plugin-evaluated Grouped flag
                if str(grouped_val).lower() != expected_grouped:
                    self.logger.debug(f"🆙 Updating 'Grouped' state for {indigo_device.name} → {expected_grouped}")
                    self.updateStateOnServer(indigo_device, "Grouped", expected_grouped)

                # Update plugin-evaluated coordinator flag
                if str(coord_val).lower() != expected_coord:
                    self.logger.debug(f"🧭 Updating 'GROUP_Coordinator' state for {indigo_device.name} → {expected_coord}")
                    self.updateStateOnServer(indigo_device, "GROUP_Coordinator", expected_coord)

                # Explicit Group_Name update using indigo_device, not dev
                old_group_name = indigo_device.states.get("GROUP_Name", "Unavailable")
                if group_name != old_group_name:
                    caller = inspect.stack()[1].function
                    self.logger.debug(f"🧭 TRACE: Group_Name has changed — invoked from: {caller} — will write new value: {group_name}")
                    try:
                        indigo_device.updateStateOnServer("GROUP_Name", group_name)
                    except Exception as e:
                        self.logger.error(f"❌ Failed to write GROUP_Name='{group_name}' to {indigo_device.name}: {e}")

                # Fallback update if not already handled
                if "GROUP_Name" not in indigo_device.states:
                    self.logger.error(f"❌ Cannot update GROUP_Name for {indigo_device.name} — state key not defined!")
                elif group_name and group_name != name_val:
                    self.logger.debug(f"🧩 I fell back so - Updating 'GROUP_Name' for {indigo_device.name} → '{group_name}' (previous: {name_val})")
                    self.updateStateOnServer(indigo_device, "GROUP_Name", group_name)

                # ✅ Add to plugin-evaluated group tracking dict
                self.logger.debug(f"✅ Adding {indigo_device.name} to evaluated group '{group_name}'")
                self.evaluated_group_members_by_coordinator[group_name].append(indigo_device)
            # ---------------- end single per-member loop ----------------

        # ✅ Consolidated bonded device injection to ensure visibility in dump_groups_to_log()
        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            if not dev or "GROUP_Name" not in dev.states:
                continue

            group_name = dev.states.get("GROUP_Name")
            if (
                not group_name
                or group_name == "Unavailable"
                or group_name.startswith("RINCON")
            ):
                continue

            dev_id = dev.id
            dev_name_lower = dev.name.lower()

            # Identify bonded devices by name patterns
            is_bonded = any(x in dev_name_lower for x in ("left", "right", "sub", "surround"))
            if not is_bonded:
                continue

            # ✅ Ensure evaluated_group_members_by_coordinator[group_name] exists
            if group_name not in self.evaluated_group_members_by_coordinator:
                self.logger.debug(f"🧰 1st Creating missing evaluated_group_members_by_coordinator['{group_name}'] for bonded injection")
                self.evaluated_group_members_by_coordinator[group_name] = []

            # 🧠 Prevent duplicates in evaluated group member list
            if all(d.id != dev_id for d in self.evaluated_group_members_by_coordinator[group_name]):
                self.logger.debug(f"➕ 1st Injecting bonded device '{dev.name}' into evaluated group '{group_name}' (fallback)")
                self.evaluated_group_members_by_coordinator[group_name].append(dev)

            # ✅ Ensure zone_group_state_cache[group_name]['members'] exists
            if group_name not in self.zone_group_state_cache:
                self.logger.debug(f"🧰 2nd Creating missing zone_group_state_cache['{group_name}'] for bonded injection")
                self.zone_group_state_cache[group_name] = {"members": []}

            if dev_id not in self.zone_group_state_cache[group_name]["members"]:
                self.logger.debug(
                    f"➕ 2nd Injecting bonded device '{dev.name}' (ID {dev_id}) into zone_group_state_cache['{group_name}']['members'] for logging"
                )
                self.zone_group_state_cache[group_name]["members"].append(dev_id)

#        # 🎯 Post-pass to align bonded Sub grouped flag with its coordinator
#        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
#            if not dev or "sub" not in dev.name.lower():
#                name, number, ver, ip, uuid = self.get_model_meta(dev)
#                self.logger.warning(f"{dev.name}: model={name} number={number} ver={ver} ip={ip} uuid={uuid}")
#                #self.logger.warning(f"⚠️ Could not find sub in the name .... This name '{dev.name}' this current group '{sub_group}'")
#                self.logger.warning(f"⚠️ Could not find sub in the name .... This name '{dev.name}")
#                continue

        # 🎯 Post-pass to align bonded Sub grouped flag with its coordinator (IP-only)
        # 📊 DO NOT REMOVE — All-devices IP-only diagnostic pass (restores original visibility)

        # 🔎 Instrument every Indigo Sonos device (IP-only path)
        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            # Get IP only from props (strict IP policy)
            ip = ""
            try:
                ip = (dev.pluginProps.get("address", "") or "").strip()
            except Exception:
                ip = ""

            # Resolve SoCo purely by IP
            soco = self.soco_by_ip.get(ip) if ip else None
            live_group = getattr(soco, "group", None) if soco else None
            live_coord = getattr(live_group, "coordinator", None) if live_group else None
            live_name  = getattr(live_coord, "player_name", "") if live_coord else ""
            lg_uid     = getattr(live_group, "uid", None) if live_group else None
            lc_uid     = getattr(live_coord, "uid", None) if live_coord else None

            # Minimal model/uuid (optional; still IP-only semantics)
            try:
                model, number, ver, _, uuid = self.get_model_meta(dev)
            except Exception:
                model, number, ver, uuid = "Unknown", "Unknown", "Unknown", "Unknown"

            grp_name = dev.states.get("GROUP_Name", "") or ""

            # 🔔 Diagnostic line for every device
            #self.logger.warning(
            #    f"📋 Device info: {dev.name} model={model} number={number} ver={ver} "
            #    f"ip={ip or '(unknown)'} uuid={uuid or 'Unknown'} "
            #    f"live_group={lg_uid if lg_uid else 'None'} live_coord={lc_uid if lc_uid else 'None'} "
            #    f"live_name='{live_name}' group_name='{grp_name or '(empty)'}'"
            #)

            # 🛠 Normalize raw ZoneGroupTopology IDs in GROUP_Name to friendly coordinator name (IP-only source of truth)
            try:
                looks_like_raw = grp_name.startswith("RINCON_") or (":" in grp_name)
                if looks_like_raw and live_name:
                    #self.logger.info(f"🛠 Normalizing GROUP_Name for '{dev.name}' → '{live_name}' (was '{grp_name}')")
                    dev.updateStateOnServer("GROUP_Name", live_name)
            except Exception as e:
                self.logger.debug(f"GROUP_Name normalize failed for {dev.name}: {e}")

            # ⚠️ Extra visibility when IP→SoCo mapping is missing
            if ip and not soco:
                self.logger.debug(f"🧭 No SoCo mapping in soco_by_ip for {dev.name} ({ip})")










            sub_group = dev.states.get("GROUP_Name", "")
            if not sub_group or sub_group == "Unavailable":

                #name, number, ver, ip, uuid = self.get_model_meta(dev)
                #self.logger.warning(f"{dev.name}: model={name} number={number} ver={ver} ip={ip} uuid={uuid}")

                #self.logger.warning(f"⚠️ So I am a sub ... so what ... {dev.name} model name =  this current group '{sub_group}'")
                #self.logger.debug(f"🔎 Bonded resolve: {dev.name} ip={ip} live_group={getattr(live_group,'uid',None)} live_coord={getattr(live_coord,'uid',None)} live_name='{live_name}'")
                continue

            # Attempt to find coordinator for this sub's group
            coordinator = None
            for member in self.evaluated_group_members_by_coordinator.get(sub_group, []):
                if member.states.get("GROUP_Coordinator", "false") == "true":
                    coordinator = member
                    break

            if not coordinator:
                #self.logger.info(f"⚠️ Must be first initialization loop - Could not find coordinator for Sub device '{dev.name}' in group '{sub_group}' - This is normal during startup")
                continue

            coord_grouped = coordinator.states.get("Grouped", "false")
            sub_grouped = dev.states.get("Grouped", "false")

            if sub_grouped != coord_grouped:
                self.logger.debug(f"🔁 Syncing Sub '{dev.name}' Grouped flag → {coord_grouped} (match coordinator '{coordinator.name}')")
                self.updateStateOnServer(dev, "Grouped", coord_grouped)

        # ✅ 🔄 Final fix: post-pass to reassign group names and flags for bonded devices missing or showing raw RINCON names
        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            if not dev:
                continue

            name_lower = dev.name.lower()
            if not any(x in name_lower for x in ("left", "right", "sub", "surround")):
                continue

            group_name = dev.states.get("GROUP_Name", "")
            if not group_name or group_name.startswith("RINCON") or group_name == "Unavailable":
                # Try to infer from evaluated groups
                for eval_group, members in self.evaluated_group_members_by_coordinator.items():
                    for m in members:
                        if m.id == dev.id:
                            group_name = eval_group
                            break
                    if group_name != "" and not group_name.startswith("RINCON"):
                        break

                if not group_name or group_name.startswith("RINCON"):
                    #self.logger.warning(f"🔍 Could not infer clean group name for bonded device '{dev.name}' — skipping post-fix")
                    continue

                self.logger.info(f"🛠 Rewriting invalid or missing GROUP_Name for bonded '{dev.name}' → '{group_name}'")
                self.updateStateOnServer(dev, "GROUP_Name", group_name)

            # Align grouped flag with group coordinator
            coordinator = None
            for m in self.evaluated_group_members_by_coordinator.get(group_name, []):
                if m.states.get("GROUP_Coordinator", "false") == "true":
                    coordinator = m
                    break

            if not coordinator:
                self.logger.debug(f"⚠️ Could not resolve coordinator for bonded '{dev.name}' in group '{group_name}'")
                continue

            coord_grouped = coordinator.states.get("Grouped", "false")
            dev_grouped = dev.states.get("Grouped", "false")
            if dev_grouped != coord_grouped:
                self.logger.info(f"🔁 Syncing bonded '{dev.name}' Grouped flag → {coord_grouped} (match coordinator '{coordinator.name}')")
                self.updateStateOnServer(dev, "Grouped", coord_grouped)

            if dev.states.get("GROUP_Coordinator", "true") == "true":
                #self.logger.info(f"🔄 Setting bonded '{dev.name}' as non-coordinator")
                self.updateStateOnServer(dev, "GROUP_Coordinator", "false")


    def get_model_meta(self, thing):
        """Return (model_name, model_number, software_ver, ip, uuid) for either a SoCo object or Indigo device."""
        soco = None
        ip = uuid = "Unknown"
        if hasattr(thing, "speaker_info"):  # SoCo
            soco = thing
        else:
            ip = (getattr(thing, "pluginProps", {}).get("address") or "").strip()
            if ip and ip.lower() != "none":
                soco = self.soco_by_ip.get(ip)

        model_name = model_number = software_ver = "Unknown"
        if soco:
            try:
                ip = getattr(soco, "ip_address", ip) or ip
                uuid = getattr(soco, "uid", uuid) or uuid
                info = getattr(soco, "speaker_info", None) or {}
                model_name   = info.get("model_name")   or getattr(soco, "model_name", "Unknown")
                model_number = info.get("model_number") or getattr(soco, "model_number", "Unknown")
                software_ver = info.get("display_version", "Unknown")
            except Exception as e:
                self.logger.debug(f"get_model_meta: speaker_info fetch failed for {ip}: {e}")
        return model_name, model_number, software_ver, ip, uuid            
                


#################################################################################################
### End - Evaluate_and_update_grouped_states
#################################################################################################






    def get_model_meta(self, dev):
        """
        Safe model info fetch. Returns (model_name, model_number, display_version, ip, uuid)
        Works even when SoCo isn't resolved; never raises.
        """
        model_name = "Unknown"
        model_number = "Unknown"
        display_version = "Unknown"
        ip = ""
        uuid = ""

        soco, ip_guess = self._resolve_soco_from_device(dev)
        ip = ip_guess or ip

        if soco:
            try:
                info = getattr(soco, "speaker_info", None) or {}
                # Common SoCo keys, with fallbacks
                model_name = info.get("model_name") or info.get("name") or model_name
                model_number = info.get("model_number") or info.get("hardware_version") or model_number
                display_version = (info.get("display_version")
                                   or info.get("software_version")
                                   or display_version)
                ip = getattr(soco, "ip_address", ip) or ip
                uuid = getattr(soco, "uid", "") or uuid
            except Exception as e:
                self.logger.debug(f"get_model_meta: speaker_info read failed for {dev.name}: {e}")

        # Final fallbacks from Indigo states if still empty
        try:
            if not uuid:
                uuid = dev.states.get("uuid") or dev.states.get("UID") or ""
        except Exception:
            pass

        return model_name, model_number, display_version, ip, uuid






    def _resolve_soco_from_device(self, dev):
        """
        Return (soco, ip) for an Indigo device.
        Tries pluginProps address, then device states, then UUID, then name match.
        Never throws; returns (None, ip_guess) if not found.
        """
        ip = ""
        try:
            ip = (dev.pluginProps.get("address") or dev.states.get("IP") or "").strip()
        except Exception:
            pass

        soco = None
        if ip:
            soco = self.soco_by_ip.get(ip)

        # Try by UUID if available
        if soco is None:
            uuid = None
            try:
                uuid = (dev.states.get("uuid")
                        or dev.states.get("UID")
                        or dev.states.get("zUID")
                        or dev.states.get("uID"))
            except Exception:
                uuid = None
            if uuid:
                try:
                    soco = self.get_soco_by_uuid(uuid)
                    if soco is not None:
                        ip = getattr(soco, "ip_address", ip) or ip
                except Exception:
                    pass

        # Fallback: name match against known SoCo objects
        if soco is None:
            dev_name = (dev.name or "").strip().lower()
            zone_hint = (dev.states.get("zoneName", "") or "").strip().lower()
            for s in self.soco_by_ip.values():
                try:
                    pn = (s.player_name or "").strip().lower()
                    if pn and (pn == dev_name or pn == zone_hint):
                        soco = s
                        ip = getattr(soco, "ip_address", ip) or ip
                        break
                except Exception:
                    continue

        return soco, ip






    # helpers (put near top of class or with your other utils)
    def _has_state(self, dev, key):
        try:
            return key in getattr(dev, "states", {})
        except Exception:
            return False

    def _update_state_if_exists(self, dev, key, value):
        if self._has_state(dev, key):
            try:
                dev.updateStateOnServer(key, value)
            except Exception as e:
                self.logger.debug(f"⚠️ Failed updating state '{key}' on {dev.name}: {e}")

    # --- lifecycle hooks ---

    def deviceStopComm(self, dev):
        """Indigo lifecycle hook: tear down comms for a single device cleanly."""
        try:
            self.logger.info(f"🛑 deviceStopComm → {dev.name} ({dev.id})")

            # 1) Unsubscribe from SoCo events for this device
            try:
                subs = None
                if hasattr(self, "soco_subs"):
                    # keys may be str or int depending on where they were inserted
                    subs = self.soco_subs.pop(str(dev.id), None) or self.soco_subs.pop(dev.id, None)
                if subs:
                    # A network unsubscribe against an offline player blocks in connect
                    # timeouts — with several devices this makes Indigo force-kill the
                    # plugin on reload. Only unsubscribe over the network if the player
                    # answers a quick probe; otherwise just cancel the local auto-renew
                    # (the player-side subscription expires on its own).
                    reachable = self.is_host_reachable(dev.address, timeout=1.0)
                    for svc_name, sub in list(subs.items()):
                        try:
                            if reachable:
                                sub.unsubscribe()
                                self.logger.debug(f"🔕 Unsubscribed {svc_name} for {dev.name}")
                            else:
                                try:
                                    sub._auto_renew_cancel()  # SoCo internal, best-effort
                                except Exception:
                                    pass
                                self.logger.debug(f"🔕 Skipped network unsubscribe ({svc_name}, {dev.name} offline); cancelled auto-renew")
                        except Exception as e:
                            self.logger.debug(f"⚠️ Unsubscribe failed ({svc_name}, {dev.name}): {e}")
            except Exception as e:
                self.logger.debug(f"soco_subs cleanup failed for {dev.name}: {e}")

            # 2) Cancel any per-device timers/pollers
            try:
                if hasattr(self, "device_pollers"):
                    poller = self.device_pollers.pop(dev.id, None)
                    if poller:
                        try:
                            poller.cancel()
                        except Exception:
                            pass
            except Exception as e:
                self.logger.debug(f"poller cleanup failed for {dev.name}: {e}")

            # 3) Clean local maps — match IP-keyed entries by device id where possible
            # so entries made under an old address (IP just changed in the config
            # dialog) are purged too, not only the current one.
            try:
                dev_ip = (dev.pluginProps.get("address") or dev.address or "").strip()
                if hasattr(self, "devices") and isinstance(self.devices, dict):
                    self.devices.pop(dev.id, None)
                if hasattr(self, "deferred_start_devices"):
                    self.deferred_start_devices.discard(dev.id)
                if hasattr(self, "ip_to_indigo_device"):
                    stale_ips = [k for k, v in self.ip_to_indigo_device.items()
                                 if getattr(v, "id", None) == dev.id]
                    for ip in stale_ips:
                        self.ip_to_indigo_device.pop(ip, None)
                        for map_name in ("soco_by_ip", "ip_to_soco_device", "uid_by_ip"):
                            m = getattr(self, map_name, None)
                            if isinstance(m, dict):
                                m.pop(ip, None)
                for map_name in ("soco_by_ip", "ip_to_soco_device", "uid_by_ip"):
                    m = getattr(self, map_name, None)
                    if isinstance(m, dict):
                        m.pop(dev_ip, None)
            except Exception as e:
                self.logger.debug(f"map cleanup failed for {dev.name}: {e}")

            # 4) OPTIONAL: mark device offline, but only if such a state exists
            # (Many Indigo devices don't define 'onOffState', so guard it.)
            self._update_state_if_exists(dev, "onOffState", False)
            self._update_state_if_exists(dev, "commPresent", False)  # also guarded; use only if your device defines it

        except Exception as e:
            self.logger.error(f"❌ deviceStopComm error for {dev.name}: {e}")

    def whackdeviceStartComm(self, dev):
        """Indigo lifecycle hook: bring device online."""
        try:
            self.logger.info(f"▶️ deviceStartComm → {dev.name} ({dev.id})")
            # Reattach subscriptions if you do that per-device (optional)
            # self.attach_subscriptions_for_device(dev)

            # Guarded state updates
            self._update_state_if_exists(dev, "onOffState", True)
            self._update_state_if_exists(dev, "commPresent", True)

        except Exception as e:
            self.logger.error(f"❌ deviceStartComm error for {dev.name}: {e}")








    def _bootstrap_now_from_zgt(self):
        """
        One-shot bootstrap that fetches ZoneGroupTopology immediately and then runs the
        same normalization/evaluation steps you run after a ZGT-driven change.
        """
        # Loud entry log so you can see it ran
        self.logger.debug("🚀 BOOTSTRAP: starting post-startup normalization from live ZoneGroupTopology")

        try:
            # Pick a reference IP: prefer your configured/root, else any discovered
            ip = (getattr(self, "rootZPIP", None) or self.getReferencePlayerIP() or "").strip()
            if not ip:
                # last-ditch: try any device from the Indigo list
                for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
                    ip = (dev.pluginProps.get("address") or dev.address or "").strip()
                    if ip:
                        break

            if not ip:
                self.logger.error("❌ BOOTSTRAP: no ZonePlayer IP available to query GetZoneGroupState")
                return

            # Pull ZGT directly (same data events carry)
            # NOTE: using your SOAPSend + parseDirty helpers so it matches the plugin's other calls
            resp = self.SOAPSend(ip, "/ZoneGroupTopology", "/ZoneGroupTopology", "GetZoneGroupState", "")
            zone_state_xml = self.parseDirty(resp, "<ZoneGroupState>", "</ZoneGroupState>") or ""

            if not zone_state_xml:
                self.logger.debug("⚠️ BOOTSTRAP: GetZoneGroupState returned no ZoneGroupState XML")
                # even if empty, still run your existing steps below so nothing is skipped
            else:
                # Parse into the same structure your event path uses
                try:
                    parsed_groups = self.parse_zone_group_state(zone_state_xml)
                    if parsed_groups:
                        # Mirror your ZGT event path: update cache under lock
                        import copy
                        with self.zone_group_state_lock:
                            self.zone_group_state_cache = copy.deepcopy(parsed_groups)
                        self.logger.info(f"💾 BOOTSTRAP: zone_group_state_cache seeded with {len(parsed_groups)} group(s)")
                    else:
                        self.logger.debug("⚠️ BOOTSTRAP: parsed_groups is empty")
                except Exception as e:
                    self.logger.error(f"❌ BOOTSTRAP: parse_zone_group_state failed: {e}")

            # === Run the same things you run after a ZGT change ===
            try:
                self.refresh_group_topology_after_plugin_zone_change()
            except Exception as e:
                self.logger.debug(f"BOOTSTRAP: refresh_group_topology_after_plugin_zone_change() failed (continuing): {e}")

            try:
                # push updated grouped states to Indigo devices
                for dev in indigo.devices.iter("self"):
                    self.updateZoneGroupStates(dev)
            except Exception as e:
                self.logger.debug(f"BOOTSTRAP: updateZoneGroupStates() sweep failed (continuing): {e}")

            try:
                self._refresh_all_group_states_helper(reason="_bootstrap_now_from_zgt")
                #self.refresh_all_group_states()
            except Exception as e:
                self.logger.debug(f"BOOTSTRAP: refresh_all_group_states() failed (continuing): {e}")

            try:
                self.evaluate_and_update_grouped_states()
            except Exception as e:
                self.logger.debug(f"BOOTSTRAP: evaluate_and_update_grouped_states() failed (continuing): {e}")

            # Optional: make the first dump match your “after change” dumps
            try:
                self.dump_group_state_to_log()
                self.audit_all_sonos_devices()
            except Exception as e:
                self.logger.debug(f"BOOTSTRAP: audit/dump skipped: {e}")

            # Your original extras you wanted at startup
            try:
                self.getSoundFiles()
            except Exception as e:
                self.logger.error(f"❌ BOOTSTRAP: getSoundFiles failed (continuing): {e}")

        finally:
            self.logger.debug("✅ BOOTSTRAP: finished post-startup normalization")


    def refresh_group_topology_after_plugin_zone_change(self):
        #self.logger.warning("🔁 Manually refreshing group topology after plugin-initiated zone change...")

        try:
            # 🧯 Debounce — an announcement ungroups/regroups several zones in quick
            # succession and each change lands here; without this, every call walks
            # every player with 5s-timeout fetches (the "ZGT storm" of issue #16).
            # Only debounce once the cache has populated at least once, so rapid-fire
            # startup calls (devices now start fast) can't starve the first real fetch.
            now = time.time()
            if getattr(self, "zone_group_state_cache", None) and \
                    now - getattr(self, "_last_topology_refresh", 0.0) < 3.0:
                self.logger.debug("⏳ Skipping topology refresh (debounced — ran <3s ago)")
                return
            self._last_topology_refresh = now
            if not hasattr(self, "_zgt_unreachable_until"):
                self._zgt_unreachable_until = {}

            # NEW: ensure coordinator-by-IP map exists on the instance for downstream use
            if not hasattr(self, "_eval_coord_dev_by_ip") or not isinstance(getattr(self, "_eval_coord_dev_by_ip"), dict):
                self._eval_coord_dev_by_ip = {}

            import http.client as httplib
            import xml.etree.ElementTree as ET

            def get_zone_group_state_from_player(ip):
                try:
                    conn = httplib.HTTPConnection(ip, 1400, timeout=5)
                    conn.request("GET", "/status/zp")
                    response = conn.getresponse()
                    if response.status == 200:
                        return response.read()
                    else:
                        self.logger.warning(f"⚠️ Failed HTTP ZGT fetch from {ip}: status {response.status}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Exception fetching ZGT from {ip}: {e}")
                return None

            def parse_zone_group_state(xml_data):
                groups = {}
                try:
                    if isinstance(xml_data, bytes):
                        xml_data = xml_data.decode("utf-8", errors="ignore")
                    elif not isinstance(xml_data, str):
                        xml_data = str(xml_data)

                    xml_data = xml_data.strip()
                    if not xml_data.startswith("<"):
                        raise ValueError("XML does not start with expected '<'")

                    #self.logger.warning("🛠 ENTERED parse_zone_group_state()")
                    #self.logger.warning(f"📨 Incoming XML data length: {len(xml_data)}")
                    #self.logger.warning(f"🔎 First 200 chars: {xml_data[:200]}")

                    root = ET.fromstring(xml_data)
                    for group in root.findall(".//ZoneGroup"):
                        group_id = group.get("ID")
                        coordinator_uuid = group.get("Coordinator")
                        members = []

                        for member in group.findall("ZoneGroupMember"):
                            zone_name = member.get("ZoneName", "").strip().lower()
                            uuid = member.get("UUID", "").strip()
                            location = member.get("Location", "").strip()

                            if zone_name == "sub":
                                #self.logger.warning(f"🚫 Skipping bonded sub: {zone_name}")
                                continue

                            members.append({
                                "uuid": uuid,
                                "location": location,
                                "zone_name": zone_name,
                            })

                        groups[group_id] = {
                            "coordinator": coordinator_uuid,
                            "members": members,
                        }

                    #self.logger.warning(f"🧪 Parsed {len(groups)} group(s) from XML.")
                except Exception as e:
                    self.logger.error(f"❌ XML parse error in zone group topology: {e}")
                return groups

            #for ip in self.soco_by_ip.keys():
            for ip in list(self.soco_by_ip.keys()):
                # Skip players that recently failed a reachability probe (30s negative
                # cache) — walking dead hosts at 5s timeout each is what melted things
                # down in issue #16 once a couple of speakers dropped off the network.
                if self._zgt_unreachable_until.get(ip, 0.0) > now:
                    continue
                if not self.is_host_reachable(ip, timeout=1.0):
                    self._zgt_unreachable_until[ip] = now + 30.0
                    self.logger.debug(f"📴 Skipping ZGT fetch from unreachable {ip} (cached for 30s)")
                    continue
                raw_xml = get_zone_group_state_from_player(ip)
                if raw_xml:
                    parsed = parse_zone_group_state(raw_xml)
                    if parsed:
                        self.zone_group_state_cache = parsed
                        self.logger.debug(f"💾 zone_group_state_cache updated 2 with {len(parsed)} group(s)")
                        break

            # 🔄 Rebuild critical mappings before group state evaluation
            if hasattr(self, "rebuild_ip_to_device_map"):
                self.rebuild_ip_to_device_map()
            if hasattr(self, "rebuild_uuid_maps_from_soco"):
                self.rebuild_uuid_maps_from_soco()
                self.logger.debug(f"📌 DEBUG: uuid_to_indigo_device now contains {len(self.uuid_to_indigo_device)} entries")

            # NEW: ensure IP→coordinator device cache always exists (avoids NameError downstream)
            try:
                if not hasattr(self, "_eval_coord_dev_by_ip") or self._eval_coord_dev_by_ip is None:
                    self._eval_coord_dev_by_ip = {}
            except Exception:
                # Failsafe: guarantee a dict even if an unexpected type is present
                self._eval_coord_dev_by_ip = {}

            #self.logger.info("📣 Calling evaluate_and_update_grouped_states() after ZoneGroupTopology change...")
            self.evaluate_and_update_grouped_states()

        except Exception as e:
            self.logger.error(f"❌ Exception in refresh_group_topology_after_plugin_zone_change: {e}")











    def refresh_group_membership(self, indigo_device, soco_device):
        try:
            group = soco_device.group
            coordinator = group.coordinator
            devices_in_group = group.members

            coordinator_ip = coordinator.ip_address.strip()
            is_coordinator = (coordinator_ip == indigo_device.address.strip())
            #self.trace_me(indigo_device)
            current_group_name = coordinator.player_name or ""

            # Update coordinator and group name state
            indigo_device.updateStateOnServer("GROUP_Coordinator", str(is_coordinator).lower())
            indigo_device.updateStateOnServer("GROUP_Name", current_group_name)
            self.safe_debug(f"🔄 Updated {indigo_device.name} → GROUP_Coordinator: {is_coordinator}, GROUP_Name: {current_group_name}")

            # === Centralized album art handling ===
            try:
                if indigo_device:
                    self.update_album_artwork(dev=indigo_device, zone_ip=indigo_device.address.strip())
                else:
                    self.logger.debug("⚠️ Skipping artwork update — Indigo device is undefined")
            except Exception as e:
                self.logger.debug(f"⚠️ Failed to update album artwork for {indigo_device.name if indigo_device else 'Unknown'}: {e}")

            # === Playback state refresh for coordinator ===
            if is_coordinator:
                current_track_info = soco_device.get_current_track_info()
                transport_info = soco_device.get_current_transport_info()

                zp_state = transport_info.get('current_transport_state', 'STOPPED').upper()
                current_track_uri = current_track_info.get('uri', '')
                current_title = current_track_info.get('title', '')
                current_artist = current_track_info.get('artist', '')
                current_creator = current_track_info.get('creator', '')                

                indigo_device.updateStateOnServer("ZP_STATE", zp_state)
                indigo_device.updateStateOnServer("ZP_TRACK", current_title or "")
                indigo_device.updateStateOnServer("ZP_ARTIST", current_artist or "")
                indigo_device.updateStateOnServer("ZP_CREATOR", current_creator or "")                
                indigo_device.updateStateOnServer("ZP_CurrentTrackURI", current_track_uri or "")

                # Derive and update ZP_SOURCE
                try:
                    source = self.determineSource(indigo_device, soco_device, transport_info, current_track_info)
                    indigo_device.updateStateOnServer("ZP_SOURCE", source)
                    self.safe_debug(f"🛰️ Set {indigo_device.name} ZP_SOURCE → {source}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to determine ZP_SOURCE for {indigo_device.name}: {e}")

                self.safe_debug(f"🔄 Refreshed standalone states for {indigo_device.name} → State: {zp_state}, Track: {current_title}, Artist: {current_artist}")

            else:
                # === Sync slave states from coordinator device ===
                master_dev = next(
                    (dev for dev in indigo.devices if dev.address.strip() == coordinator_ip),
                    None
                )

                if master_dev:
                    for state_key in ["ZP_STATE", "ZP_TRACK", "ZP_ARTIST", "ZP_CREATOR", "ZP_SOURCE", "ZP_MUTE","ZP_CurrentTrackURI", "ZP_ART"]:
                        master_value = master_dev.states.get(state_key, "")
                        indigo_device.updateStateOnServer(state_key, master_value)
                        self.safe_debug(f"🔄 Synced slave {indigo_device.name} {state_key} → {master_value}")
                else:
                    self.logger.warning(f"⚠️ Could not find master device {coordinator_ip} to sync states for slave {indigo_device.name}")

        except Exception as e:
            self.logger.error(f"❌ Exception in refresh_group_membership for {indigo_device.name}: {e}")


    def determineSource(self, indigo_device, soco_device, transport_info, track_info):
        try:
            uri = track_info.get("uri", "") or ""
            if "x-sonosapi-stream" in uri:
                return "SiriusXM"
            elif "pandora.com" in uri:
                return "Pandora"
            elif "spotify" in uri:
                return "Spotify"
            elif "tunein" in uri:
                return "TuneIn"
            elif "airplay" in uri:
                return "AirPlay"
            elif uri.startswith("x-rincon-mp3radio:"):
                return "Internet Radio"
            elif uri.startswith("x-rincon-queue:"):
                return "Queue"
            else:
                return "Unknown"
        except Exception as e:
            self.logger.warning(f"⚠️ determineSource failed for {indigo_device.name}: {e}")
            return "Unknown"






    def getIndigoDeviceFromEvent(self, event_obj):
        sid = getattr(event_obj, "sid", "")
        for dev_id, subs in self.soco_subs.items():
            if any(sub.sid == sid for sub in subs.values()):
                return indigo.devices[int(dev_id)]
        return None





#################################################################################################
### Update Album Art
#################################################################################################


    def old_update_album_artwork(self, event_obj=None, dev=None, zone_ip=None):
        import requests, shutil, io, filecmp, time, os
        from PIL import Image

        ARTWORK_FOLDER = "/Library/Application Support/Perceptive Automation/images/Sonos/"
        DEFAULT_ART_PATH = ARTWORK_FOLDER + "default_artwork.jpg"
        DEFAULT_ART_SRC = os.path.join(os.path.dirname(__file__), "default_artwork.jpg")
        MAX_DOWNLOAD_ATTEMPTS = 3

        os.makedirs(ARTWORK_FOLDER, exist_ok=True)
        if not os.path.exists(DEFAULT_ART_PATH):
            try:
                shutil.copy(DEFAULT_ART_SRC, DEFAULT_ART_PATH)
                self.logger.info(f"✅ Default artwork copied to {DEFAULT_ART_PATH}")
            except Exception as e:
                self.logger.error(f"❌ Failed to copy default artwork: {e}")
                return

        # ✅ Step 1: Infer zone_ip from dev if not provided
        if not zone_ip and dev:
            try:
                zone_ip = dev.address.strip()
                if not zone_ip:
                    self.logger.debug(f"⚠️ dev.address is empty for {dev.name}")
                    zone_ip = None
            except Exception as e:
                self.logger.debug(f"⚠️ Failed to extract IP from dev: {e}")
                zone_ip = None

        # ✅ Step 2: Try resolving zone_ip from event if not yet available
        if not zone_ip and event_obj:
            zone_ip = getattr(getattr(event_obj, "soco", None), "ip_address", None)

        # ✅ Step 3: Infer dev from event if not passed
        if not dev and event_obj:
            dev = self.getIndigoDeviceFromEvent(event_obj)

        # 🚫 Final guard: require both dev and zone_ip
        if not dev or not zone_ip:
            self.logger.debug(f"⚠️ Could not resolve device or IP for album art update — dev: {getattr(dev, 'name', '?')} | zone_ip: {zone_ip}")
            return

        self.logger.debug(f"🎯 Art update entry → dev={dev}, zone_ip={zone_ip}, event_meta={getattr(getattr(event_obj, 'variables', {}), 'get', lambda *_: None)('current_track_meta_data', None)}")

        # ✅ Step 4: Locate SoCo device and group info
        soco_device = self.getSoCoDeviceByIP(zone_ip)
        if not soco_device:
            self.logger.debug(f"⚠️ No SoCo device found for IP {zone_ip}")
            return

        try:
            group = soco_device.group
            coordinator = group.coordinator
        except Exception as e:
            self.logger.debug(f"⚠️ Failed to access group or coordinator for {zone_ip}: {e}")
            return

        is_master = ((coordinator.ip_address or "").strip() == zone_ip)
        coordinator_ip = (coordinator.ip_address or "").strip()
        coordinator_dev = self.ip_to_indigo_device.get(coordinator_ip)

        master_artwork_path = f"{ARTWORK_FOLDER}sonos_art_{coordinator_ip}.jpg"
        art_url = None

        # === Coordinator logic: fetch and save artwork ===
        if is_master:
            # If we have an event, try to refresh the master image from the player
            if event_obj:
                meta = getattr(getattr(event_obj, "variables", {}), "get", lambda *_: None)("current_track_meta_data", None)
                album_art_uri = getattr(meta, "album_art_uri", "") if meta else ""

                if album_art_uri.startswith("/"):
                    album_art_uri = f"http://{zone_ip}:1400{album_art_uri}"

                if album_art_uri:
                    for attempt in range(1, MAX_DOWNLOAD_ATTEMPTS + 1):
                        try:
                            self.logger.debug(f"🎨 Attempting album art fetch from {album_art_uri} (attempt {attempt})")
                            response = requests.get(album_art_uri, timeout=(3, 15))
                            if response.status_code == 200:
                                image = Image.open(io.BytesIO(response.content))
                                image.thumbnail((500, 500))
                                image = image.convert("RGB")
                                image.save(master_artwork_path, format="JPEG", quality=75)
                                break
                        except Exception as e:
                            self.logger.debug(f"⚠️ Failed to fetch album art: {e}")
                            time.sleep(0.5)

            # Ensure we can publish a URL for the coordinator even without a fresh event
            if os.path.exists(master_artwork_path):
                art_url = f"http://localhost:8888/sonos_art_{coordinator_ip}.jpg"
            else:
                try:
                    shutil.copyfile(DEFAULT_ART_PATH, master_artwork_path)
                except Exception as e:
                    self.logger.debug(f"⚠️ Failed to stage default artwork for coordinator {coordinator_ip}: {e}")
                art_url = "http://localhost:8888/default_artwork.jpg"

            if coordinator_dev:
                coordinator_dev.updateStateOnServer("ZP_ART", art_url)

        # 🛡️ Use Indigo's Grouped state as the sole propagation flag, but log drift against SoCo.
        coordinator_grouped_flag = "false"
        if coordinator_dev:
            coordinator_grouped_flag = coordinator_dev.states.get("Grouped", "false")

        # Build member lists and filter out bonded members (sub/left/right/surround)
        bonded_member_ips = []
        soco_member_ips = []
        try:
            members = (getattr(group, "members", []) or [])
            for m in members:
                ip = (getattr(m, "ip_address", "") or "").strip()
                if not ip:
                    continue
                soco_member_ips.append(ip)
                name_lc = (getattr(m, "player_name", "") or "").lower()
                if "sub" in name_lc or "left" in name_lc or "right" in name_lc or "surround" in name_lc:
                    bonded_member_ips.append(ip)
        except Exception:
            pass

        # Only count NON-BONDED members toward grouping
        non_bonded_ips = [ip for ip in soco_member_ips if ip not in set(bonded_member_ips)]
        soco_grouped_nonbonded = (len(set(non_bonded_ips)) > 1)

        # 🔧 Corrected drift condition: compare Indigo.Grouped to SoCo NON-BONDED grouping
        #if (coordinator_grouped_flag == "true" and not soco_grouped_nonbonded) or \
        #   (coordinator_grouped_flag != "true" and soco_grouped_nonbonded):

        #   self.logger.info(f"✅ ")
            #self.logger.info(
            #    "⚠️ Grouped state drift detected in artwork called function — This is ok during initialization - "
            #    f"Indigo.Grouped={coordinator_grouped_flag}, SoCo.non_bonded_members>1={soco_grouped_nonbonded}, "
            #    f"coord_ip={coordinator_ip}, all_members={soco_member_ips}, bonded={bonded_member_ips}, non_bonded={non_bonded_ips}"
            #)

        # Only propagate if Indigo says Grouped == "true"
        if not coordinator_dev or coordinator_grouped_flag != "true":
            self.logger.debug(
                f"⛔ Skipping artwork propagation — Indigo.Grouped={coordinator_grouped_flag}, coord={coordinator_dev.name if coordinator_dev else 'Unknown'}"
            )
            return

        # === Slave devices: copy master art ===
        # Make sure the master image exists (fallback to default so we never block propagation)
        if not os.path.exists(master_artwork_path):
            self.logger.debug(f"⚠️ Master art missing for coord {coordinator_ip}; using default for propagation")
            master_artwork_path = DEFAULT_ART_PATH

        for member in (getattr(group, "members", []) or []):
            member_ip = (member.ip_address or "").strip()
            if not member_ip or member_ip == coordinator_ip:
                continue

            slave_dev = self.ip_to_indigo_device.get(member_ip)
            if not slave_dev:
                self.logger.debug(f"⚠️ No Indigo device for slave {getattr(member, 'player_name', member_ip)} ({member_ip})")
                continue

            slave_art_path = f"{ARTWORK_FOLDER}sonos_art_{member_ip}.jpg"
            try:
                if (not os.path.exists(slave_art_path)) or (not filecmp.cmp(master_artwork_path, slave_art_path, shallow=False)):
                    shutil.copyfile(master_artwork_path, slave_art_path)
                    self.logger.debug(f"🖼️ Copied artwork to slave {slave_dev.name}")
                slave_dev.updateStateOnServer("ZP_ART", f"http://localhost:8888/sonos_art_{member_ip}.jpg")
            except Exception as e:
                self.logger.error(f"❌ Failed copying art to {slave_dev.name}: {e}")
                # Still publish a URL so UI isn't blank
                slave_dev.updateStateOnServer("ZP_ART", "http://localhost:8888/default_artwork.jpg")

        # === Standalone player handling if no event and not a coordinator ===
        if not is_master and not event_obj:
            # Use whatever we already have (or default) for this standalone device
            fallback_path = f"{ARTWORK_FOLDER}sonos_art_{zone_ip}.jpg"
            if not os.path.exists(fallback_path):
                try:
                    shutil.copyfile(DEFAULT_ART_PATH, fallback_path)
                except Exception:
                    pass
            dev.updateStateOnServer("ZP_ART", f"http://localhost:8888/sonos_art_{zone_ip}.jpg")




    def update_album_artwork(self, event_obj=None, dev=None, zone_ip=None):
        #self.logger.info(f"🖼️ Running update_album_artwork for {zone_ip}")           
        """
        Refresh/stage the coordinator's artwork file and update its ZP_ART state.
        Then delegate slave propagation to propagate_artwork_to_slaves().
        """
        import requests, shutil, io, os, time
        from PIL import Image

        ARTWORK_FOLDER   = "/Library/Application Support/Perceptive Automation/images/Sonos/"
        DEFAULT_ART_PATH = ARTWORK_FOLDER + "default_artwork.jpg"
        DEFAULT_ART_SRC  = os.path.join(os.path.dirname(__file__), "default_artwork.jpg")
        MAX_DOWNLOAD_ATTEMPTS = 3

        # Ensure paths exist
        os.makedirs(ARTWORK_FOLDER, exist_ok=True)
        if not os.path.exists(DEFAULT_ART_PATH):
            try:
                shutil.copy(DEFAULT_ART_SRC, DEFAULT_ART_PATH)
                self.logger.info(f"✅ Default artwork copied to {DEFAULT_ART_PATH}")
            except Exception as e:
                self.logger.error(f"❌ Failed to copy default artwork: {e}")
                return

        # --- Resolve dev / zone_ip ---
        if not zone_ip and dev:
            try:
                zone_ip = (dev.address or "").strip() or None
            except Exception:
                zone_ip = None

        if not zone_ip and event_obj:
            zone_ip = getattr(getattr(event_obj, "soco", None), "ip_address", None)

        if not dev and event_obj:
            dev = self.getIndigoDeviceFromEvent(event_obj)

        if not dev or not zone_ip:
            self.logger.debug(f"⚠️ update_album_artwork: cannot resolve dev/zone_ip (dev={getattr(dev,'name','?')}, ip={zone_ip})")
            return

        # --- Find SoCo, group, coordinator ---
        soco_device = self.getSoCoDeviceByIP(zone_ip)
        if not soco_device:
            self.logger.debug(f"⚠️ update_album_artwork: no SoCo for {zone_ip}")
            return

        try:
            group       = soco_device.group
            coordinator = group.coordinator
        except Exception as e:
            self.logger.debug(f"⚠️ update_album_artwork: group/coordinator access failed for {zone_ip}: {e}")
            return

        coord_ip  = (getattr(coordinator, "ip_address", "") or "").strip()
        is_master = (coord_ip == zone_ip)

        # Prefer lookup via IP→device map; fall back to current dev if it matches
        coordinator_dev = self.ip_to_indigo_device.get(coord_ip)
        if not coordinator_dev and is_master:
            coordinator_dev = dev
        if not coordinator_dev:
            self.logger.warning(f"⚠️ update_album_artwork: no Indigo device for coordinator IP {coord_ip}")
            return

        master_art_path = os.path.join(ARTWORK_FOLDER, f"sonos_art_{coord_ip}.jpg")

        # --- (Best effort) refresh the master image if we're on the coordinator or we have an event ---
        # Try event-provided art first
        album_art_uri = ""
        if event_obj:
            try:
                meta = getattr(getattr(event_obj, "variables", {}), "get", lambda *_: None)("current_track_meta_data", None)
                album_art_uri = getattr(meta, "album_art_uri", "") if meta else ""
                if album_art_uri and album_art_uri.startswith("/"):
                    album_art_uri = f"http://{coord_ip}:1400{album_art_uri}"
            except Exception:
                pass

        # If no art via event, try a quick SoCo read (only if we’re the master)
        if not album_art_uri and is_master:
            try:
                ti = soco_device.get_current_track_info() or {}
                album_art_uri = ti.get("album_art_uri") or ti.get("album_art") or ""
                if album_art_uri and album_art_uri.startswith("/"):
                    album_art_uri = f"http://{coord_ip}:1400{album_art_uri}"
            except Exception:
                pass

        if album_art_uri:
            for attempt in range(1, MAX_DOWNLOAD_ATTEMPTS + 1):
                try:
                    self.logger.debug(f"🎨 Fetching album art {album_art_uri} (attempt {attempt})")
                    r = requests.get(album_art_uri, timeout=(3, 15))
                    if r.status_code == 200:
                        img = Image.open(io.BytesIO(r.content))
                        img.thumbnail((500, 500))
                        img = img.convert("RGB")
                        img.save(master_art_path, format="JPEG", quality=75)
                        break
                except Exception as e:
                    self.logger.debug(f"⚠️ Album art fetch failed: {e}")
                    time.sleep(0.4)

        # Ensure master file exists
        if not os.path.exists(master_art_path):
            try:
                shutil.copyfile(DEFAULT_ART_PATH, master_art_path)
            except Exception as e:
                self.logger.debug(f"⚠️ Could not stage default master art for {coord_ip}: {e}")

        # Update the coordinator’s ZP_ART
        coordinator_dev.updateStateOnServer("ZP_ART", f"http://localhost:8888/sonos_art_{coord_ip}.jpg")

        # Hand off slave propagation — single place for slave logic
        try:
            self.propagate_artwork_to_slaves(coordinator_dev)
        except Exception as e:
            self.logger.warning(f"⚠️ propagate_artwork_to_slaves failed: {e}")










#################################################################################################
### End - 
#################################################################################################



    def old_propagate_artwork_to_slaves(self, coordinator_dev):
        #self.logger.info(f"🖼️ Running propagate_artwork_to_slaves for {coordinator_dev.address}")        
        """
        Copy coordinator's album artwork to all grouped slaves.
        Safe to call any time after grouping or media changes.
        """
        import os, shutil, filecmp

        ARTWORK_FOLDER = "/Library/Application Support/Perceptive Automation/images/Sonos/"
        DEFAULT_ART_PATH = ARTWORK_FOLDER + "default_artwork.jpg"

        if not coordinator_dev:
            self.logger.warning("⚠️ propagate_artwork_to_slaves called with no coordinator_dev")
            return

        coord_ip = (coordinator_dev.address or "").strip()
        if not coord_ip:
            self.logger.warning(f"⚠️ Coordinator {coordinator_dev.name} has no IP address")
            return

        master_art_path = f"{ARTWORK_FOLDER}sonos_art_{coord_ip}.jpg"
        if not os.path.exists(master_art_path):
            self.logger.warning(f"⚠️ No master artwork file for {coordinator_dev.name} ({coord_ip}), falling back to default")
            master_art_path = DEFAULT_ART_PATH

        # Identify all Indigo devices that share the same group name and are grouped
        group_name = coordinator_dev.states.get("GROUP_Name", "")
        if not group_name:
            #self.logger.warning(f"⚠️ Coordinator {coordinator_dev.name} has no GROUP_Name, skipping propagation")


            ip = (dev.address or "").strip()
            soco = self.ip_to_soco_device.get(ip)
            is_coord, is_grouped, gname = self._soco_group_truth(soco)
            self.logger.debug(f"[coord-seed] {dev.name} ip={ip} live(coord={is_coord}, grouped={is_grouped}, name='{gname}')")
            # Always perform the seed write for the coordinator; members will follow via the helper.
            self._set_group_states(dev, grouped=is_grouped, is_coord=is_coord, group_name=gname or dev.name)


            return

        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            if dev.id == coordinator_dev.id:
                continue  # skip coordinator itself
            if str(dev.states.get("Grouped", "false")).lower() != "true":
                continue
            if dev.states.get("GROUP_Name", "") != group_name:
                continue

            slave_ip = (dev.address or "").strip()
            if not slave_ip:
                continue

            slave_art_path = f"{ARTWORK_FOLDER}sonos_art_{slave_ip}.jpg"
            try:
                if (not os.path.exists(slave_art_path)) or (not filecmp.cmp(master_art_path, slave_art_path, shallow=False)):
                    shutil.copyfile(master_art_path, slave_art_path)
                    self.logger.debug(f"🖼️ Copied artwork to slave {dev.name}")

                dev.updateStateOnServer("ZP_ART", f"http://localhost:8888/sonos_art_{slave_ip}.jpg")
            except Exception as e:
                self.logger.error(f"❌ Failed copying art to {dev.name}: {e}")
                dev.updateStateOnServer("ZP_ART", "http://localhost:8888/default_artwork.jpg")





    def propagate_artwork_to_slaves(self, coordinator_dev):
        #self.logger.info(f"🖼️ Running propagate_artwork_to_slaves for {coordinator_dev.address}")        
        """
        Copy coordinator's album artwork to all grouped slaves.
        Safe to call any time after grouping or media changes.
        """
        import os, shutil, filecmp

        ARTWORK_FOLDER = "/Library/Application Support/Perceptive Automation/images/Sonos/"
        DEFAULT_ART_PATH = ARTWORK_FOLDER + "default_artwork.jpg"

        if not coordinator_dev:
            self.logger.warning("⚠️ propagate_artwork_to_slaves called with no coordinator_dev")
            return

        coord_ip = (coordinator_dev.address or "").strip()
        if not coord_ip:
            self.logger.warning(f"⚠️ Coordinator {coordinator_dev.name} has no IP address")
            return

        master_art_path = f"{ARTWORK_FOLDER}sonos_art_{coord_ip}.jpg"
        if not os.path.exists(master_art_path):
            self.logger.warning(f"⚠️ No master artwork file for {coordinator_dev.name} ({coord_ip}), falling back to default")
            master_art_path = DEFAULT_ART_PATH

        # Identify all Indigo devices that share the same group name and are grouped
        group_name = coordinator_dev.states.get("GROUP_Name", "")
        if not group_name:
            #self.logger.warning(f"⚠️ Coordinator {coordinator_dev.name} has no GROUP_Name, skipping propagation")

            # ✅ FIX: use coordinator_dev and its IP instead of undefined 'dev'
            ip = coord_ip
            soco = (getattr(self, "ip_to_soco_device", {}).get(ip)
                    or getattr(self, "soco_by_ip", {}).get(ip))
            is_coord, is_grouped, gname = self._soco_group_truth(soco)
            self.logger.debug(f"[coord-seed] {coordinator_dev.name} ip={ip} "
                              f"live(coord={is_coord}, grouped={is_grouped}, name='{gname}')")
            # Always perform the seed write for the coordinator; members will follow via the helper.
            self._set_group_states(coordinator_dev, grouped=is_grouped, is_coord=is_coord,
                                   group_name=gname or coordinator_dev.name)

            return

        for dev in indigo.devices.iter("com.ssi.indigoplugin.Sonos"):
            if dev.id == coordinator_dev.id:
                continue  # skip coordinator itself
            if str(dev.states.get("Grouped", "false")).lower() != "true":
                continue
            if dev.states.get("GROUP_Name", "") != group_name:
                continue

            slave_ip = (dev.address or "").strip()
            if not slave_ip:
                continue

            slave_art_path = f"{ARTWORK_FOLDER}sonos_art_{slave_ip}.jpg"
            try:
                if (not os.path.exists(slave_art_path)) or (not filecmp.cmp(master_art_path, slave_art_path, shallow=False)):
                    shutil.copyfile(master_art_path, slave_art_path)
                    self.logger.debug(f"🖼️ Copied artwork to slave {dev.name}")

                dev.updateStateOnServer("ZP_ART", f"http://localhost:8888/sonos_art_{slave_ip}.jpg")
            except Exception as e:
                self.logger.error(f"❌ Failed copying art to {dev.name}: {e}")
                dev.updateStateOnServer("ZP_ART", "http://localhost:8888/default_artwork.jpg")





    # Debug shim so legacy/self.debugLog calls don't explode
    def debugLog(self, msg: str):
        if getattr(self, "stateUpdatesDebug", False):
            try:
                self.logger.debug(msg)
            except Exception:
                pass

    # ─────────────────────────────────────────────────────────────────────────────
    # Plugin-level wrapper: safe state update + optional propagation to slaves
    # Keep this method on the SonosPlugin class so call sites like self.updateStateOnServer(...) work.
    # ─────────────────────────────────────────────────────────────────────────────
    def updateStateOnServer(self, dev, state, value):
        # 1) Guard: state must exist
        if state not in dev.states:
            self.logger.error(f"❌ Tried to update undefined state '{state}' on device '{dev.name}'")
            return

        # 2) Debug (respect your existing flag)
        if getattr(self, "stateUpdatesDebug", False):
            # self.debugLog(...) may not exist on your class; use logger.debug to avoid attribute errors
            self.logger.debug(u"\t Updating Device: %s, State: %s, Value: %s" % (dev.name, state, value))

        # 3) If this device is not the coordinator, block writes to group-only states
        # ❗️Changed: do NOT block the write anymore; only use this to influence propagation later.
        GROUP_Coordinator = dev.states.get('GROUP_Coordinator', "false")
        # Note: We intentionally removed the early return that skipped writes for ZoneGroupStates
        # when GROUP_Coordinator == "false". That was causing 'Grouped' to stay false and
        # triggering drift warnings during startup/transients.

        # 4) Normalize value (Indigo 2024 is Python 3; don't encode to bytes)
        val = "" if value in (None, "None") else str(value)

        # 5) Write to the device
        dev.updateStateOnServer(state, val)

        # 6) Maintain your fallback cache for GROUP_Name (unchanged behavior)
        if state == "GROUP_Name":
            if not hasattr(self, "group_name_by_device_id"):
                self.group_name_by_device_id = {}
            self.group_name_by_device_id[dev.id] = val

        # 7) Post-write verification (unchanged semantics)
        try:
            refreshed = indigo.devices[dev.id]
            _ = refreshed.states.get(state, "<missing>")
            # self.logger.info(f"🧪 POST-WRITE REFETCH: {refreshed.name} {state} = {_}")
        except Exception as e:
            self.logger.warning(f"⚠️ Post-write re-fetch failed for {dev.name}: {e}")

        # 8) Propagate group-relevant states from coordinator to slaves (your original intent)
        if GROUP_Coordinator == "true":
            try:
                # Expect ZoneGroupStates to be defined elsewhere in your module (unchanged)
                try:
                    is_group_state = (state in ZoneGroupStates)
                except NameError:
                    # If ZoneGroupStates isn't in scope, log and treat as non-group state (no propagation)
                    self.logger.warning("⚠️ ZoneGroupStates not defined; skipping slave propagation for this update.")
                    is_group_state = False

                if not is_group_state:
                    return

                # Parse the coordinator's current group membership list
                zone_list_str = dev.states.get('ZonePlayerUUIDsInGroup', "") or ""
                ZonePlayerUUIDsInGroup = [s.strip() for s in zone_list_str.split(",") if s.strip()]

                # Nothing to propagate if the group is a single member
                if len(ZonePlayerUUIDsInGroup) <= 1:
                    return

                # self.debugLog("Replicate state to slave ZonePlayers...")
                if getattr(self, "stateUpdatesDebug", False):
                    self.logger.debug("Replicate state to slave ZonePlayers...")

                # Optional special handling for current URI, keep existing behavior
                uri_group = dev.states.get("ZP_CurrentURIGroup", "")

                # Iterate over all Sonos devices in Indigo (use your plugin ID)
                # If your devices are typed with the device type id "ZonePlayer" under your plugin,
                # you can also use: indigo.devices.iter("self.ZonePlayer")
                for rdev in indigo.devices.iter("self.ZonePlayer"):
                    SlaveUID = rdev.states.get('ZP_LocalUID')
                    if not SlaveUID:
                        continue

                    if (
                        SlaveUID != dev.states.get('ZP_LocalUID') and
                        rdev.states.get('GROUP_Coordinator') == "false" and
                        SlaveUID in ZonePlayerUUIDsInGroup
                    ):
                        slave_val = "" if value in (None, "None") else str(value)
                        if state == "ZP_CurrentURI":
                            slave_val = uri_group + dev.states.get('ZP_LocalUID', "")
                        if getattr(self, "stateUpdatesDebug", False):
                            self.logger.debug(u"\t Updating Device: %s, State: %s, Value: %s" % (rdev.name, state, slave_val))
                        rdev.updateStateOnServer(state, slave_val)

            except Exception as e:
                self.logger.error(f"❌ Propagation error for coordinator '{dev.name}' state '{state}': {e}")








    def updateStateOnSlaves(self, dev):
            self.plugin.debugLog("Update all states to slave ZonePlayers...")
            ZonePlayerUUIDsInGroup = dev.states['ZonePlayerUUIDsInGroup']
            for rdev in indigo.devices.iter("self.ZonePlayer"):
                SlaveUID = rdev.states['ZP_LocalUID']
                GROUP_Coordinator = rdev.states['GROUP_Coordinator']
                # Do not update if you are yourself, not a slave, and not in the group
                if SlaveUID != dev.states['ZP_LocalUID'] and GROUP_Coordinator == "false" and SlaveUID in ZonePlayerUUIDsInGroup:
                    for state in list(ZoneGroupStates):
                        if state == "ZP_CurrentURI":
                            value = uri_group + dev.states['ZP_LocalUID']
                        else:
                            value = dev.states[state]
                        if self.plugin.stateUpdatesDebug:
                            self.plugin.debugLog(u"\t Updating Slave Device: %s, State: %s, Value: %s" % (rdev.name, state, value))
                        rdev.updateStateOnServer(state, value)
                    rdev.updateStateOnServer("ZP_ART", dev.states['ZP_ART'])
                    try:
                        shutil.copy2("/Library/Application Support/Perceptive Automation/images/Sonos/"+dev.states['ZP_ZoneName']+"_art.jpg", \
                            "/Library/Application Support/Perceptive Automation/images/Sonos/"+rdev.states['ZP_ZoneName']+"_art.jpg")
                    except:
                        pass

    def copyStateFromMaster(self, dev):
        self.plugin.debugLog("Copy states from master ZonePlayer...")

        group_name = dev.states.get("GROUP_Name", "")
        if not isinstance(group_name, str):
            self.logger.error(f"❌ GROUP_Name is not a string: {group_name!r} (type: {type(group_name).__name__})")
            return

        if ":" not in group_name:
            self.logger.error(f"❌ GROUP_Name is malformed (no ':'): {group_name!r}")
            return

        try:
            MasterUID, x = group_name.split(":")
        except Exception as e:
            self.logger.error(f"❌ Failed to split GROUP_Name '{group_name}': {e}")
            return

        for mdev in indigo.devices.iter("self.ZonePlayer"):
            if mdev.states['ZP_LocalUID'] == MasterUID:
                for state in list(ZoneGroupStates):
                    if state == "ZP_CurrentURI":
                        value = uri_group + mdev.states['ZP_LocalUID']
                    else:
                        value = mdev.states[state]
                    if self.plugin.stateUpdatesDebug:
                        self.plugin.debugLog(u"\t Updating Slave Device: %s, State: %s, Value: %s" % (dev.name, state, value))
                    dev.updateStateOnServer(state, value)

                dev.updateStateOnServer("ZP_ART", mdev.states['ZP_ART'])

                try:
                    shutil.copy2(
                        f"/Library/Application Support/Perceptive Automation/images/Sonos/{mdev.states['ZP_ZoneName']}_art.jpg",
                        f"/Library/Application Support/Perceptive Automation/images/Sonos/{dev.states['ZP_ZoneName']}_art.jpg"
                    )
                except Exception as e:
                    self.logger.warning(f"⚠️ Artwork copy failed: {e}")






# Check for messages
    #def initZones(self, dev):
    def initZones(self, dev, soco_device=None):        
        MyzonePlayerID='120169368'
        zoneIP = dev.pluginProps["address"]
        self.plugin.debugLog(u"Resetting States for zone: %s" % zoneIP)
        self.updateStateOnServer (dev, "ZP_ALBUM", "")
        self.updateStateOnServer (dev, "ZP_ART", "")
        self.updateStateOnServer (dev, "ZP_ARTIST", "")
        self.updateStateOnServer (dev, "ZP_SOURCE", "")        
        self.updateStateOnServer (dev, "ZP_CREATOR", "")
        self.updateStateOnServer (dev, "ZP_CurrentURI", "")
        self.updateStateOnServer (dev, "ZP_DURATION", "")
        self.updateStateOnServer (dev, "ZP_RELATIVE", "")
        self.updateStateOnServer (dev, "ZP_INFO", "")
        self.updateStateOnServer (dev, "ZP_MUTE", "")
        self.updateStateOnServer (dev, "ZP_STATE", "")
        self.updateStateOnServer (dev, "ZP_STATION", "")
        self.updateStateOnServer (dev, "ZP_TRACK", "")
        self.updateStateOnServer (dev, "ZP_VOLUME", "")
        self.updateStateOnServer (dev, "ZP_VOLUME_FIXED", "")
        self.updateStateOnServer (dev, "ZP_BASS", "")
        self.updateStateOnServer (dev, "ZP_TREBLE", "")
        self.updateStateOnServer (dev, "ZP_ZoneName", "")
        self.updateStateOnServer (dev, "ZP_LocalUID", "")
        self.updateStateOnServer (dev, "ZP_AIName", "")
        self.updateStateOnServer (dev, "ZP_AIPath", "")
        self.updateStateOnServer (dev, "ZP_NALBUM", "")
        self.updateStateOnServer (dev, "ZP_NART", "")
        self.updateStateOnServer (dev, "ZP_NARTIST", "")
        self.updateStateOnServer (dev, "ZP_NCREATOR", "")       
        self.updateStateOnServer (dev, "ZP_NTRACK", "")
        self.updateStateOnServer (dev, "Q_Crossfade", "off")
        self.updateStateOnServer (dev, "Q_Repeat", "off")
        self.updateStateOnServer (dev, "Q_RepeatOne", "off")
        self.updateStateOnServer (dev, "Q_Shuffle", "off")
        self.updateStateOnServer (dev, "Q_Number", "0")
        self.updateStateOnServer (dev, "Q_ObjectID", "")
        self.updateStateOnServer (dev, "GROUP_Coordinator", "")
        self.updateStateOnServer (dev, "GROUP_Name", "")
        self.updateStateOnServer (dev, "ZP_CurrentTrack", "")
        self.updateStateOnServer (dev, "ZP_CurrentTrackURI", "")
        self.updateStateOnServer (dev, "ZoneGroupID", "")
        self.updateStateOnServer (dev, "ZoneGroupName", "")
        self.updateStateOnServer (dev, "ZonePlayerUUIDsInGroup", "")
        self.updateStateOnServer (dev, "alive", "")
        self.updateStateOnServer (dev, "bootseq", "")

        url = u"http://" + zoneIP + ":1400/status/zp"
        try:
            response = requests.get(url, timeout=5)
            root = ET.fromstring(response.content)
            ZoneName = root.findtext('.//ZoneName')
            LocalUID = root.findtext('.//LocalUID')
            #SerialNumber = '5C-AA-FD-5B-5C-D6:4'
            MyzonePlayerID='120169368'
            SerialNumber = root.findtext('.//SerialNumber')
        except:
            self.plugin.errorLog("Error getting ZonePlayer data: %s" % url)
            self.plugin.errorLog("  Offending ZonePlayer: %s" % dev.name)
            self.plugin.errorLog("  ZonePlayer may be physically turned off or in a bad state.")
            self.plugin.errorLog("  Please disable communications or remove from Indigo.")
            if dev.id in self.deviceList:  # guard: raised "list.remove(x): x not in list" (issue #16)
                self.deviceList.remove(dev.id)
            dev.setErrorStateOnServer(u"error")
            return

        #self.updateStateOnServer (dev, "ZP_ZoneName", ZPInfo.findtext('ZoneName').decode('utf-8'))
        # Allow for special characters in ZoneName
        self.updateStateOnServer (dev, "ZP_ZoneName", ZoneName)
        self.updateStateOnServer (dev, "ZP_LocalUID", LocalUID)
        self.updateStateOnServer (dev, "SerialNumber", SerialNumber)

        self.getModelName (dev)

        self.updateZoneGroupStates (dev)
        self.updateZoneTopology (dev)

        indigo.server.log ("Adding ZonePlayer: %s, %s, %s" % (zoneIP, LocalUID, dev.name))
        self.ZonePlayers.append (LocalUID)
        if hasattr(dev, "pluginProps"):
            self.ZPTypes.append([LocalUID, dict(dev.pluginProps).get("model", "")])
        else:
            self.logger.warning(f"⚠️ Skipping pluginProps access — dev is not an Indigo device (type: {type(dev)})")

        self.zonePlayerState[dev.id] = {'zonePlayerAlive':True}
        self.updateStateOnServer (dev, "alive", time.asctime())

        if self.EventProcessor == "SoCo":
            self.socoSubscribe(dev, soco_device)


    def getModelName(self, dev):
        url = u"http://" + dev.pluginProps["address"] + ":1400/xml/device_description.xml"
        response = requests.get(url, timeout=5)
        if response.ok:
            root = ET.fromstring(response.content)
            ModelName = root.findtext('.//{urn:schemas-upnp-org:device-1-0}displayName')
            self.updateStateOnServer (dev, "ModelName", ModelName)
        else:
            self.plugin.errorLog("[%s] Cannot get ModelName for ZonePlayer: %s" % (time.asctime(), dev.name))




    def updateZoneTopology(self, dev):
        # Deprecated in Sonos 10.1
        #url = u"http://" + dev.pluginProps["address"] + ":1400/status/topology"
        #response = requests.get(url)
        #if response.ok:
        #   root = ET.fromstring(response.content)
        #   for ZonePlayer in root.findall("./ZonePlayers/ZonePlayer"):
        #       if ZonePlayer.get('uuid') == dev.states['ZP_LocalUID']:
        #           self.updateStateOnServer (dev, "GROUP_Coordinator", ZonePlayer.get('coordinator'))
        #           self.updateStateOnServer (dev, "bootseq", ZonePlayer.get('bootseq'))
        #else:
        #   self.plugin.errorLog("[%s] Cannot get ZoneGroupTopology for ZonePlayer: %s" % (time.asctime(), dev.name))

        res = self.restoreString(self.SOAPSend (self.rootZPIP, "/ZonePlayer", "/ZoneGroupTopology", "GetZoneGroupState", ""),1)
        ZGS = ET.fromstring(res)
        for ZoneGroup in ZGS.findall('.//ZoneGroup'):
            for ZonePlayer in ZoneGroup.findall('.//ZoneGroupMember'):
                if ZonePlayer.attrib['UUID'] == dev.states['ZP_LocalUID']:
                    if ZonePlayer.attrib['UUID'] == ZoneGroup.attrib['Coordinator']:
                        self.updateStateOnServer (dev, "GROUP_Coordinator", 'true')
                    else:
                        self.updateStateOnServer (dev, "GROUP_Coordinator", 'false')
                    #self.trace_me()
                    self.updateStateOnServer (dev, "GROUP_Name", ZoneGroup.attrib['ID'])                
                    self.updateStateOnServer (dev, "bootseq", ZonePlayer.attrib['BootSeq'])
 

    def updateZoneGroupStates(self, dev):
        zoneIP = dev.pluginProps["address"]
        res = self.SOAPSend(zoneIP, "/ZonePlayer", "/ZoneGroupTopology", "GetZoneGroupAttributes", "")

        # ✅ Removed .decode('utf-8') – not needed in Python 3
        self.updateStateOnServer(dev, "ZoneGroupName", self.parseCurrentZoneGroupName(res))
        self.updateStateOnServer(dev, "ZoneGroupID", self.parseCurrentZoneGroupID(res))
        self.updateStateOnServer(dev, "ZonePlayerUUIDsInGroup", self.parseCurrentZonePlayerUUIDsInGroup(res))


    def parsePoint (self, res, startString, stopString):
        loc = str(res).find(startString)
        if (loc > 0):
            loc_beg = loc + len(startString)
            loc_end = str(res).find(stopString, loc_beg)
            return (self.restoreString(str(res)[loc_beg:loc_end],0))
        else:
            return ""

    def parseDirty (self, res, startString, stopString):
        loc = str(res).find(startString)
        if (loc > 0):
            loc_beg = loc + len(startString)
            loc_end = str(res).find(stopString, loc_beg)
            return (str(res)[loc_beg:loc_end])
        else:
            return ""
    
    def parseFirstTrackNumberEnqueued(self, deviceId, res):
        loc = str(res).find("<FirstTrackNumberEnqueued>")
        if (loc > 0):
            loc_beg = loc + len("<FirstTrackNumberEnqueued>")
            loc_end = str(res).find("</FirstTrackNumberEnqueued>", loc_beg)
            item = self.restoreString(str(res)[loc_beg:loc_end],0)
            return item

    def parseRelTime(self, deviceId, res):
        return self.parsePoint (res, "<RelTime>", "</RelTime>")

    def parseCurrentZoneGroupName(self, res):
        return self.parsePoint (res, "<CurrentZoneGroupName>", "</CurrentZoneGroupName>")

    def parseCurrentZoneGroupID(self, res):
        return self.parsePoint (res, "<CurrentZoneGroupID>", "</CurrentZoneGroupID>")

    def parseCurrentZonePlayerUUIDsInGroup(self, res):
        return self.parsePoint (res, "<CurrentZonePlayerUUIDsInGroup>", "</CurrentZonePlayerUUIDsInGroup>")

    def parseCurrentVolume(self, res):
        return self.parsePoint (res, "<CurrentVolume>", "</CurrentVolume>")

    def parseCurrentMute(self, res):
        return self.parsePoint (res, "<CurrentMute>", "</CurrentMute>")

    def parseCurrentTransportActions(self, res):
        return self.parsePoint (res, "<Actions>", "</Actions>")

    def parseErrorCode(self, res):
        return self.parsePoint (res, "<errorCode>", "</errorCode>")

    def parseBrowseNumberReturned(self, res):
        return self.parsePoint (res, "<NumberReturned>", "</NumberReturned>")

    def parseAssignedObjectID(self, res):
        return self.parsePoint (res, "<AssignedObjectID>", "</AssignedObjectID>")

    def parsePandoraToken(self, res):
        return self.parsePoint (res, "&m=", "&f")

    def playRadio(self, zoneIP, l2p):
        self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "SetAVTransportURI", "<CurrentURI>"+l2p+"</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:upnp=\"urn:schemas-upnp-org:metadata-1-0/upnp/\" xmlns:r=\"urn:schemas-rinconnetworks-com:metadata-1-0/\" xmlns=\"urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/\"&gt;&lt;item id=\"-1\" parentID=\"-1\" restricted=\"true\"&gt;&lt;dc:title&gt;RADIO&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;&lt;desc id=\"cdudn\" nameSpace=\"urn:schemas-rinconnetworks-com:metadata-1-0/\"&gt;SA_RINCON65031_&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData>")
        self.SOAPSend (zoneIP, "/MediaRenderer", "/AVTransport", "Play", "<Speed>1</Speed>")






    def updateGroupPlaybackStates(self, coordinator_dev):
        """
        Runtime method: Propagates current playback metadata from the coordinator to all grouped slave devices.
        Only runs after startup and assumes device states are generally initialized.
        """
        try:
            #self.trace_me()
            self.logger.info(f"🔄 Runtime: Updating playback metadata to slaves for group '{coordinator_dev.states.get('GROUP_Name', 'Unknown')}'")

            coordinator_ip = coordinator_dev.address.strip()
            soco_device = self.soco_by_ip.get(coordinator_ip)
            if not soco_device:
                self.logger.debug(f"⚠️ Runtime: No SoCo found for coordinator {coordinator_dev.name} @ {coordinator_ip}")
                return

            group = soco_device.group
            if not group:
                self.logger.warning(f"⚠️ Runtime: SoCo group is None for {coordinator_dev.name}")
                return

            group_member_ips = {member.ip_address.strip() for member in group.members}
            slave_devices = [
                dev for dev in indigo.devices.iter("self")
                if dev.address.strip() in group_member_ips and dev.id != coordinator_dev.id
            ]

            # Ensure all slave devices have expected state keys
            for slave_dev in slave_devices:
                self.safe_initialize_states(slave_dev)

            # Define all playback-related state keys to copy
            playback_keys = [
                "Album", "Artist", "Track", "Source", "state",
                "CurrentAlbum", "CurrentArtist", "CurrentTrack", "CurrentSource",
                "CurrentAlbumURI", "CurrentTrackURI", "CurrentTrackArt",
                "albumArtURL", "Q_Album", "Q_Artist", "Q_Track", "Q_Source"
            ]

            # Propagate coordinator state values to all slaves
            for slave_dev in slave_devices:
                for key in playback_keys:
                    value = coordinator_dev.states.get(key, "")
                    try:
                        if value is None:
                            value = ""
                        slave_dev.updateStateOnServer(key, value)
                    except Exception as e:
                        self.logger.warning(f"⚠️ Failed to update key '{key}' on slave {slave_dev.name}: {e}")

        except Exception as e:
            self.exception_handler(e, True)









    def safe_initialize_states(self, dev):
        """
        Ensures that all expected state keys are initialized for the given device.
        This method mirrors the behavior of deviceStartComm() to prevent 'state key not defined' errors.
        """
        #self.trace_me()
        try:
            # Define all expected state keys with default empty values
            expected_keys = [
                "Album", "Artist", "Track", "Source", "state",
                "CurrentAlbum", "CurrentArtist", "CurrentTrack", "CurrentSource",
                "CurrentAlbumURI", "CurrentTrackURI", "CurrentTrackArt",
                "albumArtURL", "Q_Album", "Q_Artist", "Q_Track", "Q_Source",
                "GROUP_Coordinator", "GROUP_Name", "ZP_ART", "ZP_LocalUID", "ZonePlayerUUIDsInGroup"
            ]

            for key in expected_keys:
                if key not in dev.states:
                    dev.updateStateOnServer(key, "")
                    self.logger.debug(f"Initialized state key '{key}' for device '{dev.name}'.")

        except Exception as e:
            self.logger.error(f"Error initializing states for device '{dev.name}': {e}")






    def copyStateFromMaster(self, dev):
        try:
            #self.trace_me()
            self.safe_debug("Copy states from master ZonePlayer...")
            try:
                MasterUID, x = dev.states['GROUP_Name'].split(":")
            except Exception as exception_error:
                self.logger.error(f"copyStateFromMaster - Unable to split Group Name: {dev.states['GROUP_Name']}")
                return

            for mdev in indigo.devices.iter("self.ZonePlayer"):
                if mdev.states['ZP_LocalUID'] == MasterUID:
                    for state in list(ZoneGroupStates):
                        if state == "ZP_CurrentURI":
                            value = uri_group + mdev.states['ZP_LocalUID']
                        else:
                            value = mdev.states[state]
                        if self.plugin.stateUpdatesDebug:
                            self.safe_debug(f"\t Updating Slave Device: {dev.name}, State: {state}, Value: {value}")
                        dev.updateStateOnServer(state, value)
                    dev.updateStateOnServer("ZP_ART", mdev.states['ZP_ART'])
                    try:
                        shutil.copy2("/Library/Application Support/Perceptive Automation/images/Sonos/"+mdev.states['ZP_ZoneName']+"_art.jpg",
                                     "/Library/Application Support/Perceptive Automation/images/Sonos/"+dev.states['ZP_ZoneName']+"_art.jpg")
                    except Exception as exception_error:
                        pass

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getLocale(self):
        try:
            locale.setlocale(locale.LC_ALL, '')
            return locale.getdefaultlocale()[0]

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement




    def get_soco_device(self, ip):
        if ip in self.soco_by_ip:
            return self.soco_by_ip[ip]

        self.logger.debug(f"get_soco_device: IP {ip} not in soco_by_ip cache — creating direct SoCo instance.")
        try:
            soco_device = soco.SoCo(ip)
            self.soco_by_ip[ip] = soco_device
            return soco_device
        except Exception as e:
            self.logger.error(f"❌ get_soco_device: Could not find device with IP {ip} — {e}")
            return None



    from soco.data_structures import to_didl_string

 


    def getPlaylistsDirect(self):
        try:
            self.logger.info("📡 Loading Sonos Playlists...")

            soco_device = self.get_soco_device(self.rootZPIP)
            if not soco_device:
                self.logger.error("❌ getPlaylistsDirect: No SoCo device found.")
                return

            playlists = soco_device.get_sonos_playlists(complete_result=True)
            Sonos_Playlists.clear()

            self.safe_debug(f"🧪 Using SoCo device: {soco_device} ({soco_device.player_name})")
            self.safe_debug(f"🧪 Raw playlists returned: {playlists}")

            for pl in playlists:
                try:
                    eid = getattr(pl, "item_id", None)
                    title = getattr(pl, "title", "Unnamed Playlist")

                    # Handle Sonos item_id that might be in formats like SQ:5 or ...#5
                    if eid:
                        if eid.startswith("SQ:"):
                            uri = eid
                        elif "#" in eid:
                            uri = f"SQ:{eid.split('#')[1]}"
                        else:
                            uri = None
                    else:
                        uri = None

                    if uri:
                        Sonos_Playlists.append((uri, title, eid, pl))
                        self.safe_debug(f"➕ Playlist loaded: {title} | URI: {uri} | ID: {eid}")
                    else:
                        self.logger.warning(f"⚠️ Skipped playlist: {title} — item_id missing or unrecognized format: {eid}")

                except Exception as pe:
                    self.logger.warning(f"⚠️ Error loading playlist object: {pl} — {pe}")

            self.safe_debug(f"🧪 Final dump of Sonos_Playlists entries:")
            for entry in Sonos_Playlists:
                self.safe_debug(f"🧾 {entry}")

            self.logger.info(f"✅ Loaded {len(Sonos_Playlists)} Sonos playlists.")

        except Exception as e:
            self.logger.error(f"❌ getPlaylistsDirect: {e}")





    def getRT_FavStationsDirect(self):
        try:
            global Sonos_RT_FavStations
            list_count = 0
            Sonos_RT_FavStations = []
            ZP  = self.restoreString(self.SOAPSend(self.rootZPIP, "/MediaServer", "/ContentDirectory", "Browse", "<ObjectID>R:0/0</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria>"), 1)
            # self.safe_debug(f"ZP: {ZP}")
            ZPxml = ET.fromstring(ZP)
            # iter = ZPxml.getiterator()
            iter = list(ZPxml.iter())
            for element in iter:
                if str(element).find("}item") >= 0:
                    if element.keys():
                        for name, value in element.items():
                            if name == "id":
                                e_id = value
                    # for child in element.getchildren():
                    for child in list(element.iter()):
                        ctag = str(child.tag).split('}')
                        if ctag[1] == "title":
                            e_title = child.text
                        elif ctag[1] == "res":
                            e_res = self.restoreString(child.text, 0)
                    Sonos_RT_FavStations.append((e_res, e_title))
                    self.safe_debug(f"\tRadioTime Favorite Station: {e_id}, {e_title}, {e_res}")
                    list_count = list_count + 1
            self.logger.info(f"Loaded RadioTime Favorite Stations... [{list_count}]")

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getPandora(self, PandoraEmailAddress, PandoraPassword, PandoraNickname):
        global Sonos_Pandora

        self.logger.debug("🧪 Starting getPandora()")
        self.logger.debug(f"🧪 Pandora flag: {self.pluginPrefs.get('Pandora')}")
        self.logger.debug(f"🧪 Email: {PandoraEmailAddress}")
        self.logger.debug(f"🧪 Password: {'***' if PandoraPassword else '(empty)'}")
        self.logger.debug(f"🧪 Nickname: {PandoraNickname}")
        self.safe_debug(f"✅ Sonos_Pandora currently has {len(Sonos_Pandora)} entries")

        # 🛡️ Validate credentials early
        if not PandoraEmailAddress or not PandoraPassword:
            self.logger.warning("⚠️ Missing Pandora email or password — skipping getPandora()")
            return

        try:
            list_count = 0
            pandora = Pandora()

            self.logger.debug("🧪 Calling Pandora.authenticate()...")
            result = pandora.authenticate(PandoraEmailAddress, PandoraPassword)
            self.logger.debug(f"🧪 Returned from authenticate(): {result}")

            if not result:
                self.logger.error("❌ Pandora authentication failed — skipping station fetch.")
                return

            self.logger.info("🧪 Authentication successful — calling get_station_list()")
            stations = pandora.get_station_list()

            for station in stations:
                Sonos_Pandora.append((
                    station.get('stationId'),
                    station.get('stationName'),
                    PandoraEmailAddress,
                    PandoraNickname or ''
                ))
                self.safe_debug(f"📻 Pandora Station: {station.get('stationId')} - {station.get('stationName')}")

                list_count += 1

            self.logger.info(f"✅ Loaded Pandora Stations for {PandoraNickname or '(no nickname)'}: [{list_count}]")

        except Exception as exception_error:
            self.logger.error(f"❌ Exception in getPandora(): {exception_error}")
            self.exception_handler(exception_error, True)



    def get_artwork_filename(self, dev_name):
        # Normalize device name: lowercase, underscores instead of spaces
        safe_name = dev_name.lower().replace(" ", "_")
        return f"sonos_art_{safe_name}.jpg"


    def cleanup_old_artwork(self):
        import os
        import time

        artwork_dir = "/Library/Application Support/Perceptive Automation/images/Sonos/"
        now = time.time()
        cutoff = now - (2 * 24 * 60 * 60)  # 2 days ago

        deleted = 0
        for filename in os.listdir(artwork_dir):
            if filename.startswith("sonos_art_") and filename.endswith(".jpg"):
                filepath = os.path.join(artwork_dir, filename)
                if os.path.isfile(filepath):
                    if os.path.getmtime(filepath) < cutoff:
                        try:
                            os.remove(filepath)
                            deleted += 1
                            self.logger.info(f"🗑️ Deleted stale artwork file: {filename}")
                        except Exception as e:
                            self.logger.warning(f"⚠️ Could not delete {filename}: {e}")

        if deleted > 0:
            self.logger.info(f"🧹 Artwork cleanup done: {deleted} file(s) removed.")
        else:
            self.logger.info("🧹 No stale artwork files found.")





    def getSiriusXM(self):
        try:
            #from SiriusHelper import SiriusXM  # this must be placed inside the function for Indigo plugin compatibility

            zoneIP = self.getReferencePlayerIP()
            if not zoneIP:
                self.logger.error("❌ getSiriusXM: No reference ZonePlayer IP found.")
                return

            if not self.SiriusXMID or not self.SiriusXMPassword:
                self.logger.error("❌ getSiriusXM: SiriusXM credentials missing.")
                return

            self.logger.info(f"🔐 Attempting SiriusXM login for {self.SiriusXMID}")

            sxm = SiriusXM(self.SiriusXMID, self.SiriusXMPassword)
            if not sxm.authenticate():
                self.logger.error("❌ SiriusXM authentication failed.")
                return

            channels = sxm.get_channels()
            self.logger.info(f"✅ Loaded {len(channels)} SiriusXM channels.")
            
            # Optional: store them globally or assign to Indigo states
            global Sonos_SiriusXM
            Sonos_SiriusXM = []
            for ch in channels:
                number = ch.get("siriusChannelNumber", 0)
                name = ch.get("name", "Unknown")
                channelId = ch.get("channelId", "")
                channelGuid = ch.get("channelGuid", "")
                Sonos_SiriusXM.append((int(number), channelId, name, channelGuid))
                self.safe_debug(f"\t📻 {number}: {name} ({channelId})")

            Sonos_SiriusXM.sort(key=lambda x: x[0])

        except Exception as exception_error:
            self.exception_handler(exception_error, True)

    def getSoundFiles(self):
        try:
            self.Sound_Files = []  # << correct instance var
            list_count = 0

            self.logger.debug(f"🔍 Scanning for MP3s in: {self.SoundFilePath}")
            for f in listdir(self.SoundFilePath):
                self.logger.debug(f"🧪 Found file in folder: {f}")
                if f.lower().endswith(".mp3"):
                    self.Sound_Files.append(f)
                    self.logger.info(f"🎵 Added sound file: {f}")
                    list_count += 1

            self.logger.info(f"✅ Loaded Sound Files... [{list_count}]")
        except Exception as exception_error:
            self.exception_handler(exception_error, True)





    #################################################################################################
    ### SOAPSend function with custom filtering for known specific error responses as needed 
    #################################################################################################



    def SOAPSend(self, zoneIP, soapRoot, soapBranch, soapAction, soapPayload):
        try:
            if soapBranch == "/Queue":
                urn = "schemas-sonos-com"
            else:
                urn = "schemas-upnp-org"

            self.safe_debug(f"zoneIP: {zoneIP}, soapRoot: {soapRoot}, soapBranch: {soapBranch}, soapAction: {soapAction}")

            # Convert soapPayload to a string if currently bytes
            if isinstance(soapPayload, bytes):
                soapPayload = soapPayload.decode("utf-8")

            SM_TEMPLATE = (
                '<?xml version="1.0" encoding="utf-8"?>'
                '<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" '
                'xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'
                '<s:Body>'
                f'<ns0:{soapAction} xmlns:ns0="urn:{urn}:service:{soapBranch[1:]}:1">'
                '<InstanceID>0</InstanceID>'
                f'{soapPayload}'
                f'</ns0:{soapAction}>'
                '</s:Body></s:Envelope>'
            )

            SoapMessage = SM_TEMPLATE
            base_url = f"http://{zoneIP}:1400"

            if soapRoot == "/ZonePlayer":
                control_url = f"{soapBranch}/Control"
            else:
                control_url = f"{soapRoot}{soapBranch}/Control"

            soap_action = f"urn:{urn}:service:{soapBranch[1:]}:1#{soapAction}"
            headers = {
                'Content-Type': 'text/xml; charset="utf-8"',
                'Content-Length': str(len(SoapMessage)),
                'Host': f"{zoneIP}:1400",
                'User-Agent': 'Indigo',
                'SOAPACTION': soap_action
            }

            try:
                response = requests.post(base_url + control_url, headers=headers, data=SoapMessage.encode("utf-8"), timeout=(5, 20))
            except Exception as exception_error:
                self.logger.error(f"SOAPSend Error: {exception_error}")
                raise

            res_bytes = response.text.encode("utf-8")
            res = res_bytes.decode("utf-8")
            status = response.status_code

            # Handle non-200 errors AFTER checking errorCode
            if status != 200:
                try:
                    errorCode = self.parseErrorCode(res)

                    if errorCode == "714":
                        self.logger.info(f"🔁 Ignoring benign UPNP error 714 — already using own queue.")
                        return ""

                    elif errorCode == "701":
                        self.safe_debug(f"Ignored UPNP Error 701 (No Such Object) for {zoneIP} — likely SPDIF/TV input")
                        return ""

                    # Only log if not benign
                    self.logger.error(f"UPNP Error: {UPNP_ERRORS.get(errorCode, errorCode)}")
                    self.logger.error(f"Offending Command -> zoneIP: {zoneIP}, soapRoot: {soapRoot}, soapBranch: {soapBranch}, soapAction: {soapAction}")
                    self.logger.error(f"Error Response: {res}")

                except Exception as inner_error:
                    self.logger.error(f"UPNP Error: {status}")
                    self.logger.error(f"Offending Command -> zoneIP: {zoneIP}, soapRoot: {soapRoot}, soapBranch: {soapBranch}, soapAction: {soapAction}")
                    self.logger.error(f"Error Response: {res}")

            # Reconstruct multiline XML response
            resx = ""
            for line in res.splitlines():
                if len(line) <= 5:
                    try:
                        if 0 <= int(line, 16) <= 4096:
                            pass
                        else:
                            resx += line.rstrip('\n')
                    except Exception:
                        pass
                else:
                    resx += line.rstrip('\n')

            if getattr(self.plugin, "xmlDebug", False):
                self.safe_debug(SoapMessage)
                self.safe_debug(resx)

            return resx

        except Exception as exception_error:
            self.exception_handler(exception_error, True)



    #################################################################################################
    ### End - SOAPSend function with custom filtering for known specific error responses as needed 
    #################################################################################################



    def runConcurrentThread(self):
        self.logger.info("🔁 runConcurrentThread started")

        # Keep the plugin thread alive with a regular sleep loop
        while True:
            self.sleep(300)  # Sleep 5 minutes between wakeups

    def stopConcurrentThread(self):
        self.safe_debug("⏹ stopConcurrentThread called")
        self.stopThread = True


    def getZPDeviceList(self, filter=""):
        try:
            array = []
            if filter == "withNone":
                array.append(("00000", "No Selection"))
            for dev in indigo.devices.iter("self.ZonePlayer"):
                array.append((dev.id, dev.states['ZP_ZoneName']))
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_LIST(self, filter=""):
        try:
            array = []
            for plist in Sonos_Playlists:
                array.append((plist[0], plist[1]))
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_LIST_PlaylistObjects(self, filter=""):
        try:
            array = []
            for plist in Sonos_Playlists:
                array.append((plist[2], plist[1]))
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_LineIn(self, filter=""):
        try:
            array = []
            for dev in indigo.devices.iter("self.ZonePlayer"):
                array.append((dev.id, dev.states['ZP_ZoneName']))
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_SonosFavorites(self, filter=""):
        try:
            array = []
            for title in Sonos_Favorites:
                array.append((title[4], title[1]))
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_RT_FavStations(self, filter=""):
        try:
            return Sonos_RT_FavStations

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getZP_Pandora(self, filter="", valuesDict=None, typeId="", targetId=0):
        try:
            return [(s[0], s[1]) for s in Sonos_Pandora]
        except Exception as e:
            self.logger.error(f"❌ getZP_Pandora() failed: {e}")
            return []



    def getZP_SiriusXM(self, filter="", valuesDict=None, typeId="", targetId=0):
        if not self.siriusxm_channels:
            self.logger.error("SiriusXM channel list is empty — cannot populate dropdown.")
            return []

        self.safe_debug(f"SiriusXM total channels fetched: {len(self.siriusxm_channels)}")

        items = []
        for ch in self.siriusxm_channels:
            title = ch.get("title")
            stream_url = ch.get("streamUrl")
            if title and stream_url:
                items.append((title, title))
            elif title:
                self.safe_debug(f"SiriusXM channel '{title}' skipped — no streamUrl found.")

        if not items:
            self.logger.error("No SiriusXM channels with stream URLs found for dropdown list.")
        else:
            self.safe_debug(f"Returning {len(items)} SiriusXM channels with stream URLs to Indigo UI.")

        return items


    def getZP_SoundFiles(self, filter=""):
        try:
            return Sound_Files

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getIVONAVoices(self, filter=""):
        try:
            array = []
            for voice in IVONAVoices:
                array.append((voice[0], voice[4] + " | " + voice[1]))
            array.sort(key=lambda x: x[1])
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getPollyVoices(self, filter=""):
        try:
            array = []
            for voice in PollyVoices:
                array.append((voice[0], voice[4] + " | " + voice[1]))
            array.sort(key=lambda x: x[1])
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement

    def getAppleVoices(self, filter=""):
        try:
            # Preferred source: `say -v '?'` — lists only voices that actually
            # render (NSSpeechSynthesizer's availableVoices() includes modern ids
            # that produce silence through the deprecated API). Values are plain
            # voice names, which is what the `say`-based synthesis expects.
            try:
                import subprocess
                out = subprocess.run(["/usr/bin/say", "-v", "?"],
                                     capture_output=True, text=True, timeout=10)
                say_voices = []
                for line in (out.stdout or "").splitlines():
                    # e.g. "Samantha            en_US    # Hello..." and
                    #      "Eddy (English (UK)) en_GB    # Hello..." (single space)
                    m = re.match(r"^(.+?)\s+([A-Za-z]{2,3}[_-][A-Za-z0-9-]+)\s*#", line)
                    if m and m.group(1).strip():
                        say_voices.append((m.group(1).strip(), f"{m.group(1).strip()} ({m.group(2).strip()})"))
                if say_voices:
                    say_voices.sort(key=lambda x: x[1].lower())
                    return say_voices
            except Exception as say_error:
                self.logger.debug(f"getAppleVoices via 'say' failed ({say_error}); falling back to NSSpeechSynthesizer list")

            array = []
            # Per-voice guard: one voice id with missing attributes (common with
            # the modern com.apple.voice.* ids) must not empty the whole menu.
            for voice in NSVoices:
                try:
                    attrs = NSSpeechSynthesizer.attributesForVoice_(voice) or {}
                    name = attrs.get('VoiceName') or str(voice).rsplit(".", 1)[-1]
                    locale = re.split('-|_', attrs.get('VoiceLocaleIdentifier') or "")
                    try:
                        vl = language_codes.languages[locale[0]]
                    except Exception:
                        vl = locale[0] if locale and locale[0] else "?"
                    try:
                        vc = language_codes.countries[locale[1]]
                    except Exception:
                        vc = locale[1] if len(locale) > 1 else "?"
                    if isinstance(vl, bytes):
                        vl = vl.decode("utf-8", errors="ignore")
                    if isinstance(vc, bytes):
                        vc = vc.decode("utf-8", errors="ignore")
                    array.append((voice, f"{vc}, {vl} | {name}"))
                except Exception as voice_error:
                    self.logger.debug(f"getAppleVoices: skipping voice {voice!r}: {voice_error}")

            array.sort(key=lambda x: x[1])
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement


    def actionTogglePlay(self, indigo_device):
        zoneIP = indigo_device.address
        transport_state = indigo_device.states.get("ZP_STATE", "STOPPED").upper()

        self.safe_debug(f"🎛 ZP_STATE for {indigo_device.name} (from Indigo): {transport_state}")

        # If ZP_STATE looks unreliable, fall back to querying SoCo directly
        if transport_state not in ("PLAYING", "PAUSED_PLAYBACK", "STOPPED"):
            soco_device = self.findDeviceByIP(zoneIP)
            if soco_device:
                try:
                    transport_info = soco_device.get_current_transport_info()
                    transport_state = transport_info.get("current_transport_state", "STOPPED").upper()
                    self.safe_debug(f"🎛 ZP_STATE for {indigo_device.name} (from SoCo): {transport_state}")
                except Exception as e:
                    self.logger.warning(f"⚠️ SoCo state fetch failed for {indigo_device.name}: {e}")
                    transport_state = "STOPPED"

        # Execute based on state
        if transport_state == "PLAYING":
            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Pause",
                          "<InstanceID>0</InstanceID><Speed>1</Speed>")
            self.logger.info(f"⏸ Pause triggered for {indigo_device.name}")
        else:
            self.SOAPSend(zoneIP, "/MediaRenderer", "/AVTransport", "Play",
                          "<InstanceID>0</InstanceID><Speed>1</Speed>")
            self.logger.info(f"▶️ Play triggered for {indigo_device.name}")

    def getReferencePlayerIP(self):
        try:
            for dev in indigo.devices.iter("self"):
                if dev.enabled and dev.address:
                    return dev.address
            self.logger.warning("⚠️ No enabled Sonos devices found with IP addresses.")
        except Exception as e:
            self.logger.error(f"❌ Error in getReferencePlayerIP: {e}")
        return None


    def diagnoseSubscriptions(self):
        self.logger.info("🧪 Running SoCo subscription diagnostics...")
        try:
            if not self.soco_subs:
                self.logger.warning("⚠️ No subscriptions found in self.soco_subs.")
                return

            for dev_id, subs in self.soco_subs.items():
                try:
                    indigo_device = indigo.devices[int(dev_id)]
                    self.logger.info(f"🔍 Device: {indigo_device.name} ({indigo_device.address})")
                except Exception:
                    self.logger.warning(f"🔍 Device ID {dev_id} (not found in Indigo)")

                if not subs:
                    self.logger.warning("   ⚠️ No subscriptions registered for this device.")
                    continue

                for service_name, sub in subs.items():
                    sid = getattr(sub, 'sid', 'no-sid')
                    has_cb = hasattr(sub, 'callback') and sub.callback is not None
                    cb_name = sub.callback.__name__ if has_cb else "None"
                    self.logger.info(f"   🔔 {service_name} | SID: {sid} | Callback: {cb_name}")
        except Exception as e:
            self.logger.error(f"❌ diagnoseSubscriptions failed: {e}")

#####


    def getMicrosoftLanguages(self, filter=""):
        try:
            array = []
            for code in self.MSTranslateVoices:
                array.append((code, self.MSTranslateVoices[code]))
            array.sort(key=lambda x: x[1])
            return array

        except Exception as exception_error:
            self.exception_handler(exception_error, True)  # Log error and display failing statement


########################################################################################################################################################################
## SiriusXM Class wraps the SXM.PY app into a standalone class that will be used for login / session management / metadata capture for use within the indigo plugin   ##
########################################################################################################################################################################


class SiriusXM:
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
    REST_FORMAT = 'https://player.siriusxm.com/rest/v2/experience/modules/{}'
    LIVE_PRIMARY_HLS = 'https://siriusxm-priprodlive.akamaized.net'

    def __init__(self, username, password, logger=None):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.USER_AGENT})
        self.username = username
        self.password = password
        self.playlists = {}
        self.channels = None
        self.logger = logger  # ✅ Indigo logger passed in

    def log(self, message):
        if self.logger:
            self.logger.warning(f"<SiriusXM>: {message}")
        else:
            print(f"{datetime.datetime.now().strftime('%d.%b %Y %H:%M:%S')} <SiriusXM>: {message}")

    def is_logged_in(self):
        return 'SXMDATA' in self.session.cookies

    def is_session_authenticated(self):
        return 'AWSALB' in self.session.cookies and 'JSESSIONID' in self.session.cookies

    def get(self, method, params, authenticate=True):
        if authenticate and not self.is_session_authenticated() and not self.authenticate():
            self.log('Unable to authenticate')
            return None

        res = self.session.get(self.REST_FORMAT.format(method), params=params)
        if res.status_code != 200:
            self.log(f"Received status code {res.status_code} for method '{method}'")
            return None

        try:
            return res.json()
        except ValueError:
            self.log(f"Error decoding json for method '{method}'")
            return None

    def post(self, method, postdata, authenticate=True):
        if authenticate and not self.is_session_authenticated() and not self.authenticate():
            self.log('Unable to authenticate')
            return None

        res = self.session.post(self.REST_FORMAT.format(method), data=json.dumps(postdata))
        if res.status_code != 200:
            self.log(f"Received status code {res.status_code} for method '{method}'")
            return None

        try:
            return res.json()
        except ValueError:
            self.log(f"Error decoding json for method '{method}'")
            return None

    def login(self):
        postdata = {
            'moduleList': {
                'modules': [{
                    'moduleRequest': {
                        'resultTemplate': 'web',
                        'deviceInfo': {
                            'osVersion': 'Mac',
                            'platform': 'Web',
                            'sxmAppVersion': '3.1802.10011.0',
                            'browser': 'Safari',
                            'browserVersion': '11.0.3',
                            'appRegion': 'US',
                            'deviceModel': 'K2WebClient',
                            'clientDeviceId': 'null',
                            'player': 'html5',
                            'clientDeviceType': 'web',
                        },
                        'standardAuth': {
                            'username': self.username,
                            'password': self.password,
                        },
                    },
                }],
            },
        }
        data = self.post('modify/authentication', postdata, authenticate=False)
        if not data:
            return False

        try:
            return data['ModuleListResponse']['status'] == 1 and self.is_logged_in()
        except KeyError:
            self.log('Error decoding json response for login')
            return False

    def authenticate(self):
        if not self.is_logged_in() and not self.login():
            self.log('Unable to authenticate because login failed')
            return False

        postdata = {
            'moduleList': {
                'modules': [{
                    'moduleRequest': {
                        'resultTemplate': 'web',
                        'deviceInfo': {
                            'osVersion': 'Mac',
                            'platform': 'Web',
                            'clientDeviceType': 'web',
                            'sxmAppVersion': '3.1802.10011.0',
                            'browser': 'Safari',
                            'browserVersion': '11.0.3',
                            'appRegion': 'US',
                            'deviceModel': 'K2WebClient',
                            'player': 'html5',
                            'clientDeviceId': 'null'
                        }
                    }
                }]
            }
        }
        data = self.post('resume?OAtrial=false', postdata, authenticate=False)
        if not data:
            return False

        try:
            return data['ModuleListResponse']['status'] == 1 and self.is_session_authenticated()
        except KeyError:
            self.log('Error parsing json response for authentication')
            return False

    def get_sxmak_token(self):
        try:
            return self.session.cookies['SXMAKTOKEN'].split('=', 1)[1].split(',', 1)[0]
        except (KeyError, IndexError):
            return None

    def get_gup_id(self):
        try:
            return json.loads(urllib.parse.unquote(self.session.cookies['SXMDATA']))['gupId']
        except (KeyError, ValueError):
            return None

    def get_playlist_url(self, guid, channel_id, use_cache=True, max_attempts=5):
        if use_cache and channel_id in self.playlists:
             return self.playlists[channel_id]

        params = {
            'assetGUID': guid,
            'ccRequestType': 'AUDIO_VIDEO',
            'channelId': channel_id,
            'hls_output_mode': 'custom',
            'marker_mode': 'all_separate_cue_points',
            'result-template': 'web',
            'time': int(round(time.time() * 1000.0)),
            'timestamp': datetime.datetime.utcnow().isoformat('T') + 'Z'
        }
        data = self.get('tune/now-playing-live', params)
        if not data:
            return None

        try:
            status = data['ModuleListResponse']['status']
            message = data['ModuleListResponse']['messages'][0]['message']
            message_code = data['ModuleListResponse']['messages'][0]['code']
        except (KeyError, IndexError):
            self.log('Error parsing json response for playlist')
            return None

        if message_code in [201, 208]:
            if max_attempts > 0:
                self.log('Session expired, logging in and authenticating')
                if self.authenticate():
                    self.log('Successfully authenticated')
                    return self.get_playlist_url(guid, channel_id, use_cache, max_attempts - 1)
                else:
                    self.log('Failed to authenticate')
                    return None
            else:
                self.log('Reached max attempts for playlist')
                return None
        elif message_code != 100:
            self.log(f'Received error {message_code} {message}')
            return None

        try:
            playlists = data['ModuleListResponse']['moduleList']['modules'][0]['moduleResponse']['liveChannelData']['hlsAudioInfos']
        except (KeyError, IndexError):
            self.log('Error parsing json response for playlist')
            return None

        for playlist_info in playlists:
            if playlist_info['size'] == 'LARGE':
                playlist_url = playlist_info['url'].replace('%Live_Primary_HLS%', self.LIVE_PRIMARY_HLS)
                self.playlists[channel_id] = self.get_playlist_variant_url(playlist_url)
                return self.playlists[channel_id]

        return None

    def get_playlist_variant_url(self, url):
        params = {
            'token': self.get_sxmak_token(),
            'consumer': 'k2',
            'gupId': self.get_gup_id(),
        }
        res = self.session.get(url, params=params)

        if res.status_code != 200:
            self.log(f"Received status code {res.status_code} on playlist variant retrieval")
            return None

        for line in res.text.split('\n'):
            if line.rstrip().endswith('.m3u8'):
                return f"{url.rsplit('/', 1)[0]}/{line.rstrip()}"

        return None

    def get_channels(self):
        if not self.channels:
            postdata = {
                'moduleList': {
                    'modules': [{
                        'moduleArea': 'Discovery',
                        'moduleType': 'ChannelListing',
                        'moduleRequest': {
                            'consumeRequests': [],
                            'resultTemplate': 'responsive',
                            'alerts': [],
                            'profileInfos': []
                        }
                    }]
                }
            }
            data = self.post('get', postdata)
            if not data:
                self.log('Unable to get channel list')
                return []

            try:
                self.channels = data['ModuleListResponse']['moduleList']['modules'][0]['moduleResponse']['contentData']['channelListing']['channels']
            except (KeyError, IndexError):
                self.log('Error parsing json response for channels')
                return []

        return self.channels

    def get_channel(self, name):
        name = name.lower()
        for channel in self.get_channels():
            if (channel.get('name', '').lower() == name or
                channel.get('channelId', '').lower() == name or
                channel.get('siriusChannelNumber', '').lower() == name or
                channel.get('channelGuid') == name):
                return (channel['channelGuid'], channel['channelId'])

        return (None, None)