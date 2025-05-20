from utils import interval_zooming, read_file, write_file


def read_meta_file(file_path: str):
    PMF = {}
    CDF = {}

    with open(file_path.rsplit('.', 1)[0] + '.meta', 'r') as f:
        lines = f.readlines()
        extension = lines[0].strip()
        prev = 0
        for line in lines[1:]:
            symbol, value = line.split(':')
            b = int(symbol.strip())
            val = int(value.strip())
            CDF[b] = prev
            PMF[b] = val - prev
            prev = val

    return PMF, CDF, extension


class ArithmeticDecoder:
    def __init__(self, code_file_path):
        self.code_file_path = code_file_path
        self.output_file_path = code_file_path.rsplit('.', 2)[0]

    def decode(self):
        data = read_file(self.code_file_path)
        PMF, CDF, extension = read_meta_file(self.code_file_path)
        decoded_data = interval_zooming(encoding=False, data=data, PMF=PMF, CDF=CDF)
        write_file(self.output_file_path + '_decoded', extension, decoded_data)


if __name__ == '__main__':
    decoder = ArithmeticDecoder('input.txt.arth')
    decoder.decode()
