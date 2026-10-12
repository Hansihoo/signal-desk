"""Read edition-bound illustrations without requiring raster preview files."""
import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path


def reviewed_asset(visual, directory):
    filename = visual['asset']
    if Path(filename).name != filename:
        raise ValueError('Invalid visual asset filename')
    data = (Path(directory) / filename).read_bytes()
    if hashlib.sha256(data).hexdigest() != visual['sha256']:
        raise ValueError('Visual asset does not match reviewed bytes')
    if filename.endswith('.png') and data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png', data
    if filename.endswith('.svg'):
        try:
            root = ET.fromstring(data)
        except ET.ParseError as exc:
            raise ValueError('Invalid SVG illustration') from exc
        if root.tag != '{http://www.w3.org/2000/svg}svg':
            raise ValueError('Invalid SVG illustration')
        for element in root.iter():
            if element.tag.split('}')[-1].lower() in ('script', 'foreignobject'):
                raise ValueError('SVG illustration must contain static graphics')
            for name, value in element.attrib.items():
                name = name.split('}')[-1].lower()
                if name.startswith('on') or (name == 'href' and not value.startswith('#')):
                    raise ValueError('SVG illustration must contain static graphics')
        return 'image/svg+xml', data
    raise ValueError('Visual asset does not match reviewed bytes')
