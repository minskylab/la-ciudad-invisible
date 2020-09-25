import smartcrop
from PIL import Image
import json

sc = smartcrop.SmartCrop()


def crop_image(original_image: str) -> str:
    image = Image.open(original_image)

    res = sc.crop(image, image.width, image.width*9/16)

    if "top_crop" not in res:
        return original_image

    crop = res["top_crop"]

    x1 = int(crop["x"])
    y1 = int(crop["y"])
    x2 = x1 + int(crop["width"]) if x1 + \
        int(crop["width"]) < image.width else image.width
    y2 = x1 + int(crop["height"]) if y1 + \
        int(crop["height"]) < image.height else image.height

    area = (x1, y1, x2, y2)

    cropped_img = image.crop(area)

    parts = original_image.split("/")
    print(parts)

    filename = parts[-1].split(".")
    print(filename)
    filename = ".".join([filename[0] + "_cropped", ".".join(filename[1:])])
    print(filename)
    new_path = "/".join(parts[:-1].append(filename))

    print(new_path)

    cropped_img.save(new_path)

    return new_path
