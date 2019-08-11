# Questions

## What's `stdint.h`?

It is a file (heading) that contains simple data types that are defined by either a C/C++ typedef or #define statement.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

U in those types stands for unsigned. It means than the first bit is no longer reservef gor a sign (+/-).
The point of using it is that we know that all bits in a bmp file are positive, so we can just abort the first
signing bit and save some space and work with larger values using this type of a bit.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

1, 4, 4, 2

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

BM

## What's the difference between `bfSize` and `biSize`?

bfSze is the size, in bytes, of the bitmap file, while biSize is the number of bytes required by the structure.
(struct BITMAPINFOHEADER).

## What does it mean if `biHeight` is negative?

If biHeight is negative, it maeans that the filw goes from top to bottom, from left to right.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in `copy.c`?

Because there might be not file with a particular name.

## Why is the third argument to `fread` always `1` in our code?

In order to read a one element of the data.

## What value does `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

It is used to move a file pointer to a certain location the file.

## What is `SEEK_CUR`?

It moves file pointer position to a given location.
