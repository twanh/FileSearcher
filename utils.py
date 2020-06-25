import os

# Keeps track of which type of extension should be classified as what
fileTypes = {
    'document_ext': ['.docx', '.doc', '.odt', '.pdf', '.gdoc', '.xls', '.xlsx', '.ods', '.ppt', '.pptx', '.md', '.gslides', '.gsheets'],
    # Image extensions
    'image_ext': ['.gif', '.png', '.jpg', '.jpeg', '.webp', '.tiff', '.psd', '.ai'],
}

# Stores the strings used to keep track of the file type.
fileTypeNames = {
    'directory':'dir',
    'document': 'doc',
    'image': 'img',
    'other': 'any',
}

# Returns the type of file (from the fileTypeNames dict) based on the file types stored in fileTypes
def getFileType(path: str) -> str:
    if os.path.isdir(path): 
        return fileTypeNames['directory']
    filename, ext = os.path.splitext(path)
    if ext in fileTypes['document_ext']:
        return fileTypeNames['document']
    if ext in fileTypes['image_ext']:
        return fileTypeNames['image']
    return fileTypeNames['other']
