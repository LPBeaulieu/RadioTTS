# RadioTTS
RadioTTS lets you add your commentary to your playlist directly in the file names!

![Image RTF basic mode](https://github.com/LPBeaulieu/Typewriter-OCR-TintypeText/blob/main/TintypeText%20basic%20rtf%20mode%20screenshot.jpg)
<h3 align="center">RadioTTS</h3>
<div align="center">
  
  [![License: AGPL-3.0](https://img.shields.io/badge/License-AGPLv3.0-brightgreen.svg)](https://github.com/LPBeaulieu/TintypeText/blob/main/LICENSE)
  
  
</div>

---

<p align="left"> <b>RadioTTS</b> is a tool enabling you to add Text To Speech (TTS) introductions to your favorite songs using the very lifelike voices of gTTS (Google Text-to-Speech), with multilingual support! You can generate entire playlists with song introductions and also more in-depth song or artist descriptions, all of which are generated using gTTS. What you get out of this are actual mp3 files, each of which are prefixed with a track number that lets you listen to them in sequence, with the option of shuffling your tracks for you!</p>

<p align="left"> A neat functionality of <b>RadioTTS</b> is that your file names are actually the script for your TTS introductions. It is also very easy to add language tags flanking phrases in other languages than your default setting. For example "(fr ca)Nocturne(fr ca) in D-flat major, opus 27 number 2, by (fr ca)Frédéric Chopin(fr ca).mp3", where (fr ca) stands for Canadian French and the passages "Nocturne" and "Frédéric Chopin" would be rendred in French, and the rest in English (or your other default language). Another interesting feature of <b>RadioTTS</b> is that you can personalize how your file names will be introduced, for example: "The next musical piece is:" followed by your file name. The code will randomly select the introductions that are provided in the "Intros_CSV.csv" file, so that your announcer will be even more engaging! 
  
    <br> 
</p>

## 📝 Table of Contents
- [Dependencies / Limitations](#limitations)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

## ⛓️ Dependencies / Limitations <a name = "limitations"></a>

The code depends on the Python Google Text-to-Speech (gTTS) and Pydub libraries to generate TTS and handle audio files respectively. The steps needed for their installation on your computer will be covered in the "Getting Started" section.

- You should avoid punctuation marks before or after closing language tags, as otherwise when reverting back to English you might hear "dot" instead of the inflection due to a period, as the TTS would litterally read the punctuation mark. The segments in other languages end with a closing inflection by default, so no punctuation marks are needed.

- You should routinely make a backup of your CSV files and original music tracks, to prevent data losses in the event of the program crashing. This also would facilitate your task should you wish to generate other playlists with additional content, add custom descriptions or simply shuffle your tracks.

- In a lot of cases, should you encounter an error while running the code, it helps to delete the CSV file within the "In" subfolder of the "Music_Files" folder. Once again, be sure to make frequent backups of your CSV files to avoid losing information!

- When opening your CSV files, make sure to only select the equal sign ("=") as a delimiter in-between cells, and to tick the "Detect special numbers in order to properly display the track times in column "D". This will allow you to do summations along the "D" column to figure out how long your playlist is.

- The different song introductions (for example: "The next score is:") are contained in the "Intros_CSV.csv" file found in the "Intro_CSV" folder of your working folder. You can modify this list and add all of your favorite phrases to get personalized introductions.

- Please ensure that the working folder contains the "Music_Files" folder, along with its "In" and "Out" subfolders. You will need to place the music tracks that you wish to add introductions to in the "In" folder, and the generated tracks will be found in the "Out" folder. Your CSV playlist file will be generated in the "In" folder, so that you may easily store the CSV file along with the starting audio files in your backups.  

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
