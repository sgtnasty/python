#include <stdio.h>
#include <string.h>

int main ()
{
    /* variable definition */

    char StudentName[100];
    float ExamValue, Sum, Avg;
    int students, exams;

    // Loop thru Students until name == blank

    while(1)
    {
        // reset Sum to 0

        Sum = 0.0;

        printf("Enter Student Name (use 0 to exit): \n");
        scanf("%s", StudentName);

        if (strcmp("0", StudentName) != 0)
        {
            // Nested Loop for Exams
            for (exams=0; exams <3; exams++)
            {
                printf("Enter exam grade: \n");
                scanf("%f", &ExamValue);
                Sum += ExamValue;
            }

            Avg = Sum/3.0;
            printf("Average for %s is %f\n", StudentName, Avg);
        }
        else {
            printf("Exiting program\n");
            break;
        }
    }
    return 0;
}