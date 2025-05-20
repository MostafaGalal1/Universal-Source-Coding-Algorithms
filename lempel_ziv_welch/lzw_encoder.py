from utils import read_file, write_file


class LZWEncoder:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    def encode(self):
        data = read_file(self.data_file_path)

        dictionary = {bytes([i]): i for i in range(256)}
        index = 255
        pointer = 0
        byte = 0
        shifts = 8

        code = bytearray()
        encoded_data = bytearray()

        for b in data:
            code.append(b)
            if bytes(code) not in dictionary:
                num = dictionary[bytes(code[:-1])]
                for i in range(shifts):
                    byte |= ((num >> shifts - 1 - i) & 1) << 7 - pointer % 8
                    pointer += 1
                    if pointer % 8 == 0:
                        encoded_data.append(byte)
                        byte = 0

                if index & (index-1) == 0:
                    shifts += 1
                index += 1
                dictionary[bytes(code)] = index
                code = bytearray([b])

        if code:
            num = dictionary[bytes(code)]
            for i in range(shifts):
                byte |= ((num >> (shifts - 1 - i)) & 1) << (7 - pointer % 8)
                pointer += 1
                if pointer % 8 == 0:
                    encoded_data.append(byte)
                    byte = 0

        if pointer % 8 != 0:
            encoded_data.append(byte)

        write_file(self.data_file_path, 'lzw', encoded_data)


if __name__ == '__main__':
    encoder = LZWEncoder('input.txt')
    encoder.encode()
