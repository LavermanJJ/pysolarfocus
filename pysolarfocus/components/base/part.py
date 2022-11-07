from abc import abstractmethod


class Part(object):
    """
    Performing performance calculations
    """
    
    @property
    @abstractmethod
    def scaled_value(self)->float:
        pass