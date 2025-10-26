# * Adapted from: https://https://github.com/kwsch/PKHeX/blob/master/PKHeX.Core/PKM/Util/PokeCrypto

class PokeCrypto:
    BlockCount = 4
    SIZE_9BLOCK = 80
    SIZE_9STORED = 8 + (BlockCount * SIZE_9BLOCK)
    SIZE_9PARTY = SIZE_9STORED + 0x10

    BlockPosition = [
            0, 1, 2, 3,
            0, 1, 3, 2,
            0, 2, 1, 3,
            0, 3, 1, 2,
            0, 2, 3, 1,
            0, 3, 2, 1,
            1, 0, 2, 3,
            1, 0, 3, 2,
            2, 0, 1, 3,
            3, 0, 1, 2,
            2, 0, 3, 1,
            3, 0, 2, 1,
            1, 2, 0, 3,
            1, 3, 0, 2,
            2, 1, 0, 3,
            3, 1, 0, 2,
            2, 3, 0, 1,
            3, 2, 0, 1,
            1, 2, 3, 0,
            1, 3, 2, 0,
            2, 1, 3, 0,
            3, 1, 2, 0,
            2, 3, 1, 0,
            3, 2, 1, 0,
            0, 1, 2, 3,
            0, 1, 3, 2,
            0, 2, 1, 3,
            0, 3, 1, 2,
            0, 2, 3, 1,
            0, 3, 2, 1,
            1, 0, 2, 3,
            1, 0, 3, 2,]

    BlockPositionInvert = [
        0, 1, 2, 4, 3, 5, 6, 7, 12, 18, 13, 19, 8, 10, 14, 20, 16, 22, 9, 11, 15, 21, 17, 23,
        0, 1, 2, 4, 3, 5, 6, 7,]

    @staticmethod
    def CryptArray(data: bytearray, seed):
        for i in range(int(len(data)/2)):
            seed = (0x41C64E6D * seed) + 0x00006073
            xor = (seed >> 16) & 0xFFFF
            xor = int.from_bytes(xor.to_bytes(length=2), byteorder="little")
            data[i*2:((i+1)*2)] = (int.from_bytes(data[i*2:((i+1)*2)]) ^ xor).to_bytes(length=2)
        return(data)
    @staticmethod
    def CryptPKM(data: bytearray, pv, blockSize):
        start = 8
        end = (PokeCrypto.BlockCount * blockSize) + start
        data[start:end] = PokeCrypto.CryptArray(data[start:end], pv)
        if len(data) > end:
            data[end:] = PokeCrypto.CryptArray(data[end:], pv)
        return(data)
    @staticmethod
    def ShuffleArray(data, sv, block_size):
        result = bytearray(len(data))
        index = sv * PokeCrypto.BlockCount
        start = 8
        result[:start] = data[:start]
        end = start + (block_size * PokeCrypto.BlockCount)
        result[end:] = data[end:]
        for block in range(PokeCrypto.BlockCount):
            dest_start = start + (block_size * block)
            dest_end = dest_start + block_size
            ofs = PokeCrypto.BlockPosition[index + block]
            src_start = start + (block_size * ofs)
            src_end = src_start + block_size
            result[dest_start:dest_end] = data[src_start:src_end]
        return(result)
    @staticmethod
    def DecryptArray9(ekr: bytearray):
        pv = int.from_bytes(ekr[0:4], byteorder="little")
        sv = (pv >> 13) & 31

        ekr = PokeCrypto.CryptPKM(ekr, pv, PokeCrypto.SIZE_9BLOCK)
        return PokeCrypto.ShuffleArray(ekr, sv, PokeCrypto.SIZE_9BLOCK)
    @staticmethod
    def EncryptArray9(pk: bytearray):
        pv = int.from_bytes(pk[0:4], byteorder="little")
        sv = (pv >> 13) & 31
        ekm = PokeCrypto.ShuffleArray(pk, PokeCrypto.BlockPositionInvert[sv], PokeCrypto.SIZE_9BLOCK)
        return PokeCrypto.CryptPKM(ekm, pv, PokeCrypto.SIZE_9BLOCK)
    
