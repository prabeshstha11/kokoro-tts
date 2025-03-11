from kokoro import KPipeline
import soundfile as sf

pipeline = KPipeline(lang_code='a') 

file_path = "test.txt"

def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

text = read_text_from_file(file_path)

generator = pipeline(
    text, voice='',
    speed=1, split_pattern=r'\n+'
)

gs, ps, audio = next(generator)
output_filename = 'output.wav' 
sf.write(output_filename, audio, 24000)
print(f"Saved: {output_filename}")
