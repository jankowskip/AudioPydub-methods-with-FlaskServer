import pyaudio
import wave
import sys
from Tkinter import Tk
from tkFileDialog import askopenfilename
from pydub import AudioSegment
from pydub import playback
import os
from flask import Flask, request, render_template

app = Flask(__name__)



@app.route('/')
def hello():
	print "hello"
	
@app.route('/upload/', methods=['POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			a = 'file uploaded'
			return render_template('upload.html', data = a)
	


# http://stackoverflow.com/questions/13386681/streaming-data-with-python-and-flask


	
	
# Pydub test
song = AudioSegment.from_file(filename, format="wav")
							# Methods on song
def reverse(song):						
	song = AudioSegment.from_file(song, format="wav")
	song = song.reverse()   
	#return song

def normalization(song):
	song = AudioSegment.from_file(filename, format="wav")
	song = song.apply_gain(-sound.max_dBFS) 
	#return song
def toMonoStereo(x, song):  # 1 mino , 2 stereo
	song = AudioSegment.from_file(filename, format="wav")
	song = song.set_channels(x)
	#return song
def IncresingBeginning(x, song): # 1-10 lub 15 20 s bym zrobil
	x = x*1000
	song = AudioSegment.from_file(filename, format="wav")
	song = song.fade(from_gain=-120.0, start=0, duration=x) # 1000= 1s
	#return song
def fadeEnd(x, song): # tu tak jak w powyzszym
	x = x*1000
	song = AudioSegment.from_file(filename, format="wav")
	song = song.fade(to_gain=-120.0, end=0, duration=x) # Wygaszanei koncowki 10s
	#return song
def setFrameRate(x, song):
	song = AudioSegment.from_file(filename, format="wav")
	song = song.set_frame_rate(x) #  # Czestotliwosc wyswietlania klatek  Common values are 44100 (CD), 48000 (DVD), 22050, 24000, 12000 and 11025.
	#return song
def setSampleWidth(x, song):
	song = AudioSegment.from_file(filename, format="wav")
	song = song.set_sample_width(x) # # Ilosc bajtow na probke 1=8 2=16 4=32/64	
	#return song	
def speedup(x, song):
	song = AudioSegment.from_file(filename, format="wav")
	song = song.speedup(playback_speed=x, chunk_size=20, crossfade=25)		# Przyspieszenie piosenki 1-2	
	#return song

									# Methods on song that doesnt work
	
#song = song.invert_phase #										
#song = song.strip_silence(silence_len=100, silence_thresh=-16, padding=100);
#song = song.speedup(playback_speed=0.5, chunk_size=150, crossfade=25)	# Is slowing possible?	or only 1-2 

												#Converter
def toMp3(song):
	song.export("AudioTownSong.mp3", format="mp3") # zapisanie piosenki w formacie mp3
	#return song
def toWave(song):
	song.export("AudioTownSong.wav", format="wav") # zapisanie piosenki w fromacie wav
	#return song
 
						 # Song Analyze 
def soundAnalyze():						
	loudness = song.dBFS  
	print "Glosnosc piosenki wynosi (dBFS): ",loudness 
  
	bytes_per_sample = song.sample_width  
	print "Ilosc bitow na probke, 1 oznacza 8 bajtow, 2 oznacza 16 bajtow. Wynik:: ",bytes_per_sample

	channel_count = song.channels 
	print "Liczba kanalow piosenki, 1 oznacza mono, 2 oznacza stereo. Wynik:: ",channel_count
  
	frames_per_second = song.frame_rate
	print "Ilosc klatek na sekunde w Hz wynosi:",frames_per_second
   
	peak_amplitude = -song.max_dBFS 
	print "Najwyzsza amplituda w piosence (dBFS) wynosi:", peak_amplitude
   
	song.duration_seconds == (len(song) / 1000.0)
	print "Dlugosc piosenki w sekundach: ",song.duration_seconds
def volumeup(x,song):
	song = song.apply_gain(x)  # podglasnianie 0-40
#louder_via_operator = song + 3.5
def volumedown(x,song):
	song = song.apply_gain(x)  # Przyciszanie -40-0
#quieter_via_operator = song - 5.7


# Streaming


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("3001"),
        debug=True
    )
