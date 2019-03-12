# A First Look at Deep Learning Apps on Smartphones
This is the official project page. Please read the [paper](https://arxiv.org/abs/1812.05448) for more details.
## Data & code needed

### Data needed
1. Snapshots of the app market (apk files) in early Jun. 2018 (deleted), early Sep. 2018 (apks_sep_2018.tar) and mid February 2019 (apks_feb_2019.tar) (each contains 16,500 the most popular apps covering 33 different categories listed on Google Play)
2. meta information crawled from Google Play Web page in early Sep. 2018 (htmls_sep_2018.tar) and mid February 2019 (htmls_feb_2019.tar)
3. apk files of DL-apps extracted in early Sep. 2018 (DL_apks_sep_2018.tar)
4. meta information of DL-apps crawled from Google Play Web page in early Sep. 2018 (DL_htmls_sep_2018.tar)
5. apps that use DL frameworks (apps_DL frameworks.xlsx)
 listed libs (Tensorflow, Caffe, etc.); no lib
6. DL usage in different apps (apps and usages.xlsx)
 Usage, Detailed usage, As core feature
7. DL models used in apps (apps_models.xlsx)
Apps, Framework, Model types, How to obtain model files

### Code needed
1. basic_func.py
 basic functions used by other files (run command lines, get file size, etc.)
2. extract_zip.py
extract zip files
3. decompose_apps.py
Extract apk files using **apktool**
4. extract_so.py
Extract useful information from .so libs using **readelf**
5. DL_Sniffer_Model_extractor.py
 Find apps that use DL and Find model files of DL-apps
6. model_analyzer.py
analyze model size, type (DNN, CNN, or RNN?), depth, usage, layers
7. apps_info.py
comparison between DL-apps and non-DL-apps (reviews, downloads, ratings, size) and information of DL-apps (downloads, reviews, rankings, developers, checkin and checkout, category)
8. DL_apps.py (all codes implemented in one file)

###Instructions on how to run the code
#### requirements
You will need the following installed:
* python 2.7+
* tensorflow
* collections
* google.protobuf
* bs4

#### preparations
1. Run decompose_apps.py to decompose raw apk files using **apktool**
`python decompose_apps.py input_apk_path output_dir`
example: `python decompose_apps.py ../data/raw_apks/ ../data/decomposed_apks/`
2. Run extract_so.py to extract section data using **readelf**
`python extract_so.py input_apk_path decomposed_apk_path output_dir`
example: `python extract_so.py ../data/raw_apks/ ../data/decomposed_apks/ ../data/section_data/`
#### find DL-apps and their models
1. Run DL_Sniffer_Model_extractor.py to get DL-apps stored in *DL_PKGS* and their models stored in *DL_MODELS* as output,  in *MODEL_BLKLIST* we put known models that are not analyzable, you can change the *magic_str* and *find_model_via_suffix* part in each sub section according to your findings. 
`python DL_Sniffer_Model_extractor.py input_apk_path decomposed_apk_path section_data_path`
example: `python DL_Sniffer_Model_extractor.py ../data/raw_apks/ ../data/decomposed_apks/ ../data/section_data/`
#### analyze DL models
1. In model_analyzer.py, change *model_xsl* to store the models extracted from DL_Sniffer_Model_extractor.py in the following format:
`apk_name \t model_path \t framework \t suffix \t usable \n`, (the models extracted in this project are stored in code/configuration/model_xsl.txt)run this code to analyze models. (supporting Tensorflow, Tensorflow lite, Caffe, ncnn)
`python model_analyzer.py decomposed_apk_path`
example: `python model_analyzer.py ../data/decomposed_apks/`

#### extract information on apps
1. In apps_info.py, *RAW_APK_PATH_NEW* is used to store the newly crawled apps, and you should run the whole process above for them, too; *HTML_PATH* and *HTML_PATH_NEW* is used to store the information page of apps and *html_path* is used to store the information page of found DL-apps; Change *final_dl_pkgs* and *new_final_dl_pkgs* to store the DL-apps found by DL_Sniffer_Model_extractor.py. Run this code to get information (downloads, reviews, etc.) on apps.
2. In apps_lib_size.py, change *raw_txt* to store the libs found by extract_so.py with the following format: `apk name \t lib name \t framework \n`, and run this code to get the size of the lib files.
`python apps_lib_size.py decomposed_apk_path new_apk_path`
example: `python apps_lib_size.py ../data/decomposed_apks/ ../data/raw_apks_new/`