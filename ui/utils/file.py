import os
import shutil
import tempfile
import streamlit as st


# generate tmp folder to save pdf file
def get_tmp_folder():
    if "tmp_folder" not in st.session_state:
        st.session_state["tmp_folder"] = tempfile.mkdtemp()
    return st.session_state["tmp_folder"]


# save pdf file to tmp folder
def save_pdf(pdf_file):
    tmp_folder = get_tmp_folder()
    pdf_path = os.path.join(tmp_folder, "problem.pdf")
    st.session_state["problem_pdf"] = pdf_path
    with open(pdf_path, "wb") as f:
        f.write(pdf_file)
    return pdf_path


# open pdf file from tmp folder
def open_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    return pdf_bytes


# remove tmp folder and all files
def remove_tmp_folder():
    if "tmp_folder" in st.session_state:
        tmp_folder = st.session_state["tmp_folder"]
        if os.path.exists(tmp_folder):
            shutil.rmtree(tmp_folder)
        del st.session_state["tmp_folder"]

    if "zip_file" in st.session_state:
        zip_file = st.session_state["zip_file"]
        if os.path.exists(zip_file):
            os.remove(zip_file)
        del st.session_state["zip_file"]

    if "temp_folders" in st.session_state:
        temp_folders = st.session_state["temp_folders"]
        for folder in temp_folders:
            if os.path.exists(folder):
                shutil.rmtree(folder)
        del st.session_state["temp_folders"]


# list folder all file paths
def list_folder(folder):
    if "tmp_folder" in st.session_state:
        tmp_folder = st.session_state["tmp_folder"]
        folder = os.path.join(tmp_folder, folder)
        if os.path.exists(folder):
            return os.listdir(folder)
        else:
            os.makedirs(folder, exist_ok=True)
    return []


# open file from tmp folder to string
def open_file(folder, filename):
    if "tmp_folder" in st.session_state:
        tmp_folder = st.session_state["tmp_folder"]
        filepath = os.path.join(tmp_folder, folder, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return f.read()
    return ""


# save text file to tmp folder
def save_file(folder, filename, data):
    tmp_folder = get_tmp_folder()
    filepath = os.path.join(tmp_folder, folder, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(data)
    return filepath


# delete file from tmp folder
def delete_file(path):
    tmp_folder = get_tmp_folder()
    filepath = os.path.join(tmp_folder, path)
    if os.path.exists(filepath):
        os.remove(filepath)


# get or create file from temp folder, and return file content
def get_or_create_file(path, default_content=""):
    tmp_folder = get_tmp_folder()
    filepath = os.path.join(tmp_folder, path)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return f.read()
    else:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write(default_content)
        return default_content


# cteate folder in tmp folder
def create_folder(folder):
    tmp_folder = get_tmp_folder()
    folder = os.path.join(tmp_folder, folder)
    os.makedirs(folder, exist_ok=True)
    return folder


# check folder exists in tmp folder
def folder_exists(folder):
    tmp_folder = get_tmp_folder()
    folder = os.path.join(tmp_folder, folder)
    return os.path.exists(folder)


# list files in folder, and return file paths
def list_files(folder):
    tmp_folder = get_tmp_folder()
    folder = os.path.join(tmp_folder, folder)
    if os.path.exists(folder):
        return list(sorted(os.listdir(folder)))
    else:
        os.makedirs(folder, exist_ok=True)
    return []


def pair_files(paths):
    # Sort the paths first to ensure pairing is in order
    sorted_paths = sorted(paths)
    # Create a dictionary to store pairs
    pairs = {}
    for path in sorted_paths:
        # Split the path to get the base part and the extension
        base, ext = path.rsplit(".", 1)
        if base not in pairs:
            pairs[base] = [None, None]
        # Assign the file to the appropriate slot in the pair (0 for .in, 1 for .ans)
        pairs[base][0 if ext == "in" else 1] = path
    # Extract the pairs and return
    return list(pairs.values())


def get_next_filename(paths, parent_folder):
    # Extract the numeric parts of the filenames
    numbers = [int(path.split("/")[-1].split(".")[0]) for path in paths]
    # Find the maximum number
    max_number = max(numbers) if numbers else 0
    # Generate the next number and create filenames
    next_number = max_number + 1
    next_filenames = [
        str(os.path.join(parent_folder, f"{next_number}.in")),
        str(os.path.join(parent_folder, f"{next_number}.ans")),
    ]
    return next_filenames


# create zip file from tmp folder, and can set zip file name, save to new tmp folder
def create_zip_file(zip_name=None):
    tmp_folder = get_tmp_folder()
    zip_name = zip_name or "problem"
    new_tmp_folder = tempfile.mkdtemp()
    if "temp_folders" in st.session_state:
        st.session_state["temp_folders"].append(new_tmp_folder)
    else:
        st.session_state["temp_folders"] = [new_tmp_folder]
    zip_path = os.path.join(new_tmp_folder, zip_name)
    out = shutil.make_archive(zip_path, "zip", tmp_folder)
    path = os.path.join(new_tmp_folder, out)
    return path
