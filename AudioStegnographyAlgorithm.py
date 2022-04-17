from abc import ABC, abstractmethod

# abstract class cho thuật toán mã hóa pha
class AudioStego(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def encodeAudio(self, audioLocation, stringToEncode) -> str:
        pass

    @abstractmethod
    def decodeAudio(self, audioLocation) -> str:
        pass

    @abstractmethod
    def convertToByteArray(self, audio):
        pass

    @abstractmethod
    def saveToLocation(self, audioArray, location) -> str:
        pass
