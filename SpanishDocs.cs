using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MathNet.Numerics.LinearAlgebra;
using MathNet.Numerics.Data.Text;
using MathNet.Numerics.LinearAlgebra.Double;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;

namespace Cross_lingual
{
    class SpanishDocs
    {
        //a mothod that read the word embeddings and assign them to a dictionary  
        public static Dictionary<string, Vector<double>> dicVic()
        {
            Dictionary<string, Vector<double>> dic = new Dictionary<string, Vector<double>>();
            foreach (var line in File.ReadLines(@"C:\Mannheim Uni\New folder\SBW-vectors-300-min5.txt"))
            {
                Vector<double> V = DenseVector.OfArray(Array.ConvertAll(line.Split().Skip(1).ToArray(), double.Parse));
                dic.Add(line.Split()[0], V);
            }
            return dic;
        }

        //read the vocabulary index and assign them to a dictionary
        public static Dictionary<string, string> wIndexer = new Dictionary<string, string>();
        public static void Wordindenx()
        {

            foreach (var line in File.ReadLines(@"C:\Mannheim Uni\New folder\vocab.txt"))
            {
                wIndexer.Add(line.Split()[0], line.Split()[1]);
            }

        }


        static void Main(string[] args)
        {
            //initialize the vocabulary index dictionary
            Wordindenx();
            //initialize the word embedding vector 
            var dv = dicVic();
            Console.WriteLine("dictionay vec loaded");
            //declare a dictionary for the documents embeddings
            Dictionary<int, Vector<double>> docEm = new Dictionary<int, Vector<double>>();
            //declare a indexer
            int i = 0;
            //declare a variable for the weights' sum
            double WeightSum = 0;
            //declare a vector for the sum of the word vector embeddings
            Vector<double> vecSum = Vector.Build.Dense(300);
            //loop for read the dataset in Spanish 
            foreach (var line in File.ReadLines(@"C:\Mannheim Uni\New folder\train_es.txt"))
            {

                if (Convert.ToInt32(line.Split()[0]) == i)
                {
                    if (dv.ContainsKey(wIndexer[line.Split()[1]]))
                    {
                        //Obtain the word embedding  
                        Vector<double> V = dv[wIndexer[line.Split()[1]]];
                        //multiply the Vector with the word weight
                        V = V * Convert.ToDouble(line.Split()[2]);
                        //aggregate the vectors
                        vecSum += V;
                        WeightSum += Convert.ToDouble(line.Split()[2]);
                    }
                }
                else {
                    //aggregate the vectors and divide them on the weights sum
                    vecSum = vecSum / WeightSum;
                    // add the final document embedding vector to the dictionary
                    docEm.Add(i, vecSum);
                    WeightSum = 0;
                    vecSum = 0 * vecSum;
                    i++;
                }
            }
            Console.WriteLine("done");

            //write the final document embadding in excel file
            using (StreamWriter file = new StreamWriter(@"C:\Mannheim Uni\New folder\test.csv"))
            {
                foreach (var item in docEm)
                {
                    file.Write(item.Key + "," + string.Join(" ", item.Value.ToArray()));
                    file.Write(Environment.NewLine);
                }
            }
                    Console.WriteLine("Press any key to exit");
            Console.ReadKey();
        }



    }
}