#include <cs50.h>
#include <stdio.h>
#include <crypt.h>
#include <string.h>

const string ALPHA[52] = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", 
                          "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                          "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"};

string concat(const string s1, const string s2);
bool crack1(string salt_hash, string salt, string hash);
bool crack2(string salt_hash, string salt, string hash);
bool crack3(string salt_hash, string salt, string hash);
bool crack4(string salt_hash, string salt, string hash);
bool crack5(string salt_hash, string salt, string hash);

int main(int argc, string argv[])
{
    string salt_hash;
    // If user provided an argument
    if (argc == 2)
    {
        salt_hash = argv[1];
    }
    // If user didn't provide an argument or provided more than one argument
    else
    {
        printf("Usage ./crack hash\n");
        return 1;
    }
    // Contains salt values - first two chars.
    char salt[3];
    for (int i = 0; i < 2; i++)
    {
        salt[i] = salt_hash[i];
    } 
    // Contains other hash value except salt - i decided to call it just hash
    char hash[11];
    for (int i = 2; i < strlen(salt_hash); i++)
    {
        hash[i - 2] = salt_hash[i];
    }
    //printf("Hash is %s\n", hash);
    //printf("Salt is %c%c\n", salt[0], salt[1]);
    if (crack1(salt_hash, salt, hash))
    {
        return 0;
    }
    else if (crack2(salt_hash, salt, hash))
    {
        return 0;
    }
    else if (crack3(salt_hash, salt, hash))
    {
        return 0;
    }
    else if (crack4(salt_hash, salt, hash))
    {
        return 0;
    }
    else if (crack5(salt_hash, salt, hash))
    {
        return 0;
    }
}
// Function for concatenating two strings.
string concat(const string s1, const string s2)
{
    string result = malloc(strlen(s1) + strlen(s2) + 1); // +1 for the null-terminator
    // in real code you would check for errors in malloc here
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}
// If password is one character long
bool crack1(string salt_hash, string salt, string hash)
{
    for (int i = 0; i < 52; i++)
    {
        string pass = ALPHA[i];
        string guess = crypt(pass, salt);
        if (!strcmp(guess, salt_hash))
        {
            printf("%s\n", pass);
            return true;
        }
    }
    return false;
}
// If password is two characters long
bool crack2(string salt_hash, string salt, string hash)
{
    for (int i = 0; i < 52; i++)
    {
        for (int j = 0; j < 52; j++)
        {
            string pass = concat(ALPHA[i], ALPHA[j]);
            string guess = crypt(pass, salt);
            if (!strcmp(guess, salt_hash))
            {
                printf("%s\n", pass);
                return true;
            }    
        }
    }
    return false;
}
// If password is three characters long
bool crack3(string salt_hash, string salt, string hash)
{
    for (int i = 0; i < 52; i++)
    {
        for (int j = 0; j < 52; j++)
        {
            for (int k = 0; k < 52; k++)
            {
                string pass1 = concat(ALPHA[i], ALPHA[j]);
                string pass2 = concat(pass1, ALPHA[k]);
                string guess = crypt(pass2, salt);
                if (!strcmp(guess, salt_hash))
                {
                    printf("%s\n", pass2);
                    return true;
                }    
            }
        }
    }
    return false;
}
// If password is four characters long
bool crack4(string salt_hash, string salt, string hash)
{
    for (int i = 0; i < 52; i++)
    {
        for (int j = 0; j < 52; j++)
        {
            for (int k = 0; k < 52; k++)
            {
                for (int l = 0; l < 52; l++)
                {
                    string pass1 = concat(ALPHA[i], ALPHA[j]);
                    string pass2 = concat(ALPHA[k], ALPHA[l]);
                    string pass3 = concat(pass1, pass2);
                    string guess = crypt(pass3, salt);
                    if (!strcmp(guess, salt_hash))
                    {
                        printf("%s\n", pass3);
                        return true;
                    }        
                } 
            }
        }
    }
    return false;
}
// If password is five characters long
bool crack5(string salt_hash, string salt, string hash)
{
    for (int i = 0; i < 52; i++)
    {
        for (int j = 0; j < 52; j++)
        {
            for (int k = 0; k < 52; k++)
            {
                for (int l = 0; l < 52; l++)
                {
                    for (int m = 0; m < 52; m++)
                    {
                        string pass1 = concat(ALPHA[i], ALPHA[j]);
                        string pass2 = concat(ALPHA[k], ALPHA[l]);
                        string pass3 = concat(pass1, pass2);
                        string pass4 = concat(pass3, ALPHA[m]);
                        string guess = crypt(pass4, salt);
                        if (!strcmp(guess, salt_hash))
                        {
                            printf("%s\n", pass4);
                            return true;
                        }          
                    }    
                } 
            }
        }
    }
    return false;
}
