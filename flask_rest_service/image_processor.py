import os
from flask_restful import Resource
from flask import Flask, url_for, json, request
from wand.image import Image
import zipfile
import StringIO
from flask import send_file

class InMemoryZip(object):
    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_zip = StringIO.StringIO()

    def append(self, filename_in_zip, file_contents):
        '''Appends a file with name filename_in_zip and contents of
        file_contents to the in-memory zip.'''
        # Get a handle to the in-memory zip in append mode
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0

        return self

    def read(self):
        '''Returns a string with the contents of the in-memory zip.'''
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()

    def writetofile(self, filename):
        '''Writes the in-memory zip to a file.'''
        f = file(filename, "w")
        f.write(self.read())
        f.close()

class ImageiOS():

    def __init__(self, dict):
        self.size = tuple(dict["size"].split("x"))
        self.scale = dict["scale"][0]
        self.idiom = dict["idiom"]
        self.filename = dict["filename"]

    def real_size(self):
        a, b = self.size
        ra = float(a) * float(self.scale)
        rb = float(b) * float(self.scale)
        return int(ra), int(rb)


class HelloWorld(Resource):

    def size_list(self):
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "resources/", "Contents.json")
        data = json.load(open(json_url))
        res =  map(lambda x:ImageiOS(x), data["images"])
        return res

    def resize_image(self, image):
        imz = InMemoryZip()
        for item in self.size_list():
            with image.clone() as i:
                i.resize(item.real_size()[0], item.real_size()[1])
                #i.save(filename=item.filename)
                imz.append("AppIcon.appiconset/"+item.filename, i.make_blob("png"))
                #myzip.write(item.filename)
        #imz.writetofile("test.zip")
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "resources/", "Contents.json")
        data = open(json_url).read()
        imz.append("AppIcon.appiconset/Contents.json", data)
        return imz

    def post(self):
        img = Image(blob=request.files["image"].stream)
        res = self.resize_image(img)

        res.in_memory_zip.seek(0)
        return  send_file(res.in_memory_zip, mimetype=' application/octet-stream')