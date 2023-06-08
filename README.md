# RadioTTS
This typewriter OCR application can convert JPEG typewritten text images into RTF documents, while removing typos for you!

![Image RTF basic mode](https://github.com/LPBeaulieu/Typewriter-OCR-TintypeText/blob/main/TintypeText%20basic%20rtf%20mode%20screenshot.jpg)
<h3 align="center">RadioTTS</h3>
<div align="center">
  
  [![License: AGPL-3.0](https://img.shields.io/badge/License-AGPLv3.0-brightgreen.svg)](https://github.com/LPBeaulieu/TintypeText/blob/main/LICENSE)
  
  
</div>

---

<p align="left"> <b>RadioTTS</b> is a tool enabling you to add Text To Speech (TTS) introductions to your favorite songs using the very lifelike voices of gTTS (Google Text-to-Speech), with multilingual support! You can generate entire playlists with song introductions and also more in-depth song or artist descriptions, all of which are generated using gTTS. What you get out of this are actual mp3 files, each of which are prefixed with a track number that lets you listen to them in sequence, with the option of shuffling your tracks for you!</p>

<p align="left"> A neat functionality of <b>RadioTTS</b> is that your file names are actually the script for your TTS introductions. It is also very easy to add language tags flanking phrases in other languages than your default setting. For example "(fr ca)Nocturne(fr ca) in D-flat major, opus 27 number 2, by (fr ca)Frédéric Chopin(fr ca).mp3", where (fr ca) stands for Canadian French and the passages "Nocturne" and "Frédéric Chopin" would be rendred in French, and the rest in English (or your other default language). Another interesting feature of <b>RadioTTS</b> is that you can personalize how your file names will be introduced, for example: "The next musical piece is:" followed by your file name. Simply add all of your favorite phrases to the "Intros_CSV.csv" file found in the "Intro_CSV" folder of your working folder and the code will automatically randomize the introductions, so that your announcer will be more engaging! 
  
  - You can get my <b>deep learning models</b> for both typewriters on which I developed the code on my Google Drive (<i>2021 
Royal Epoch</i> https://drive.google.com/drive/folders/1DUKqYf7wIkRAobC8fYPjum5gFOJqJurv?usp=sharing and <i>1968 Olivetti Underwood Lettera 33</i> https://drive.google.com/drive/folders/1sykG3zUfr8RJVbk59ClnzHjO3qgkXTmF?usp=sharing), where the datasets and other useful information to build your own datasets may be found. 
- The code showcased in this github page is the one that was used to generate a model with <b>99.93% optical character recognition (OCR) accuracy</b> with the 2021 Royal Epoch typewriter, which is in production and commercially available (I'm not affiliated with them, no worries).
- The generalizability of the model trained on a 2021 Royal Epoch typewriter was assessed on another unit of the same model (2019 Royal Epoch typewriter), with a text over 6,000 characters long. It gave an OCR accuracy of 99.22%, thus demonstrating that deep learning models trained with <b>Tintype¶Text</b> could be used with other typewriters of the same model (albeit with somewhat lower accuracy).
  
    <br> 
</p>

## 📝 Table of Contents
- [Dependencies / Limitations](#limitations)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

## ⛓️ Dependencies / Limitations <a name = "limitations"></a>



## 🏁 Getting Started <a name = "getting_started"></a>



<b>Step 1</b>- Go to the command line in your working folder and install the <b>Atom</b> text editor to make editing the code easier:
```
sudo snap install atom --classic
```

<b>Step 2</b>- Create a virtual environment (called <i>env</i>) in your working folder:
```
python3 -m venv env
```

<b>Step 3</b>- Activate the <i>env</i> virtual environment <b>(you will need to do this step every time you use the Python code files)</b> 
in your working folder:
```
source env/bin/activate
```

<b>Step 7</b>- Install <b>alive-Progress</b> (Python module for a progress bar displayed in command line):
```
pip install alive-progress
```
<b>Step 9</b>- You're now ready to use <b>Tintype¶Text</b>! 🎉

## 🎈 Usage <a name="usage"></a>


        
  <br><b>And that's it!</b> You're now ready to convert your typewritten manuscript into digital format! You can now type away at the cottage or in the park without worrying about your laptop's battery life 
  and still get your document polished up in digital form in the end! 🎉📖
  
  
## ✍️ Authors <a name = "author"></a>
- 👋 Hi, I’m Louis-Philippe!
- 👀 I’m interested in natural language processing (NLP) and anything to do with words, really! 📝
- 🌱 I’m currently reading about deep learning (and reviewing the underlying math involved in coding such applications 🧮😕)
- 📫 How to reach me: By e-mail! LPBeaulieu@gmail.com 💻


## 🎉 Acknowledgments <a name = "acknowledgments"></a>
- Hat tip to [@kylelobo](https://github.com/kylelobo) for the GitHub README template!




<!---
LPBeaulieu/LPBeaulieu is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
