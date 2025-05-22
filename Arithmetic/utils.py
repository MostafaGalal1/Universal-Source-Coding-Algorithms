MAX_RANGE = (1 << 32) - 1
HALF = 1 << 31
QUARTER = 1 << 30


def read_file(file_path: str):
    with open(file_path, 'rb') as f:
        data = f.read()
    return data


def write_file(file_path: str, extension: str, data:  bytearray):
    with open(file_path + '.' + extension, 'wb') as f:
        f.write(data)


def interval_zooming(encoding, data, PMF, CDF):
    low, high = 0, MAX_RANGE
    underflow = 0

    code = 0
    pointer = 0

    input_length = len(data)
    data_length = sum(PMF.values())
    output = bytearray()

    if not encoding:
        for count in range(4):
            code = (code << 8) | (data[count] if count < input_length else 0)
            pointer += 8
        input_length *= 8

    for index in range(data_length):
        interval = high - low + 1

        b = None
        if encoding:
            b = data[index]
        else:
            value = ((code - low + 1) * data_length - 1) // interval
            for s, _ in CDF.items():
                if CDF[s] <= value < CDF[s] + PMF[s]:
                    b = s
                    break

            output.append(b)

        high = low + interval * (CDF[b] + PMF[b]) // data_length - 1
        low = low + interval * CDF[b] // data_length

        while True:
            if (low & HALF) == (high & HALF):
                if encoding:
                    bit = low >> 31

                    code |= bit
                    pointer += 1
                    if pointer % 8 == 0:
                        output.append(code)
                        code = 0
                    else:
                        code <<= 1

                    while underflow > 0:
                        code |= 1 - bit
                        pointer += 1
                        underflow -= 1
                        if pointer % 8 == 0:
                            output.append(code)
                            code = 0
                        else:
                            code <<= 1
            elif (low & QUARTER) and not (high & QUARTER):
                low -= QUARTER
                high -= QUARTER
                if encoding:
                    underflow += 1
                else:
                    code -= QUARTER
            else:
                break
            low = (low << 1) & MAX_RANGE
            high = ((high << 1) & MAX_RANGE) | 1
            if encoding:
                continue
            code = ((code << 1) & MAX_RANGE) | (
                1 if pointer < input_length and data[pointer // 8] >> (7 - pointer % 8) & 1 else 0)
            pointer += 1

    if encoding:
        underflow += 1
        bit = 1 if low < QUARTER else 0

        code |= 1 - bit
        code <<= 1
        pointer += 1
        if pointer % 8 == 0:
            output.append(code)
            code = 0
        for _ in range(underflow):
            code |= bit
            pointer += 1
            if pointer % 8 == 0:
                output.append(code)
                code = 0
            else:
                code <<= 1

        pointer += 1
        while pointer % 8 != 0:
            code <<= 1
            pointer += 1
        output.append(code)

    return output
