def recalc_crop_coordinates(crop, kwargs):
    """

    :param crop: port or land or None
    :param kwargs:
    :return: tuple(x1, y1, x2, y2), elems are strs
    """
    if not crop:
        return ','.join(map(lambda x: str(x), (kwargs['x1'], kwargs['y1'], kwargs['x2'], kwargs['y2'])))
    kwargs = {k: int(v) for k, v in kwargs.items()}
    if crop == 'port':
        return ','.join(map(lambda x: str(x), get_portrait_crop_coordinates(kwargs)))
    elif crop == 'land':
        return ','.join(map(lambda x: str(x), get_landscape_crop_coordinates(kwargs)))


def get_portrait_crop_coordinates(kwargs):
    x1, y1, x2, y2 = kwargs['x1'], kwargs['y1'], kwargs['x2'], kwargs['y2']
    width = x2 - x1
    crop_x_value = round(width * 0.25 / 2)
    x1 += crop_x_value
    x2 -= crop_x_value
    return x1, y1, x2, y2


def get_landscape_crop_coordinates(kwargs):
    x1, y1, x2, y2 = kwargs['x1'], kwargs['y1'], kwargs['x2'], kwargs['y2']
    width = y2 - y1
    crop_y_value = round(width * 0.5 / 2)
    y1 += crop_y_value
    y2 -= crop_y_value
    return x1, y1, x2, y2


