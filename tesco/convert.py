from PIL import Image
import pathlib

GROCERY_SHOP = "tesco"
# img_files = [x for x in img_paths if x.is_file()]


class Convertor:
    def __init__(self, grocery_shop=GROCERY_SHOP):
        """
        prepare a list of directories for the conversion in later steps
        """
        img_path = pathlib.Path.cwd()/"screenshots"
        pdf_path = pathlib.Path.cwd()/"pdfs"
        grocery_screenshots_dir = img_path/grocery_shop
        grocery_pdfs_dir = pdf_path/grocery_shop
        img_paths = pathlib.Path(grocery_screenshots_dir).rglob("*.png")
        self.img_file_paths = list(filter(pathlib.Path.is_file, img_paths))
        # using the first file as out filename
        filename = self.get_filename(self.img_file_paths[0])
        self.out_path = grocery_pdfs_dir/f"{filename}.pdf"
        self.converted_imgs = []

    def convert_pdf(self):
        """
        convert a list of imgs based on its filepath into pdf,
        and save to designated location
        """
        for img_path in self.img_file_paths:
            converted_img = Image.open(img_path).convert('RGB')
            self.converted_imgs.append(converted_img)

    def save_pdf(self):
        """
        save a list of converted pdf (binary) to file
        """
        self.converted_imgs[0].save(
            self.out_path, save_all=True, quality=100, append_images=self.converted_imgs[1:])

    def get_filename(self, img_filepath):
        """
        get the pdf filename based on img file name 
        e.g. tesco img file:tesco-Apr 28 - May 04
        pdf file:
        """
        return img_filepath.stem[6:]


if __name__ == "__main__":
    convertor = Convertor(GROCERY_SHOP)
    convertor.convert_pdf()
    convertor.save_pdf()
