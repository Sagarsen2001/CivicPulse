"""
=========================================
CivicPulse File Utilities
=========================================

Utility functions for handling uploaded files.

Author : Sagar Sen
Project: CivicPulse
"""

import os
import uuid


# ==========================================
# Allowed Extensions
# ==========================================

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}


# ==========================================
# Check Allowed File
# ==========================================

def allowed_file(filename):
    """
    Check whether the uploaded file has
    an allowed image extension.
    """

    if not filename:

        return False

    if "." not in filename:

        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in ALLOWED_EXTENSIONS


# ==========================================
# Get File Extension
# ==========================================

def get_file_extension(filename):
    """
    Return the extension of a file.
    """

    if not filename or "." not in filename:

        return ""

    return filename.rsplit(
        ".",
        1
    )[1].lower()


# ==========================================
# Generate Unique Filename
# ==========================================

def generate_unique_filename(filename):
    """
    Generate a unique filename while
    preserving the original extension.
    """

    extension = get_file_extension(
        filename
    )

    unique_name = uuid.uuid4().hex

    if extension:

        return f"{unique_name}.{extension}"

    return unique_name


# ==========================================
# Create Directory
# ==========================================

def create_directory(directory_path):
    """
    Create a directory if it does not exist.
    """

    if not directory_path:

        return False

    try:

        os.makedirs(
            directory_path,
            exist_ok=True
        )

        return True

    except OSError as error:

        print(
            "❌ Directory Creation Error:",
            error
        )

        return False


# ==========================================
# Delete File
# ==========================================

def delete_file(file_path):
    """
    Delete a file safely.
    """

    if not file_path:

        return False

    try:

        if os.path.exists(file_path):

            os.remove(file_path)

            return True

        return False

    except OSError as error:

        print(
            "❌ File Deletion Error:",
            error
        )

        return False