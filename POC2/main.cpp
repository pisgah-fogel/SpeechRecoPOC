#include <iostream>

#include <portaudio.h>

int main(int argc, char** argv)
{
    PaError err = Pa_Initialize();

    if(err != paNoError) {
        std::cout<<"Error: Cannot initialise PortAudio: "<<Pa_GetErrorText(err)<<std::endl;
        return 1;
    }
    std::cout<<"PortAudio initialized successfully"<<std::endl;

    err = Pa_Terminate();
    if(err != paNoError) {
        std::cout<<"Error: Cannot free PortAudio's ressources: "<<Pa_GetErrorText(err)<<std::endl;
        return 1;
    }
    std::cout<<"PortAudio's ressources freed"<<std::endl;

    return 0;
}
