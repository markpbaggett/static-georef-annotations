from iiif_prezi3 import Canvas, load_bundled_extensions, AnnotationPage, Annotation, ResourceItem
import httpx
import json


class AnnotatedCanvas:
    def __init__(self, iiif_image, annotations=None, **kwargs):
        self.iiif_image = iiif_image
        self.annotations = annotations
        self.client = httpx.Client(follow_redirects=True)
        self.image_details = self.__get_image_response(iiif_image)
        self.canvas_id = kwargs.get('canvas_id', 'https://example.org/georeferencing-example/canvas/p1')
        print(self.canvas_id)
        self.canvas_label = self.__get_canvas_label(kwargs.get('canvas_label', 'Example Georeferencing Annotation List'))
        print(self.canvas_label)
        self.extensions = self.__build_extensions()

    @staticmethod
    def __get_canvas_label(label):
        return {'none': [label]}

    def __build_extensions(self):
        georef = self.client.get('http://iiif.io/api/extension/georef/1/context.json').json()
        return load_bundled_extensions([georef])

    def __get_image_response(self, image):
        r = self.client.get(f"{image}/info.json")
        return r.json()

    def __get_service(self):
        context = self.image_details['@context']
        if context == 'https://iiif.io/api/image':
            return {
                "id": self.iiif_image,
                "type": "ImageService3",
                "profile": "level2"
            }
        elif context == 'http://iiif.io/api/image/2/context.json':
            return {
                "@context": "http://iiif.io/api/image/2/context.json",
                "id": self.iiif_image,
                "profile": "http://iiif.io/api/image/2/level2.json",
                "type": "ImageService2"
            }

    def build(self):
        canvas = Canvas(
            id=self.canvas_id,
            label=self.canvas_label,
            height=self.image_details.get('height'),
            width=self.image_details.get('width'),
        )
        an_annotation = Annotation(type='Annotation', id=f"{self.canvas_id}/annotation/0", target=self.canvas_id)
        an_annotation.motivation = 'painting'
        an_annotation.body = ResourceItem(
            service=[self.__get_service()],
            id=f"{self.iiif_image}/full/full/0/default.png",
            type='Image'
        )
        an_annotation_page = AnnotationPage(type='AnnotationPage')
        an_annotation_page.items = [an_annotation]
        canvas.items = [an_annotation_page]
        georef_features = self.__build_annotations()
        if georef_features:
            canvas.annotations = [georef_features]
        canvas_string = canvas.json(indent=2)
        canvas_as_json = json.loads(canvas_string)
        canvas_as_json['@context'] = ["http://iiif.io/api/extension/georef/1/context.json", "http://iiif.io/api/presentation/3/context.json"]
        return canvas_as_json

    def write_to_file(self, path):
        with open(path, 'w') as outfile:
            json.dump(self.build(), outfile)

    def __build_annotations(self):
        if self.annotations:
            an_annotation = Annotation(
                type='Annotation',
                id=f"{self.canvas_id}/georef/annotation/0",
                target=self.canvas_id
            )
            an_annotation.motivation = 'georeferencing'
            an_annotation.body = ResourceItem(
                id=f"{self.canvas_id}/feature-collection",
                type='FeatureCollection',
                transformation={
                    "type": "polynomial",
                    "options": {
                        "order": 1
                    }
                },
            )
            an_annotation_page = AnnotationPage(type='AnnotationPage')
            an_annotation_page.items = [an_annotation]
            return an_annotation_page
        else:
            return None


if __name__ == "__main__":
    x = AnnotatedCanvas(
        iiif_image='https://api.library.tamu.edu/iiif/2/f10c7823-4e52-334d-829a-239b69b9f81d;1',
        canvas_id='https://example.org/georeferencing-example/canvas/p2',
        canvas_label='Mark'
    )
    x.write_to_file('examples/test.json')