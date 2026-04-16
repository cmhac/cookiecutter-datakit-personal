"""Generate and upload a simple HTML index for project files in S3."""

import sys

import boto3

S3_RESOURCE = boto3.resource("s3")
BUCKET_NAME = "data-reporting-datakit-output-v2-prod"
BUCKET = S3_RESOURCE.Bucket(BUCKET_NAME)


def get_files(project_repo):
    """
    Retrieve file paths in the S3 bucket for a given project.

    Return each path as a list of nested directory parts.
    """
    files = []
    for file_path in BUCKET.objects.filter(Prefix=project_repo):
        # path `project/dir/file.txt` becomes [`project`, `dir`, `file.txt`]
        split_path = str(file_path.key).split("/")
        # don't need the "project" part of the path since we're only concerned
        # with files related to the same project
        files.append(split_path[1:])

    return files


def structure_files(project_repo):
    """
    Convert project file paths from S3 into a nested directory mapping.

    Each key in the dictionary represents one directory or file name.
    """
    files = get_files(project_repo)

    output = {}
    for path in files:
        helper = output
        for directory in path:
            if directory not in helper:
                helper[directory] = {}
            helper = helper[directory]

    return output


def get_all_directories(files, nested):
    """
    Return file-path elements recursively as HTML fragments.

    Nested levels are represented with progressively larger left margins.
    """
    for key, value in files.items():
        # put an extra line break above a new branch's "subdirectory" section
        line_break = "<br>" if nested == 0 else ""
        # Style top-level entries like headers, and indent by nesting depth.
        style_str = (
            ' style="font-size: 28px; font-weight: bold; margin-bottom: 15px"'
            if nested == 0
            else f' style="font-size: 20px; margin-left: {nested * 15}px"'
        )
        yield f"<p{style_str}>{line_break}> {key}</p>"
        # retrieves the next nested item(s) if any are there
        if isinstance(value, dict):
            yield from get_all_directories(value, nested + 1)


def construct_index(project_repo):
    """Construct the HTML body for a project's root `index.html` file."""
    files = structure_files(project_repo)

    # Unsure why, but we can't use f-strings!
    html_string = (
        "<html><head><style>body {margin: 50px}</style></head>"
        f"<body><h1>Directory for {project_repo}</h1>"
    )

    for directory in get_all_directories(files, 0):
        html_string += directory

    html_string += "</body></html>"

    return html_string


def write_index(project_repo):
    """Write `index.html` to the S3 path for the given project."""
    index_content = construct_index(project_repo)

    s3_object = S3_RESOURCE.Object(BUCKET_NAME, f"{project_repo}/index.html")
    s3_object.put(
        Body=index_content,
        ContentType="text/html",
        ContentDisposition="inline",
    )


if __name__ == "__main__":
    write_index(sys.argv[1])
