#!/usr/bin/env python3

from collections import defaultdict
from functools import lru_cache

from glob import glob


BLACKLIST = [
    "jenkins-dood",
    "jenkins-slave-texlive",
    "jenkins-slave-texlive-personal"
]


TEMPLATE_BASE = """\
stages:
    - pull
{build_stages}
    - push
    - cleanup

image: docker:latest
before_script:
    - docker info
{pull}
{content}

cleanup unused docker images:
    stage: cleanup
    allow_failure: true
    script: >
        docker images --format '{{{{.ID}}}} {{{{.Tag}}}}' |
        awk '$2 ~ /<none>/ {{print $1}}' |
        xargs docker rmi
"""

TEMPLATE_STAGE = """    - build stage {i}"""

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
        - docker login --username "$DOCKER_HUB_USERNAME" --password "$DOCKER_HUB_PASSWORD"
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
        - docker login --username "$DOCKER_HUB_USERNAME" --password "$DOCKER_HUB_PASSWORD"
        - docker push pitkley/{package}:{version}
"""


@lru_cache()
def get_base_image(path):
    with open(path, "r") as fh:
        for line in fh.readlines():
            if not line.startswith("FROM "):
                continue
            return line.split(" ")[1].strip()


def get_image_and_tag(image):
    i = image.rsplit("/", maxsplit=1)[-1].split(":", maxsplit=1)
    if len(i) == 1:
        return (i[0], "latest")
    return tuple(i)


def Tree():
    return defaultdict(Tree)


def dicts(tree):
    return {k: dicts(tree[k]) for k in tree}


def insert_into_tree(tree, element):
    image, tag, _ = element
    for sub_element in tree:
        i, t, _ = sub_element
        if image == i:
            # Image exists
            if tag < t:
                # Insert before
                val = tree[sub_element]
                new_tree = Tree()
                new_tree[sub_element] = val
                del tree[sub_element]
                tree[element] = new_tree
            else:
                # Update the structure recursively
                insert_into_tree(tree[sub_element], element)
            break
    else:
        # Image did not yet exist, create it as a sibling
        tree[element]


def move_into_baseimages(tree, images, base_images):
    def get_base_image(image, tag, _):
        for (i, t, b, _) in images:
            if i == image and t == tag:
                return b
        return None

    for top_level_image in list(tree.keys()):
        base = base_in_tree(tree, get_image_and_tag(get_base_image(*top_level_image)))
        if base:
            remove_base(base_images, base)
            tree[base][top_level_image] = tree[top_level_image]
            del tree[top_level_image]


def remove_base(base_images, base):
    try:
        base_images.remove("pitkley/{}".format(base[0]))
    except:
        pass

def base_in_tree(tree, base):
    try:
        return list(filter(lambda e: e[0] == base[0] and e[1] == base[1], tree.keys()))[0]
    except:
        return None


def convert_to_buckets(t, l):
    try:
        # This works for a single item
        l.append(list(t.keys()))
        convert_to_buckets(list(t.values()), l)
    except AttributeError:
        # We probably have a list, not a single item
        if t == []:
            return

        keys = [k for ks in t for k in ks.keys()]
        if keys != []:
            l.append(keys)

        convert_to_buckets([v for vs in t for v in vs.values()], l)


def get_template_content(stage, path):
    path = path.split("/")

    if len(path) == 2:
        # path is of form "package/Dockerfile"
        return TEMPLATE_CONTENT.format(stage=stage, package=path[0])
    elif len(path) == 3:
        # path is of form "package/version/Dockerfile"
        return TEMPLATE_CONTENT_VERSION.format(stage=stage, package=path[0], version=path[1])
    else:
        raise Exception


def main():
    base_images = set()
    images = []

    # Get packages
    for path in sorted(filter(lambda e: e.split("/")[0] not in BLACKLIST,
                              glob('*/**/Dockerfile', recursive=True)),
                       key=lambda e: e.split("/")):
        base_image = get_base_image(path)
        if base_image:
            base_images.add(base_image)

        s = path.split("/")
        try:
            name, tag, _ = s
        except:
            name, tag = s[0], "latest"
        images.append((name, tag, base_image, path))

    T = Tree()
    for (i, t, _, p) in images:
        insert_into_tree(T, (i, t, p))
    move_into_baseimages(T, images, base_images)

    buckets = []
    convert_to_buckets(T, buckets)

    # Build output
    pull = "\n".join([TEMPLATE_PULL] + [TEMPLATE_PULL_SCRIPT.format(image=image)
                                        for image in sorted(base_images)])
    content = [get_template_content(n + 1, path) for n in range(len(buckets))
               for (_, _, path) in sorted(buckets[n])]
    output = TEMPLATE_BASE.format(
        build_stages="\n".join([TEMPLATE_STAGE.format(i=n + 1) for n in range(len(buckets))]),
        pull=pull,
        content="".join(content)
    )

    print(output)

if __name__ == '__main__':
    main()
