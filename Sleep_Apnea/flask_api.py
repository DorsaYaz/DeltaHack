from flask import Flask, Response, request, jsonify
from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt


app = Flask(__name__)

sample_freq   = 1000
apnia_seconds = 10


def get_apnia_info(audio_path):
    try:
        # get the sample frequence and sound array
        sampFreq, snd_arr = wavfile.read(audio_path)

        # cut out one of the audio channels 
        new_snd_arr = snd_arr[:,0] 
        
        # down sample the sound array 
        secs = int(len(new_snd_arr)/sampFreq)
        samps = secs*sample_freq
        new_snd_arr = signal.resample(new_snd_arr, samps)

        # scale the data between -1 and +1
        new_snd_arr  = new_snd_arr / np.max(np.abs(new_snd_arr))

        # convert any negative values to positive
        new_snd_arr = np.absolute(new_snd_arr)

        # determine threshold for audio level that determines any time inbetween breaths
        threshold = np.mean(new_snd_arr) * 4

        apnia_tracker = []

        apnia_state = 0
        sample_counter = 0
        # find periods of encounterd apnia
        for sample in new_snd_arr:
            if not apnia_state:
                if sample < threshold:
                    apnia_state = 1
            elif apnia_state:
                if sample < threshold:
                    sample_counter += 1
                else:
                    apnia_state = 0
                    if (sample_counter / sample_freq) >= apnia_seconds:
                        apnia_tracker.append(sample_counter / sample_freq)
                    sample_counter = 0
        return len(apnia_tracker)
    except:
        return 0


@app.route('/get_data')
def get_data():
    user_id = request.args.get('file_name')
    print(user_id)
    num_apnia_tracker = get_apnia_info(user_id)
    return jsonify(num_apnia_tracker)


if __name__ == '__main__':
    app.run(debug=True)