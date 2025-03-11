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
    text, voice='af_heart',
    speed=1, split_pattern=r'\n+'
)

for i, (gs, ps, audio) in enumerate(generator):
    output_filename = f'{i}_output.wav' 
    sf.write(output_filename, audio, 24000)
    print(f"Saved: {output_filename}")
