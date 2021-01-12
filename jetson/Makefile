00_forward_4s: arduino.o 00_forward_4s.cpp
	g++ -c 00_forward_4s.cpp -o 00_forward_4s.o -Isources/
	g++ -o 00_forward_4s arduino.o 00_forward_4s.o


01_forward_4s_simple:  arduino.o simple_arduino.o 01_forward_4s_simple.cpp
	g++ -c 01_forward_4s_simple.cpp -o 01_forward_4s_simple.o -Isources/
	g++ -o 01_forward_4s_simple arduino.o simple_arduino.o 01_forward_4s_simple.o

02_get_frame: 02_get_frame.cpp
	g++ 02_get_frame.cpp -o 02_get_frame `pkg-config --cflags --libs opencv`


simple_arduino.o: arduino.o sources/simple_arduino.hpp sources/simple_arduino.cpp
	g++ -c sources/simple_arduino.cpp -o simple_arduino.o -Isources/


arduino.o: sources/arduino.hpp sources/arduino.cpp
	g++ -c sources/arduino.cpp -o arduino.o


clean:
	rm *.o 00_forward_4s 01_forward_4s_simple 02_get_frame

