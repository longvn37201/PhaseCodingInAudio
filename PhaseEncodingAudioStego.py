import os.path

import numpy as np
from scipy.io import wavfile

from AudioStegnographyAlgorithm import AudioStego


class PhaseEncodingAudioStego(AudioStego):

    # ma hoa
    def encodeAudio(self, audioLocation, stringToEncode) -> str:

        self.convertToByteArray(audioLocation)

        stringToEncode = stringToEncode.ljust(100, '~')

        #Bước 1: Chia dữ liệu âm thanh gốc thành các khối (segments)
        textLength = 8 * len(stringToEncode)
        blockLength = int(2 * 2 ** np.ceil(np.log2(2 * textLength)))
        blockNumber = int(np.ceil(self.audioData.shape[0] / blockLength))
        # chuyển sang mảng numpy 2 chiều
        if len(self.audioData.shape) == 1:
            print("1")
            self.audioData.resize(blockNumber * blockLength, refcheck=False)
            self.audioData = self.audioData[np.newaxis]
        else:
            print("2")
            self.audioData.resize((blockNumber * blockLength, self.audioData.shape[1]), refcheck=False)
            self.audioData = self.audioData.T
        blocks = self.audioData[0].reshape((blockNumber, blockLength))

        #Bước 2: Biến đổi DFT cho mỗi khối,
        # với ma trận độ lớn pha (phases) và ma trận độ lớn tín hiệu (magnitudes)
        blocks = np.fft.fft(blocks)
        magnitudes = np.abs(blocks)
        phases = np.angle(blocks)

        #Bước 3: Tính toán sự chênh lệch pha các đoạn kề nhau  (phaseDiffs)
        phaseDiffs = np.diff(phases, axis=0)

        #Bước 4: Mã hóa dữ liệu nhị phân của thông điệp
        textInBinary = np.ravel([[int(y) for y in format(ord(x), "08b")] for x in stringToEncode]) #chuyển thông điệp về bin arr
        textInPi = textInBinary.copy()
        # nếu bit =1 -> pha mới -pi/2
        # nếu bit =0 -> pha mới pi/2
        textInPi[textInPi == 0] = -1
        textInPi = textInPi * -np.pi / 2

        #Bước 5: Giấu tin vào vector pha đoạn đầu tiên
        blockMid = blockLength // 2
        phases[0, blockMid - textLength: blockMid] = textInPi
        phases[0, blockMid + 1: blockMid + 1 + textLength] = -textInPi[::-1]

        #Bước 6: Kết hợp ma trận độ lớn tín hiệu ở Bước2
        #Tái tạo lại ma trận pha của các đoạn kề nhau
        for i in range(1, len(phases)):
            phases[i] = phases[i - 1] + phaseDiffs[i - 1]
        blocks = (magnitudes * np.exp(1j * phases))

        #Bước 7: DFT ngược và ghép các block lại để tạo lại dữ liệu âm thanh
        blocks = np.fft.ifft(blocks).real
        self.audioData[0] = blocks.ravel().astype(np.int16)

        # lưu file đã giấu tin
        return self.saveToLocation(self.audioData.T, audioLocation)

    # giải mã
    def decodeAudio(self, audioLocation) -> str:

        self.convertToByteArray(audioLocation)
        textLength = 800

        # tính toán độ dài các block (segment)
        blockLength = 2 * int(2 ** np.ceil(np.log2(2 * textLength)))
        blockMid = blockLength // 2

        # lấy đoạn đầu ra
        if len(self.audioData.shape) == 1:
            secret = self.audioData[:blockLength]
        else:
            secret = self.audioData[:blockLength, 0]

        # Thực hiện DFT để lấy ra bin arr, chứa thông điệp đã giấu
        secretPhases = np.angle(np.fft.fft(secret))[blockMid - textLength:blockMid]
        secretInBinary = (secretPhases < 0).astype(np.int8)

        # chuyển đổi sang dạng int code
        secretInIntCode = secretInBinary.reshape((-1, 8)).dot(1 << np.arange(8 - 1, -1, -1))

        # ghép lại thành thông điệp
        return "".join(np.char.mod("%c", secretInIntCode)).replace("~", "")

    def convertToByteArray(self, audio):
        # Chuyển đổi sang dạng byte arr
        try:
            self.rate, self.audioData = wavfile.read(audio)
        except:
            pass
        self.audioData = self.audioData.copy()

    def saveToLocation(self, audioArray, location) -> str:
        # save file
        dir = os.path.dirname(location)
        wavfile.write(dir + "/output-pc.wav", self.rate, audioArray)
        return dir + "/output-pc.wav"
