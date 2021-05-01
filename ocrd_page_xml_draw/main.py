import ocrd
import ocrd_modelfactory
import ocrd_models.ocrd_page as ocrd_page
import ocrd_models.ocrd_page_generateds as ocrd_page_gends
import ocrd_utils

from os.path import join
from pathlib import Path
from json import load

from page_xml_draw.struct.xml import XmlTraverser
from page_xml_draw.struct.json import JsonSchema, JsonInstance
from page_xml_draw.core import ImageDrawer

from ocrd_page_xml_draw.tool import OCRD_TOOL
from ocrd_page_xml_draw.util import pil_to_cv2_rgb, cv2_to_pil_rgb


class OcrdPageXmlDraw(ocrd.Processor):
    tool = "ocrd-page-xml-draw"
    log = ocrd_utils.getLogger("processor.OcrdPageXmlDraw")

    def __init__(self, *args, **kwargs):
        kwargs['ocrd_tool'] = OCRD_TOOL['tools'][self.tool]
        kwargs['version'] = OCRD_TOOL['version']
        super(OcrdPageXmlDraw, self).__init__(*args, **kwargs)

    @property
    def file_id(self):
        file_id = self.input_file.ID.replace(
            self.input_file_grp,
            self.output_file_grp
        )

        if file_id == self.input_file.ID:
            file_id = ocrd_utils.concat_padded(
                self.output_file_grp,
                self.page_num
            )

        return file_id

    def process(self):
        for (self.page_num, self.input_file) in enumerate(self.input_files):
            self.log.info(
                "Processing input file: %i / %s",
                self.page_num,
                self.input_file
            )

            self.workspace.download_file(self.input_file)

            traverser = XmlTraverser(self.input_file.local_filename)

            # Create a new PAGE file from the input file:
            page_id = self.input_file.pageId or self.input_file.ID
            page = traverser.pcgts.get_Page()

            # Get image from PAGE:
            page_image, _, _ = self.workspace.image_from_page(
                page,
                page_id
            )

            # Convert PIL to cv2 (RGB):
            page_image, alpha = pil_to_cv2_rgb(page_image)

            # Read profile (instance) from JSON file and validate:
            with open(self.parameter['profile'], 'r') as fp:
                schema = JsonSchema.default()
                styles = JsonInstance(load(fp))
                schema.validate(styles)

            drawer = ImageDrawer(
                traverser,
                styles,
                base_dir=Path(self.workspace.directory)
            )

            if self.parameter['output-format'] == "image/png":
                drawing = drawer.draw()

                # Retrieve overlay and convert image back to PIL:
                page_image = cv2_to_pil_rgb(drawing.result, alpha=alpha)

                # Save image:
                self.workspace.save_image_file(
                    image=page_image,
                    file_id=self.file_id+page_id,
                    file_grp=self.output_file_grp,
                    page_id=page_id,
                    mimetype="image/png"
                )

            elif self.parameter['output-format'] == "text/html":
                image_map = drawer.map()

                # Render image map and write it to output file:
                self.workspace.add_file(
                    ID=self.file_id,
                    file_grp=self.output_file_grp,
                    pageId=page_id,
                    mimetype="text/html",
                    local_filename=join(
                        self.output_file_grp,
                        self.file_id
                    ) + ".html",
                    content=image_map.result
                )
