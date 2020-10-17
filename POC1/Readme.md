
Fs = Sampling Frequency = 8000 Hz
Input format: Audio Stream -> WAV NIST SPhere, signed 8bit PCM or loaded from file
Tsample = Maximal duration of a sample/word = 0.6s
Nfreq = Number of frequency inside our signal (after FFT) = 1024

Every 10 samples we are going to perform a (discret) Fast Fourier Transform.

For every samples in the buffer (Tsample*Fs) we are going to apply a weight for every word we want to detect.

In order to perform it in real time we have to stay under t = 1/Fs * 10 = 1,25ms
To test the feasability of the project let's consider a CPU, single core, at 800MHz.
Number of operation to perform = Nfreq*Tsample*Fs/10 = 500K
At 800MHz it's 625us.

Some operations will be perform in parallel thanks to big registers (64bit = 4*8bit) and/or SSX.
However to be used on small devices the FFT and conversion from the device... should stay < 600us.

Objectives:
- FFT of 0.6*8000 values under 600us
- Measure audio stream capture's overhead
- Implement the recognition (One word first)

Problems:
- This is only for 1 word, and for 10... ?