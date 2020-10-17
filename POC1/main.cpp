#define BOOST_TEST_MODULE SPEECHPOC1
#include <boost/test/included/unit_test.hpp>
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

BOOST_AUTO_TEST_SUITE( ts_speechPOC1)

BOOST_AUTO_TEST_CASE( tc_printFDFT )
{
  generateTestFDFT();
  printFDFT();

  BOOST_TEST_REQUIRE( true );
}

BOOST_AUTO_TEST_SUITE_END()