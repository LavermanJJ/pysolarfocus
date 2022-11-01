from pysolarfocus import SolarfocusAPI,Systems

# Create the Solarfocus API client
# TODO: Adapt IP-Address
solarfocus = SolarfocusAPI(ip="IP-Address", system=Systems.Vampair)
solarfocus.connect()
# Fetch the values
solarfocus.update()

# Print the values
print(solarfocus.heating_circuits[0])
print("\n")
print(solarfocus.boilers[0])
print("\n")
print(solarfocus.buffers[0])
print("\n")
print(solarfocus.heatpump)
print("\n")
print(solarfocus.photovoltaic)
