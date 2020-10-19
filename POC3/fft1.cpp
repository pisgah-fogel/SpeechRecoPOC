#include <stdio.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "fft1.hpp"
#include "lowOverheadUnitTest.hpp"

#define FFT_DEPTH 1024 // Size of the FFT

void rearrange(float data_re[],float data_im[],const unsigned int N)
{
	unsigned int target = 0;
	for(unsigned int position=0; position<N;position++)
	{
		if(target>position) {
			const float temp_re = data_re[target];
			const float temp_im = data_im[target];
			data_re[target] = data_re[position];
			data_im[target] = data_im[position];
			data_re[position] = temp_re;
			data_im[position] = temp_im;
		}
		unsigned int mask = N;
		while(target & (mask >>=1))
			target &= ~mask;
		target |= mask;
	}
}

void compute(float data_re[],float data_im[],const unsigned int N)
{
	const float pi = -3.14159265358979323846;
	for(unsigned int step=1; step<N; step <<=1) {
		const unsigned int jump = step << 1;
		const float step_d = (float) step;
		float twiddle_re = 1.0;
		float twiddle_im = 0.0;
		for(unsigned int group=0; group<step; group++)
		{
			for(unsigned int pair=group; pair<N; pair+=jump)
			{
				const unsigned int match = pair + step;
				const float product_re = twiddle_re*data_re[match]-twiddle_im*data_im[match];
				const float product_im = twiddle_im*data_re[match]+twiddle_re*data_im[match];
				data_re[match] = data_re[pair]-product_re;
				data_im[match] = data_im[pair]-product_im;
				data_re[pair] += product_re;
				data_im[pair] += product_im;
			}
			// we need the factors below for the next iteration
			// if we don't iterate then don't compute
			if(group+1 == step)
			{
				continue;
			}
			float angle = pi*((float) group+1)/step_d;
			twiddle_re = cos(angle);
			twiddle_im = sin(angle);
		}
	}
}

void fft1(float data_re[], float data_im[],const int N)
{
	rearrange(data_re,data_im,N);
	compute(data_re,data_im,N);
}

// ***********  TESTS ************

void print_arr(const float data[],const unsigned int N)
{
	printf("{");
	for(unsigned int i=0;i<N-1;i++)
		printf("%.3f,",data[i]);
	printf("%.3f}\n",data[N-1]);
}

int compare_arrays(const float x[],const float y[], const unsigned int N,const float eps)
{
	int result = 1;
	for(unsigned int i=0;i<N;i++)
	{
		if(fabs(x[i]-y[i])>eps) {
			result = 0;
		}
	}

	if(result==0)
	{
		printf("Expected: ");
		print_arr(y,N);
		printf("Got     : ");
		print_arr(x,N);
	}

	return result;
}

int fft1_test1(void)
{
	float data1_re[8] = {0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0};
	float data1_im[8] = {7.0,6.0,5.0,4.0,3.0,2.0,1.0,0.0};
	float expected1_re[8] = {28.0,5.656,0.0,-2.343,-4.0,-5.656,-8.0,-13.656};
	float expected1_im[8] = {28.0,13.656,8.0,5.656,4.0,2.343,0.0,-5.656};
	fft1(data1_re,data1_im,8);
	int tc1_re = compare_arrays(data1_re,expected1_re,8,0.01);
	int tc1_im = compare_arrays(data1_im,expected1_im,8,0.01);
	if (!tc1_re or !tc1_im)
		return 1;
	else
		return 0;
}
START_TEST(fft1_test1);
