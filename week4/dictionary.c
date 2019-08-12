// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];
int SIZE = 0;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        SIZE++;
        // We calculate it's hash
        int hashed = hash(word);
        node *n = malloc(sizeof(node));
        // Some error checking
        if (!n)
        {
            return 1;
        }
        // We Put values in this node.
        for (int i = 0; i < strlen(word); i++)
        {
            n->word[i] = word[i];
        }
        n->next = NULL;

        // if it is a pointer
        if (hashtable[hashed])
        {
            for (node *ptr = hashtable[hashed]; ptr != NULL; ptr = ptr->next)
            {
                if (!ptr->next)
                {
                    ptr->next = n;
                    break;
                }
            }
        }
        else
        {
            hashtable[hashed] = n;
        }

    }

    // Close dictionary
    fclose(file);
    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return SIZE;
}

// Returns true if word is in dictionary else false

// Must be case-insensetive
// Should return true for words that are actually in the dictionary
bool check(const char *word)
{
    for (int i = 0; i < N; i++)
    {
        for (node *ptr = hashtable[i]; ptr != NULL; ptr = ptr->next)
        {
            if (!strcasecmp(word,  ptr->word))
            {
                return true;
            }

        }

    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        while (hashtable[i] != NULL)
        {
            node *next = hashtable[i]->next;
            free(hashtable[i]);
            hashtable[i] = next;
        }
    }
    return true;
}
