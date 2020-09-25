from PIL import Image
import smartcrop

sc = smartcrop.SmartCrop()


def crop_image(original_image: str) -> str:
    image = Image.open(original_image)

    res = sc.crop(image, image.width, image.width*9/16)

    if "top_crop" not in res:
        return original_image

    crop = res["top_crop"]

    w = int(crop["width"])
    h = int(crop["height"])

    x1 = int(crop["x"])
    y1 = int(crop["y"])

    x2 = x1 + w if x1 + w < image.width else image.width
    y2 = y1 + h if y1 + h < image.height else image.height

    area = (x1, y1, x2, y2)

    cropped_img = image.crop(area)

    parts = original_image.split("/")

    filename = parts[-1].split(".")
    filename = ".".join([filename[0] + "_cropped", ".".join(filename[1:])])

    final = parts[:-1]
    final.append(filename)

    new_path = "/".join(final)

    cropped_img.save(new_path)

    return new_path
