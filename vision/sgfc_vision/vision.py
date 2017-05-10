import cv2

DEFAULT_JPEG_QUALITY=95

global _capture_devices
_capture_devices = {}

def get_device(dev_index):
    global _capture_devices

    if dev_index not in _capture_devices:
        _capture_device = cv2.VideoCapture(dev_index)

        if not _capture_device.isOpened():
            raise RuntimeError("Could not acquire capture device!")

        _capture_devices[dev_index] = _capture_device

    return _capture_devices[dev_index]

def get_compressed_image(capture_device, quality=DEFAULT_JPEG_QUALITY):
    result, captured_frame = capture_device.read()
    if not result:
        raise RuntimeError("Could not acquire image!")

    encode_params = [cv2.IMWRITE_JPEG_QUALITY, DEFAULT_JPEG_QUALITY]
    result, compressed_image = cv2.imencode('.jpg', captured_frame, encode_params)
    if not result:
        raise RuntimeError("Could not encode image!")

    return compressed_image
