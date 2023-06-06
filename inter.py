import tkinter as tk
import pyaudio
import wave

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Live Audio Recorder")
        
        # Create label to display instructions
        self.label = tk.Label(self.root, text="Press the 'Record' button to start recording, and 'Stop' to stop recording.")
        self.label.pack()
        
        # Create 'Record' button
        self.record_button = tk.Button(self.root, text="Record", command=self.record)
        self.record_button.pack(side="left")
        
        # Create 'Stop' button
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack(side="right")
        
        self.frames = []
        self.is_recording = False
        
        self.root.mainloop()
    
    def record(self):
        self.is_recording = True
        
        # Open audio stream
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        
        # Enable 'Stop' button and disable 'Record' button
        self.stop_button.config(state=tk.NORMAL)
        self.record_button.config(state=tk.DISABLED)
        
        # Start recording
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)
        
    def stop(self):
        self.is_recording = False
        
        # Stop recording
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        
        # Disable 'Stop' button and enable 'Record' button
        self.stop_button.config(state=tk.DISABLED)
        self.record_button.config(state=tk.NORMAL)
        
        # Save recorded audio to file
        wave_file = wave.open("recorded_audio.wav", "wb")
        wave_file.setnchannels(1)
        wave_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(44100)
        wave_file.writeframes(b"".join(self.frames))
        wave_file.close()

app = App()
