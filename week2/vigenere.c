#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int shift(char key);
char caesar(char letter, int k);

int main(int argc, string argv[])
{
    string keyword;
    if (argc == 2) 
    {
        keyword = argv[1];
        for (int i = 0; i < strlen(keyword); i++)
        {
            if (isdigit(keyword[i]))
            {
                printf("Usage: ./vigenere keyword\n");
                return 1;
            }
        }
        string message = get_string("plaintext: ");   
        int key = 0;
        for (int i = 0; i < strlen(message); i++)
        {
            if (isalpha(message[i]))
            {   
                if (key >= strlen(keyword))
                {
                    key = 0;
                }
                message[i] = caesar(message[i], shift(keyword[key]));
                key++;
            }
        }
        printf("ciphertext: %s\n", message);
        return 0;
    }
    printf("Usage: ./vigenere keyword\n");
    return 1;
}

int shift(char key)
{
    if (!islower(key))
    {
        key = tolower(key);
    }   
    return key - 'a';
}    

char caesar(char letter, int k)
{
    // if char is in uppercase
    if (64 < letter && letter < 91)
    {
        if (64 < letter + k && letter + k < 91)
        {
            letter += k;
        }
        // if goes around the alphabet
        else 
        {
            letter = (letter + k - 90 + 65 - 1);
        }
    }
    // if char is in lowercase
    else if (96 < letter && letter < 123)
    {
        if (96 < letter + k && letter + k < 123)
        {
            letter += k;
        }
        else
        {
            letter = letter + k - 122 + 97 - 1;
        }
    }
    return letter;
}
