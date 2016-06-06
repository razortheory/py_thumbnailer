import os
import tempfile
from io import BytesIO

from PIL import Image

from . import exceptions
from .sh_utils import run


class Thumbnailer(object):
    executable = None

    @classmethod
    def is_available(cls):
        return os.path.exists(cls.executable)

    @classmethod
    def _args(cls, resize_to=None):
        raise NotImplementedError

    @classmethod
    def thumbnail(cls, source_file, resize_to=None):
        if not cls.is_available():
            raise exceptions.ThumbnailerNotReadyException('%s is not ready' % cls.__name__)
        return run(cls._args(resize_to=resize_to), input_data=source_file)


class InputFileThumbnailer(object):
    @classmethod
    def _args(cls, resize_to=None, source_filename=None):
        raise NotImplementedError

    @classmethod
    def thumbnail(cls, source_file, resize_to=None):
        temp_file = None
        if hasattr(source_file, 'read'):
            source_file.seek(0)
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(source_file.read())
            temp_file.close()
            source_file = temp_file.name

        try:
            return run(cls._args(resize_to=resize_to, source_filename=source_file))
        finally:
            if temp_file:
                os.remove(temp_file.name)


class PDFThumbnailer(Thumbnailer):
    executable = '/usr/bin/pdftoppm'

    @classmethod
    def _args(cls, resize_to=None):
        args = [cls.executable, '-jpeg']
        if resize_to:
            args += ['-scale-to', str(resize_to)]
        args += ['-f', '1', '-l', '1']
        return args


class ImageThumbnailer(Thumbnailer):
    @classmethod
    def is_available(cls):
        return True

    @classmethod
    def thumbnail(cls, source_file, resize_to=None):
        im = Image.open(source_file)
        if resize_to:
            im.thumbnail((resize_to, resize_to))
        output = BytesIO()
        im.save(output, format='jpeg', quality=100)
        output.seek(0)
        return output


class PSThumbnailer(Thumbnailer):
    executable = '/usr/bin/ps2pdf'

    @classmethod
    def _args(cls, resize_to=None):
        return [cls.executable, '-', '-']

    @classmethod
    def thumbnail(cls, source_file, resize_to=None):
        pdf_buffer = super(PSThumbnailer, cls).thumbnail(source_file, resize_to=resize_to)
        return PDFThumbnailer.thumbnail(pdf_buffer, resize_to=resize_to)


class FFMPEGThumbnailer(InputFileThumbnailer):
    executable = '/usr/bin/ffmpeg'

    @classmethod
    def _args(cls, resize_to=None, source_filename=None):
        return [
            cls.executable,
            '-v', 'quiet',
            '-i', source_filename,
            '-f', 'singlejpeg',
            '-frames:v', '1',
            '-ss', '10',
            '-vsync', 'vfr',
            '-'
        ]

    @classmethod
    def thumbnail(cls, source_file, resize_to=None):
        image_buffer = super(FFMPEGThumbnailer, cls).thumbnail(source_file, resize_to=resize_to)
        if resize_to:
            return ImageThumbnailer.thumbnail(image_buffer, resize_to=resize_to)
        return image_buffer


class UnoconvThumbnailer(InputFileThumbnailer):
    executable = '/usr/bin/unoconv'

    @classmethod
    def _args(cls, resize_to=None, source_filename=None):
        return [
            cls.executable,
            '-f', 'pdf',
            '--stdout',
            source_filename,
        ]

    @classmethod
    def thumbnail(cls, source_file, resize_to=None):
        pdf_buffer = super(UnoconvThumbnailer, cls).thumbnail(source_file, resize_to=resize_to)
        return PDFThumbnailer.thumbnail(pdf_buffer, resize_to=resize_to)
