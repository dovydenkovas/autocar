all: 01_forward_4s 02_get_frame

01_forward_4s: arduino.o 01_forward_4s.cpp
	g++ -c 01_forward_4s.cpp -o 01_forward_4s.o -Isources/
	g++ -o 01_forward_4s arduino.o 01_forward_4s.o


02_get_frame: 02_get_frame.cpp
	g++ 02_get_frame.cpp -o 02_get_frame `pkg-config --cflags --libs opencv4`


simple_arduino.o: arduino.o sources/simple_arduino.hpp sources/simple_arduino.cpp
	g++ -c sources/simple_arduino.cpp -o simple_arduino.o -Isources/


arduino.o: sources/arduino.hpp sources/arduino.cpp
	g++ -c sources/arduino.cpp -o arduino.o


clean:
	rm -f *.o 01_forward_4s 02_get_frame
