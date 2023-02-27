from pysolarfocus import SolarfocusAPI,Systems,ApiVersions

# Create the Solarfocus API client
# TODO: Choose either Vampair or Therminator and adapt IP-Address and version
solarfocus = SolarfocusAPI(ip="IP-Address", system=Systems.Vampair, api_version=ApiVersions.V_21_140)

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
if solarfocus.system is Systems.Therminator:
    print(solarfocus.pelletsboiler)
if solarfocus.system is Systems.Vampair:
    print(solarfocus.heatpump)
print("\n")
print(solarfocus.photovoltaic)
print("\n")
print(solarfocus.solar)