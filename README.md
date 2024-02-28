# PDF to Audio

This is a simple tool for converting PDFs to MP3 files using OpenAI. I have used this to let me listen to papers while programming. Note that this works best for papers where diagram reading is not important. Also the wisdom of converting PDF files to audio is questionable anyways.

This requires FFmpeg to be installed, an OpenAI API key (your own!) as well as the following libraries:

1. openai
2. ffmpeg-python
3. fitz

After that, from the command prompt simply run

    python pdf_to_audio.py pdf_filename output_filename voice -clean

The clean flag is optional, but uses ChatGPT to clean out artifacts and unwanted gunk from the PDF (clever regex solutions welcomed). The voice argument should be the chosen OpenAI voice model (e.g. onyx).
