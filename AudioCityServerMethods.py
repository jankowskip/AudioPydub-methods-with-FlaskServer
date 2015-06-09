import pyaudio
import wave
import sys
from Tkinter import Tk
from tkFileDialog import askopenfilename
from pydub import AudioSegment
from pydub import playback
import os
from flask import Flask, request, render_template,redirect, url_for
from werkzeug import secure_filename
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import ClosingIterator, wrap_file

app = Flask(__name__)

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = set(['wav'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/hello')
def hello():
	return 'helloWorld'
	
@app.route('/upload', methods=['GET', 'POST'])  # path upload http://127.0.0.1:3001/upload
def upload():
	if request.method == 'POST':
		file = request.files['file']
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			a = 'file uploaded'
			return a

			
@app.route('/stream/<filename>')	# path stream http://127.0.0.1:3001/stream/NazwaPiosenki
def stream(filename):
	song = file(os.path.join(os.path.dirname(__file__), 'files', filename))
	return Response(song, direct_passthrough=True)
	
@app.route('/Path/<filename>')	
def getFilePath(filename):
	return os.path.join(os.path.dirname(__file__), 'files', filename)
	
#@app.route('/Audio/<filename>')
#def getAudio(filename):
#	return AudioSegment.from_file(getFilePath(filename, format="wav")

@app.route('/Audio/<filename>')
def getAudio(filename):
	return AudioSegment.from_file(getFilePath(filename, format="wav")
	#song = AudioSegment.from_file(getFilePath(filename, format="wav")
	#return song
	
#@app.route('/rev/<filename>')
#def reverse(filename):
#	song = getAudio(filename)
#	song = song.reverse()		
							
@app.route('/normalization/<filename>')	
def normalization(filename):
	song = getAudio(filename)
	song = song.apply_gain(-sound.max_dBFS) 

@app.route('/toMonoStereo/<filename>')	
def toMonoStereo(x, filename):  # 1 mino , 2 stereo
	song = getAudio(filename)
	song = song.set_channels(x)
	
@app.route('/IncresingBeginning/<filename>')	
def IncresingBeginning(x, filename): # 1-10 lub 15 20 s bym zrobil
	x = x*1000
	song = getAudio(filename)
	song = song.fade(from_gain=-120.0, start=0, duration=x) # 1000= 1s
	#return song
@app.route('/fadeEnd/<filename>')	
def fadeEnd(x,filename): # tu tak jak w powyzszym
	x = x*1000
	song = getAudio(filename)
	song = song.fade(to_gain=-120.0, end=0, duration=x) # Wygaszanei koncowki 10s
	#return song
@app.route('/Framerate/<filename>')	
def setFrameRate(x,filename):
	song = getAudio(filename)
	song = song.set_frame_rate(x) #  # Czestotliwosc wyswietlania klatek  Common values are 44100 (CD), 48000 (DVD), 22050, 24000, 12000 and 11025.
	#return song
@app.route('/SampleWidth/<filename>')	
def setSampleWidth(x,filename):
	song = getAudio(filename)
	song = song.set_sample_width(x) # # Ilosc bajtow na probke 1=8 2=16 4=32/64	
	#return song	
@app.route('/speedup/<filename>')	
def speedup(x,filename):
	song = getAudio(filename)
	song = song.speedup(playback_speed=x, chunk_size=20, crossfade=25)		# Przyspieszenie piosenki 1-2	
	#return song

									# Methods on song that doesnt work
	
#song = song.invert_phase #										
#song = song.strip_silence(silence_len=100, silence_thresh=-16, padding=100);
#song = song.speedup(playback_speed=0.5, chunk_size=150, crossfade=25)	# Is slowing possible?	or only 1-2 

@app.route('/tomp3/<filename>')													#Converter
def toMp3(filename):
	song = getAudio(filename)
	song.export("AudioTownSong.mp3", format="mp3") # saving mp3
	#return song
@app.route('/towave/<filename>')
def toWave(filename):
	song = getAudio(filename)
	song.export("AudioTownSong.wav", format="wav") # saving wav
	#return song
 
						 # Song Analyze 
@app.route('/soundanalzye/<filename>')
def soundAnalyze(filename):		
	song = getAudio(filename)				
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
@app.route('/volumeup/<filename>')
def volumeup(x,filename):
	song = getAudio(filename)
	song = song.apply_gain(x)  #  0-40

@app.route('/volumedown/<filename>')
def volumedown(x,filename):
	song = getAudio(filename)
	song = song.apply_gain(x)  #  -40-0



# test chrome-extension://hgmloofddffdnphfgcellkdfbfbjeloo/RestClient.html


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("3001"),
        debug=True
    )

