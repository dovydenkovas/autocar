all: 00_read_video 01_find_line 02_find_line_func 03_select_sign 04_rec_signs 06_line_and_signs


00_read_video: 00_read_video.cpp
	g++ 00_read_video.cpp -o 00_read_video `pkg-config --cflags --libs opencv4`

01_find_line: 01_find_line.cpp
	g++ 01_find_line.cpp -o 01_find_line `pkg-config --cflags --libs opencv4`

02_find_line_func: 02_find_line_func.cpp
	g++ 02_find_line_func.cpp -o 02_find_line_func `pkg-config --cflags --libs opencv4`

03_select_sign: 03_select_sign.cpp
	g++ 03_select_sign.cpp -o 03_select_sign `pkg-config --cflags --libs opencv4`

04_rec_signs: 04_rec_signs.cpp
	g++ 04_rec_signs.cpp -o 04_rec_signs `pkg-config --cflags --libs opencv4`

05_rec_signs_func: 05_rec_signs_func.cpp
	g++ 05_rec_signs_func.cpp -o 05_rec_signs_func `pkg-config --cflags --libs opencv4`

06_line_and_signs: 06_line_and_signs.cpp
	g++ 06_line_and_signs.cpp -o 06_line_and_signs `pkg-config --cflags --libs opencv4`

clean:
	rm -f *.o
	rm -f 00_read_video
	rm -f 01_find_line 02_find_line_func
	rm -f 03_select_sign 04_rec_signs 05_rec_signs_func
	rm -f 06_line_and_signs
