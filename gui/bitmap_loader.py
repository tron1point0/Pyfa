# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

import io
import os.path
from collections import OrderedDict

# noinspection PyPackageRequirements
import wx
from logbook import Logger

import config

logging = Logger(__name__)


class BitmapLoader(object):
    # try:
    #     archive = zipfile.ZipFile(os.path.join(config.pyfaPath, 'imgs.zip'), 'r')
    #     logging.info("Using zipped image files.")
    # except (IOError, TypeError):
    #     logging.info("Using local image files.")
    #     archive = None

    logging.info("Using local image files.")
    archive = None

    cached_bitmaps = OrderedDict()
    dont_use_cached_bitmaps = False
    max_cached_bitmaps = 500

    scaling_factor = None

    @classmethod
    def getStaticBitmap(cls, name, parent, location):
        static = wx.StaticBitmap(parent)
        static.SetBitmap(cls.getBitmap(name or 0, location))
        return static

    @classmethod
    def getBitmap(cls, name, location):
        if cls.dont_use_cached_bitmaps:
            return cls.loadBitmap(name, location)

        path = "%s%s" % (name, location)

        if len(cls.cached_bitmaps) == cls.max_cached_bitmaps:
            cls.cached_bitmaps.popitem(False)

        if path not in cls.cached_bitmaps:
            bmp = cls.loadBitmap(name, location)
            cls.cached_bitmaps[path] = bmp
        else:
            bmp = cls.cached_bitmaps[path]

        return bmp

    @classmethod
    def getImage(cls, name, location):
        bmp = cls.getBitmap(name, location)
        if bmp is not None:
            return bmp.ConvertToImage()
        else:
            return None

    @classmethod
    def loadBitmap(cls, name, location):
        if cls.scaling_factor is None:
            import gui.mainFrame
            cls.scaling_factor = int(gui.mainFrame.MainFrame.getInstance().GetContentScaleFactor())

        scale = cls.scaling_factor

        filename, img = cls.loadScaledBitmap(name, location, scale)

        while img is None and scale > 0:
            # can't find the correctly scaled image, fallback to smaller scales
            scale -= 1
            filename, img = cls.loadScaledBitmap(name, location, scale)

        if img is None:
            print(("Missing icon file: {0}/{1}".format(location, filename)))
            return None

        bmp: wx.Bitmap = img.ConvertToBitmap()
        if scale > 1:
            bmp.SetSize((bmp.GetWidth() // scale, bmp.GetHeight() // scale))
        return bmp

    @classmethod
    def loadScaledBitmap(cls, name, location, scale=0):
        """Attempts to load a scaled bitmap.

        Args:
            name (str): TypeID or basename of the image being requested.
            location (str): Path to a location that may contain the image.
            scale (int): Scale factor of the image variant to load. If ``0``, attempts to load the unscaled variant.

        Returns:
            (str, wx.Image): Tuple of the filename that may have been loaded and the image at that location. The
                filename will always be present, but the image may be ``None``.
        """
        filename = "{0}@{1}x.png".format(name, scale) if scale > 0 else "{0}.png".format(name)
        img = cls.loadImage(filename, location)
        return filename, img

    @classmethod
    def loadImage(cls, filename, location):
        if cls.archive:
            path = os.path.join(location, filename)
            if os.sep != "/" and os.sep in path:
                path = path.replace(os.sep, "/")

            try:
                img_data = cls.archive.read(path)
                sbuf = io.StringIO(img_data)
                return wx.ImageFromStream(sbuf)
            except KeyError:
                print(("Missing icon file from zip: {0}".format(path)))
        else:
            path = os.path.join(config.pyfaPath, 'imgs' + os.sep + location + os.sep + filename)

            if os.path.exists(path):
                return wx.Image(path)
            else:
                return None
