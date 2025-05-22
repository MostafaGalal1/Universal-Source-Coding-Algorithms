import time

from utils import interval_zooming, read_file, write_file


def create_probability_model(data):
    PMF = {}
    for b in data:
        PMF[b] = PMF.get(b, 0) + 1

    CDF = {}
    acc = 0
    for s, _ in sorted(PMF.items()):
        CDF[s] = acc
        acc += PMF[s]

    return PMF, CDF


def write_meta_file(file_path: str, PMF: dict, CDF: dict):
    with open(file_path + '.meta', 'w') as f:
        f.write(file_path.rsplit('.', 1)[1] + '\n')
        for symbol, value in CDF.items():
            f.write(f"{symbol}: {value + PMF[symbol]}\n")


class ArithmeticEncoder:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    def encode(self):
        start_time = time.time()

        data = read_file(self.data_file_path)
        PMF, CDF = create_probability_model(data)
        encoded_data = interval_zooming(encoding=True, data=data, PMF=PMF, CDF=CDF)
        write_meta_file(self.data_file_path, PMF, CDF)
        write_file(self.data_file_path, 'arth', encoded_data)

        end_time = time.time()
        print(f"Encoding time: {end_time - start_time:.2f} seconds")


if __name__ == '__main__':
    encoder = ArithmeticEncoder('input.txt')
    encoder.encode()
