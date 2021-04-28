from PIL import Image
import pathlib

GROCERY_SHOP = "tesco"
# image_files = [x for x in image_paths if x.is_file()]


class Convertor:
    def __init__(self, grocery_shop=GROCERY_SHOP):
        """
        prepare a list of directories for the conversion in later steps
        """
        img_path = pathlib.Path.cwd()/"screenshots"
        pdf_path = pathlib.Path.cwd()/"pdfs"
        grocery_screenshots_dir = img_path/grocery_shop
        self.grocery_pdfs_dir = pdf_path/grocery_shop
        image_paths = pathlib.Path(grocery_screenshots_dir).rglob("*.png")
        self.image_files = list(filter(pathlib.Path.is_file, image_paths))

    def convert_pdf(self):
        """
        convert a list of images based on its filepath into pdf,
        and save to designated location
        """
        for img_path in self.image_files:
            filename = self.get_filename(img_path)
            converted_img = Image.open(img_path).convert('RGB')
            converted_img.save(self.grocery_pdfs_dir/f"{filename}.pdf")

    def get_filename(self, img_filepath):
        """
        get the pdf filename based on image file name 
        e.g. tesco img file:tesco-Apr 28 - May 04
        pdf file:
        """
        return img_filepath.stem[6:]


if __name__ == "__main__":
    convertor = Convertor(GROCERY_SHOP)
    convertor.convert_pdf()
