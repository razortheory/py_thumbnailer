=====================
Documents Thumbnailer
=====================

Main idea was taken from https://github.com/FelixSchwarz/anythumbnailer.
Code rewriten from zero.

A CLI utility/Python library to create thumbnails for different file types
(including PDF, mp4 videos and Microsoft Office documents aka docx/xlsx/pptx).

All the heavy-lifting is done by commonly-used tools such as LibreOffice/unoconv,
ffmpeg, poppler and ImageMagick so format support is limited by what these tools
can process.


Program requirements
--------------------
Video encoding: `ffmpeg`
Pdf encoding: `poppler-utils`
Office files: `unoconv`
Imagemagic external libraries: `http://pillow.readthedocs.org/en/3.2.x/installation.html#external-libraries`


Installation
------------
    ::

        $ pip install py-thumbnailer
        
Usage
-----
From command line:
    ::

        $ py-thumbnailer SOURCEFILE [OUTPUTFILE]

From python code:
    ::

        from py_thumbnailer.thumbnail import create_thumbnail
        output_buffer = create_thumbnail(source_file)


Unoconv doesn't support multiprocessing, so you have to use mutex
    ::

        import fcntl

        try:
            fcntl.flock(converter_lock, fcntl.LOCK_EX)
            preview_buffer = create_thumbnail(document.document_file, resize_to=400)
        finally:
            fcntl.flock(converter_lock, fcntl.LOCK_UN)
