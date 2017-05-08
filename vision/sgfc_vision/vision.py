import cv2


def get_compressed_image(dev_index=1):
    capture_device = cv2.VideoCapture(dev_index)

    captured_frame = None
    try:
        result, captured_frame = capture_device.read()
    finally:
        if capture_device:
            capture_device.release()

    encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, compressed_image = cv2.imencode('.jpg', captured_frame, encode_params)

    print("Orig:", len(captured_frame))
    print("Jpg:", len(compressed_image))

    return compressed_image

class Vision(object):
    pass
