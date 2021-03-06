#!/bin/bash

#Versión 1.0. 10/2016. Rodrigo Alonso Suárez

# PROGRAMAS
main='/rolo/Wsate/PRS/server-sat-01/libs/PRS-sat/PRSbase/PRSsat_IRB_test';
libs='/rolo/Wsate/PRS/server-sat-01/libs/PRS-sat/PRSbase/lib_PRSsat';

# PARAMETROS
folders='/rolo/Wsate/PRS/server-sat-01/libs/PRS-sat/PRSbase/data/job_folders_ALL_test';
spatial='/rolo/Wsate/PRS/server-sat-01/libs/PRS-sat/PRSbase/data/job_spatial_IRB_test';
imglist='/rolo/Wsate/PRS/server-sat-01/libs/PRS-sat/PRSbase/data/job_imglist_IRB_test';
product=('/B02-TX/' '/B02-MK/' '/B03-TX/' '/B03-MK/' '/B04-TX/' '/B04-MK/' '/B06-TX/' '/B06-MK/');

echo '=== Carpetas =================================================================';
j=1;
while read line; do
	if [ $j -eq 2 ]; then
		RUTAsal=$line;
	fi
	let j=$j+1;
done < $folders
j=1;
while read line; do
	if [ $j -eq 9 ]; then
		codigo=$line;
	fi
	let j=$j+1;
done < $spatial
RUTAdes=$RUTAsal$codigo;
if [ ! -d $RUTAdes'/meta/' ]; then
	mkdir -p $RUTAdes'/meta/';
fi
if [ ! -d $RUTAdes'/test/' ]; then
	mkdir -p $RUTAdes'/test/';
fi
if [ ! -d $RUTAdes'/zCRR/' ]; then
	mkdir -p $RUTAdes'/zCRR/';
fi
for line in $(<$imglist); do
	year=${line:15:4};
	#echo $year;
	for prod in ${product[*]}
	do
    	if [ ! -d $RUTAdes$prod$year ]; then
			mkdir -p $RUTAdes$prod$year;
		fi
		if [ ! -d $RUTAdes'/zIMP'$prod$year ]; then
			mkdir -p $RUTAdes'/zIMP'$prod$year;
		fi
	done
done

echo '=== Compilacion ==============================================================';
gcc -o $libs'.o' -c $libs'.c' -lnetcdf -lm;
gcc -o $main $main'.c' $libs'.o' -lnetcdf -lm;

echo '=== Run ======================================================================';
time $main $folders $spatial $imglist;
