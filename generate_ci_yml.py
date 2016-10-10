#!/usr/bin/env python3.5

from glob import glob

TEMPLATE_BASE = """
stages:
    - pull
    - build
    - push

before_script:
    - docker info

{pull}
{content}
"""

TEMPLATE_PULL = """
pull:
    stage: pull
    script:"""
TEMPLATE_PULL_SCRIPT = """        - 'docker pull {image} || :'"""

TEMPLATE_CONTENT = """
{package}:latest:build:
    stage: build
    script:
        - cd {package}
        - docker build -t pitkley/{package}:latest .

{package}:latest:push:
    stage: push
    only:
        - master
    script:
        - docker push pitkley/{package}:latest
"""

TEMPLATE_CONTENT_VERSION = """
{package}:{version}:build:
    stage: build
    script:
        - cd {package}/{version}
        - docker build -t pitkley/{package}:{version} .

{package}:{version}:push:
    stage: push
    only:
        - master
    script:
        - docker push pitkley/{package}:{version}
"""

def get_base_image(path):
    with open(path, "r") as fh:
        for line in fh.readlines():
            if not line.startswith("FROM "):
                continue
            return line.split(" ")[1].strip()


def get_template_content(path):
    path = path.split("/")

    if len(path) == 2:
        # path is of form "package/Dockerfile"
        return TEMPLATE_CONTENT.format(package=path[0])
    elif len(path) == 3:
        # path is of form "package/version/Dockerfile"
        return TEMPLATE_CONTENT_VERSION.format(package=path[0], version=path[1])


def main():
    base_images = set()
    packages = []

    # Get packages
    for path in sorted(glob('*/**/Dockerfile', recursive=True), key=lambda e: e.split("/")):
        image = get_base_image(path)
        if image:
            base_images.add(image)
        packages.append(get_template_content(path))

    pull = "\n".join([TEMPLATE_PULL] + [TEMPLATE_PULL_SCRIPT.format(image=image) for image in sorted(base_images)])
    print(TEMPLATE_BASE.format(pull=pull, content="".join(packages)))

if __name__ == '__main__':
    main()
