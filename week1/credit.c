#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

string get_card_number(void);
bool check_if_digits(string card);
char get_card_type(string card);
bool check_even_card(string card);
bool check_odd_card(string card);

int main(void)
{
    string card = get_card_number();
    char type = get_card_type(card);
    if (type == 'v' && strlen(card) == 13)
    {
        if (check_odd_card(card))
        {
            printf("VISA\n");
            return 0;
        }
        else
        {
            printf("INVALID\n");
            return 0;
        }
    }
    else if (type == 'v' && strlen(card) == 16)
    {
        if (check_even_card(card))
        {
            printf("VISA\n");
            return 0;
        }
        else
        {
            printf("INVALID\n");
            return 0;
        }
    }
    else if (type == 'a')
    {
        if (check_odd_card(card))
        {
            printf("AMEX\n");
            return 0;
        }
        else
        {
            printf("INVALID\n");
            return 0;
        }
    }
    else if (type == 'm')
    {
        if (check_even_card(card))
        {
            printf("MASTERCARD\n");
            return 0;
        }
        else
        {
            printf("INVALID\n");
            return 0;
        }
    }
}
// Prompts user for credit card number.
string get_card_number(void)
{
    string card;
    do
    {
        card = get_string("Number: ");
    }
    while (!check_if_digits(card)); 
    return card;
}
// Checks if number provided by user is all digits.
bool check_if_digits(string card)
{
    if (strlen(card) == 0)
    {
        return false;
    }
    for (int i = 0; i < strlen(card); i++)
    {
        if (!isdigit(card[i]))
        {
            return false;
        }
    }
    return true;
}
// Returns v - if visa, a -if american express, m - if mastercaed
char get_card_type(string card)
{
    if (card[0] == '4' && (strlen(card) == 13 || strlen(card) == 16))
    {
        return 'v';
    }
    else if (card[0] == '3' && (card[1] == '4' || card[1] == '7') && strlen(card) == 15)
    {
        return 'a';
    }
    else if (strlen(card) == 16 && (card[0] == '5' && (card[1] == '1' || card[1] == '2' || 
                                    card[1] == '3' || card[1] == '4' || card[1] == '5')))
    {
        return 'm';
    }
    else
    {
        printf("INVALID\n");
        return 0;
    }
}
// If card length is even, then we use this function to implement Luhns algorithm.
bool check_even_card(string card)
{
    int sum1 = 0;
    for (int i = strlen(card) - 2; i >= 0; i -= 2)
    {
        int num = card[i] - '0';
        num *= 2;
        if (num > 9)
        {
            sum1 += num / 10 + num % 10;
        }
        else
        {
            sum1 += num;
        }
    }
    int sum2 = 0;
    for (int i = strlen(card) - 1; i >= 1; i -= 2)
    {
        sum2 += card[i] - '0';
    }
    int sum = sum1 + sum2;
    if (sum % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
// If card length is odd, then we use this function to implement Luhns algorithm.
bool check_odd_card(string card)
{
    int sum1 = 0;
    for (int i = strlen(card) - 2; i >= 1; i -= 2)
    {
        int num = card[i] - '0';
        num *= 2;
        if (num > 9)
        {
            sum1 += num / 10 + num % 10;
        }
        else
        {
            sum1 += num;
        }
    }
    int sum2 = 0;
    for (int i = strlen(card) - 1; i >= 0; i -= 2)
    {
        sum2 += card[i] - '0';
    }
    int sum = sum1 + sum2;
    if (sum % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
