This repo contains the code and data for our paper "A First Look at Deep Learning Apps on Smartphones" (WWW'19, [arxiv](https://arxiv.org/abs/1812.05448)).

### Dataset (please contact Mengwei Xu for the dataset)
Snapshots of the app market (apk files) in early Jun. 2018 (deleted), early Sep. 2018 (apks_sep_2018.tar) and mid February 2019 (apks_feb_2019.tar) (each contains 16,500 the most popular apps covering 33 different categories listed on Google Play)
2. meta information crawled from Google Play Web page in early Sep. 2018 (htmls_sep_2018.tar) and mid February 2019 (htmls_feb_2019.tar)

### requirements
You will need the following installed:
* python 2.7+
* tensorflow
* collections
* google.protobuf
* bs4
* readelf
* apktool
* aapt (as standalone tool)

### preparations
1. Run decompose_apps.py to decompose raw apk files using **apktool**
```sh
python decompose_apps.py ../data/raw_apks/ ../data/decomposed_apks/
```
2. Run extract_so.py to extract section data using **readelf**
```sh
python extract_so.py ../data/raw_apks/ ../data/decomposed_apks/ ../data/section_data/
```

### find DL-apps and their models
1. Run DL_Sniffer_Model_extractor.py to get DL-apps stored in *DL_PKGS* and their models stored in *DL_MODELS* as output,  in *MODEL_BLKLIST* we put known models that are not analyzable, you can change the *magic_str* and *find_model_via_suffix* part in each sub section according to your findings. 
```sh
python DL_Sniffer_Model_extractor.py ../data/raw_apks/ ../data/decomposed_apks/ ../data/section_data/
```

### analyze DL models
1. In model_analyzer.py, change *model_xsl* to store the models extracted from DL_Sniffer_Model_extractor.py in the following format:
`apk_name \t model_path \t framework \t suffix \t usable \n`, (the models extracted in this project are stored in code/configuration/model_xsl.txt)run this code to analyze models. (supporting Tensorflow, Tensorflow lite, Caffe, ncnn)
```sh
python model_analyzer.py ../data/decomposed_apks/
```

### extract information on apps
1. In apps_info.py, *RAW_APK_PATH_NEW* is used to store the newly crawled apps, and you should run the whole process above for them, too; *HTML_PATH* and *HTML_PATH_NEW* is used to store the information page of apps and *html_path* is used to store the information page of found DL-apps; Change *final_dl_pkgs* and *new_final_dl_pkgs* to store the DL-apps found by DL_Sniffer_Model_extractor.py. Run this code to get information (downloads, reviews, etc.) on apps.
2. In apps_lib_size.py, change *raw_txt* to store the libs found by extract_so.py with the following format: `apk name \t lib name \t framework \n`, and run this code to get the size of the lib files.
```sh
python apps_lib_size.py ../data/decomposed_apks/ ../data/raw_apks_new/
```

### Notes:
This is a very primitive attempt to analyze deep learning apps on smartphones. The current tool is still flawed in many aspects and there's a rich unexplored space for this topic. Thus we appreciate any kinds of contributions to push forward this analysis.
