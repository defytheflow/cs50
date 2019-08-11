// Resizes a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

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
    float n;
    n = atof(argv[1]);
    if (!(n >= 0.0 && n <= 100.0))
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

    // Create BITMAPFILEHEADER and BITMAPINFOHEADER and copy infile values to there.
    BITMAPFILEHEADER out_bf = in_bf;
    BITMAPINFOHEADER out_bi = in_bi;

    // Change width and height by the factor of n
    out_bi.biWidth = round(in_bi.biWidth * n);
    //printf("%i\n", in_bi.biHeight);
    //printf("%f\n", round(n));
    out_bi.biHeight = round(in_bi.biHeight * n);
    int out_padding = (4 - (out_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    out_bi.biSizeImage = ((sizeof(RGBTRIPLE) * out_bi.biWidth) + out_padding) * abs(out_bi.biHeight);

// BITMAPFILEHEADER
    out_bf.bfSize = out_bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    // write outfile's BITMAPFILEHEADER
    fwrite(&out_bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    // write outfile's BITMAPINFOHEADER
    fwrite(&out_bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    int in_padding = (4 - (in_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    if (n >= 1.0)
    {
        // for each row in file
        for (int i = 0, biHeight = abs(in_bi.biHeight); i < biHeight; i++)
        {
            for (int s = 0; s < round(n); s++)
            {
                // for each pixel in infile
                for (int j = 0; j < in_bi.biWidth; j++)
                {
                    // create temporary container for a pixel
                    RGBTRIPLE triple;
                    // read bytes of a single pixel into container
                    fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                    // write this pixel to the outfile n times
                    for (int k = 0; k < round(n); k++)
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
    }
    else
    {
        // for each row
        for (int i = 0, biHeight = abs(in_bi.biHeight); i < biHeight; i += biHeight / (biHeight * n))
        {
            printf("%f\n", biHeight / (biHeight * n));
            // for each pixel in infile
            for (int j = 0; j < in_bi.biWidth; j += in_bi.biWidth / (in_bi.biWidth * n))
            {
                // create temporary container for a pixel
                RGBTRIPLE triple;
                // read bytes of a single pixel into container
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                for (int k = 1; k < in_bi.biWidth / (in_bi.biWidth * n); k++)
                {
                    fseek(inptr, sizeof(RGBTRIPLE), SEEK_CUR);
                }
                // write this pixel to the outfile n times
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);

                //fseek(inptr, sizeof(RGBTRIPLE), SEEK_CUR);
            }
            // add padding if row not multiple of 4
            for (int k = 0; k < out_padding; k++)
            {
                fputc(0x00, outptr);
            }
            // skip padding in infile
            for (int k = 1; k < in_bi.biWidth / (in_bi.biWidth * n); k++)
            {
                fseek(inptr, in_padding, SEEK_CUR);

                fseek(inptr, sizeof(RGBTRIPLE) * in_bi.biWidth + in_padding, SEEK_CUR);
            }
        }
    }
    // close infile
    fclose(inptr);
    // close outfile
    fclose(outptr);
    // success
    return 0;
}

