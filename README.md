# pysolarfocus: Python Client for Solarfocus eco<sup>_manager-touch_</sup>

## What's Supported 

### Software Version

This integration has been tested with Solarfocus eco<sup>manager-touch</sup> version `21.040`.

### Solarfocus Components

| Components | Supported |
|---|---|
| Heating Circuits (_Heizkreis_)| :white_check_mark: |
| Buffers (_Puffer_) | :white_check_mark: |
| Solar (_Solar_)| :x:|
| Boilers (_Boiler_) | :white_check_mark: |
| Heatpump (_Wärmepumpe_) | :white_check_mark: |
| Biomassboiler (_Kessel_) | :white_check_mark: | 

_Note: Different components or heating systems could be supported in the future_

## Usage

```python
from pysolarfocus import SolarfocusAPI,Systems

# Create the Solarfocus API client
solarfocus = SolarfocusAPI(ip=[Your-IP],system=Systems.Vampair)
# Connect to the heating system
solarfocus.connect() 
# Fetch the values
solarfocus.update()

# Print the values
print(solarfocus.buffer)
print(solarfocus.heating_circuit)
```

### Handling multiple components e.g. heating circuits
_Solarfocus systems allow the use of multiple heating circuits, buffers and boilers. The api can be configured to interact with multiple components._

```python 

# Create the Solarfocus API client with 2 Heating Circuits
solarfocus = SolarfocusAPI(ip=[Your-IP],heating_circuit_count=2,system=Systems.Vampair)
# Connect to the heating system
solarfocus.connect()

# Update all heating circuits
solarfocus.update_heating()

# Update only the first heating circuit
solarfocus.heating_circuits[0].update()
# Print the first heating circuit
print(solarfocus.heating_circuits[0])

# Set the temperature of the first heating circuit to 30°C
solarfocus.heating_circuits[0].indoor_temperatur_external.set_unscaled_value(30)
# Write the value to the heating system
solarfocus.heating_circuits[0].indoor_temperatur_external.commit()