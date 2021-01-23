
opencv_lib=`pkg-config --cflags --libs opencv4`

all: 00_read_video 01_find_line 02_find_line_func 03_select_sign 04_rec_signs 05_rec_signs_func 06_line_and_signs 07_add_tr


00_read_video: 00_read_video.cpp
	g++ 00_read_video.cpp -o 00_read_video $(opencv_lib)

01_find_line: 01_find_line.cpp
	g++ 01_find_line.cpp -o 01_find_line $(opencv_lib)


02_find_line_func: 02_find_line_func.cpp
	g++ 02_find_line_func.cpp -o 02_find_line_func $(opencv_lib)


03_select_sign: 03_select_sign.cpp
	g++ 03_select_sign.cpp -o 03_select_sign $(opencv_lib)


04_rec_signs: 04_rec_signs.cpp
	g++ 04_rec_signs.cpp -o 04_rec_signs $(opencv_lib)


05_rec_signs_func: 05_rec_signs_func.cpp
	g++ 05_rec_signs_func.cpp -o 05_rec_signs_func $(opencv_lib)


06_line_and_signs: 06_line_and_signs.cpp
	g++ 06_line_and_signs.cpp -o 06_line_and_signs $(opencv_lib)


07_add_tr: 07_add_tr.cpp
	g++ 07_add_tr.cpp -o 07_add_tr $(opencv_lib)


clean:
	rm -f *.o
	rm -f 00_read_video
	rm -f 01_find_line 02_find_line_func
	rm -f 03_select_sign 04_rec_signs 05_rec_signs_func
	rm -f 06_line_and_signs 07_add_tr
