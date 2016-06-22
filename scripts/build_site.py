"""Build the image analysis project static web site."""

import os
import os.path
import shutil
from distutils.dir_util import copy_tree

import yaml
from slugify import slugify
from jinja2 import FileSystemLoader, Environment, Template

HERE = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(HERE, "templates")
BASE_DIR = os.path.join(HERE, "..")
PROJECTS_DIR = os.path.join(BASE_DIR, "project_descriptions")
BUILD_DIR = os.path.join(BASE_DIR, "build")


INDEX_TEMPLATE_FNAME = "index.html"


class BioimageProject(object):

    def __init__(self, directory):
        if directory.endswith("/"):
            directory = directory[:-1]
        self.directory = directory

        self._info_init()
        self._image_init()

    def _info_init(self):
        info_fpath = os.path.join(self.directory, "project.yml")
        self.info = yaml.load(file(info_fpath))

    def _image_init(self):
        self.image_fpath = None

        image_dir = os.path.join(BUILD_DIR, "images")
        input_image = os.path.join(self.directory, "image-400x200px.png")

        if os.path.isfile(input_image):
            if not os.path.isdir(image_dir):
                os.makedirs(image_dir)
            image_fname = slugify(unicode(self.info["name"])) + ".png"
            output_image = os.path.join(image_dir, image_fname)
            shutil.copy(input_image, output_image)
            self.image_fpath = os.path.join("images", image_fname)



def load_template(template_fname):
    template_loader = FileSystemLoader(TEMPLATE_DIR)
    template_environment = Environment(loader=template_loader)
    template = template_environment.get_template(template_fname)
    return template

def copy_supporting_files():
    """Copy javascript, CSS and font files to output directory."""

    support_dirs = ['css',]
#   support_dirs = ['js', 'css', 'fonts']

    for dirname in support_dirs:
        source_path = os.path.join(TEMPLATE_DIR, dirname)
        dest_path = os.path.join(BUILD_DIR, dirname)
        copy_tree(source_path, dest_path)


def build_site():
    if not os.path.isdir(BUILD_DIR):
        os.mkdir(BUILD_DIR)

    copy_supporting_files()

    projects = []
    for proj_name in os.listdir(PROJECTS_DIR):
        proj_dir = os.path.join(PROJECTS_DIR, proj_name)
        proj = BioimageProject(proj_dir)
        if "public" in proj.info and proj.info["public"]:
            projects.append(proj)
    template = load_template(INDEX_TEMPLATE_FNAME)
    html = template.render(projects=projects)

    index_fpath = os.path.join(BUILD_DIR, "index.html")
    with open(index_fpath, "w") as fh:
        fh.write(html)


def main():
    build_site()


if __name__ == "__main__":
    main()
