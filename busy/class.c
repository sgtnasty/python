#include <stdio.h>

int main ()
{
    /* variable definition */

    char StudentName[100];

    float ExamValue, Sum, Avg;

    int students, exams;

    // Loop thru 5 Students

    for (students=0; students <5; students++)
    {
        // reset Sum to 0

        Sum = 0.0;

        printf("Enter Student Name: \n");
        scanf("%s", StudentName);

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
    return 0;
}