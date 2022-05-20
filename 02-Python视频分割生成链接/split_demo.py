# -*- coding: utf-8 -*-
# @Author: AI悦创
# @Date:   2022-05-19 11:40:50
# @Last Modified by:   aiyc
# @Last Modified time: 2022-05-20 11:28:48
import os, time

def parse_path(path):
	# for i in os.walk(path):
	for dirpath, dirnames, filenames in os.walk(path):
		# print(i)
		for path in filenames:
			# print(os.path.join(dirpath, path))
			# file_path = os.path.join(dirpath, path)
			# if file_path.split(".")[-1] == "mp4": 
			if path.split(".")[-1] == "mp4": 
				# print(file_path)
				return path

def generate_html():
	pass
def split_movie(path, movie_name="Defualt"):
	# os.system("cd result")
	os.chdir("result")  # 指定输出路径
	print(os.getcwd())
	time.sleep(6)
	os.system(f"ffmpeg -i {path} -profile:v " \
		"baseline -level 3.0 -s 1920x1080 -start_number 0 " \
		f"-hls_time 10 -hls_list_size 0 -f hls {movie_name}.m3u8")

def main():
	path = "."
	file_path = parse_path(path)
	r_path = os.path.join(os.getcwd(), file_path)
	# movie_name = file_path.split(".")[0].replace("\\", "")
	movie_name = file_path.split(".")[0]
	print(f"r_path: {r_path}, \nmovie_name: {movie_name}")
	# print(os.getcwd())
	# print(os.path.join(os.getcwd(), file_path))
	split_movie(r_path, movie_name)

if __name__ == "__main__":
	main()