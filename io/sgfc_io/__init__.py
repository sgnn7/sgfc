import importlib

from .devices.api_interface import IoDeviceApi

# TODO: Make this dynamic
I2C = IoDeviceApi.I2C

def get_device(dev_type, flags=None):
    device_impl_module = importlib.import_module('.devices.%s' % dev_type, __name__)
    device_impl_class_name = dev_type.title().replace('_','') + 'IoDevice'

    device_class = getattr(device_impl_module, device_impl_class_name)

    return device_class(flags)
