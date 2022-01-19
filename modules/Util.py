# converts raw h2o data to ppb
import binascii


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


def time_elapsed_string(time_duration):
    _days = strfdelta(time_duration, "{days}")
    _hours = strfdelta(time_duration, "{hours}")
    _mins = strfdelta(time_duration, "{minutes}")

    if _days != '0':
        time_elapsed = strfdelta(time_duration, "{days} {hours} hours {minutes} minutes")
    else:
        if _hours != '0':
            time_elapsed = strfdelta(time_duration, "{hours} hours {minutes} minutes")
        else:
            time_elapsed = strfdelta(time_duration, "{minutes} minutes")
    return time_elapsed


def raw_to_ppb(data):
    raw_hex = str(binascii.hexlify(data[2:]))
    c = [raw_hex[i:i + 2] for i in range(0, len(raw_hex), 2)]
    try:
        byte1 = "{:08b}".format(int(c[1], base=16))
        byte2 = "{:08b}".format(int(c[2], base=16))
        byte3 = "{:08b}".format(int(c[3], base=16))
        byte4 = "{:08b}".format(int(c[4], base=16))
        byte5 = "{:08b}".format(int(c[5], base=16))

        h20_bin = byte1 + byte2 + byte3 + byte4 + byte5

        m1 = h20_bin[14:16]
        m2 = h20_bin[17:24]
        m3 = h20_bin[25:32]
        m4 = h20_bin[33:40]
        m = m1 + m2 + m3 + m4

        mantissa = (int(m[0]) * 2 ** 22 + int(m[1]) * 2 ** 21 + int(m[2]) * 2 ** 20 + int(m[3]) * \
                    2 ** 19 + int(m[4]) * 2 ** 18 + int(m[5]) * 2 ** 17 + int(m[6]) * 2 ** 16 + int(m[7]) * \
                    2 ** 15 + int(m[8]) * 2 ** 14 + int(m[9]) * 2 ** 13 + int(m[10]) * 2 ** 12 + int(m[11]) * \
                    2 ** 11 + int(m[12]) * 2 ** 10 + int(m[13]) * 2 ** 9 + int(m[14]) * 2 ** 8 + int(m[15]) * \
                    2 ** 7 + int(m[16]) * 2 ** 6 + int(m[17]) * 2 ** 5 + int(m[18]) * 2 ** 4 + int(m[19]) * \
                    2 ** 3 + int(m[20]) * 2 ** 2 + int(m[21]) * 2 ** 1 + int(m[22]) * 2 ** 0) / 8388608

        e1 = h20_bin[5:8]
        e2 = h20_bin[9:14]
        e = e1 + e2
        exponent = int(e, 2)
        sign = (-1) ** (int(h20_bin[4], 2))

        h20_ppb = sign * (2 ** (exponent - 127)) * (1 + mantissa)

        return (str(h20_ppb))
    except:
        pass

