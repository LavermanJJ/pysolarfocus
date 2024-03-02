"""Solarfocus abstract part"""

from abc import abstractmethod


class Part:
    """
    Abstraction of a metric of the heating system
    """

    @property
    @abstractmethod
    def scaled_value(self) -> float:
        pass
