class Feature:
    def __init__(self, data, **kwargs):
        self.data = data
        self.kwargs = kwargs

    def __add_properties(self):
        return {
            "resourceCoords": [
                    [int(point) for point in self.data['image_points'].split(',')]
            ]
        }

    def __add_geometry(self):
        return {
            "type": "Point",
            "coordinates": [
                float(self.data['longitude']),
                float(self.data['latitude'])
            ]
        }

    def __add_metadata(self):
        return {
            "label": self.data['annotation_label'],
            "tags": [tag.strip() for tag in self.data['annotation_tags'].split(';')],
            "url": self.data['annotation_url'],
            "xywh": self.data['image_region'],
        }

    def build(self):
        return {
            "type": "Feature",
            "properties": self.__add_properties(),
            "geometry": self.__add_geometry(),
            "metadata": self.__add_metadata(),
        }
