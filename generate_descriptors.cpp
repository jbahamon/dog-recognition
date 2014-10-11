#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/ml/ml.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

int main (int argc, const char** argv) 
{
    // computing descriptors
    Ptr<DescriptorExtractor> extractor = new SiftDescriptorExtractor();

    Mat training_descriptors;

    SiftFeatureDetector detector;

    vector<KeyPoint> keypoints;

    Mat descriptors;
    Mat img;
    stringstream name_stream;
    String filename;

    for (int i = 0; i < 5000; i++) 
    {
        name_stream << "corpus/" << i << ".jpg";
        filename = name_stream.str();
        name_stream.str(std::string());

        img  = imread(filename, 0);

        detector.detect(img, keypoints);

        extractor->compute(img, keypoints, descriptors);

        training_descriptors.push_back(descriptors);

        if (i % 1000 == 0)
            cout << i << endl;

    }

    srand(unsigned(time(NULL)));
    vector<int> seeds;

    for (int cont = 0; cont < training_descriptors.rows; cont++)
        seeds.push_back(cont);

    randShuffle(seeds);

    Mat chosen_descriptors;

    for (int i = 0; i < 100000; i++) 
    {
        chosen_descriptors.push_back(training_descriptors.row(seeds[i]));        
    }
    
    FileStorage f;

    f.open("descriptors.yml", FileStorage::WRITE);
    f << "descriptors" << chosen_descriptors;
    f.release();


    return 0;
}
