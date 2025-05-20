from utils import read_file, write_file


class LZWDecoder:
    def __init__(self, code_file_path):
        self.code_file_path = code_file_path
        self.output_file_path = code_file_path.rsplit('.', 2)[0]

    def decode(self):
        encoded_data = read_file(self.code_file_path)
        pointer = 0
        total_bits = len(encoded_data) * 8

        dictionary = {i: bytes([i]) for i in range(256)}
        index = 255
        shifts = 8
        decoded_data = bytearray()

        prev_code = 0
        for i in range(shifts):
            prev_code |= ((encoded_data[pointer // 8] >> (7 - pointer % 8)) & 1) << (shifts - 1 - i)
            pointer += 1
        if prev_code >= index:
            raise ValueError("Invalid first code")

        decoded_data.extend(dictionary[prev_code])
        prev_entry = dictionary[prev_code]

        while pointer + shifts <= total_bits:
            curr_code = 0
            for i in range(shifts):
                curr_code |= ((encoded_data[pointer // 8] >> (7 - pointer % 8)) & 1) << (shifts - 1 - i)
                pointer += 1
            if curr_code in dictionary:
                entry = dictionary[curr_code]
            elif curr_code == index+1:
                entry = prev_entry + prev_entry[:1]
            else:
                raise ValueError(f"Invalid code: {curr_code}")

            decoded_data.extend(entry)

            dictionary[index+1] = prev_entry + entry[:1]
            index += 1

            if index & (index - 1) == 0:
                shifts += 1

            prev_entry = entry

        extension = self.code_file_path.rsplit('.', 2)[1].rsplit('.', 1)[0]
        write_file(self.output_file_path + '_decoded', extension, decoded_data)


if __name__ == '__main__':
    decoder = LZWDecoder('input.txt.lzw')
    decoder.decode()
