#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover image\n");
        return 1;
    }

    char *card_file = argv[1];

    FILE *memory_card = fopen(card_file, "r");

    if (memory_card == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", card_file);
        return 2;
    }

    bool found_jpeg;
    bool end_of_file = false;
    int file_counter = 0;
    FILE *img;
    // Until the end of the file we do the following steps
    while (!end_of_file)
    {
        // If already not found a JPEG
        if (!found_jpeg)
        {
            // We read the first 512 byte block
            BYTE buffer[512];
            fread(&buffer, 512, 1, memory_card);

            // Is it a start of a new JPEG?
            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
            {
                found_jpeg = true;
                //we create a name for an output file
                char filename[8];
                sprintf(filename, "%03i.jpg", file_counter);
                file_counter++;

                // We open the output image file
                img = fopen(filename, "w");

                // We write that block to an output file
                fwrite(buffer, 512, 1, img);

            }
            // If not found the JPEG, just continue loooking
            else
            {
                continue;
            }
        }
        // If already found a JPEG
        else
        {
            // We read the first 512 byte block
            BYTE buffer[512];
            if (fread(&buffer, 1, 512, memory_card) < 512)
            {
                end_of_file = true;

                fclose(img);
                fclose(memory_card);

                return 0;
            }
            // if not end of the file
            else
            {
                // Is it a start of a new JPEG?
                if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
                {
                    // close the previous jpeg
                    fclose(img);

                    // create a new jpeg;
                    char filename[8];
                    sprintf(filename, "%03i.jpg", file_counter);
                    file_counter++;

                    // We open the output image file
                    img = fopen(filename, "w");

                    // We write that block to an output file
                    fwrite(buffer, 512, 1, img);

                }
                // Not the start of a new JPEG
                else
                {
                    // We write that block to an output file
                    fwrite(buffer, 512, 1, img);
                }
            }

        }

    }


}

