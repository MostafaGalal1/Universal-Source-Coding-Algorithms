import time

from utils import read_file, write_file


class LZWEncoder:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    def encode(self):
        start_time = time.time()

        dictionary = {bytes([i]): i for i in range(256)}
        data = read_file(self.data_file_path)

        index = 256
        pointer = 0
        byte = 0
        shifts = 8

        encoded_data = bytearray()

        def _output(n):
            nonlocal byte, pointer, shifts, encoded_data
            for i in range(shifts):
                byte |= (n >> shifts - 1 - i & 1) << 7 - pointer % 8
                pointer += 1
                if pointer % 8 == 0:
                    encoded_data.append(byte)
                    byte = 0

        next_code = bytearray()
        for b in data:
            next_code.append(b)
            if bytes(next_code) not in dictionary:
                num = dictionary[bytes(next_code[:-1])]
                _output(num)

                if index & (index - 1) == 0:
                    shifts += 1
                dictionary[bytes(next_code)] = index
                index += 1

                next_code = bytearray([b])

        num = dictionary[bytes(next_code)]
        _output(num)

        if pointer % 8 != 0:
            encoded_data.append(byte)

        write_file(self.data_file_path, 'lzw', encoded_data)

        end_time = time.time()
        print(f"Encoding time: {end_time - start_time:.2f} seconds")


if __name__ == '__main__':
    encoder = LZWEncoder('input.txt')
    encoder.encode()
