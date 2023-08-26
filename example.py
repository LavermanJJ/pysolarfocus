from pysolarfocus import SolarfocusAPI, Systems, ApiVersions

# Create the Solarfocus API client
solarfocus = SolarfocusAPI(
    ip="solarfocus", system=Systems.VAMPAIR, api_version=ApiVersions.V_23_020  # adapt IP-Address  # change to Systems.Therminator
)  # select Solarfocus version

solarfocus.connect()
# Fetch the values
solarfocus.update()

# Print the values
print(solarfocus)
print(solarfocus.heating_circuits[0])
print("\n")
print(solarfocus.boilers[0])
print("\n")
print(solarfocus.buffers[0])
print("\n")
if solarfocus.system is Systems.THERMINATOR:
    print(solarfocus.biomassboiler)
if solarfocus.system is Systems.VAMPAIR:
    print(solarfocus.heatpump)
print("\n")
print(solarfocus.photovoltaic)
print("\n")
print(solarfocus.solar)
print("\n")
