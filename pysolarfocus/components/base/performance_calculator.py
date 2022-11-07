from .part import Part

class PerformanceCalculator(Part):
    """
    Performing performance calculations
    """
    
    nominator:Part
    denominator:Part
    value:int = None
    
    def __init__(self, nominator:Part, denominator:Part) -> None:
        self.nominator = nominator
        self.denominator = denominator
    
    @property
    def value(self)->float:
        """
        Return value of the calculation
        """
        if self.denominator.scaled_value:
            return self.nominator.scaled_value / self.denominator.scaled_value
        return 0.0
    
    @property
    def scaled_value(self)->float:
        """
        To provide a uniform interface for integrating, a scaled value property is offered
        """
        return self.value
            