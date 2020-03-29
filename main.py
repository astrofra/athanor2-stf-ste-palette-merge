# STF/STE palette merger
# The purpose of this tool is to merge both palettes of the same image
# so that it displays properly on the ATARI STF and ATARI STE computers.
# The source required to generate a file is : 
#  * An original .NEO file (created with Debabelizer, for example)
#  * A PNG file of the same image, including the STE specific palette
#
# typedef struct _NeochromeHeader
# {
# 	WORD Flag;             /* Flag byte (always 00h) */
# 	WORD Resolution;       /* Image resolution */
# 	WORD Palette[16];      /* Color palette */
# 	CHAR FileName[12];     /* Name of image file */
# 	WORD Limits;           /* Color animation limits */
# 	WORD Speed;            /* Color animation speed and direction */
# 	WORD NumberOfSteps;    /* Number of color steps */
# 	WORD XOffset;          /* Image X offset (always 00h) */
# 	WORD YOffset;          /* Image Y offset (always 00h) */
# 	WORD Width;            /* Image width (always 320) */
# 	WORD Height;           /* Image height (always 200) */
# 	WORD Reserved[33];     /* Reserved (always 00h) */ # /!\ NOT FOUND IN AN ACTUAL NEO FILE
# } NEOCHROMEHEAD;
#
# STE Color encoding
# STF: xbbb xggg xrrr
# STE: bbbb gggg rrrr
# Bits ordered as: 0321
#
# Distributed with a tiny subset of ImageMagick (Windows Binary)

import os
import shutil
import json

in_folder = 'in'
out_folder = 'out'
bin_folder = 'bin'
tmp_folder = '_tmp'

neo_bitmap_size = (320 * 200) // 2
# neo_byte_size = 32128


def c4bits(fcol):
	return max(0, min(15, int((fcol / 256.0) * 16)))


def main():
	if not os.path.exists(out_folder):
		os.mkdir(out_folder)

	if os.path.exists(tmp_folder):
		shutil.rmtree(tmp_folder)
	os.mkdir(tmp_folder)

	# for each folder
	for entry in os.listdir(in_folder):
		print("Scanning folder '" + in_folder + "/" + entry + "'")

		# get 2 files :
		# STE PNG file
		# STF NEO file
		in_files = os.listdir(os.path.join(in_folder, entry))
		if len(in_files) >= 2:
			ste_png = [x for x in in_files if x.lower().endswith('_ste.png')]
			stf_neo = [x for x in in_files if x.lower().endswith('_stf.neo')]
			if not ste_png or not stf_neo:
				print("!Missing one of the 2 files (ste.png/stf.neo")
			else:
				ste_png = ste_png[0]
				stf_neo = stf_neo[0]

				# create out folder
				out_file_path = os.path.join(out_folder, entry)
				if os.path.exists(out_file_path):
					shutil.rmtree(out_file_path)
				os.mkdir(out_file_path)

				# fetch STE palette
				# convert.exe png\vue_01_gui-ste.png json: > pal\vue_01_gui-ste.txt
				json_out_file = os.path.join(tmp_folder, ste_png + '.json')
				cmd_line = bin_folder + '\\' + 'convert.exe '
				cmd_line += os.path.join(in_folder, entry, ste_png)
				cmd_line += ' json: > '
				cmd_line += json_out_file
				try:
					os.popen(cmd_line).read()
					with open(json_out_file) as json_extract:
						data = json.load(json_extract)
						json_palette = data['image']['colormap']
						# print(json_palette)
						ste_palette = []
						json_palette = json_palette[:16]
						for color in json_palette:
							r = c4bits(int(color[1:3], 16))
							g = c4bits(int(color[3:5], 16))
							b = c4bits(int(color[5:], 16))

							ste_palette.append([r, g, b])

						print(ste_palette)
				except:
					print("!cannot extract palette!")
					ste_palette = [[7, 0, 7]] * 16

				# open NEO file
				with open(os.path.join(in_folder, entry, stf_neo), "rb") as neo_file:
					# skip header
					neo_file.read(4)
					# get palette
					neo_stf_palette = neo_file.read(16 * 2)
					# skip the remaining header
					neo_file.read(12 + 2 + 2 + 2 + 2 + 2 + 2 + 2)
					# get bitmap
					neo_b_bitmap = neo_file.read(neo_bitmap_size)

				with open(os.path.join(out_file_path, stf_neo.replace('_stf.neo', '.ne2')), "wb") as neo_out_file:
					# write STF palette
					neo_out_file.write(neo_stf_palette)

					# write STE palette
					for col in ste_palette:
						# encode the STE palette

						r, g, b = col[0], col[1], col[2]

						r <<= 4
						g <<= 4
						b <<= 4

						w = ((r & 0xe0) << 3) | ((r & 0x10) << 7)
						w |= ((g & 0xe0) >> 1) | ((g & 0x10) << 3)
						w |= ((b & 0xe0) >> 5) | ((b & 0x10) >> 1)

						hi_byte = w >> 8
						low_byte = w & 0xff

						neo_out_file.write(hi_byte.to_bytes(1, byteorder='big', signed=False))
						neo_out_file.write(low_byte.to_bytes(1, byteorder='big', signed=False))

					# write the remaining of the NEO file
					neo_out_file.write(neo_b_bitmap)

					neo_out_file.close()
		else:
			print("Files missing!")
			print(in_files)


if __name__ == "__main__":
	main()
