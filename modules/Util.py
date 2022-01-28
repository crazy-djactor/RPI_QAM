# converts raw h2o data to ppb
import binascii
from datetime import datetime

from modules.AdjustFigure import AdjustFigure


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

        return str(h20_ppb)
    except:
        pass


def config_canvas_test(co2, ch2o, option,
                       lbl_o2, value_o2, lbl_h2o, value_h2o,
                       label_time, label_time_value,
                       label_date, label_date_value):
    ext_fig = AdjustFigure.ext_figure_conf()
    default_fig = AdjustFigure.default_figure_conf()
    ext_position = AdjustFigure.image_ext_axis()
    o2_position = AdjustFigure.o2_axis()
    h2o_position = AdjustFigure.ho2_axis()

    extend_width = ext_fig['w'] * ext_fig['dpi'] - 1
    extend_height = ext_fig['h'] * ext_fig['dpi']
    default_width = default_fig['w'] * default_fig['dpi'] - 1
    default_height = default_fig['h'] * default_fig['dpi']
    labels_axis = AdjustFigure.test_labels_axis()['single']

    if option == 'radO2':
        co2.get_tk_widget().config(width=extend_width, height=extend_height)
        co2.get_tk_widget().place(x=ext_position['img_x'], y=ext_position['img_y'] - 40)
        ch2o.get_tk_widget().place_forget()
        lbl_o2.place(x=ext_position['label_x'], y=ext_position['label_y'] - 42)
        value_o2.place(x=ext_position['value_x'], y=ext_position['value_y'] - 42)
        lbl_h2o.place_forget()
        value_h2o.place_forget()
    elif option == 'radH2O':
        ch2o.get_tk_widget().config(width=extend_width, height=extend_height)
        ch2o.get_tk_widget().place(x=ext_position['img_x'], y=ext_position['img_y'] - 40)
        co2.get_tk_widget().place_forget()
        lbl_h2o.place(x=ext_position['label_x'], y=ext_position['label_y'] - 42)
        value_h2o.place(x=ext_position['value_x'], y=ext_position['value_y'] - 42)
        lbl_o2.place_forget()
        value_o2.place_forget()

    else:
        co2.get_tk_widget().config(width=default_width, height=default_height)
        ch2o.get_tk_widget().config(width=default_width, height=default_height)
        co2.get_tk_widget().place(x=o2_position['img_x'], y=o2_position['img_y'] - 40)
        ch2o.get_tk_widget().place(x=h2o_position['img_x'], y=h2o_position['img_y'] - 40)
        lbl_o2.place(x=o2_position['label_x'], y=o2_position['label_y'] - 42)
        value_o2.place(x=o2_position['value_x'], y=o2_position['value_y'] - 42)
        lbl_h2o.place(x=h2o_position['label_x'], y=h2o_position['label_y'] - 42)
        value_h2o.place(x=h2o_position['value_x'], y=h2o_position['value_y'] - 42)
        labels_axis = AdjustFigure.test_labels_axis()['double']
    label_time.place(x=labels_axis['label_time_x'], y=labels_axis['label_time_y'])
    label_time_value.place(x=labels_axis['label_time_value_x'], y=labels_axis['label_time_value_y'])
    # Start Date Display
    label_date.place(x=labels_axis['label_date_x'], y=labels_axis['label_date_y'])
    label_date_value.place(x=labels_axis['label_date_value_x'], y=labels_axis['label_date_value_y'])


