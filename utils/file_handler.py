import os


UPLOAD_FOLDER = "uploads/waste_images"


def create_upload_directory():

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )


def save_uploaded_file(
        uploaded_file):

    if uploaded_file is None:
        return ""

    create_upload_directory()

    file_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(
            file_path,
            "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )

    return file_path


def file_exists(
        file_path):

    return (
        file_path
        and
        os.path.exists(file_path)
    )