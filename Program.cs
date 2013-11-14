using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            int[] numbers = {2, 4, -1, -5, 8, 10, -11};
            Max_Sum(numbers);
        }
        static int Max_Sum(int[] numbers)
        {
                        
            int max_sum = 0;
            int temp_sum = 0;
            foreach (int element in numbers)
            {
                temp_sum += element;
                if (element > 0)
                {
                    max_sum = Math.Max(max_sum, temp_sum);
                }
                else if (element <= 0 && temp_sum <= 0)
                {
                    temp_sum = 0;
                }
             }
            return max_sum;
        }
    }
}
