import time

from utils import read_file, write_file


class LZWDecoder:
    def __init__(self, code_file_path):
        self.code_file_path = code_file_path
        self.output_file_path = code_file_path.rsplit('.', 2)[0]

    def decode(self):
        start_time = time.time()

        dictionary = {i: bytes([i]) for i in range(256)}
        encoded_data = read_file(self.code_file_path)

        total_bits = len(encoded_data) * 8

        index = 256
        pointer = 0
        shifts = 8

        decoded_data = bytearray()

        def _input():
            nonlocal pointer, shifts
            codeword = 0
            for i in range(shifts):
                codeword |= (encoded_data[pointer // 8] >> 7 - pointer % 8 & 1) << (shifts - 1 - i)
                pointer += 1
            return codeword

        code = _input()
        entry = dictionary[code]
        decoded_data.extend(entry)
        prev_entry = entry
        shifts += 1

        while pointer + shifts <= total_bits:
            code = _input()
            if code in dictionary:
                entry = dictionary[code]
            elif code == index:
                entry = prev_entry + prev_entry[:1]
            else:
                raise ValueError(f"Invalid code: {code}")

            decoded_data.extend(entry)

            dictionary[index] = prev_entry + entry[:1]
            prev_entry = entry
            index += 1

            if index & (index - 1) == 0:
                shifts += 1

        extension = self.code_file_path.rsplit('.', 2)[1].rsplit('.', 1)[0]
        write_file(self.output_file_path + '_decoded', extension, decoded_data)

        end_time = time.time()
        print(f"Decoding time: {end_time - start_time:.2f} seconds")


if __name__ == '__main__':
    decoder = LZWDecoder('input.txt.lzw')
    decoder.decode()