def replace_objects(obj_o2, obj_h2o, option,
                    lbl_o2=None, value_o2=None, lbl_h2o=None, value_h2o=None):
    place_info1 = obj_o2.place_info()
    place_info2 = obj_h2o.place_info()
    o2_position = AdjustFigure.o2_axis()
    h2o_position = AdjustFigure.ho2_axis()
    ext_position = AdjustFigure.image_ext_axis()
    if option == 'radBoth':
        if place_info1.get('x') != f"{o2_position['img_x']}":  # need to replace
            obj_o2.place(x=o2_position['img_x'], y=o2_position['img_y'])
        if lbl_o2 is not None and lbl_o2.place_info().get('x') != f"{o2_position['label_x']}":
            lbl_o2.place(x=o2_position['label_x'], y=o2_position['label_y'])
            value_o2.place(x=o2_position['value_x'], y=o2_position['value_y'])

        if place_info2.get('x') != f"{h2o_position['img_x']}":
            obj_h2o.place(x=h2o_position['img_x'], y=h2o_position['img_y'])
        if lbl_h2o is not None and lbl_h2o.place_info().get('x') != f"{h2o_position['label_x']}":
            lbl_h2o.place(x=h2o_position['label_x'], y=h2o_position['label_y'])
            value_h2o.place(x=h2o_position['value_x'], y=h2o_position['value_y'])
    elif option == 'radH2O':
        if place_info2.get('x') != f"{ext_position['img_x']}":
            obj_h2o.place(x=ext_position['img_x'], y=ext_position['img_y'])
        if lbl_h2o is not None and value_h2o is not None and lbl_h2o.place_info().get(
                'x') != f"{ext_position['label_x']}":
            lbl_h2o.place(x=ext_position['label_x'], y=ext_position['label_y'])
            value_h2o.place(x=ext_position['value_x'], y=ext_position['value_y'])
        if place_info1.get('x'):
            obj_o2.place_forget()
            if lbl_o2 is not None and value_o2 is not None:
                lbl_o2.place_forget()
                value_o2.place_forget()
    elif option == 'radO2':
        if place_info1.get('x') != f"{(ext_position['img_x'])}":
            obj_o2.place(x=ext_position['img_x'], y=ext_position['img_y'])
        if lbl_o2 is not None and lbl_o2.place_info().get('x') != f"{ext_position['label_x']}":
            lbl_o2.place(x=ext_position['label_x'], y=ext_position['label_y'])
            value_o2.place(x=ext_position['value_x'], y=ext_position['value_y'])
        if place_info2.get('x'):
            obj_h2o.place_forget()
            if lbl_h2o is not None:
                lbl_h2o.place_forget()
                value_h2o.place_forget()


#### ~lines0-500 are serial communication functions ###
# Function for converting decimal to binary
def float_bin(number, places=3):
    whole, dec = str(number).split(".")
    print("whole = " + str(whole))
    print("dec = " + str(dec))
    whole = int(whole)
    dec = int(dec)
    if dec == 0:
        dec = 1
    if dec < 10:
        dec += 10
    for z in str(dec):
        if z == 0:
            z = 1
    res = bin(whole).lstrip("0b") + "."
    print("res = " + str(res))
    for x in range(places):
        whole, dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        res += whole

    return res


# converts whole numbers to decimal equivalent (234 becomes .234)
def decimal_converter(num):
    while num > 1:
        num /= 10
    return num

    # function for converting a float number to a 5 byte IEEE-754 packet


def IEEE754(n):
    # identifying whether the number
    # is positive or negative
    sign = 0
    if n < 0:
        sign = 1
        n = n * (-1)
    p = 30

    # convert float to binary
    dec = float_bin(n, places=p)

    # separate the decimal part
    # and the whole number part
    whole, dec = str(dec).split(".")
    whole = int(whole)

    # calculating the exponent(E)
    exponent = len(str(whole)) - 1
    exponent_bits = 127 + exponent

    # converting the exponent from
    # decimal to binary
    exponent_bits = bin(exponent_bits).lstrip("0b")

    # finding the mantissa
    mantissa = str(whole)[1:exponent + 1]
    mantissa = mantissa + dec
    mantissa = mantissa[0:23]

    # the IEEE754 notation in binary
    final = str(sign) + str(exponent_bits) + mantissa
    byte1 = "0000" + final[0:4]
    byte2 = "0" + final[4:11]
    byte3 = "0" + final[11:18]
    byte4 = "0" + final[18:25]
    byte5 = "0" + final[25:32]
    databyte1 = bytearray([int(byte1, 2)])
    databyte2 = bytearray([int(byte2, 2)])
    databyte3 = bytearray([int(byte3, 2)])
    databyte4 = bytearray([int(byte4, 2)])
    databyte5 = bytearray([int(byte5, 2)])

    return (databyte1, databyte2, databyte3, databyte4, databyte5)


def pdf_time(time_elapsed):
    if time_elapsed.days > 0:
        string_elapsed = f"{time_elapsed.days}D {time_elapsed.seconds // 3600}H {time_elapsed.seconds // 60 % 60}M"
    elif time_elapsed.seconds > 3600:
        string_elapsed = f"{time_elapsed.seconds // 3600}hr {time_elapsed.seconds // 60 % 60}min"
    else:
        string_elapsed = f"{time_elapsed.seconds // 60 % 60}minutes"
    return string_elapsed
