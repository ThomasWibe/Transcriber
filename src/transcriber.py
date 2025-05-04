import whisper
import os

class AudioTranscriber:
    def __init__(self, model_name="base"):
        print(f"Load Whisper Model: '{model_name}'...")
        self.model = whisper.load_model(model_name)

    def get_user_path(self):
        print("=== Whisper Transcriptiontool ===")
        audio_path = input("Pass the path to the audio file: ").strip()
        while not os.path.isfile(audio_path):
            print("The file does not exsist, try again...")
            audio_path = input("Pass the path to the audio file: ").strip()

        output_path = input("Put in the path to the output file: (ex: output.txt) ").strip()
        if not output_path.endswith(".txt"):
            output_path += ".txt"

        return audio_path, output_path
    
    def format_timestamp(self, seconds):
        hrs = int((seconds // 3600))
        mins = int((seconds % 3600) // 60)
        secs = int((seconds % 60))
        millis = int((seconds -int(seconds )) * 1000)

        return f"{hrs:02}:{mins:02}:{secs:02}:{millis:03}"

    def transcribe(self, audio_path):
        print("Transcribing audio file...")
        result = self.model.transcribe(audio_path, verbose=False)
        return result["segments"]

    def save_to_file(self, segments, output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            for segment in segments:
                start = self.format_timestamp(segment["start"])
                end = self.format_timestamp(segment["end"])
                text = segment["text"].strip()
                f.write(f"[{start} ---> {end}] {text}\n")
        print(f"Transcription with timestamps are saved in: {output_path}")
    
    def run (self):
        audio_path, output_path = self.get_user_path()
        segments = self.transcribe(audio_path)
        
        print("\n === Transcribing text with timestamps ===")
        for segment in segments:
            start = self.format_timestamp(segment["start"])
            end = self.format_timestamp(segment["end"])
            print(f"[{start}] ---> {end}] {segment['text'].strip()}")

        self.save_to_file(segments, output_path)

if __name__ == "__main__":
    transcriber = AudioTranscriber(model_name="base")
    transcriber.run()