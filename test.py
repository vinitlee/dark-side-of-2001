import numpy
#from scipy.io import wavfile
import wave
import cv2
import cv
import os

def get_vid(stream, begin, end):

    for x in xrange(begin):
        if not x%100: print x
        stream.read()
    raw = [stream.read()[1][:, :, 0] for x in xrange(end - begin)]
    return numpy.array(raw)

def important_frames(vid):
    X = numpy.diff(vid, axis=2)
    #diff = get_diff_raw(fname, begin, end)
    diff_mean = X.mean(0).mean(1)
    diff_maxs = numpy.where(
        diff_mean > numpy.percentile(diff_mean, 95))
    return diff_maxs

def get_imp_streaming(stream, begin, end):
    diff = []
    for i in xrange(end):
        frame = stream.read()[1][:, :, 0]
        if i < begin: 
            prev_frame = frame
            continue
        diff.append(numpy.linalg.norm(frame - prev_frame))
        prev_frame = frame
    return numpy.array(diff)

def get_music(framerate):
    wavs = []
    filen = [filenames for filenames in os.walk('./music')][0][2]
    filen.sort()
    for f in filen:
	print f
        if f.find('.wav') >= 0 and f.find('05') >= 0:
            wav = (wave.open('./music/'+f))
	    ft_temp = 0
            for ft in numpy.arange(0,wav.getnframes(),wav.getframerate()/framerate)[1:]:
		ft = int(numpy.round(ft))
		wavs.append(int(numpy.mean(map(lambda x: abs(ord(x)),list(wav.readframes(ft - ft_temp))))))
		ft_temp = ft
    return numpy.array(wavs)

def music_moments(stream):
    window = stream.read(1024) * numpy.hanning()
    spect = numpy.abs(numpy.fft.fft(window))
    diff = numpy.linalg.norm(prev_spec - spec)
        
if __name__ == '__main__':
    vid_cap = cv2.VideoCapture('space.mp4')
    print 'n_frames', vid_cap.get(cv.CV_CAP_PROP_FRAME_COUNT)

    wavs    = get_music(vid_cap.get(cv.CV_CAP_PROP_FPS))
    wavs_d1 = numpy.insert((numpy.diff(wavs))   ,0,0)
    wavs_d2 = numpy.insert((numpy.diff(wavs_d1)),0,0)
    wavs_d2 = wavs_d2 * (wavs_d2 > 0) 

#map(lambda x: str(int(x/30.0/60))+":"+str(int((x/30.0)%60)),numpy.arange(0,len(wavs))[wavs_d1 > 70])
