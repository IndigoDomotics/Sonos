# Sonos Plugin for Indigo

Control your entire Sonos system from [Indigo](https://www.indigodomo.com) — playback, volume, grouping, favourites, streaming services, announcements, soundbar tuning, and native Sonos alarms — as first-class Indigo devices, actions, and triggers.

**Current version: 2025.2.4** · Requires Indigo 2025.2+ (API 3.4) · Bundled SoCo 0.30.9 · Python 3

---

## Highlights of 2025.2.4

This release overhauls the announcement system end-to-end and fixes several bugs reported against 2025.2.3.

### Bug fixes

- **Multi-zone announcements fixed** — a grouping-semantics regression made the coordinator sequentially join every other zone's group instead of the zones joining the coordinator; announcements only played on one speaker. All selected zones now group correctly and play together.
- **Polly TTS "Unable to locate credentials" fixed** — Polly/IVONA/Pandora/SiriusXM/Microsoft credentials (and Apple voices) are loaded at plugin startup again, not only after re-saving the config dialog.
- **TTS announcements fixed** — all TTS engines wrote their audio where the announcement HTTP server never looked (silent 404s), and File announcements could measure a stale file's duration and cut off mid-play. All announcement audio now lives in one served location.
- **Apple text-to-speech reworked** — synthesis now uses macOS `say` (the previous `NSSpeechSynthesizer` API is deprecated and renders silence for modern voices), the voice menu lists only voices that actually work, and output is Sonos-compatible 44.1 kHz WAV (the old AIFF output was an AIFF-C container Sonos rejects).
- **Device IP changes self-heal** — a player that moves to a new DHCP address is found again by its Sonos id during background retry and its Indigo device address is updated automatically; no more delete-and-recreate or control-page edits (forum-requested).
- **Stale group-state ghosts fixed** — plugin caches are resynced from live topology after announcements, so Indigo device states track what the players are actually doing.

### New: full group & playback restore around announcements

Announcements now snapshot every target zone (SoCo Snapshot/Restore — the same mechanism Home Assistant uses; selectable in Plugin Config, on by default) and afterwards rebuild the **exact pre-announcement state**: original groups re-form (including group members that weren't part of the announcement), standalone zones return to standalone, volumes/mutes restore, and interrupted music resumes at the same track and position. See the Known Limitation in the version history: cloud-queue sources (Alexa-initiated, Spotify Connect, AirPlay) cannot be programmatically resumed.

### Cross-VLAN diagnostics

Players on a separate VLAN must be able to reach the Indigo Mac on tcp/8889 (announcements), tcp/8888 (album art), and tcp/1400 (event notifications) — a one-way firewall breaks all three silently while normal control keeps working. The plugin now detects players on a different subnet at startup and logs the exact rules needed, and a fetch watchdog reports when a player never pulled the announcement file.

### Quieter, more useful logging

The plugin log file always captures full debug detail (nothing is lost when the Event Log is set to normal), while Event Log noise — album-art fetch retries, per-event state chatter, startup floods — has been sharply reduced. Album-art fetches use longer timeouts, and the last unbounded HTTP calls got timeouts.

---

## Highlights of 2025.2.3

This release is a major reliability and completeness overhaul, addressing the failure cascade reported in [IndigoDomotics/Sonos#16](https://github.com/IndigoDomotics/Sonos/issues/16) and restoring a number of actions that had silently stopped working.

### Rock-solid with offline players and flaky networks

Previously, a single unplugged speaker could freeze the whole plugin — minutes-long startups, a config dialog that would not open, reloads needing a force-kill, and log storms hammering healthy players. All of that is fixed:

- **Fast reachability probes everywhere** — an offline player is detected in ~1 second, marked with an `offline` device state in Indigo, and skipped (with a 30-second back-off) instead of blocking the plugin in serial 10–20 s network timeouts.
- **Automatic recovery** — offline players are re-checked in the background every 60 seconds and come back to life on their own when the network returns. No plugin restart needed.
- **Every network call is time-bounded** — no more unbounded HTTP requests anywhere on the hot path (SoCo's global request timeout is also capped at 5 s).
- **Clean, fast plugin stop/reload** — unsubscribing from an offline player no longer blocks shutdown, so reloads complete without Indigo force-killing the process.
- **Announcement storm fix** — group announcements no longer trigger a flood of topology fetches against every player for every zone change (debounced + probe-gated), which previously could knock healthy WiFi speakers off the network mid-announcement.
- **Player UIDs resolve instantly from cached Indigo state** — no repeated `DeviceProperties` fetches against dead players.

### Full support for routed / VLAN'd Sonos networks

If your players live on a dedicated subnet (e.g. Sonos on `192.168.30.0/24`, Indigo Mac on `192.168.1.0/24`):

- Interface selection now falls back to the **OS routing table** when no local interface sits directly on the Sonos subnet — announcements and event subscriptions work across the router instead of failing with *"No interface found on target Sonos subnet"*.
- All player communication is **direct-by-IP**; multicast discovery (which cannot cross a router) is never required and no longer spams warnings when it finds nothing.

### Previously broken actions — now working

An automated end-to-end audit (Actions.xml → plugin.py → handler) found **10 actions that were offered in the UI but did nothing** (logging *"Unknown or unsupported action"*) or crashed. All are restored and verified:

| Action | Status |
|---|---|
| Play RadioTime Favourite Station | Restored (was breaking alarm/announcement action groups) |
| Bass / Treble (set to level) | Restored — no handler existed at all |
| Night Mode | Restored |
| Play Queue | Restored |
| Sleep Timer | Restored |
| TV Input (soundbars) | Restored |
| Dump URI (diagnostics) | Restored |
| Pandora Thumbs Up / Thumbs Down | Restored — handler method was missing |
| Test SiriusXM Channel | Fixed malformed action definition + missing callback |
| Line-In | Fixed in 2025.2.1 ([#15](https://github.com/IndigoDomotics/Sonos/pull/15)) |

Also fixed in this area:

- **Sonos Favourites playback** — a Python‑2 remnant (`urllib.unquote`) crashed favourites; fixed. Favourite routing also corrected: `x-sonosapi-hls:` is a *generic* HLS scheme (Sonos Radio HD, Apple Music radio, …) and is no longer misrouted to the SiriusXM handler — only URIs carrying `channel-linear:<guid>` are SiriusXM. Generic HLS/HTTP favourites now play via their stored URI + metadata.
- **SiriusXM from favourites** — the handler now accepts the channel GUID embedded in a favourite's URI, not just the action's channel dropdown.
- Two latent dispatch-signature crashes (`ZP_SiriusXM` missing `props`, `Q_Crossfade` arity) fixed.
- Stale device state lists (the *"state key Grouped not defined"* error spam) are resynced automatically from Devices.xml on startup.

### New features (Home Assistant parity)

Feature set cross-checked against Home Assistant's Sonos integration; the following were added using the same SoCo/UPnP semantics:

**Equalizer / soundbar controls** (Actions → Sonos → Equalizer):

- **Speech Enhancement** on/off (Arc, Beam, Playbar dialog clarity)
- **Audio Delay (Lip Sync)** 0–5
- **Surround Speakers** on/off
- **Surround Level (TV)** −15…15
- **Surround Level (Music)** −15…15
- **Music Playback Full Volume** — full-volume vs ambient music on surrounds

**Native Sonos alarm management** (Actions → Sonos → Alarms):

- **Set Alarm On/Off** — lists your household's Sonos alarms live (`07:00 — Master Bedroom — DAILY — enabled`), with Enable / Disable / Toggle and an optional volume override. Perfect for "disable the wake-up alarm on public holidays" style automations.

---

## Installation

1. Download the latest release and double-click `Sonos.indigoPlugin` — Indigo installs and enables it.
2. Open **Plugins → Sonos → Configure…**:
   - **Reference ZonePlayer IP** — any player's IP, or `auto`. Used to load favourites/playlists/stations.
   - **Sonos Target Subnet** — the subnet your players live on (e.g. `192.168.30.0/24`). If your Mac isn't directly on that subnet, the plugin automatically uses the routed interface — you don't need to change anything.
   - Announcement/streaming host + port, event processor settings, and optional Pandora / SiriusXM credentials.
3. Create one Indigo device (type **Sonos ZonePlayer**) per player, entering each player's IP address. Use fixed IPs / DHCP reservations for your players.

Players that are offline when the plugin starts show an `offline` device state and are picked up automatically when they reappear.

## Devices & States

Each ZonePlayer device exposes rich states usable in triggers and control pages, including transport state, track metadata + album art, volume/mute/bass/treble, grouping (`Grouped`, `GROUP_Coordinator`, `GROUP_Name`, `ZonePlayerUUIDsInGroup`), queue flags (repeat/shuffle/crossfade), and identity (`ZP_LocalUID`, model, serial).

Grouped players mirror the coordinator's enriched metadata states, so a control page bound to any group member shows what's actually playing.

## Actions overview

- **Transport**: Play, Pause, Toggle Play/Pause, Stop, Next, Previous, Channel Up/Down
- **Volume**: set/up/down, mute on/off/toggle — per player and per group, plus relative group volume
- **Equalizer**: Bass, Treble (set or step), Loudness via player, Night Mode, Speech Enhancement, Audio Delay, Surround on/off + levels, Music Full Volume
- **Music sources**: Sonos Favourites, Sonos Playlists, RadioTime Favourite Stations, Sonos Radio, Pandora (+ Thumbs Up/Down), SiriusXM (+ channel list, test), Spotify/containers, Line-In, TV input, Play Queue
- **Queue**: Clear, Save, Crossfade, Repeat / Repeat One / Toggle, Shuffle / Toggle
- **Grouping**: Add player(s) to zone, Set standalone (one/all), with group-state resync
- **Announcements**: file/MP3 announcements over the built-in HTTP server, with automatic ungroup → announce → regroup and state save/restore; Amazon Polly TTS supported
- **Alarms**: enable/disable/toggle native Sonos alarms, optional volume override
- **Utilities**: Save/Restore player states, Dump URI, group/topology diagnostic dumps (menu items)

## Troubleshooting

- **Announcements play no audio / artwork blank / states go stale, but control works (players on a separate VLAN)** — the players *pull* announcements, album art, and push event notifications *to* the Indigo Mac. A one-way LAN→VLAN firewall breaks all three silently. Allow the Sonos VLAN → Indigo Mac on **tcp/8889** (announcements), **tcp/8888** (album art), and **tcp/1400** (event notifications). The plugin logs a startup warning naming the exact rules when it detects players on another subnet.
- **A player shows `offline`** — the plugin probes it every 60 s and will restore it automatically once reachable. Nothing to do.
- **Config dialog, favourites lists, or actions feel slow** — check the log for a player timing out; one unreachable IP no longer blocks the plugin, but fixing the network (or deleting a decommissioned player's device) keeps logs clean.
- **Favourite won't play** — check the log: unknown favourite types are logged with their URI. Open an issue including that line.
- **Menu → dump options** — group topology, subscribed devices, and SiriusXM channel dumps are available as diagnostic aids under the plugin menu.

## Version history

**2025.2.4** — Announcement system overhaul: multi-zone announcements fixed (grouping semantics regression), full **group & playback restore** after announcements — zones return to their exact pre-announcement groups (including group members that weren't part of the announcement) and music resumes at the same track/position via SoCo Snapshot/Restore (selectable in Plugin Config, on by default, with the legacy flow as fallback). Apple text-to-speech reworked onto macOS `say` (voice menu now lists only voices that actually render; output is Sonos-compatible 44.1 kHz WAV). Polly/IVONA/Pandora/SiriusXM credentials and Apple voices load at startup again. TTS audio unified onto the announcement HTTP server's folder (TTS previously 404'd; File announcements could probe a stale file's duration). Cross-VLAN diagnostics: startup warning + a fetch watchdog name the exact firewall rules needed (players must reach the Mac on tcp/8889 announcements, tcp/8888 album art, tcp/1400 event notifications). DHCP-moved players self-heal by matching their RINCON id in discovery and updating the device address automatically. Plugin log file now always captures full debug detail; Event Log noise sharply reduced. Album-art fetches use longer timeouts and no longer warn.

> **Known limitation — announcement playback resume:** sources Sonos exposes as *cloud queues* — Alexa-initiated music, Spotify Connect, and AirPlay streams — cannot be restarted programmatically (Sonos provides no API to resume them; Home Assistant has the same limitation). After an announcement, grouping and volume are still restored for those zones, but that music will not auto-resume. Local queue playback, Sonos favourites, and radio streams all resume normally, at the same track and position.

**2025.2.3** — Offline-player resilience (probe gating, UID caching, bounded timeouts, clean shutdown), routed-VLAN support, announcement topology-storm fix, state-list resync, 10 restored actions, favourites routing fixes, new Equalizer/soundbar actions, native Sonos alarm management. See [PR #17](https://github.com/IndigoDomotics/Sonos/pull/17).

**2025.2.1** — Line-In action fix ([#15](https://github.com/IndigoDomotics/Sonos/pull/15)); HTTPStreamer port leak and Polly prefs fixes ([#14](https://github.com/IndigoDomotics/Sonos/pull/14)); dynamic install-path resolution ([#13](https://github.com/IndigoDomotics/Sonos/pull/13)).

**1.0.2** — SoCo 0.30.9 upgrade; rewritten subscriptions with fallback; VLAN-aware discovery; corrected volume/bass/treble controls; SiriusXM login + channel processing; Pandora auth ported to Python 3; artwork/metadata server; group metadata mirroring; diagnostic menu dumps.

## Credits

Originally by Vic Solomon; Python 3 port and ongoing maintenance by the Indigo community (IndigoDomotics), with contributions from forum users and plugin contributors. Uses the [SoCo](https://github.com/SoCo/SoCo) library. Not affiliated with Sonos, Inc.

## License

See [LICENSE](LICENSE).
