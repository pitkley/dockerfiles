#!/usr/bin/env python3.5

from collections import defaultdict
from functools import lru_cache
from itertools import chain, islice, tee, zip_longest

from glob import glob


TEMPLATE_BASE = """
stages:
    - pull
{build_stages}
    - push

before_script:
    - docker info

{pull}
{content}
"""

TEMPLATE_STAGE ="""    - build stage {i}"""

TEMPLATE_PULL = """
pull:
    stage: pull
    script:"""
TEMPLATE_PULL_SCRIPT = """        - 'docker pull {image} || :'"""

TEMPLATE_CONTENT = """
{package}:latest:build:
    stage: build stage {stage}
    only:
        - master
        - /ci-/
        - /-ci/
        - /{package}/
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
    stage: build stage {stage}
    only:
        - master
        - /ci-/
        - /-ci/
        - /{package}/
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


# Based on: http://stackoverflow.com/a/1012089/758165
def this_and_next(some_iterable):
    items, nexts = tee(some_iterable)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(items, nexts)


@lru_cache()
def get_base_image(path):
    with open(path, "r") as fh:
        for line in fh.readlines():
            if not line.startswith("FROM "):
                continue
            return line.split(" ")[1].strip()


def get_template_content(stage, path):
    path = path.split("/")

    if len(path) == 2:
        # path is of form "package/Dockerfile"
        return TEMPLATE_CONTENT.format(stage=stage, package=path[0])
    elif len(path) == 3:
        # path is of form "package/version/Dockerfile"
        return TEMPLATE_CONTENT_VERSION.format(stage=stage, package=path[0], version=path[1])


def build_buckets(groups):
    naive_buckets = [list(filter(None.__ne__, l)) for l in zip_longest(*groups.values())]
    buckets = []

    done = set()
    for naive_bucket, next_bucket in this_and_next(naive_buckets):
        # Create data structures
        bucket = []

        # Create set of images in this bucket
        images = set()
        for image in naive_bucket:
            e = image.split("/")
            if len(e) == 2:
                images.add("pitkley/{}".format(e[0]))
            elif len(e) == 3:
                images.add("pitkley/{}:{}".format(e[0], e[1]))

        # Work through images
        for image in naive_bucket:
            base_image = get_base_image(image)

            if base_image in images and base_image not in done:
                next_bucket.append(image)
                continue

            bucket.append(image)

        buckets.append(bucket)

    return buckets


def main():
    base_images = set()

    groups = defaultdict(list)

    # Get packages
    for path in sorted(glob('*/**/Dockerfile', recursive=True), key=lambda e: e.split("/")):
        image = get_base_image(path)
        if image:
            base_images.add(image)

        name = path.split("/")[0]
        groups[name].append(path)

    # Build buckets from groups
    buckets = build_buckets(groups)

    # Build output
    pull = "\n".join([TEMPLATE_PULL] + [TEMPLATE_PULL_SCRIPT.format(image=image) for image in sorted(base_images)])
    content = [get_template_content(n + 1, path) for n in range(len(buckets)) for path in sorted(buckets[n])]
    output = TEMPLATE_BASE.format(
        build_stages="\n".join([TEMPLATE_STAGE.format(i=n + 1) for n in range(len(buckets))]),
        pull=pull,
        content="".join(content)
    )

    print(output)

if __name__ == '__main__':
    main()
