#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    int k;
    if (argc == 2) 
    {
        string key = argv[1];
        for (int i = 0; i < strlen(key); i++)
        {
            if (!isdigit(key[i]))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        // printf("Success\n");
        k = atoi(argv[1]);
        k = k % 26;
        // printf("%i\n", k);
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    string message = get_string("plaintext: ");
    for (int i = 0; i < strlen(message); i++)
    {
        // if char is in uppercase
        if (64 < message[i] && message[i] < 91)
        {
            if (64 < message[i] + k && message[i] + k < 91)
            {
                message[i] += k;
            }
            // if goes around the alphabet
            else 
            {
                message[i] = message[i] + k - 26;
            }
        }
        // if char is in lowercase
        else if (96 < message[i] && message[i] < 123)
        {
            if (96 < message[i] + k && message[i] + k < 123)
            {
                message[i] += k;
            }
            else
            {
                message[i] = message[i] + k - 26;
            }
        }
    }
    printf("ciphertext: %s\n", message);
}
