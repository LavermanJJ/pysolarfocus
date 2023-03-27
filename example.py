from pysolarfocus import SolarfocusAPI,Systems,ApiVersions

# Create the Solarfocus API client
# TODO: Choose either Vampair or Therminator and adapt IP-Address and version
solarfocus = SolarfocusAPI(ip="solarfocus", system=Systems.Vampair, api_version=ApiVersions.V_23_020)

solarfocus.connect()
# Fetch the values
solarfocus.update()

# Print the values
print("Solarfocus "+ solarfocus.system.name +", version " + str(solarfocus.api_version.value))
print(solarfocus.heating_circuits[0])
print("\n")
print(solarfocus.boilers[0])
print("\n")
print(solarfocus.buffers[0])
print("\n")
if solarfocus.system is Systems.Therminator:
    print(solarfocus.pelletsboiler)
if solarfocus.system is Systems.Vampair:
    print(solarfocus.heatpump)
print("\n")
print(solarfocus.photovoltaic)
print("\n")
print(solarfocus.solar)