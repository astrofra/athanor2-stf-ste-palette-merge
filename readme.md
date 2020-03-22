# STF/STE palette merger

The purpose of this tool is to merge both palettes of the same image
so that it displays properly on the ATARI STF and ATARI STE computers.

The source required to generate a file is : 
* An original .NEO file (created with Debabelizer, for example)
* A PNG file of the same image, including the STE specific palette

## Detail of a NEO header

```cpp
typedef struct _NeochromeHeader
{
	WORD Flag;             /* Flag byte (always 00h) */
	WORD Resolution;       /* Image resolution */
	WORD Palette[16];      /* Color palette */
	CHAR FileName[12];     /* Name of image file */
	WORD Limits;           /* Color animation limits */
	WORD Speed;            /* Color animation speed and direction */
	WORD NumberOfSteps;    /* Number of color steps */
	WORD XOffset;          /* Image X offset (always 00h) */
	WORD YOffset;          /* Image Y offset (always 00h) */
	WORD Width;            /* Image width (always 320) */
	WORD Height;           /* Image height (always 200) */
	WORD Reserved[33];     /* Reserved (always 00h) /!\ NOT FOUND IN AN ACTUAL NEO FILE */
} NEOCHROMEHEAD;
```

## Color encoding in the resulting file

* STf : xxxx xRRR xVVV xBBB
* STe : xxxx RRRR VVVV BBBB

## About...

* *This tool was made for the ATARI ST version of Athanor 2. It has no other purpose*
* *Distributed with a tiny subset of [ImageMagick](https://imagemagick.org) (Windows Binary)*
* *Possible improvment : automatically convert the STF PNG file into a NEO file*
* *Any question : astrofra[at]gmail[dot*