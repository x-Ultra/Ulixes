import base64
import csv
import urllib.request
import functools

IMAGES_PATH = "./images"
MAX_SEC_IN_CACHE = 3600
MAX_CACHE_SIZE = 20

# verrà tenuta traccia delle immagini già scaricate
downloaded_images = []

class Image:

    def __init__(self, pict_name, pict_url):
        # nomi delle immagini salvate senza spazi
        self.name = pict_name.replace(" ", "")
        self.url = pict_url

    def get_name(self):
        return self.name

    def get_url(self):
        return self.url


def downloadPicture(imageClass):
    if imageClass.get_name() not in downloaded_images:
        urllib.request.urlretrieve(imageClass.get_url(), IMAGES_PATH + "/" + imageClass.get_name())
        downloaded_images.append(imageClass.get_name())
        # print("Downloaded {}\n".format(imageClass.get_name()))
    # else:
    # print("Picture {} already downloaded".format(downloaded_images))


def downloadPicturesByCsv(csv_file_path):
    csvfile = open(csv_file_path, newline='')
    csv_reader = csv.DictReader(csvfile)
    images = []
    for row in csv_reader:
        name = row["Location"]
        url = row["PictureUrl"]
        image = Image(name, url)
        images.append(image)

    dowloadPicturesByImagesList(images)


def dowloadPicturesByImagesList(images_list):
    for image in images_list:
        downloadPicture(image)


# funzione che verrà direttamente chiamata da ulisse per ottenere la base64 di un immagine
@functools.lru_cache(maxsize=MAX_CACHE_SIZE)
def getBase64Picture(imageClass):

    # scarica l'immagine, se necessario
    downloadPicture(imageClass)

    # apri il file e crea la sua codifica base64
    img = open(IMAGES_PATH + "/" + imageClass.get_name(), "rb")
    base64pict = base64.b64encode(img.read()).decode("utf-8")

    return base64pict


def downloadAll():
    downloadPicturesByCsv("../landmarksComplete.csv")

"""
if __name__ == "__main__":
    img = Image("Statua di Pasquino",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Pasquino.jpg/1200px-Pasquino.jpg")
    res = getBase64Picture(img)
    print(res)
"""
