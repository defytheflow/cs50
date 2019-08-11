// Resizes a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // if not 4 command arguments something went wrong
    if (argc != 4)
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }

    // Checking n value
    int n;
    n = atoi(argv[1]);
    if (!(n >= 1 && n <= 100))
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }

    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER in_bf;
    fread(&in_bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER in_bi;
    fread(&in_bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (in_bf.bfType != 0x4d42 || in_bf.bfOffBits != 54 || in_bi.biSize != 40 ||
        in_bi.biBitCount != 24 || in_bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }


// Here we need to implement the functionality
// 1. Open an infile
// 2. Create an outfile

// 3. Update ourfile's header info
// The resized file will have an updated header info.
// File size changes, image size, width and height.
// BITMAPINFOHEADER has - biWidth (width of image in pixels, WITHOUT padding) and - biHeight (height of image).
// biSizeImage - total size of image in bytes (includes pixels and padding).
// bi.biSizeIamge = ((sizeof(RGBTRIPLE) * bi.biWidth) + padding) * abs(bi.biHeight);
// BITMAPFILEHEADER has - bfSize total size of file in bytes (includes pixels, padding and headers)
// bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
// bi.biWidth -> bi.biWidth *= n
// bi.biHeight -> bi.biHeight *= n
// bi.biSizeImage -> ?
// bi.bfSize -> ?
// padding -> ? keep track of both the old and the new padding
// By calculating all this stuff we will be done with the header.

// 4. Read infile's scanline pixel by pixel (RGBTRIPLE)
// fread(data, size, number, inptr);
// data: pointer to a struct that will contain the bytes you're reading
// size: size of each element to read (sizeof())
// number: number of elements to read
// inptr: FILE * to read from

// 5. Resize horizontally
// for each row
//      for each pixel in row
//          write to outfile n times
//      write outfile's padding
//      skip over infile's padding (so that we reach the next row of the infile)

// fwrite(data, size, number, outptr); we call this function to write our pixels into outfile
// data: pointer to the struct thaht contains the bytes you're reading from
// outptr: FILE * to write to

// 6. Remember padding
// Each pixel is 3 bytes; length of each scanline must be a multiple of 4 bytes
// If the number of pixels isn't a multiple of 4, we need "padding"
// Padding is just zeros (0x00)
// the outfile and infile have different widths so the padding is different
// padding isn;t an RGBTRIPLE we can't fread padding
// to write padding use fputc*(chr, outptr); like fputc(0x00, outptr);


// 2. re-copy methods
// go back to the start of the original scanline
// re-scale scanline
//
// file position indicator
// fseek(inptr, offset, from);
// inptr - FILE * to seek in; offset - number of bytes to move cursor
// from - SEEK_CUR (current position in file), SEEK_SET(beggining of file), SEEK_END (end of file)




    // Create BITMAPFILEHEADER and BITMAPINFOHEADER and copy infile values to there.
    BITMAPFILEHEADER out_bf = in_bf;
    BITMAPINFOHEADER out_bi = in_bi;

    // Change width and height by the factor of n
    out_bi.biWidth = in_bi.biWidth * n;
    out_bi.biHeight = in_bi.biHeight * n;
    int out_padding = (4 - (out_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    out_bi.biSizeImage = ((sizeof(RGBTRIPLE) * out_bi.biWidth) + out_padding) * abs(out_bi.biHeight);

// BITMAPFILEHEADER
    out_bf.bfSize = out_bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    // write outfile's BITMAPFILEHEADER
    fwrite(&out_bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    // write outfile's BITMAPINFOHEADER
    fwrite(&out_bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    // 7. Resize vertically
    // every pixel repeated n times
    // every row repeated n times
    // for each row
    //      for n-1 times
    //      write pixels, padding to outfile
    //      send infile cursor back
    // write pixels, padding to outfile
    // skip over infile padding

    int in_padding = (4 - (in_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;


    // for each row in file
    for (int i = 0, biHeight = abs(in_bi.biHeight); i < biHeight; i++)
    {
        for (int s = 0; s < n; s++)
        {
            // for each pixel in infile
            for (int j = 0; j < in_bi.biWidth; j++)
            {
                // create temporary container for a pixel
                RGBTRIPLE triple;
                // read bytes of a single pixel into container
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write this pixel to the outfile n times
                for (int k = 0; k < n; k++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }
            // add padding if row not multiple of 4
            for (int k = 0; k < out_padding; k++)
            {
                fputc(0x00, outptr);
            }
            // skip padding in infile
            fseek(inptr, -sizeof(RGBTRIPLE) * in_bi.biWidth, SEEK_CUR);

        }
        fseek(inptr, sizeof(RGBTRIPLE) * in_bi.biWidth + in_padding, SEEK_CUR);

    }


    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
