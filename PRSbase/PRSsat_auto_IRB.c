#include <sys/types.h>
#include <sys/dir.h>
#include <sys/param.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "lib_PRSsat.h"

#define FALSE 0
#define TRUE !FALSE
#define CMAXstr 200
#define CINPstr 42
#define CSPTstr 23

// Versión 1.0, 09/2016 -- Rodrigo Alonso Suárez.

int main(int argc, char *argv[]){

	FILE * data;
	char PATHimg[CMAXstr];
	char RUTAent[CMAXstr];
	char RUTAsal[CMAXstr];
	char RUTAcal[CMAXstr];
	char DATAspatial[CMAXstr];
	char DATAfolders[CMAXstr];
	char DATAimglist[CMAXstr];
	char imgs[CINPstr];
	char CODEspatial[CSPTstr];
	int		h1, h2, h3, Ci, Cj, Ct, tag, Cimgs, OK;
	double	LATmax, LATmin, LONmax, LONmin, dLATgri, dLONgri, dLATcel, dLONcel;
	int * MSKmat;
	int * CNT1mat;
	int * CNT2mat;
	double * TXmat;
	double * LATmat; double * LONmat;
	double * LATvec; double * LONvec;
	double * CALirb_m;
	double * CALirb_n;
	double * CALirb_a;
	double * CALirb_b1;
	double * CALirb_b2;

	// IMAGEN A PROCESAR
	strncpy(DATAfolders, argv[1], CMAXstr);
	strncpy(DATAspatial, argv[2], CMAXstr);
	strncpy(DATAimglist, argv[3], CMAXstr);

	// ABRO ARCHIVO FOLDERS:
	data = fopen(DATAfolders, "ro");
	if (data == NULL) {printf("No se encontro archivo folders. Cerrando.\n"); return 0;}
	fscanf(data, "%s\n", &RUTAent[0]);
	fscanf(data, "%s\n", &RUTAsal[0]);
	fscanf(data, "%s\n", &RUTAcal[0]);
	fclose(data);

	// ABRO ARCHIVO SPATIAL:
	data = fopen(DATAspatial, "ro");
	if (data == NULL) {printf("No se encontro archivo spatial. Cerrando.\n"); return 0;}
	fscanf(data, "%lf\n", &LATmax);
	fscanf(data, "%lf\n", &LATmin);
	fscanf(data, "%lf\n", &LONmax);
	fscanf(data, "%lf\n", &LONmin);
	fscanf(data, "%lf\n", &dLATgri);
	fscanf(data, "%lf\n", &dLONgri);
	fscanf(data, "%lf\n", &dLATcel);
	fscanf(data, "%lf\n", &dLONcel);
	fscanf(data, "%s\n",  &CODEspatial[0]);
	fclose(data);

	// ABRO ARCHIVO IMGLIST:
	Cimgs = 0;
	data = fopen(DATAimglist, "ro");
	if (data == NULL) {printf("No se encontro archivo imglist. Cerrando.\n"); return 0;}
	while(fscanf(data, "%s\n", &imgs[0]) != EOF){
		Cimgs = Cimgs + 1;
	}
	fclose(data);
	char array_imgs[Cimgs][CINPstr]; 
	Cimgs = 0;
	data = fopen(DATAimglist, "ro");
	if (data == NULL) {printf("No se encontro archivo imglist. Cerrando.\n"); return 0;}
	while(fscanf(data, "%s\n", &imgs[0]) != EOF){
		strcpy(array_imgs[Cimgs], &imgs[0]);
		Cimgs = Cimgs + 1;
	}
	fclose(data);

	// INIT
	OK = 0;

	// RUTA DE SALIDA
	strcat(RUTAsal, CODEspatial); strcat(RUTAsal, "/");

	// INFORMACION DE LOS ARCHIVOS CARGADOS
	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Archivos y Rutas -------------------------------------------------------------\n");
	printf("FOLDERS: %s\n", &DATAfolders[0]);
	printf("SPATIAL: %s\n", &DATAspatial[0]);
	printf("IMGLIST: %s\n", &DATAimglist[0]);
	printf("RUTAent: %s\n", &RUTAent[0]);
	printf("RUTAsal: %s\n", &RUTAsal[0]);
	printf("RUTAcal: %s\n", &RUTAcal[0]);
	printf("CODIGO : %s\n", &CODEspatial[0]);
	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Resolucion Espacial ----------------------------------------------------------\n");
	printf("LAT = [%+07.3f .. %+07.3f] --- GRILLA = [%+07.3f, %+07.3f]\n", LATmax, LATmin, dLATgri, dLONgri);
	printf("LON = [%+07.3f .. %+07.3f] --- CELDAS = [%+07.3f, %+07.3f]\n", LONmax, LONmin, dLATcel, dLONcel);
	printf("-----------------------------------------------------------------------------------\n");

	// GRILLAS
	printf("---- Trabajos iniciales -----------------------------------------------------------\n");
	OK = generar_grilla(&LATmat, &LONmat, &LATvec, &LONvec,
		LATmax, LATmin, LONmax, LONmin, dLATgri, dLONgri, &Ci, &Cj, &Ct);
	printf("Grillas generadas. OK = [%d]. Ci = [%d] :: Cj = [%d] :: Ct = [%d].\n", OK, Ci, Cj, Ct);
	OK = guardar_grilla(RUTAsal, Ci, Cj, Ct, LATmax, dLATgri, LONmin, dLONgri,
		&LATvec[0], &LONvec[0], &LATmat[0], &LONmat[0]);
	printf("Grillas grabadas.  OK = [%d].\n", OK);
	OK = cargar_calibracion_IRB(RUTAcal,
		&CALirb_m, &CALirb_n, &CALirb_a, &CALirb_b1, &CALirb_b2);
	printf("Calibracion IRB.   OK = [%d].\n", OK);
	printf("-----------------------------------------------------------------------------------\n");	
	printf("---- Imagenes procesadas ----------------------------------------------------------\n");
	
	// PROCESAR LISTA DE IMAGENES
	for (h1=0; h1<Cimgs; h1++){

		printf("-----------------------------------------------------------------------------------\n");	

		// RUTA A LA IMAGEN
		strncpy(PATHimg, RUTAent, CMAXstr); strcat(PATHimg, array_imgs[h1]);

		// PROCESO IMAGEN
		OK = procesar_NetCDF_IRB_gri(&TXmat, &MSKmat, &CNT1mat, &CNT2mat, &tag,
	   		dLATgri, dLONgri, dLATcel, dLONcel, LATmax, LATmin, LONmax, LONmin,
	   		Ct, Ci, Cj, PATHimg, RUTAsal, 
	   		CALirb_m, CALirb_n, CALirb_a, CALirb_b1, CALirb_b2);

		// SI NO SE USA, BORRO
		free(TXmat); free(MSKmat); free(CNT1mat); free(CNT2mat);

		// FINAL IMAGEN
		printf("IMAGEN : %s. TAG = [%d]. OK = [%d].\n", &PATHimg[0], tag, OK);
	}
	printf("-----------------------------------------------------------------------------------\n");
	// printf("---- Lista de imagenes ------------------------------------------------------------\n");
	// for (h1=0; h1<Cimgs; h1++){
	// 	printf("%s\n", array_imgs[h1]);
	// }
	// printf("-----------------------------------------------------------------------------------\n");

	// mostrar_vector_double(CALirb_m, 12, 4);
	// printf("-----------------------------------------------------------------------------------\n");
	// mostrar_vector_double(CALirb_b1, 12, 4);
	// printf("-----------------------------------------------------------------------------------\n");
	// mostrar_vector_double(CALirb_n, 12, 4);
	// printf("-----------------------------------------------------------------------------------\n");
	// mostrar_vector_double(CALirb_a, 12, 4);
	// printf("-----------------------------------------------------------------------------------\n");
	// mostrar_vector_double(CALirb_b2, 12, 4);
	// printf("-----------------------------------------------------------------------------------\n");

	//mostrar_vector_double(FRmat, Ct, Cj);
	//mostrar_vector_double(CZmat, Ct, Cj);
	//mostrar_vector_double(RPmat, Ct, Cj);
	//mostrar_vector_int(MSKmat, Ct, Cj);

	return 1;
}
