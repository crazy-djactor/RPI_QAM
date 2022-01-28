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
            'img_x': 25,
            'img_y': 200,
            'label_x': 405,
            'label_y': 805,
            'value_x': 605,
            'value_y': 805
        }

    @classmethod
    def ho2_axis(cls):
        return {
            'img_x': 975,
            'img_y': 200,
            'label_x': 1355,
            'label_y': 805,
            'value_x': 1555,
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
            'single': {
                'label_time_x': 100,
                'label_time_y': 720,
                'label_time_value_x': 105,
                'label_time_value_y': 750,
                'label_date_x': 250,
                'label_date_y': 720,
                'label_date_value_x': 255,
                'label_date_value_y': 750,
            },
            'double': {
                'label_time_x': 750,
                'label_time_y': 720,
                'label_time_value_x': 755,
                'label_time_value_y': 750,
                'label_date_x': 1000,
                'label_date_y': 720,
                'label_date_value_x': 1005,
                'label_date_value_y': 750,
            }
        }

    @classmethod
    def start_page_buttons(cls):
        return {
            'begin_testing': {'x': 25},
            'save_graph': {'x': 500},
            'about': {'x': 1450},
            'modify_report': {'x': 975},
            'change_settings': {'x': 1445}

        }

    @classmethod
    def page_one_buttons(cls):
        return {
            'equip': {'x': 25, 'y': 835, 'w': 920, 'h': 95},
            'stop_test': {'x': 975, 'y': 835, 'w': 920, 'h': 95}
        }