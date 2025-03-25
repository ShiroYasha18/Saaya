# ML Ticket #2

Okay so basically for our 2 types of preprocessing, amplitude and frequency ka can be done pretty easily

#### 1. Amplitude
- measure the overall loudness as an average (RMS)
- identify sudden peaks in loudness
- difference in the loudness of the peaks and the global and local average (assume a short time frame for local averages)
- set a threshold range for when the loudness spike should be marked as a point of interest and specifically search that time period for flags

*Output Format*
	• Spike Start Time: 12.35s
	• Spike End Time: 12.50s
	• Duration: 0.15s
	• Amplitude Increase: +12 dB (compared to global avg)

#### 2. Frequency
- identify sounds based on pitch (high or low)
- measure frequency speed which can be useful for differentiating sounds
- Mel-Frequency Cepstral Coefficients (MFCCs): Helps with speech and sound classification.
- Pitch Estimation (F0): Detects high-pitched or low-pitched sounds, useful for emotion detection.
- Spectral Centroid: average of all the frequencies in a particular time duration  (higher the value, higher the frequency)
- Spectral Rolloff: where most of the energy is contained
- STFT Peaks: to detect sudden jumps in frequency

*Output Format*
	• Spike Start Time: 20.80s
	• Spike End Time: 21.00s
	• Duration: 0.20s
	• Frequency Increase: +3.5 kHz (compared to avg)


### Preprocessing

Converting to mono and resampling to 16kHz is easily doable. We'll receive individual packets of audio (jitna bhi time we set up per packet), convert to mono and resample, then feed it into our queue pipeline for further processing.
