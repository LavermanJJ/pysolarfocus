"""Solarfocus fresh water module component"""
from .. import ApiVersions
from .base.component import Component
from .base.data_value import DataValue


class FreshWaterModule(Component):
    def __init__(self, input_address=700, api_version: ApiVersions = ApiVersions.V_23_020) -> None:
        super().__init__(input_address)
        self.state = DataValue(address=0)

        if api_version.greater_or_equal(ApiVersions.V_23_040.value):
            self.supply_temperature = DataValue(address=1, count=1, multiplier=0.1)
            self.flow_rate = DataValue(address=2, count=1, multiplier=0.1)
            self.target_temperature = DataValue(address=3, count=1, multiplier=0.1)
            self.valve = DataValue(address=4, count=1)


class FreshWaterModuleCascade(Component):
    """Fresh Water Module Cascade component (addresses 800-802)"""

    def __init__(self, input_address=800, api_version: ApiVersions = ApiVersions.V_23_040) -> None:
        super().__init__(input_address)

        if api_version.greater_or_equal(ApiVersions.V_23_040.value):
            self.state = DataValue(address=0)  # Statuszeile Kaskade FWM
            self.total_flow_rate = DataValue(address=1, multiplier=0.1)  # FWM Kaskade Gesamtdurchfluss
            self.target_temperature = DataValue(address=2, multiplier=0.1)  # FWM Kaskade Solltemperatur


class CirculationModule(Component):
    """Circulation Module component for DHW (addresses 850-851)"""

    def __init__(self, input_address=850, api_version: ApiVersions = ApiVersions.V_23_040) -> None:
        super().__init__(input_address)

        if api_version.greater_or_equal(ApiVersions.V_23_040.value):
            self.dhw_supply_temperature = DataValue(address=0, multiplier=0.1)  # Zirkultionsmodul WW-Vorlauftemperatur
            self.dhw_flow_rate = DataValue(address=1, multiplier=0.1)  # Zirkulationsmodul WW-Durchfluss
