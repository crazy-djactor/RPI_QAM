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

    @classmethod
    def test_labels_axis(cls):
        return {
            'label_time_x': 100,
            'label_time_y': 720,
            'label_time_value_x': 105,
            'label_time_value_y': 750,
            'label_date_x': 250,
            'label_date_y': 720,
            'label_date_value_x': 255,
            'label_date_value_y': 750,
        }