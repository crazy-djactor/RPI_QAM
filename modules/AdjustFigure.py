class AdjustFigure:
    @classmethod
    def ext_figure_conf(cls):
        return {
            'w': 9.2,
            'h': 3.2,
            'dpi': 200
        }

    @classmethod
    def default_figure_conf(cls):
        return {
            'w': 4.6,
            'h': 3.2,
            'dpi': 200
        }

    @classmethod
    def o2_axis(cls):
        return {
            'img_x': 20,
            'img_y': 200,
            'label_x': 400,
            'label_y': 805,
            'value_x': 600,
            'value_y': 805
        }

    @classmethod
    def ho2_axis(cls):
        return {
            'img_x': 970,
            'img_y': 200,
            'label_x': 1350,
            'label_y': 805,
            'value_x': 1550,
            'value_y': 805
        }

    @classmethod
    def image_ext_axis(cls):
        return {
            'img_x': 20,
            'img_y': 200,
            'label_x': 880,
            'label_y': 805,
            'value_x': 1080,
            'value_y': 805
        }