# -*- coding: utf-8 -*-

"""
Copyright (C) 2006-2007 Adolfo González Blázquez <code@infinicode.org>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version. 

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details. 

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

If you find any bugs or have any suggestions email: code@infinicode.org
"""

import os
import dircache
import glob
import re
import sys
import time

import pyrenamer_globals
import EXIF
if pyrenamer_globals.have_eyed3:
    import eyeD3

STOP = False

def set_stop(stop):
    """ Set stop var to see if ther's no need to keep reading files """
    global STOP
    STOP = stop


def get_stop():
    return STOP


def escape_pattern(pattern):
    """ Escape special chars on patterns, so glob doesn't get confused """
    pattern = pattern.replace('[', '[[]')
    return pattern


def get_file_listing(dir, pattern=None):
    """ Returns the file listing of a given directory. It returns only files.
    Returns a list of [file,/path/to/file] """
    
    filelist = []
    
    if  pattern == (None or ''):
        listaux = dircache.listdir(dir)
    else:
        if dir != '/': dir += '/'
        dir = escape_pattern(dir + pattern)
        listaux = glob.glob(dir)
    
    listaux.sort(key=str.lower)
    for elem in listaux:
        if STOP: return filelist
        if not os.path.isdir(os.path.join(dir,elem)): filelist.append([os.path.basename(elem),os.path.join(dir,elem)])
    
    return filelist


def get_file_listing_recursive(dir, pattern=None):
    """ Returns the file listing of a given directory recursively.
    It returns only files. Returns a list of [file,/path/to/file] """
    
    filelist = []
    
    # Get root directory files
    filelist = get_file_listing(dir, pattern)
    
    # Get files from subdirs
    for root, dirs, files in os.walk(dir):
        if STOP: return filelist
        for directory in dirs:
            if STOP: return filelist
            elem = get_file_listing(os.path.join(root, directory), pattern)
            for i in elem:
                if STOP: return filelist
                filelist.append(i)    
    
    print "stop", dir
    return filelist
    

def get_dir_listing(dir):
    """ Returns the subdirectory listing of a given directory. It returns only directories.
     Returns a list of [dir,/path/to/dir] """
    
    dirlist = []
    
    listaux = dircache.listdir(dir)
    listaux.sort(key=str.lower)
    for elem in listaux:
        if STOP: return dirlist
        if os.path.isdir(os.path.join(dir,elem)): dirlist.append([os.path.basename(elem),os.path.join(dir,elem)])
    
    return dirlist


def get_new_path(name, path):
    """ Remove file from path, so we have only the dir"""
    dirpath = os.path.split(path)[0]
    if dirpath != '/': dirpath += '/'
    return dirpath + name


def replace_spaces(name, path, mode):
    """ if mode == 0: ' ' -> '_'
        if mode == 1: '_' -> ' '
        if mode == 2: '_' -> '.'
        if mode == 3: '.' -> ' ' """
    if mode == 0:
        newname = name.replace(' ', '_')
    elif mode == 1:
        newname = name.replace('_', ' ')
    elif mode == 2:
        newname = name.replace(' ', '.')
    elif mode == 3:
        newname = name.replace('.', ' ')
        
    newpath = get_new_path(newname, path)
    return newname, newpath


def replace_capitalization(name, path, mode):
    """ 0: all to uppercase
    1: all to lowercase
    2: first letter uppercase
    3: first letter uppercase of each word """
    if mode == 0:
        newname = name.upper()
    elif mode == 1:
        newname = name.lower()
    elif mode == 2:
        newname = name.capitalize()
    elif mode == 3:
        #newname = name.title()
        newname = ' '.join([x.capitalize() for x in name.split()])

    newpath = get_new_path(newname, path)
    return newname, newpath
    

def replace_with(name, path, orig, new):
    """ Replace all occurences of orig with new """
    newname = name.replace(orig, new)
    newpath = get_new_path(newname, path)
    return newname, newpath


def replace_accents(name, path):
    """ Remove accents, umlauts and other locale symbols from words """
    newname = name.replace('á', 'a')
    newname = newname.replace('à', 'a')
    newname = newname.replace('ä', 'a')
    newname = newname.replace('â', 'a')
    newname = newname.replace('Á', 'A')
    newname = newname.replace('À', 'A')
    newname = newname.replace('Ä', 'A')
    newname = newname.replace('Â', 'A')
    
    newname = newname.replace('é', 'e')
    newname = newname.replace('è', 'e')
    newname = newname.replace('ë', 'e')
    newname = newname.replace('ê', 'e')
    newname = newname.replace('É', 'E')
    newname = newname.replace('È', 'E')
    newname = newname.replace('Ë', 'E')
    newname = newname.replace('Ê', 'E')
    
    newname = newname.replace('í', 'i')
    newname = newname.replace('ì', 'i')
    newname = newname.replace('ï', 'i')
    newname = newname.replace('î', 'i')
    newname = newname.replace('Í', 'I')
    newname = newname.replace('Ì', 'I')
    newname = newname.replace('Ï', 'I')
    newname = newname.replace('Î', 'I')
            
    newname = newname.replace('ó', 'o')
    newname = newname.replace('ò', 'o')
    newname = newname.replace('ö', 'o')
    newname = newname.replace('ô', 'o')
    newname = newname.replace('Ó', 'O')
    newname = newname.replace('Ò', 'O')
    newname = newname.replace('Ö', 'O')
    newname = newname.replace('Ô', 'O')
       
    newname = newname.replace('ú', 'u')
    newname = newname.replace('ù', 'u')
    newname = newname.replace('ü', 'u')
    newname = newname.replace('û', 'u')
    newname = newname.replace('Ú', 'U')
    newname = newname.replace('Ù', 'U')
    newname = newname.replace('Ü', 'U')
    newname = newname.replace('Û', 'U')
    
    newpath = get_new_path(newname, path)
    return newname, newpath


