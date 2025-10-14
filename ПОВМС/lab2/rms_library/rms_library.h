#pragma once

#ifdef RMSLIBRARY_EXPORTS
#define RMSLIBRARY_API _declspec(dllexport)
#else 
#define RMSLIBRARY_API _declspec(dllimport)
#endif // RMSLIBRARY_EXPORTS

#include <iostream>
#include <cmath>
#include <fstream>

extern "C" RMSLIBRARY_API typedef struct WAVHeader {

	int   ChunkID;
	int   ChunkSize;
	int   Format;

	int   Subchunk1ID;
	int   Subchunk1Size;
	short AudioFormat;
	short NumChannels;
	int   SampleRate;
	int   ByteRate;
	short BlockAlign;
	short BitsPerSample;

	int   SubChunk2ID;
	int   Subchunk2Size;

}wavheader;

extern "C" RMSLIBRARY_API typedef struct WAVInfo {

	WAVHeader    Header;
	unsigned int  NumberOfSamples;
}wavinfo;

extern "C" RMSLIBRARY_API int* wavread(char* filename, WAVInfo& info);
extern "C" RMSLIBRARY_API int wavwrite(char* filename, WAVInfo& info, int* data);
extern "C" RMSLIBRARY_API double calculate(float* signal, WAVInfo& info);