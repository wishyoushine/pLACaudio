# pLACaudio

A minimalist tool designed for the simple and fast conversion of large libraries of lossless audio files.

Input folder of lossless files can include the following formats:
- ALAC
- [FLAC](https://xiph.org/flac/)
- WAV
- AIFF

Output lossy formats are either:
- [MP3](http://lame.sourceforge.net/)
- [Ogg Vorbis](https://xiph.org/vorbis/)
- [Opus](http://opus-codec.org/)

pLACaudio runs on a number of cores chosen by the user for a fast conversion of a potentially large library.

pLACaudio uses ffMPEG (A complete, cross-platform solution to record, convert and stream audio and video) is a free software and distributed under the terms of the GNU General Public License v3 see https://www.ffmpeg.org/ for more information).

Three settings of the output quality audio are possible.

<p align="center">
  <img src="./img/Windows_win10.png" width="200"/>
  <img src="./img/Windows_linux.png" width="200"/>
</p>
<p align="center">
   <b>pLACaudio on Windows 10 and GNU/Linux</b>
</p>

Requirements
============

- Python 3 and PyQt5
- [ffMPEG](https://www.ffmpeg.org) converter

Use
===

An executable version is provided for Windows 64 bits. See the Release section.

For the use with CLI:
`>python 3 pLACaudio.py`
and make sure that `ffmpeg` is a known executable of your operating system.


License
=======

This package is provided under the GNU GPL license v3

Contributions
=============

Contributions are always welcome.

When contributing to please consider discussing the changes you wish to make via issue.

Enjoy ;-)