def rename_using_patterns(name, path, pattern_ini, pattern_end, count):
    """ This method parses te patterns given by the user and stores the new filename
    on the treestore. Posibble patterns are:
        
    {#} Numbers
    {L} Letters
    {C} Characters (Numbers & letters, not spaces)
    {X} Numbers, letters, and spaces
    {@} Trash
    """
    
    pattern = pattern_ini
    newname = pattern_end
    
    pattern = pattern.replace('.','\.')
    pattern = pattern.replace('[','\[')
    pattern = pattern.replace(']','\]')
    pattern = pattern.replace('(','\(')
    pattern = pattern.replace(')','\)')
    pattern = pattern.replace('?','\?')
    pattern = pattern.replace('{#}', '([0-9]*)')
    pattern = pattern.replace('{L}', '([a-zA-Z]*)')
    pattern = pattern.replace('{C}', '([\S]*)')
    pattern = pattern.replace('{X}', '([\S\s]*)')
    pattern = pattern.replace('{@}', '(.*)')
    
    repattern = re.compile(pattern)
    try:
        groups = repattern.search(name).groups()
    
        for i in range(len(groups)):
            newname = newname.replace('{'+`i+1`+'}',groups[i])
    except:
        return None, None
    
    # Replace {num} with item number.
    # If {num2} the number will be 02
    # If {num3-10} the number will be 010
    count = `count`
    cr = re.compile("{(num)([0-9]*)}"
                    "|{(num)([0-9]*)-([0-9]*)}")
    try:
        cg = cr.search(newname).groups()
        if len(cg) == 5:
            if cg[0] == 'num':
                if cg[1] != '': count = count.zfill(int(cg[1]))
                newname = cr.sub(count, newname)
            if cg[2] == 'num':
                if cg[4] != '': count = str(int(count)+int(cg[4])-1)
                if cg[3] != '': count = count.zfill(int(cg[3]))
        newname = cr.sub(count, newname)
    except:
        pass
    
    # Replace {dir} with directory name
    dir = os.path.dirname(path)
    dir = os.path.basename(dir)
    newname = newname.replace('{dir}', dir)
    
    # Some date replacements
    newname = newname.replace('{date}', time.strftime("%d%b%Y", time.localtime()))
    newname = newname.replace('{year}', time.strftime("%Y", time.localtime()))
    newname = newname.replace('{month}', time.strftime("%m", time.localtime()))
    newname = newname.replace('{monthname}', time.strftime("%B", time.localtime()))
    newname = newname.replace('{monthsimp}', time.strftime("%b", time.localtime()))
    newname = newname.replace('{day}', time.strftime("%d", time.localtime()))
    newname = newname.replace('{dayname}', time.strftime("%A", time.localtime()))
    newname = newname.replace('{daysimp}', time.strftime("%a", time.localtime()))
        
    # Returns new name and path
    newpath = get_new_path(newname, path)
    return newname, newpath


def replace_images(name, path, newname, newpath):
    """ Pattern replace for images """
    
    # Image EXIF replacements
    date, width, height, cameramaker, cameramodel = get_exif_data(get_new_path(name, path))
    
    if date != None:
        newname = newname.replace('{imagedate}', time.strftime("%d%b%Y", date))
        newname = newname.replace('{imageyear}', time.strftime("%Y", date))
        newname = newname.replace('{imagemonth}', time.strftime("%m", date))
        newname = newname.replace('{imagemonthname}', time.strftime("%B", date))
        newname = newname.replace('{imagemonthsimp}', time.strftime("%b", date))
        newname = newname.replace('{imageday}', time.strftime("%d", date))
        newname = newname.replace('{imagedayname}', time.strftime("%A", date))
        newname = newname.replace('{imagedaysimp}', time.strftime("%a", date))
        newname = newname.replace('{imagetime}', time.strftime("%H_%M_%S", date))
        newname = newname.replace('{imagehour}', time.strftime("%H", date))
        newname = newname.replace('{imageminute}', time.strftime("%M", date))
        newname = newname.replace('{imagesecond}', time.strftime("%S", date))
    else:
        newname = newname.replace('{imagedate}','')
        newname = newname.replace('{imageyear}', '')
        newname = newname.replace('{imagemonth}', '')
        newname = newname.replace('{imagemonthname}', '')
        newname = newname.replace('{imagemonthsimp}', '')
        newname = newname.replace('{imageday}', '')
        newname = newname.replace('{imagedayname}', '')
        newname = newname.replace('{imagedaysimp}', '')
        newname = newname.replace('{imagetime}', '')
        newname = newname.replace('{imagehour}', '')
        newname = newname.replace('{imageminute}', '')
        newname = newname.replace('{imagesecond}', '')
        
    if width != None: newname = newname.replace('{imagewidth}', width)
    else: newname = newname.replace('{imagewidth}', '')
    
    if height != None: newname = newname.replace('{imageheight}', height)
    else: newname = newname.replace('{imageheight}', '')

    if cameramaker != None: newname = newname.replace('{cameramaker}', cameramaker)
    else: newname = newname.replace('{cameramaker}', '')

    if cameramodel != None: newname = newname.replace('{cameramodel}', cameramodel)
    else: newname = newname.replace('{cameramodel}', '')
        
        
    # Returns new name and path
    newpath = get_new_path(newname, path)
    return newname, newpath


