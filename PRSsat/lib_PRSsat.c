#include <sys/types.h>
#include <sys/dir.h>
#include <sys/param.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define PI 3.1415926
#define FALSE 0
#define TRUE !FALSE
#define coszTHR 0.05
#define n1THR 0.465
#define Rmin 0.06
#define Rmax 0.465
#define Ccods 1200

// Versión 1.0, 10/2016 -- Rodrigo Alonso Suárez.

int mostrar_vector_double(double * vec, int cvec){

	int		h1, h2, cmax;
	
	h2 = 1;
	cmax = 11;
	for (h1 = 0; h1 < cvec; h1++){
		if (h2==cmax){
			printf("%+06.2f\n", vec[h1]); h2=1;
		}else{
			printf("%+06.2f  ", vec[h1]); h2=h2+1;
		}
	}

	if (h2 > 1){printf("\n");}
	
	// FIN
	return 1;
}