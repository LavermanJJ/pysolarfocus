__version__ = '0.0.1'

from .const import B1_REGMAP_INPUT, B1_START_ADDR


class SolarfocusAPI():
    """Solarfocus Heating System"""

    @property
    def hc1_supply_temp(self):
        """Supply temperature of heating circuit 1"""
        return self._block_1_input_regs.get('HC_1_SUPPLY_TEMPERATURE')['value'] * 0.1


    def __init__(self, conn, slave, update_on_read=False):
        """Initialize Solarfocus communication."""
        self._conn = conn
        self._block_1_input_regs = B1_REGMAP_INPUT
        self._slave = slave
        self._update_on_read = update_on_read

    def connect(self):
        return self._conn.connect()

    def update(self):
        """Read values from Heating System"""
        ret = True
        try:
            block_1_result_input = self._conn.read_input_registers(
                unit=self._slave,
                address=B1_START_ADDR,
                count=len(self._block_1_input_regs)).registers
        except AttributeError:
            # The unit does not reply reliably
            ret = False
            print("Modbus read failed")

        else:
            for k in self._block_1_input_regs:
                self._block_1_input_regs[k]['value'] = \
                    block_1_result_input[
                        self._block_1_input_regs[k]['addr'] - B1_START_ADDR]

        return ret