def get_exif_data(path):
    """ Get EXIF data from file. """
    date = None
    width = None
    height = None
    cameramaker = None
    cameramodel = None
    
    try:
        file = open(path, 'rb')
    except:
        print "ERROR: Opening image file", path
        return date, width, height, cameramaker, cameramodel
    
    tags = EXIF.process_file(file)
    if not tags:
        print "ERROR: No EXIF tags on", path
        return date, width, height, cameramaker, cameramodel
    
    # tags['EXIF DateTimeOriginal'] = "2001:03:31 12:27:36"
    if tags.has_key('EXIF DateTimeOriginal'):
        data = str(tags['EXIF DateTimeOriginal'])
        try:
            date = time.strptime(data, "%Y:%m:%d %H:%M:%S")
        except:
            date = None
        
    if tags.has_key('EXIF ExifImageWidth'):
        width = str(tags['EXIF ExifImageWidth'])
        
    if tags.has_key('EXIF ExifImageLength'):
        height = str(tags['EXIF ExifImageLength'])
        
    if tags.has_key('Image Make'):
        cameramaker = str(tags['Image Make'])
        
    if tags.has_key('Image Model'):
        cameramodel = str(tags['Image Model'])
        
    return date, width, height, cameramaker, cameramodel
    

def replace_music(name, path, newname, newpath):
    """ Pattern replace for mp3 """
    
    file = get_new_path(name, path)
    
    if eyeD3.isMp3File(file):
        audioFile = eyeD3.Mp3AudioFile(file, eyeD3.ID3_ANY_VERSION)
        tag = audioFile.getTag()
        artist = tag.getArtist()
        album  = tag.getAlbum()
        title  = tag.getTitle()
        track  = tag.getTrackNum()[0]
        trackt = tag.getTrackNum()[1]
        genre  = tag.getGenre().getName()
        year   = tag.getYear()
        
        if artist != None: newname = newname.replace('{artist}', artist)
        else: newname = newname.replace('{artist}', '')
        
        if album != None: newname = newname.replace('{album}', album)
        else: newname = newname.replace('{album}', '')
            
        if title != None: newname = newname.replace('{title}', title)
        else: newname = newname.replace('{title}', '')
            
        if track != None: newname = newname.replace('{track}', str(track))
        else: newname = newname.replace('{track}', '')
            
        if trackt != None: newname = newname.replace('{tracktotal}', str(trackt))
        else: newname = newname.replace('{tracktotal}', '')
        
        if genre != None: newname = newname.replace('{genre}', genre)
        else: newname = newname.replace('{genre}', '')
            
        if year != None: newname = newname.replace('{year}', year)
        else: newname = newname.replace('{year}', '')
    else:
        newname = newname.replace('{artist}', '')
        newname = newname.replace('{album}', '')
        newname = newname.replace('{title}', '')
        newname = newname.replace('{track}', '')
        newname = newname.replace('{tracktotal}', '')
        newname = newname.replace('{genre}', '')
        newname = newname.replace('{year}', '')
        
    # Returns new name and path
    newpath = get_new_path(newname, path)
    return newname, newpath


def rename_file(ori, new):
    """ Change filename with the new one """
    if os.path.exists(new):
        print "Error while renaming %s to %s! -> %s already exists!" % (ori, new, new)
        return False
    
    try:
        os.rename(ori, new)
        print "Renaming %s to %s" % (ori, new)
        return True
    except Exception, e:
        print "Error while renaming %s to %s!" % (ori, new)
        print e
        return False


def insert_at(name, path, text, pos):
    """ Append text at given position"""
    if pos >= 0:
        ini = name[0:pos]
        end = name[pos:len(name)]
        newname = ini + text + end
    else: 
        newname = name + text
        
    newpath = get_new_path(newname, path)
    return newname, newpath


def delete_from(name, path, ini, to):
    """ Delete chars from ini till to"""
    textini = name[0:ini]
    textend = name[to+1:len(name)]
    newname = textini + textend
    
    newpath = get_new_path(newname, path)
    return newname, newpath
