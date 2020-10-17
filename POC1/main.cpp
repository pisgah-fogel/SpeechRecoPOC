#define UNIT
#include "lowOverheadUnitTest.hpp"

#include <iostream>
#include <deque>
#include <stdint.h> // uint8_t
#include <stdio.h> // printf

#define FREQDEFINITION 2 ///< Number of frequency in the signal (TODO: 1024)
#define FREQTYPE uint8_t ///< Data type used in frequency domain (TODO: uint8_t)
#define BUFFERSIZE 5 ///< How many samples in the buffer = <FDFT Samping frequency> * <Max phoeneme duration>

FREQTYPE fft_buffer[BUFFERSIZE][FREQDEFINITION];

/**
 * @brief Fast Discret Fourier Tranformer fake outputs for test purposes
 */
void generateTestFDFT()
{
  // Pattern A
  fft_buffer[0][0] = 0; fft_buffer[0][1] = 0;
  fft_buffer[1][0] = 0; fft_buffer[1][1] = 1;
  fft_buffer[2][0] = 0; fft_buffer[2][1] = 1;
  fft_buffer[3][0] = 1; fft_buffer[3][1] = 1;
  fft_buffer[4][0] = 0; fft_buffer[4][1] = 0;
}

void printFDFT()
{
  std::cout<<"  ";
  for (size_t i = 0; i < BUFFERSIZE; i++) {
    printf("\tt%lu", i);
  }
  std::cout<<std::endl;
  for (size_t i = 0; i < FREQDEFINITION; i++) {
    printf("F%lu", i);
    for (size_t z = 0; z < BUFFERSIZE; z++)
      printf("\t%d", fft_buffer[z][i]);
    std::cout<<std::endl;
  }
}

int predictA()
{
  if (FREQDEFINITION != 2) {
    std::cout<<"Error: FREQDEFINITION has changed"<<std::endl;
    return 1;
  }
  if (BUFFERSIZE != 5) {
    std::cout<<"Error: BUFFERSIZE has changed"<<std::endl;
    return 1;
  }
  const uint8_t wa[5][2] = { // Weigth for Sample A
    {0, 0},
    {0, 255},
    {0, 255},
    {255, 255},
    {0, 0}
  };
  const unsigned int threshold = 3; // = SUM(wa) - Tolerance
  bool matchA = false;

  generateTestFDFT();

  unsigned int probability = 0;
  for (size_t i = 0; i<5; i++) { // For every sample (frequency domain)
    for (size_t z = 0; z < 2; z++) { // For every frequency
      probability += wa[i][z] & fft_buffer[i][z];
    }
  }

  if (probability > threshold) {
    matchA = true;
  }

  if (matchA)
    return 0; // Test passed
  else {
    std::cout<<"Bad prediction, prob="<<probability<<", threshold="<<threshold<<std::endl;
    return 1; // Test failed
  }

  return -1; // Missing
}
START_TEST(predictA);

int printTests(void)
{
  generateTestFDFT();
  printFDFT();

  return 0;
}
START_TEST(printTests);

int main()
{
  std::cout<<"This is still in development, nothing to do yet"<<std::endl;
  return 0;
}