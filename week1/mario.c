// This program drwas pyramids out of hashes from mario computer game.

#include <cs50.h>
#include <stdio.h>

int prompt(void);
void drawPyramid(int height);

int main(void)
{
    int height = prompt();
    drawPyramid(height);
}

// Prompts the user for specific height.
int prompt(void)
{    
    int height;
    do 
    {
       height = get_int("Give me the height of the pyramid?\n");
    } 
    while (height <= 0 || height > 9);
    return height;
}

// Displays a pyramid with user's height in the console.
void drawPyramid(int height)
{
    char hash = '#';
    int space = height - 1;
    
    for (int i = 1; i < height + 1; i++) 
    {
        for (int j = 0; j < space; j++) 
        {
            printf(" ");    
        }
        for (int k = 1; k <= i; k++ )
        {
            printf("%c", hash);
        }
        printf("  ");
        for (int k = 1; k <= i; k++ )
        {
            printf("%c", hash);
        }
        for (int j = 0; j < space; j++) 
        {
            printf("  ");    
        }
        space -= 1;
        printf("\n");
    }
}
