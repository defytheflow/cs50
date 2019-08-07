#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollars;
    do 
    {
        dollars = get_float("Changed owed:\n");
    } 
    while (dollars < 0);
    
    int cents = round(dollars * 100);
    int result = 0;
    
    if (cents > 25) 
    {
        int quarters;
        quarters = cents / 25;
        cents -= quarters * 25;
        result += quarters;
    }
    
    if (cents > 10) 
    {
        int dimes;
        dimes = cents / 10;
        cents -= dimes * 10;
        result += dimes;
    }
    
    if (cents > 5) 
    {
        int nickels;
        nickels = cents / 5;
        cents -= nickels * 5;
        result += nickels;
    }
    
    if (cents > 0)
    {
        int pennies;
        pennies = cents;
        result += pennies;
    }
    printf("%i\n", result);
}
