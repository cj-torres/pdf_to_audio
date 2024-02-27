import argparse
import fitz
import ffmpeg
import os
from openai import OpenAI

MAX_LEN = 2048


def max_split(text):
    if len(text) < MAX_LEN:
        return [text]
    else:
        start_index = len(text)-MAX_LEN
        # paragraph split first
        for i in range(start_index, len(text)):
            if text[i] == '\n':
                return max_split(text[:i]) + [text[i+1:]]
        # if that fails sentence split
        for i in range(start_index, len(text)):
            if text[i] == '.' and text[i+1] == ' ':
                return max_split(text[:i+1]) + [text[i+2:]]
        # if that fails split on space
        for i in range(start_index, len(text)):
            if text[i] == ' ':
                return max_split(text[:i]) + [text[i+1:]]


def concatenate_audio(files, output_file):
    inputs = (ffmpeg.input(files))
    joined = ffmpeg.concat(*inputs, v=0, a=1).node
    ffmpeg.output(joined[0], output_file).run(overwrite_output=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Text to Audio Converter')

    parser.add_argument('source_file', type=str, help='The source text file to convert')
    parser.add_argument('new_file', type=str, help='The output audio file name')
    parser.add_argument('voice', type=str, help='The voice to be used for conversion')

    args = parser.parse_args()

    with fitz.open(args.source_file) as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    text_blocks = max_split(text)

    client = OpenAI()

    sub_files = []
    for i, text in enumerate(text_blocks):
        response = client.audio.speech.create(
            model = 'tts-1',
            voice = args.voice,
            input = text
        )
        sub_files.append(f'output/{args.new_file}_{i}.mp3')
        response.write_to_file(f'output/{args.new_file}_{i}.mp3')
    concatenate_audio(sub_files, f'output/{args.new_file}.mp3')
    for file in sub_files:
        os.remove(file)




