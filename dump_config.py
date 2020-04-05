#!/usr/bin/python

if __name__ == '__main__':
    import json
    from location import *
    _temperature_probes = [{k: v} for (k, v) in temperature_probes.items()]
    temperature_probes = _temperature_probes
    del(_temperature_probes, k, v)
    print(json.dumps({ key:value for (key, value) in locals().items() if type(value) in [str, dict, float, int, list] and not key.startswith('__')}))
