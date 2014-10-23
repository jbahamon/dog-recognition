#include <iostream>
#include <fstream>
#include <opencv2/core/core.hpp>
#include <opencv2/ml/ml.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

// aweonao eran doubles no ints :3 por eso todo se iba a la mierda, saludos
// cordiales
void save_sparse_descriptors(ostream& stream, vector<int> labels, vector<Mat> data) 
{

    cout << data.size() << endl;

    for (int i = 0; i < data.size(); ++i)
    {
        Mat descriptor = data[i];
        int len = descriptor.cols;
        double val;

        stream << labels[i];

        for(int j = 0; j < len; ++j)
        {
            val = descriptor.at<float>(0, j);

            if (val == 0) continue;

            stream << " " << (j + 1) << ":" << val;
        }
        stream << endl;
    }       

}

int main (int argc, const char** argv) 
{

    int K_values[4] = { 100, 500, 1000, 1500 };

    String dog_folder = "./dogs/eval/";
    String nondog_folder = "./no-dogs/eval/";
    stringstream filename;

    Ptr<FeatureDetector > detector(new SiftFeatureDetector());
    Ptr<DescriptorMatcher > matcher(new BruteForceMatcher<L2<float> >());
    Ptr<DescriptorExtractor> extractor(new
            SiftDescriptorExtractor());
    Ptr<BOWImgDescriptorExtractor> bowide(new BOWImgDescriptorExtractor(extractor,matcher));

    FileStorage f("kmeans.yml", FileStorage::READ);

    stringstream param_name;
    vector<KeyPoint> keypoints;

    vector<int> labels;

    Mat histogram;
    Mat img;

    for (int k_idx = 0; k_idx < 4; k_idx++) 
    {
        Mat vocabulary;

        param_name << "kmeans" << K_values[k_idx];
        f[param_name.str()] >> vocabulary;
        param_name.str(std::string());

        bowide->setVocabulary(vocabulary);

        vector<Mat> histograms;

        for (int i = 0; i < 200; i++) 
        {
            filename << dog_folder << i << ".jpg";
            img = imread(filename.str(),0);
            filename.str(std::string());
            
            detector->detect(img,keypoints);
            bowide->compute(img, keypoints, histogram);
            labels.push_back(1);
            histograms.push_back(histogram);

        }
        
        for (int i = 0; i < 200; i++) 
        {
            filename << nondog_folder << i << ".jpg";
            img = imread(filename.str(),0);
            filename.str(std::string());
            
            detector->detect(img,keypoints);
            bowide->compute(img, keypoints, histogram);
            labels.push_back(0);
            histograms.push_back(histogram);

        }
        
        param_name << "eval_" << K_values[k_idx];

        ofstream histograms_file;
        histograms_file.open(param_name.str().c_str());
        save_sparse_descriptors(histograms_file, labels, histograms);
        histograms_file.close();
        param_name.str(std::string());

    }


    f.release();

}
