from pysolarfocus import SolarfocusAPI, PORT,Systems

# Create the Solarfocus API client
# TODO: Adapt IP-Address
solarfocus = SolarfocusAPI("IP-Address", Systems.Therminator)
solarfocus.connect()
# Fetch the values
solarfocus.update()

# Print the values
print(solarfocus.heating_circuit)
print("\n")
print(solarfocus.boiler)
print("\n")
print(solarfocus.buffer)
print("\n")
print(solarfocus.heatpump)
print("\n")
print(solarfocus.photovoltaic)
