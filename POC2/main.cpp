#include <iostream>

#include <portaudio.h>

#define SAMPLE_RATE (44100)

typedef struct
{
    float left_phase;
    float right_phase;
}   
paTestData;
static paTestData data;
/* This routine will be called by the PortAudio engine when audio is needed.
 * It may called at interrupt level on some machines so don't do anything
 * that could mess up the system like calling malloc() or free().
*/ 
static int patestCallback( const void *inputBuffer, void *outputBuffer,
                           unsigned long framesPerBuffer,
                           const PaStreamCallbackTimeInfo* timeInfo,
                           PaStreamCallbackFlags statusFlags,
                           void *userData )
{
    /* Cast data passed through stream to our structure. */
    paTestData *data = (paTestData*)userData; 
    float *out = (float*)outputBuffer;
    unsigned int i;
    (void) inputBuffer; /* Prevent unused variable warning. */
    
    for( i=0; i<framesPerBuffer; i++ )
    {
         *out = data->left_phase;  /* left */
         out++;
         *out = data->right_phase;  /* right */
         out++;
        /* Generate simple sawtooth phaser that ranges between -1.0 and 1.0. */
        data->left_phase += 0.01f;
        /* When signal reaches top, drop back down. */
        if( data->left_phase >= 1.0f ) data->left_phase -= 2.0f;
        /* higher pitch so we can distinguish left and right. */
        data->right_phase += 0.03f;
        if( data->right_phase >= 1.0f ) data->right_phase -= 2.0f;
    }
    return 0;
}


void openStreamOnDefaultDevice_playSquareWave() {
    PaStream *stream;
    PaError err;
    /* Open an audio I/O stream. */
    err = Pa_OpenDefaultStream(&stream,
        0,          /* no input channels */
        2,          /* stereo output */
        paFloat32,  /* 32 bit floating point output */
        SAMPLE_RATE,
        256,        /* frames per buffer, i.e. the number
                    of sample frames that PortAudio will
                    request from the callback. Many apps
                    may want to use
                    paFramesPerBufferUnspecified, which
                    tells PortAudio to pick the best,
                    possibly changing, buffer size.*/
        patestCallback, /* this is your callback function */
        &data
    ); /*This is a pointer that will be passed to your callback*/
    if(err != paNoError) {
        std::cout<<"Error: Cannot Open Default Stream: "<<Pa_GetErrorText(err)<<std::endl;
        return;
    }

    err = Pa_StartStream(stream);
    if(err != paNoError) {
        std::cout<<"Error: Cannot Start Stream: "<<Pa_GetErrorText(err)<<std::endl;
        return;
    }

    // Usefull fonctions:
    //err = Pa_IsStreamStopped(stream) // TODO: Start again streams which are "Callback Stopped"
    //err = Pa_IsStreamActive(stream)
    //const PaStreamInfo *    Pa_GetStreamInfo (PaStream *stream)
    //PaTime  Pa_GetStreamTime (PaStream *stream)
    //double  Pa_GetStreamCpuLoad (PaStream *stream)
    //PaError Pa_GetSampleSize (PaSampleFormat format)

    Pa_Sleep(2*1000);

    err = Pa_StopStream(stream);
    if(err != paNoError) {
        std::cout<<"Error: Cannot Stop Stream: "<<Pa_GetErrorText(err)<<std::endl;
        return;
    }

    err = Pa_CloseStream(stream);
    if(err != paNoError) {
        std::cout<<"Error: Cannot Close Stream: "<<Pa_GetErrorText(err)<<std::endl;
        return;
    }
}

void listDevices()
{
    int numDevices;
    numDevices = Pa_GetDeviceCount();
    if( numDevices < 0 )
    {
        std::cout<<"Error: Cannot list audio devices, returned "<<numDevices<<std::endl;
    }
    const   PaDeviceInfo *deviceInfo;
    for( size_t i=0; i<numDevices; i++ )
    {
    deviceInfo = Pa_GetDeviceInfo( i );
    std::cout<<" - "<<deviceInfo->name<<", maxInputs: "<<deviceInfo->maxInputChannels<<", maxOutputs: "<<deviceInfo->maxOutputChannels<<", default sample rate: "<<deviceInfo->defaultSampleRate<<std::endl;
    }
}

int main(int argc, char** argv)
{
    PaError err = Pa_Initialize();

    if(err != paNoError) {
        std::cout<<"Error: Cannot initialise PortAudio: "<<Pa_GetErrorText(err)<<std::endl;
        return 1;
    }
    std::cout<<Pa_GetVersionText()<<std::endl;
    std::cout<<"PortAudio initialized successfully"<<std::endl;

    std::cout<<"Available devices:"<<std::endl;
    listDevices();

    openStreamOnDefaultDevice_playSquareWave();

    err = Pa_Terminate();
    if(err != paNoError) {
        std::cout<<"Error: Cannot free PortAudio's ressources: "<<Pa_GetErrorText(err)<<std::endl;
        return 1;
    }
    std::cout<<"PortAudio's ressources freed"<<std::endl;

    return 0;
}
