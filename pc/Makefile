all: 00_read_video 01_find_line 02_stop_sign


00_read_video: 00_read_video.cpp
	g++ 00_read_video.cpp -o 00_read_video `pkg-config --cflags --libs opencv4`

01_find_line: 01_find_line.cpp
	g++ 01_find_line.cpp -o 01_find_line `pkg-config --cflags --libs opencv4`

02_find_line_func: 02_find_line_func.cpp
	g++ 02_find_line_func.cpp -o 02_find_line_func `pkg-config --cflags --libs opencv4`

03_select_sign: 03_select_sign.cpp
	g++ 03_select_sign.cpp -o 03_select_sign `pkg-config --cflags --libs opencv4`

clean:
	rm -f *.o 00_read_video 01_find_line 02_find_line_func 03_select_sign
