#include <iostream>
#include <cmath>
#include "wav_lib.h"

class RMSMeter {
private:
    WAVInfo info;

public:
    RMSMeter(WAVInfo info) {
        this->info = info;
        std::cout << "Object created" << std::endl;
    }
    ~RMSMeter() {
        std::cout << "Object removed" << std::endl;
    }

    double calculate(float* signal) {
        double   sum_sq = 0.0;

        for (int i = 0; i < info.NumberOfSamples; i++)
            sum_sq += signal[i] * signal[i];

        return std::sqrt(sum_sq / info.NumberOfSamples);
    }
};

int main() {
	WAVInfo info_a; 
	char file_a[] = "a_sound.wav";
    WAVInfo info_sh;
	char file_sh[] = "sh_sound.wav";
        
	int* signal_a = wavread(file_a, info_a);
	int* signal_sh = wavread(file_sh, info_sh);

    float* signal_a_float, *signal_sh_float;
    signal_a_float = (float*)malloc(info_a.NumberOfSamples * sizeof(float));
    signal_sh_float = (float*)malloc(info_sh.NumberOfSamples * sizeof(float));

    RMSMeter meter_a(info_a);
    RMSMeter meter_sh(info_sh);

    for (int i = 0; i < info_a.NumberOfSamples; i++){
        signal_a_float[i] = (float)(signal_a[i]) / 32768;
    }

    for (int i = 0; i < info_sh.NumberOfSamples; i++){
        signal_sh_float[i] = (float)(signal_sh[i]) / 32768;
    }

    float  rms_a = meter_a.calculate(signal_a_float);
    float  rms_sh = meter_sh.calculate(signal_sh_float);

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