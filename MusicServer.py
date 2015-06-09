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
import json

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

			

	

def getFilePath(filename):
	return os.path.join(os.path.dirname(__file__), 'files', filename)
	

def getAudio(filename):
	song = AudioSegment.from_file(getFilePath(filename), format="wav")
	return song
		
@app.route('/rev/<filename>')
def reverse(filename):
	song = getAudio(filename)
	song = song.reverse()
	song.export("files/reverse_"+filename, format="wav") 
	return "reverse_"+filename
	
@app.route('/invertPhase/<filename>')
def invertPhase(filename):
	song = getAudio(filename)
	song = song.invert_phase()
	song.export("files/invertPhase_"+filename, format="wav") 
	return "invertPhase_"+filename
							
@app.route('/normalization/<filename>')	
def normalization(filename):
	song = getAudio(filename)
	song = song.apply_gain(-song.max_dBFS) 
	song.export("files/normalization_"+filename, format="wav")
	return "normalization_"+filename
					# methods for equalizer
					
@app.route('/toMonoStereo/<filename>')	
def toMonoStereo(x, filename):  # x  1 mono, 2 stereo
	song = getAudio(filename)
	song = song.set_channels(x)
	song.export("files/MonoStereo_"+filename+"_"+x, format="wav")
	return "MonoStereo_"+filename+"_"+x
	
@app.route('/IncresingBeginning/<filename>')	
def IncresingBeginning(x, filename): # x 1-20 
	x = x*1000 # 1000= 1s
	song = getAudio(filename)
	song = song.fade(from_gain=-120.0, start=0, duration=x)
	song.export("files/IncreaseBeginning_"+filename+"_"+x, format="wav")
	return "IncreaseBeginning_"+filename+"_"+x
	
@app.route('/fadeEnd/<filename>')	
def fadeEnd(x,filename): #x 1-20
	x = x*1000
	song = getAudio(filename)
	song = song.fade(to_gain=-120.0, end=0, duration=x)
	song.export("files/fadeEnd_"+filename+"_"+x, format="wav")
	return "fadeEnd_"+filename+"_"+x
	
@app.route('/Framerate/<filename>')	
def setFrameRate(x,filename):		# x Common values are 44100 (CD), 48000 (DVD), 22050, 24000, 12000 and 11025.
	song = getAudio(filename)
	song = song.set_frame_rate(x) 
	song.export("files/setFrameRate_"+filename+"_"+x, format="wav")
	return "seFrameRate_"+filename+"_"+x
	
@app.route('/SampleWidth/<filename>')	
def setSampleWidth(x,filename):  # x= 1 = 8 , x=2=16, x = 4 = 32
	song = getAudio(filename)
	song = song.set_sample_width(x) 
	song.export("files/SampleWidth_"+filename+"_"+x, format="wav")
	return "SampleWidth_"+filename+"_"+x
	
@app.route('/speedup/<filename>')	
def speedup(x,filename):		# x 1-2
	song = getAudio(filename)
	song = song.speedup(playback_speed=x, chunk_size=20, crossfade=25)	
	song.export("files/Speedup_"+filename+"_"+x, format="wav")
	return "Speedup_"+filename+"_"+x	
	

	
													# mini Converter
@app.route('/tomp3/<filename>')													
def toMp3(filename):
	song = getAudio(filename)
	song.export(files/filename+".mp3", format="mp3") # saving mp3
	return filename+".mp3"
	
@app.route('/towave/<filename>')
def toWave(filename):
	song = getAudio(filename)
	song.export(files/filename+".wav", format="wav") # saving wav
	return filename+".wav"
	
 
													# Song Analyze 
@app.route('/soundanalzye/<filename>')
def soundAnalyze(filename):		
	song = getAudio(filename)		
	
	data = {}
	data['loudness'] = song.dBFS
	data['bytes_per_sample'] = song.sample_width
	data['channel_count'] = song.channels
	data['frames_per_second'] = song.frame_rate
	data['peak_amplitude'] = -song.max_dBFS
	data['song_duration'] = (len(song) / 1000.0)
	json_data = json.dumps(data)
	return json_data
											# Volume up and down
@app.route('/volumeup/<filename>')
def volumeup(x,filename):
	song = getAudio(filename)
	song = song.apply_gain(x)  #  0-40
	song.export("files/volumeup_"+filename+"_"+x, format="wav")
	return "volumeup_"+filename+"_"+x

@app.route('/volumedown/<filename>')
def volumedown(x,filename):
	song = getAudio(filename)
	song = song.apply_gain(x)  #  -40-0
	song.export("files/volumedown_"+filename+"_"+x, format="wav")
	return "volumedown_"+filename+"_"+x
											# Player for tests
@app.route('/TestPlay/<filename>')   # just for tests 
def player(filename):
	song = getAudio(filename)
	playback.play(song)
	return filename

# test chrome-extension://hgmloofddffdnphfgcellkdfbfbjeloo/RestClient.html stream and request
											# stream
@app.route('/stream/<filename>')
def stream(filename):
	song = file(os.path.join(os.path.dirname(__file__), 'files', filename))
	return Response(song, direct_passthrough=True)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("3001"),
        debug=True
    )

