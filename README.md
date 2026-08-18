[![Version](https://img.shields.io/github/v/tag/lavermanjj/pysolarfocus?style=for-the-badge&label=Version&color=orange)](https://img.shields.io/github/v/tag/lavermanjj/pysolarfocus?style=for-the-badge&label=Version&color=orange)
[![License](https://img.shields.io/github/license/lavermanjj/pysolarfocus?style=for-the-badge)](https://img.shields.io/github/license/lavermanjj/pysolarfocus?style=for-the-badge)


<p align="center">
  <a href="https://github.com/lavermanjj/home-assistant-solarfocus">
    <img src="https://brands.home-assistant.io/solarfocus/logo.png" alt="Logo" height="80">
  </a>
</p>

<h3 align="center">pysolarfocus</h3>

<p align="center">
  Python client for <a href="https://www.solarfocus.com/">Solarfocus</a> eco<sup>manager-touch</sup>  via Modbus TCP
</p>


<details open="open">
  <summary>Table of Contents</summary>

1. [About](#about)
2. [Supported Solarfocus Software and Hardware](#supported-solarfocus-software-and-hardware)
3. [How To](#how-to)
   - [Installation](#installation)
   - [Basic Example](#basic-example)
   - [Detecting the configuration](#detecting-the-configuration)
   - [Handling multiple components](#handling-multiple-components)
   - [Conveniently set modes](#convenitently-set-modes)
   - [API-Version specification](#api-version-specification)
4. [Changelog of API-Versions](#changelog-of-api-versions)


</details>


## About

Python client library to interact with heating systems of [Solarfocus](https://www.solarfocus.com/) (eco<sup>_manager-touch_</sup>) via Modbus TCP. This library has been developed for the integration into [Home-Assistant](https://www.home-assistant.io/) via a [custom integration](https://github.com/LavermanJJ/home-assistant-solarfocus), but can be used indepdently.

> **Warning**
> Use with caution, in case of doubt check with Solarfocus or your installer if a feature / functionality (e.g. cooling) is supported by your installation to avoid damages to your heating system or the building.


## Supported Solarfocus Software and Hardware

### Software

> **Important**
> This integration has been tested with Solarfocus eco<sup>manager-touch</sup> version `25.030`.

Supported versions: `21.140` - `26.020`. Features added in later versions are not yet supported.

The eco<sup>manager-touch</sup> Modbus TCP specification can be found [here](https://www.solarfocus.com/partnerbereich/ecomanager-touch_modbus-tcp_registerdaten_anleitung1.pdf)).

### Hardware

The eco<sup>manager-touch</sup> can integrate the following heating systems
- [Vamp<sup>air</sup>](https://www.solarfocus.com/en/products/air-source-heat-pump-vampair) heat pumps
- [Thermin<sup>nator</sup>](https://www.solarfocus.com/en/products/biomassheating) biomass boilers
- [Ecotop<sup>light</sup> / Ecotop<sup>zero</sup>](https://www.solarfocus.com/de/produkte/biomasseheizung/pelletkessel/ecotop) biomass boilers
- [Octo<sup>plus</sup>](https://www.solarfocus.com/en/products/biomassheating/pellet-boiler/octoplus) biomass boilers
- [Pellet<sup>top</sup>](https://www.solarfocus.com/en/products/biomassheating/pellet-boiler/pellettop) biomass boilers

| Components | Supported |
|---|---|
| Heating Circuit 1 - 8 (_Heizkreis_)| :white_check_mark: |
| Buffer 1 - 4 (_Puffer_) | :white_check_mark: |
| Solar 1 - 4 (_Solar_)| :white_check_mark: |
| Boiler 1 - 4 (_Boiler_) | :white_check_mark: |
| Heat Pump (_Wärmepumpe_) | :white_check_mark: |
| Biomass Boiler (_Kessel_) | :white_check_mark: |
| Fresh Water Module 1 - 4 (_Frischwassermodul_) | :white_check_mark: |
| Differential Module 1 - 4 (_Differenzmodul_)| :white_check_mark: |
| Circulation 1 - 4 (_Zirkulation_)| :white_check_mark: |

## How To

### Installation

```
$ pip3 install pysolarfocus
```

### Basic Example

```python
from pysolarfocus import SolarfocusAPI,Systems,ApiVersions

# Create the Solarfocus API client
solarfocus = SolarfocusAPI(
    ip="solarfocus",                    # adapt IP-Address
    system=Systems.VAMPAIR,             # for biomass boiler change to Systems.THERMINATOR / ECOTOP
    api_version=ApiVersions.V_25_030)   # select Solarfocus version

solarfocus.connect()
# Fetch the values
solarfocus.update()

# Print the values
print(solarfocus)
print(solarfocus.heating_circuits[0])
```

Output:

```
❯ uv run example.py
--------------------------------------------------
SolarfocusAPI, v5.1.1
--------------------------------------------------
+ System: Vampair
+ Version: 25.030
--------------------------------------------------
============
HeatingCircuit
============
---Input:
supply_temperature | raw:257 scaled:25.700000000000003
room_temperature | raw:224 scaled:22.400000000000002
humidity | raw:480 scaled:48.0
limit_thermostat | raw:1 scaled:1
circulator_pump | raw:0 scaled:0
mixer_valve | raw:0 scaled:0
state | raw:0 scaled:0
---Holding:
target_supply_temperature | raw:0 scaled:0.0
cooling | raw:0 scaled:0
mode | raw:3 scaled:3
target_room_temperature | raw:0 scaled:0.0
indoor_temperature_external | raw:224 scaled:22.4
indoor_humidity_external | raw:480 scaled:48.0
heating_mode | raw:2 scaled:2


============
Boiler
============
---Input:
....
```

### Detecting the configuration

Rather than being told which system, version and components it is talking to, the
client can ask the heating system:

```python
from pysolarfocus import SolarfocusAPI

solarfocus = SolarfocusAPI.autodetect(ip="[Your-IP]")
solarfocus.connect()
solarfocus.update()

print(solarfocus.detection.system)       # Systems.VAMPAIR
print(solarfocus.detection.api_version)  # ApiVersions.V_26_020
```

To detect without building a client - to show the result to a user first, say -
use the detector on its own and hand the outcome to the constructor:

```python
from pysolarfocus import SolarfocusAPI, SolarfocusDetector

detector = SolarfocusDetector(ip="[Your-IP]")
detector.connect()
detection = detector.detect()
detector.close()

print(detection.heating_circuit_count, detection.solar_count)
solarfocus = SolarfocusAPI(ip="[Your-IP]", **detection.as_api_kwargs())
```

Detection costs around ninety register reads - a few seconds - so it belongs in
setup rather than in anything that runs repeatedly.

#### How it works, and what it cannot tell you

The eco<sup>manager-touch</sup> has no register listing what is installed, so
detection reads two different things:

- **Which registers exist.** An address the firmware does not map is refused
  with *illegal data address*. That establishes the API version and the register
  layout, and almost nothing else: on a `26.020` controller every documented
  register was mapped except the X35 sensors of the buffers that are not there.
- **What the registers say.** The specification defines *nicht vorhanden* and
  *nicht freigeschaltet* values for the components that repeat, and an
  unconfigured sensor channel reports a temperature far outside its range
  (`130.0 °C`, `270.0 °C` or `-1`). The counts come from these.

`DetectionResult.evidence` holds the values each conclusion was reached from, so
a wrong answer can be argued with rather than guessed at.

Two things to know before trusting it:

- **Differential modules are never detected.** `differential_module_count` is
  always `0`, for the user to raise. On the installation this was written
  against the block read as though a module were there - three channels each
  repeating a temperature belonging to another component - while none was
  configured, and nothing in the registers separates the two cases.
- **Solar circuits have no "not present" value.** A circuit is taken to be
  absent when its whole register block reads plain zero. A channel that is
  configured but has no sensor on it reports `130.0 °C` or `270.0 °C` and counts
  as present; only zero says the circuit is not there.
- **Only vampair systems have been checked against real hardware.** Telling a
  therminator, ecotop and octoplus apart is reasoned from the specification -
  log wood at `2412`, Kesselbetriebsart at `2409`, the octoplus buffer at
  `2410`/`2411` - and `DetectionResult.system_confident` is `False` when no heat
  generator reported anything alive at all.

### Handling multiple components
Solarfocus systems allow the use of multiple heating circuits, buffers, boilers, and fresh water modules. The api can be configured to interact with multiple components.

```python
# Create the Solarfocus API client with 2 Heating Circuits
solarfocus = SolarfocusAPI(ip="[Your-IP]",heating_circuit_count=2,system=Systems.VAMPAIR)
# Connect to the heating system
solarfocus.connect()

# Update all heating circuits
solarfocus.update_heating()

# Update only the first heating circuit
solarfocus.heating_circuits[0].update()
# Print the first heating circuit
print(solarfocus.heating_circuits[0])

# Set the temperature of the first heating circuit to 30°C
solarfocus.heating_circuits[0].indoor_temperature_external.set_unscaled_value(30)
# Write the value to the heating system
solarfocus.heating_circuits[0].indoor_temperature_external.commit()
```

### Convenitently set modes
Control the heating system by setting modes using the provided classes

```python
# Without convenience method
solarfocus.heating_circuits[0].mode.set_unscaled_value(0)
solarfocus.heating_circuits[0].mode.commit()

# RECOMMENDED: Uitilizing convenience methods for modes
solarfocus.set_heating_circuit_mode(0, HeatingCircuitMode.ALWAYS_ON)
```

### API-Version specification
By default, the integration uses API-Version`21.140`. If your system is newer, you can specify
the version by using the `api_version` parameter.

```python
solarfocus = SolarfocusAPI(ip="[Your-IP]", system=Systems.VAMPAIR, api_version=ApiVersions.V_23_020)
```

You can find the API-Version displayed in the header of the screen of your Solarfocus system:

<img src="images/sf-version.png?raw=true" width="500">

## Changelog of API-Versions
> **Note**
> The API-Version of Solarfocus is independent of the versions of this library. Below list refers to
> the Solarfocus versions. See [releases](https://github.com/LavermanJJ/pysolarfocus/releases) for the changelog
> of this library.

#### 26.020
* Add HEMS target electrical power for the PV overcharge (`photovoltaic.hems_target_electrical_power`, register `33415`).

#### 25.030
* Add differential modules
* Add circulation
* Add multiple solar modules
* Adapt for changes in registers for heat pump

#### 23.020
* Add fresh water module state.

#### 23.010
* Add biomass boiler pellet statistics.

#### 22.090
* Add biomass boiler sweep function control.
* Allow input of external buffer values.
