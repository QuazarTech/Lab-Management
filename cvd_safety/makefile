objects = lab_safety_iQ.o

CC = "/usr/bin/g++"

test : $(objects)
	@ echo Building $@
	$(CC) -o test lab_safety_iQ.o -pthread -Wall -O3 -std=c++14 -lL412B -lftdi

lab_safety_iQ.o : lab_safety_iQ.cxx
	$(CC) -c lab_safety_iQ.cxx -pthread -Wall -O3 -std=c++14 -lL412B -lftdi

.PHONY : clean
clean :
	@ echo Cleaning...
	rm -f test $(objects)