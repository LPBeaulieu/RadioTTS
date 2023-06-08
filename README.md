# RadioTTS
RadioTTS lets you add your commentary to your playlist directly in the file names!

<p align="center">
  <img src="[https://github.com/LPBeaulieu/GIF2Flipbook/blob/main/BettyBoopDemo.gif](https://github.com/LPBeaulieu/RadioTTS/blob/main/RadioTTS%20Demo.mp4)" alt="A demonstration video showcasing the TTS introduction to Beethoven's Moonlight Sonata." />
</p>
<h3 align="center">RadioTTS</h3>
<div align="center">
  
  [![License: AGPL-3.0](https://img.shields.io/badge/License-AGPLv3.0-brightgreen.svg)](https://github.com/LPBeaulieu/RadioTTS/blob/main/LICENSE)
  [![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
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

- The code depends on the Python Google Text-to-Speech (<b>gTTS</b>) and <b>Pydub</b> libraries to generate TTS and handle audio files respectively. The steps needed for their installation on your computer will be covered in the "Getting Started" section.

- You should avoid punctuation marks before or after closing language tags, as otherwise when reverting back to English you might hear "dot" instead of the inflection due to a period, as the TTS would litterally read the punctuation mark. The segments in other languages end with a closing inflection by default, so no punctuation marks are needed.

- You should routinely make a backup of your CSV files and original music tracks, to prevent data losses in the event of the program crashing. This also would facilitate your task should you wish to generate other playlists with additional content, add custom descriptions or simply shuffle your tracks.

- In a lot of cases, should you encounter an error while running the code, it helps to delete the CSV file within the "In" subfolder of the "Music_Files" folder. Once again, be sure to make frequent backups of your CSV files to avoid losing information!

- When opening your CSV files, make sure to only select the equal sign ("=") as a delimiter in-between cells, and to tick the "Detect special numbers in order to properly display the track times in column "D". This will allow you to do summations along the "D" column to figure out how long your playlist is.

- The different song introductions (for example: "The next score is:") are contained in the "Intros_CSV.csv" file found in the "Intro_CSV" folder of your working folder. You can modify this list and add all of your favorite phrases to get personalized introductions.

- Please ensure that the working folder contains the "Music_Files" folder, along with its "In" and "Out" subfolders. You will need to place the music tracks that you wish to add introductions to in the "In" folder, and the generated tracks will be found in the "Out" folder. Your CSV playlist file will be generated in the "In" folder, so that you may easily store the CSV file along with the starting audio files in your backups.  

## 🏁 Getting Started <a name = "getting_started"></a>

The following instructions will be provided in great detail, as they are intended for a broad audience and will allow to run a copy of <b>RadioTTS</b> on a local computer.

The instructions below are for Windows operating systems, but the code runs very nicely on Linux as well.

Start by downloading the zipped working folder, by going to the top of this github repo and clicking on the green "Code" button, and then click on the "Download Zip" option. Extract the zipped folder to your desired location. Next, hold the "Shift" key while right-clicking in your working folder, then select "Open PowerShell window here" to access the PowerShell in your working folder and enter the commands described below.

<b>Step 1</b>- Install <b>gTTS</b>, a Python module allowing for TTS (https://pypi.org/project/gTTS/) by entering the following command in the Powershell in your working folder:
```
py -m pip install gTTS
```

<b>Step 2</b>- Install <b>Pydub</b>, a Python module used to handle the audio files. You will first need to head over to the <b>Pydub</b> repository (https://github.com/jiaaro/pydub) and follow the instructions to install the <b>ffmpeg</b> dependency. Once that is done, enter the following in Powershell to install <b>Pydub</b>
```
py -m pip install pydub
```

<b>Step 3</b>- Install <b>alive-Progress</b> (Python module for a progress bar displayed in command line):
```
py -m pip install alive-progress
```
<b>Step 4</b>- You're now ready to use <b>RadioTTS</b>! 🎼📻🎙

## 🎈 Usage <a name="usage"></a>

After placing the audio files you wish to add TTS introductions to in the "In" subfolder of the "Music_Files" folder, simply run <b>RadioTTS</b> by entering the following command in your working folder's Powershell:
```
py radio_tts.py "intro"
```

- There are a few arguments such as "intro" that may be added to the Python call "py radio_tts.py" when running the code, which will allow you go get specific results. The <b>"intro"</b> parameter allows you to preface each Text to speech (TTS)-rendered file name with phrases such as "The next piece is". 

- Should you wish to build on the TTS-rendered file name by adding some text of your choosing that would further describe the song or the artist, you may pass in the argument <b>"custom"</b> when running the code. A CSV file with equal signs ("=") as a delimiter in-between fields will be generated and the program will exit at that point. You will then amend the CSV file (found within the "In" subfolder of the "Music_Files" folder) with your desired script at selected points in the playlist. To do this, simply paste your track description in the appropriate row of the fifth column ("E" column in LibreOffice Calc), save the file as a CSV and then run the Python code once again without the "custom" argument (which effectively bypasses audio file generation) in order to generate the music files with custom TTS-rendered introductions.

- Should you want to shuffle the items of a playlist, which would be useful if you enjoy listening to mixes and want to ensure that each successive song receives a different introduction, you would then add the <b>"shuffle"</b> argument when running the Python code.

- Should you like to merge the audio files to generate a block of music pieces, each preceded by their TTS-rendered file name, simply pass in <b>"merge:minutes"</b> as an additional argument while running the code, where you would change "minutes" for the maximal number of minutes (as a decimal number, without units) that the block duration will be. For example, 'py radio_tts.py merge_length:25.5' would merge the audio
files until the next file would go over the maximal merged playlist duration of 25 minutes and 30 seconds, before moving on to the generation
of the next merged playlist.

- Should you want to add more music files to an existing CSV file, which you placed within the "In" subfolder of the "Music_Files" folder,
simply pass in the <b>"append"</b> argument when running the code and they will be appended to the end of it.


- The default bit rate of the exported mp3 files is set to 256 kbps. Should you want to bring it down to 128 kbps (or any other value), simply enter the number (without units) after the <b>"bit_rate:"</b> argument when running the code. The code will then select the minimum between the original track bit rate and the default or specified bit rate as the bit rate for the generated audio files, as the new files cannot have higher bit rates than the original ones.

- The default TTS language is set to English (your local variant would automatically be selected), and you can modify this to any other supported language and local language accent by providing these after the <b>"language:"</b> argument, the language and its accent being separated by colons. For example, setting the default language to Canadian French would require you to pass in the following additional argument when running the code: "language: fr:ca", with the language ("fr" for French) preceding the accent ("ca" for Canadian). Note that the language and accent are separated by a colon. Please consult the gTTS documentation for the letter codes for the different languages and accents: https://gtts.readthedocs.io/en/v2.2.1/_modules/gtts/lang.html and https://gtts.readthedocs.io/en/latest/module.html#logging.

- The <b>"pause_after_tts:"</b> and <b>"pause_after_song"</b> arguments define the duration of the silent segment after the TTS-rendered
introduction to the music piece and after the song, respectively. You can modify the default duration of these silent segments (half a second for the pause after the introductions and 1 second for the pause after songs) by passing in the number of seconds (in decimal form and without units) after the <b>"pause_after_tts:"</b> and <b>"pause_after_song:"</b> arguments, respectively, when running the code. For example, 'py radio_tts.py "pause_after_tts:1" "pause_after_song:1.5"' would result in a 1 second pause after the TTS introductions and 1.5 seconds after the songs. Please note that any existing silent segments at the start and end of the songs are trimmed by the code before adding these pauses.

<br><b>And there you have it!</b> You're now ready create your own customized radio show playlist with your favorite music tracks! 🎼📻🎙
  
  
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
