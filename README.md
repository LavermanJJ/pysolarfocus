# pysolarfocus: Python Client for Solarfocus eco<sup>_manager-touch_</sup>

## What's Supported 

### Software Version

This integration has been tested with Solarfocus eco<sup>manager-touch</sup> version `21.040`.

### Solarfocus Components

| Components | Supported |
|---|---|
| Heating Circuit 1 (_Heizkreis_)| :white_check_mark: |
| Buffer 1 (_Puffer_) | :white_check_mark: |
| Solar (_Solar_)| :x:|
| Boiler 1 (_Boiler_) | :white_check_mark: |
| Heatpump (_Wärmepumpe_) | :white_check_mark: |
| Biomassboiler (_Kessel_) | :white_check_mark: | 

_Note: The number of supported Heating Circuits, Buffers, and Boilers could be extended in the future_

## Usage

```python
from pymodbus.client import ModbusTcpClient as ModbusClient
from pysolarfocus import SolarfocusAPI
from pysolarfocus.const import PORT,Systems

# Create a Modbus client
client = ModbusClient(IP, port=PORT)
client.connect()

# Create the Solarfocus API client
solarfocus = SolarfocusAPI(client, Systems.Vampair)

# Fetch the values
solarfocus.update()

# Print the values
print(solarfocus.buffer)
print(solarfocus.heating_circuit)
```
