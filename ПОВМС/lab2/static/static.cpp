#include "rms_library.h"

int main()
{
	WAVInfo info_a; 
	char file_a[] = "a_sound.wav";
    WAVInfo info_sh;
	char file_sh[] = "sh_sound.wav";
        
	int* signal_a = wavread(file_a, info_a);
	int* signal_sh = wavread(file_sh, info_sh);

    float* signal_a_float, *signal_sh_float;
    signal_a_float = (float*)malloc(info_a.NumberOfSamples * sizeof(float));
    signal_sh_float = (float*)malloc(info_sh.NumberOfSamples * sizeof(float));

    for (int i = 0; i < info_a.NumberOfSamples; i++){
        signal_a_float[i] = (float)(signal_a[i]) / 32768;
    }

    for (int i = 0; i < info_sh.NumberOfSamples; i++){
        signal_sh_float[i] = (float)(signal_sh[i]) / 32768;
    }

    float  rms_a = calculate(signal_a_float,info_a);
    float  rms_sh = calculate(signal_sh_float, info_sh);

    std::cout << std::endl << " RMS for 'A': " << rms_a << std::endl;
    std::cout << " RMS for 'Sh': " << rms_sh << std::endl << std::endl;

    delete[] signal_a;
    delete[] signal_sh;
    free(signal_a_float);
    free(signal_sh_float);
    //delete[] signal_a_float;
    //delete[] signal_sh_float;
	return 0;
}