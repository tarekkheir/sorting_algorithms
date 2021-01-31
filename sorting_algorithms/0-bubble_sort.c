#include "sort.h"

void bubble_sort(int *array, size_t size)
{
    size_t i = 0;
    size_t tmp = 0;
    size_t restart = 0;

    while(i < size)
    {
        if (array[i - 1] > array[i] && i != 0)
        {
            tmp = array[i - 1];
            array[i - 1] = array[i];
            array[i] = tmp;
            print_array(array, size);
            restart = 1;
        }
        i++;
    }
    if (restart != 0)
        bubble_sort(array, size);
}
