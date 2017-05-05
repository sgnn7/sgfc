import importlib

def get_device(dev_type, dev_address, callback, error_callback, device=None):
    device_impl_module = importlib.import_module('.devices.%s' % dev_type, __name__)
    device_impl_class_name = dev_type.title().replace('_','') + 'CommDevice'

    device_class = getattr(device_impl_module, device_impl_class_name)

    return device_class(device, dev_address, callback=callback, error_callback=error_callback)
