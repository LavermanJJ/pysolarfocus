from .part import Part

class PerformanceCalculator(Part):
    """
    Performing performance calculations
    """
    
    nominator:Part
    denominator:Part
    value:int
    
    def __init__(self, nominator:Part, denominator:Part) -> None:
        self.nominator = nominator
        self.denominator = denominator
    
    @property
    def scaled_value(self)->float:
        """
        To provide a uniform interface for integrating, a scaled value property is offered
        """
        if self.denominator.scaled_value:
            self.value =  self.nominator.scaled_value / self.denominator.scaled_value
        else:
            self.value = 0.0
            
        return self.value