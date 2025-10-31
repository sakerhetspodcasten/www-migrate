# Transcribe

A mp3 to markdown transcription script, wrapping Open Whisper.

## Usage

Transcribe markdown files, downloading MP3's on the fly:

`./transcribe.py --dir-mp3 out/mp3 --dir-trans out/trans content/*.md`

Usage help:

`./transcribe.py -h`

``` plain
usage: transcribe.py [-h] --dir-mp3 DIR_MP3 --dir-trans DIR_TRANS
                     [--transcribe-header TRANSCRIBE_HEADER]
                     [--transcribe-description TRANSCRIBE_DESCRIPTION]
                     [--whisper-bin WHISPER_BIN]
                     file [file ...]

transcription tool

positional arguments:
  file                  files to process

options:
  -h, --help            show this help message and exit
  --dir-mp3 DIR_MP3     directory to download mp3s to
  --dir-trans DIR_TRANS
                        directory to store transcriptions to
  --transcribe-header TRANSCRIBE_HEADER
                        directory prefix to append to file names
  --transcribe-description TRANSCRIBE_DESCRIPTION
                        A short comment about the transcription
  --whisper-bin WHISPER_BIN
                        whisper executable

Hope this help was helpful! :-)
```
