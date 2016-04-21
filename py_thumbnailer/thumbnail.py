import mimetypes
import re

from . import exceptions, thumbnailers


def create_thumbnail(source_file, resize_to=None):
    if isinstance(source_file, basestring):
        source_file = open(source_file, 'rb')

    mime_type, encoding = mimetypes.guess_type(source_file.name, strict=False)
    if (mime_type is None) and ('.' in source_file.name):
        extension = source_file.name.rsplit('.', 1)[-1].lower()
        mime_type = mimetypes_by_extension.get(extension)
    if mime_type is None:
        raise exceptions.MimeTypeNotFoundException('Can\'t find mimetype for %s' % source_file.name)

    thumbnail_class = thumbnailer_for(mime_type)
    return thumbnail_class.thumbnail(source_file, resize_to)


thumbnailers_by_mimetype = {
    'application/postscript': thumbnailers.PSThumbnailer,
    'application/pdf': thumbnailers.PDFThumbnailer,

    # "Office" documents
    'application/msword': thumbnailers.UnoconvThumbnailer,
    # doc
    re.compile('^'+re.escape('application/vnd.ms-')): thumbnailers.UnoconvThumbnailer,
    # xls/ppt
    re.compile('^'+re.escape('application/vnd.openxmlformats-officedocument.')): thumbnailers.UnoconvThumbnailer,
    # docx, pptx, xlsx
    'application/vnd.ms-excel.sheet.macroEnabled.12': thumbnailers.UnoconvThumbnailer,
    # xlsm: xlsx with macros

    # specific mime types have precedence over regexes so PNMToImage will be
    # preferred over ImageMagick for pnm files.
    'image/x-portable-pixmap': thumbnailers.ImageThumbnailer,
    'image/x-portable-bitmap': thumbnailers.ImageThumbnailer,

    # all image-like formats, also uncommon ones like
    #    .psd -> image/vnd.adobe.photoshop
    #    .tga -> image/x-targa
    re.compile('^image/'): thumbnailers.ImageThumbnailer,

    re.compile('^video/'): thumbnailers.FFMPEGThumbnailer,
    # videos
    # ogg is a container format both for audio (Ogg Vorbis) and videos (Ogg
    # Theora). Python's mimetypes library does not differentiate between these
    # two so we just try ffmpeg for both. It'll just fail for audio but that
    # shouldn't do any harm.
    'audio/ogg': thumbnailers.FFMPEGThumbnailer,
}

# Python's mimetypes library does not detect all file formats so we have a
# fallback to "detect" a mime type based on the file extension.
mimetypes_by_extension = {
    'f4v': 'video/x-flv',
}


def thumbnailer_for(mime_type):
    thumbnailer_class = thumbnailers_by_mimetype.get(mime_type)
    if thumbnailer_class is None:
        regex_thumbnailers = filter(lambda key: not isinstance(key, basestring), thumbnailers_by_mimetype)
        for regex in regex_thumbnailers:
            if regex.match(mime_type):
                thumbnailer_class = thumbnailers_by_mimetype[regex]
                break
        else:
            raise exceptions.ThumbnailerNotFoundException('Thumbnailer can\'t be found for %s' % mime_type)

    return thumbnailer_class
