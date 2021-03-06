"""     _               _____                _ _
       | |        /\   / ____|              | (_)
  _ __ | |       /  \ | |     __ _ _   _  __| |_  ___
 | '_ \| |      / /\ \| |    / _` | | | |/ _` | |/ _ \
 | |_) | |____ / ____ \ |___| (_| | |_| | (_| | | (_) |
 | .__/|______/_/    \_\_____\__,_|\__,_|\__,_|_|\___/
 | |
 |_|

This file is part of pLAC-audio.

pLAC-audio is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pLAC-audio is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pLAC-audio.  If not, see <http://www.gnu.org/licenses/>

Copyright (c) 2019 Fabrice Zaoui

License GNU GPL v3

"""
import os
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal


class MP3Thread(QThread):
    update_progress_bar = pyqtSignal()

    def __init__(self, audio_files, lossless_folder, lossy_location, qvalue, codec, samplerate, channels):
        QThread.__init__(self)
        self.audio_files = audio_files
        self.lossless_folder = lossless_folder
        self.lossy_location = lossy_location
        self.qval = qvalue
        self.codec = codec
        self.samplerate = samplerate
        self.channels = channels
        self.sep = '/'
        self.null = '/dev/null'
        if os.name == 'nt':
            self.sep = '\\'
            self.null = 'NUL'

    def __del__(self):
        self.wait()

    def convert2lossy(self, audio_file_in):
        path_audio = os.path.dirname(audio_file_in)
        file_name = os.path.splitext(os.path.basename(audio_file_in))[0]
        file_name_ext = os.path.splitext(os.path.basename(audio_file_in))[1]
        len_indir = len(self.lossless_folder)
        path_audio = path_audio[len_indir:]
        path_audio = self.lossy_location + path_audio
        ffmpeg = 'ffmpeg'
        # if sys.platform == 'darwin':
        #    ffmpeg = '/Applications/pLACaudio.app/Contents/MacOS/ffmpeg'
        if not os.path.isdir(path_audio):
            try:
                os.makedirs(path_audio)
            except OSError:
                # logging.exception('Unable to create the destination folder')
                pass
        chn = '-ac ' + str(self.channels) + ' '
        if self.codec == 'MP3':
            ext = 'mp3'
            audio_file = file_name + '.' + ext
            audio_file_out = path_audio + self.sep + audio_file
            if not os.path.isfile(audio_file_out):
                subprocess.call(ffmpeg + ' -nostats -loglevel 0 -i '
                          + '"' + audio_file_in + '"'
                          + ' -vn -acodec libmp3lame -q:a '+ self.qval + ' -map_metadata 0'
                          + ' -id3v2_version 3 ' + chn
                          + '"' + audio_file_out + '"' + ' > ' + self.null,
                                shell=True)
        elif self.codec == 'AAC':
            ext = 'm4a'
            audio_file = file_name + '.' + ext
            audio_file_out = path_audio + self.sep + audio_file
            if not os.path.isfile(audio_file_out):
                subprocess.call(ffmpeg + ' -nostats -loglevel 0 -i '
                                + '"' + audio_file_in + '"'
                                + ' -vn -acodec aac -b:a ' + self.qval + ' -map_metadata 0 ' + chn
                                + '"' + audio_file_out + '"' + ' > ' + self.null,
                                shell=True)
        elif self.codec == 'Ogg Vorbis':
            ext = 'ogg'
            audio_file = file_name + '.' + ext
            audio_file_out = path_audio + self.sep + audio_file
            if file_name_ext == '.dsf':
                fe = '-ar 44100 '
            else:
                fe = ''
            if not os.path.isfile(audio_file_out):
                subprocess.call(ffmpeg + ' -nostats -loglevel 0 -i '
                                + '"' + audio_file_in + '"'
                                + ' -vn -acodec libvorbis -q:a ' + self.qval + ' -map_metadata 0 ' + fe + chn
                                + '"' + audio_file_out + '"' + ' > ' + self.null,
                                shell=True)
        elif self.codec == 'Opus':
            ext = 'opus'
            audio_file = file_name + '.' + ext
            audio_file_out = path_audio + self.sep + audio_file
            if not os.path.isfile(audio_file_out):
                subprocess.call(ffmpeg + ' -nostats -loglevel 0 -i '
                                + '"' + audio_file_in + '"'
                                + ' -vn -acodec libopus -b:a ' + self.qval + ' -map_metadata 0 ' + chn
                                + '"' + audio_file_out + '"' + ' > ' + self.null,
                                shell=True)
        elif self.codec == 'FLAC':
            ext = 'flac'
            audio_file = file_name + '.' + ext
            audio_file_out = path_audio + self.sep + audio_file
            fe = ''
            if file_name_ext == '.dsf':
                if self.samplerate == 1:
                    fe = '-ar 44100 '
                elif self.samplerate == 2:
                    fe = '-ar 88200 '
                elif self.samplerate == 3:
                    fe = '-ar 176400 '
                elif self.samplerate == 4:
                    fe = '-ar 352800 '
            if not os.path.isfile(audio_file_out):
                subprocess.call(ffmpeg + ' -nostats -loglevel 0 -i '
                                + '"' + audio_file_in + '"'
                                + ' -vn -compression_level ' + self.qval + ' -map_metadata 0 ' + fe + chn
                                + '"' + audio_file_out + '"' + ' > ' + self.null,
                                shell=True)
        elif self.codec == 'ALAC':
            ext = 'm4a'
            audio_file = file_name + '.' + ext
            audio_file_out = path_audio + self.sep + audio_file
            fe = ''
            if file_name_ext == '.dsf':
                if self.samplerate == 1:
                    fe = '-ar 44100 '
                elif self.samplerate == 2:
                    fe = '-ar 88200 '
                elif self.samplerate == 3:
                    fe = '-ar 176400 '
                elif self.samplerate == 4:
                    fe = '-ar 352800 '
            if not os.path.isfile(audio_file_out):
                subprocess.call(ffmpeg + ' -nostats -loglevel 0 -i '
                                + '"' + audio_file_in + '"'
                                + ' -vn -acodec alac -compression_level ' + self.qval + ' -map_metadata 0 ' + fe + chn
                                + '"' + audio_file_out + '"' + ' > ' + self.null,
                                shell=True)
        elif self.codec == 'WAV':
            ext = 'wav'
            audio_file = file_name + '.' + ext
            audio_file_out = path_audio + self.sep + audio_file
            fe = ''
            if file_name_ext == '.dsf':
                if self.samplerate == 1:
                    fe = '-ar 44100 '
                elif self.samplerate == 2:
                    fe = '-ar 88200 '
                elif self.samplerate == 3:
                    fe = '-ar 176400 '
                elif self.samplerate == 4:
                    fe = '-ar 352800 '
            if not os.path.isfile(audio_file_out):
                subprocess.call(ffmpeg + ' -nostats -loglevel 0 -i '
                                + '"' + audio_file_in + '"'
                                + ' -vn ' + ' -map_metadata 0 ' + fe + chn
                                + '"' + audio_file_out + '"' + ' > ' + self.null,
                                shell=True)
        elif self.codec == 'AIFF':
            ext = 'aif'
            audio_file = file_name + '.' + ext
            audio_file_out = path_audio + self.sep + audio_file
            fe = ''
            if file_name_ext == '.dsf':
                if self.samplerate == 1:
                    fe = '-ar 44100 '
                elif self.samplerate == 2:
                    fe = '-ar 88200 '
                elif self.samplerate == 3:
                    fe = '-ar 176400 '
                elif self.samplerate == 4:
                    fe = '-ar 352800 '
            if not os.path.isfile(audio_file_out):
                subprocess.call(ffmpeg + ' -nostats -loglevel 0 -i '
                                + '"' + audio_file_in + '"'
                                + ' -vn ' + ' -map_metadata 0 ' + fe + chn
                                + '"' + audio_file_out + '"' + ' > ' + self.null,
                                shell=True)
    def run(self):
        for audio_file_in in self.audio_files:
            self.convert2lossy(audio_file_in)
            self.update_progress_bar.emit()
