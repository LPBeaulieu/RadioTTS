# RadioTTS
RadioTTS lets you generate audio tracks with TTS introductions, directly from their file names!

https://github.com/LPBeaulieu/RadioTTS/assets/101344807/04ca463f-aa4c-46c5-8875-6bf448c6e870


<h3 align="center">RadioTTS</h3>
<div align="center">
  
  [![License: AGPL-3.0](https://img.shields.io/badge/License-AGPLv3.0-brightgreen.svg)](https://github.com/LPBeaulieu/RadioTTS/blob/main/LICENSE)
  [![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
  [![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
  [![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
 
</div>

---

<p align="left"> <b>RadioTTS</b> is a tool enabling you to add Text To Speech (TTS) introductions to your favorite songs using the very lifelike voices of gTTS (Google Text-to-Speech), with multilingual support! You can generate entire playlists with song introductions and also more in-depth song or artist descriptions, all of which are generated using gTTS. What you get out of this are actual mp3 files, each of which are prefixed with a track number that lets you listen to them in sequence, with the option of shuffling your tracks for you!</p>

<p align="left"> A neat functionality of <b>RadioTTS</b> is that your file names are actually the script for your TTS introductions. It is also very easy to add language tags flanking phrases in other languages than your default setting. For example "(fr ca)Nocturne(fr ca) in D-flat major, opus 27 number 2, by (fr ca)Frédéric Chopin(fr ca).mp3", where (fr ca) stands for Canadian French and the passages "Nocturne" and "Frédéric Chopin" would be rendred in French, and the rest in English (or your other default language). Another interesting feature of <b>RadioTTS</b> is that you can personalize how your file names will be announced, for example: "The next musical piece is:" followed by your file name. The code will randomly select the introductions that are provided in the "Intros_CSV.csv" file, so that your announcer will be even more engaging! 
</p>

## 📝 Table of Contents
- [Dependencies / Limitations](#limitations)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Author](#author)
- [Acknowledgments](#acknowledgments)


## ⛓️ Dependencies / Limitations <a name = "limitations"></a>

- The code depends on the Python Google Text-to-Speech (<b>gTTS</b>) and <b>Pydub</b> libraries to generate TTS and handle audio files, respectively. The steps needed for their installation on your computer will be covered in the "Getting Started" section.

- You should <b>avoid punctuation marks before or after closing language tags</b>, as otherwise when reverting back to English you might hear "dot" instead of the inflection due to a period, as the TTS would litterally read the punctuation mark. The segments in other languages end with a closing inflection by default, so no punctuation marks are needed.

- Make sure to <b>include commas in the file names and additional TTS scripts where you want pauses in the final TTS-rendered text</b>. Should you wish for a pause in-between the song announcement (for example: "The following piece is") and the TTS-rendered file name, simply add a comma at the start of your file name (You would need to generate a new CSV should you modify the file names, as these and the file paths are stored in them). Howerver, should your file name begin with a language tag, there would be no need to precede it by a comma, as two different TTS-rendered files would then be merged, the first of which would end with a closing inflection, as mentioned above (for example: first TTS-rendered segment: "Next is" and second TTS-rendered segment: "(fr ca)Nocturne(fr ca) rest of file name". As the file name starts with a language tag, there is therefore no need to precede it with a comma).

- <b>You should routinely make a backup of your CSV files and original music tracks</b>, to prevent data losses in the event of the program crashing. This also would facilitate your task should you wish to generate other playlists with additional content, add custom descriptions or simply shuffle your tracks.

- In a lot of cases, should you encounter an error while running the code, it helps to delete the CSV file within the "In" subfolder of the "Music_Files" folder. Once again, be sure to make frequent backups of your CSV files to avoid losing information!

- When opening your CSV files, make sure to <b>only select the equal sign ("=") as a delimiter in-between cells, and to tick the "Detect special numbers</b> in order to properly display the track times in column "D". This will allow you to do summations along the "D" column to figure out how long your playlist is. The image bellow illustrates this.
<p align="center">
  <img src="https://github.com/LPBeaulieu/RadioTTS/blob/main/Detect%20special%20numbers.png" alt="Instructions on how to open the CSV file" /><hr> <b>Figure 1.</b> Make sure to only select the equal sign ("=") as a delimiter in-between cells and to tick the "Detect special numbers" option.
</p><br>

- The columns of the CSV files contain the following information: Column "A" displays the file name. Column "B" shows the complete path to the audio file. Column "C" indicates the track number. As mentioned above, column "D" shows the track duration (in hh:mm:ss.ms format), provided that you didn't select the "merge" option described further on in the "Usage" section. Should you want to generate further song or artist TTS descriptions, you would paste the additional TTS script in the Column "E" of the row corresponding to the music piece. This is illustrated in the screenshot below. 
<p align="center">
 <img src="https://github.com/LPBeaulieu/RadioTTS/blob/main/CSV%20file%20and%20In%20and%20Out%20folders.png" alt="Description of the different fields of the CSV file."/><hr><b>Figure 2.</b> Description of the different fields of the CSV file.
</p><br>

- The different song introductions (for example: "The next score is:") are contained in the "Intros_CSV.csv" file found in the "Intro_CSV" folder of your working folder. You can modify this list and add all of your favorite phrases to get personalized introductions.

- Please ensure that the working folder contains the "Music_Files" folder, along with its "In" and "Out" subfolders. You will need to place the music tracks that you wish to add introductions to in the "In" folder, and the generated tracks will be found in the "Out" folder. Your CSV playlist file will be generated in the "In" folder, so that you may easily store the CSV file along with the starting audio files in your backups.
  

## 🏁 Getting Started <a name = "getting_started"></a>

The following instructions will be provided in great detail, as they are intended for a broad audience and will allow to run a copy of <b>RadioTTS</b> on a local computer.

The instructions below are for Windows operating systems, but it runs nicely on Linux as well.

Start by downloading the zipped working folder, by going to the top of this github repo and clicking on the green "Code" button, and then click on the "Download Zip" option. Extract the zipped folder to your desired location. Next, hold the "Shift" key while right-clicking in your working folder, then select "Open PowerShell window here" to access the PowerShell in your working folder and enter the commands described below.

<b>Step 1</b>- Install <b>gTTS</b>, a Python module allowing for TTS (https://pypi.org/project/gTTS/) by entering the following command in the Powershell in your working folder:
```
py -m pip install gTTS
```

<b>Step 2</b>- Install <b>ffmpeg</b>, a dependency of the <b>Pydub</b> Python module used to handle the audio files. One way to do this is to copy the contents of the bin folder (from the extracted folder downloaded according to the steps 1-6 of the instructions in the following link: https://www.wikihow.com/Install-FFmpeg-on-Windows) to your working folder. The other way would be to head over to the <b>Pydub</b> repository (https://github.com/jiaaro/pydub) and follow the steps in the "Getting ffmpeg set up" section of the Readme page.

<b>Step 3</b>- Install <b>Pydub</b>, a Python module used to handle the audio files:
```
py -m pip install pydub
```

<b>Step 4</b>- Install <b>alive-Progress</b> (Python module for a progress bar displayed in command line):
```
py -m pip install alive-progress
```

<b>Step 5</b>- You're now ready to use <b>RadioTTS</b>! 🎼📻🎙


## 🎈 Usage <a name="usage"></a>

After placing the audio files that you wish to add TTS introductions to in the "In" subfolder of the "Music_Files" folder, simply run <b>RadioTTS</b> by entering the following command in your working folder's Powershell:
```
py radio_tts.py "intro"
```

- There are a few arguments such as "intro" that may be added to the Python call "py radio_tts.py" when running the code, which will allow you go get specific results. The <b>"intro"</b> parameter allows you to preface each Text to speech (TTS)-rendered file name with phrases such as "The next piece is". You can pass in any number of these arguments when running the code, but please remember to <b> place the arguments within quotes and include a space in-between each argument</b> (for example: py radio_tts.py "intro" "shuffle").

- Should you wish to build on the TTS-rendered file name by adding some text of your choosing that would further describe the song or the artist, you may pass in the argument <b>"custom"</b> when running the code. A CSV file with equal signs ("=") as a delimiter in-between fields will be generated and the program will exit at that point. You will then amend the CSV file (found within the "In" subfolder of the "Music_Files" folder) with your desired script at selected points in the playlist. To do this, simply paste your track description in the appropriate row of the fifth column ("E" column in LibreOffice Calc), save the file as a CSV and then run the Python code once again without the "custom" argument (which effectively bypasses audio file generation) in order to generate the music files with custom TTS-rendered introductions.

- Should you want to shuffle the items of a playlist, which would be useful if you enjoy listening to mixes and want to ensure that each successive song receives a different announcing phrase, you would then add the <b>"shuffle"</b> argument when running the Python code.

- Should you like to merge the audio files to generate a block of music pieces, each preceded by their TTS-rendered file name, simply pass in <b>"merge:minutes"</b> as an additional argument while running the code, where you would change "minutes" for the maximal number of minutes (as a decimal number, without units) that the block duration will be. For example, 'py radio_tts.py merge_length:25.5' would merge the audio
files until the next file would go over the maximal merged playlist duration of 25 minutes and 30 seconds, before moving on to the generation
of the next merged playlist.

- Should you want to add more music files to an existing CSV file, which you placed within the "In" subfolder of the "Music_Files" folder,
simply pass in the <b>"append"</b> argument when running the code and they will be appended to the end of it.

- Should you wish to normalize the volume of your tracks, you could then pass in the <b>"normalization:target dBFS"</b> argument when running the code, with "target dBFS" being your target decibels relative to full scale (or dBFS for short). The default target dBFS is set to -20 dB and will change to any number you provide after the colon. The code will then perform average amplitude normalization according to the difference between the target dBFS and that of the audio track being normalized. This difference will then be used to apply gain correction to the audiosegment.

- The default bit rate of the exported mp3 files is set to 256 kbps. Should you want to bring it down to 128 kbps (or any other value), simply enter the number (without units) after the <b>"bit_rate:"</b> argument when running the code. The code will then select the minimum between the original track bit rate and the default or specified bit rate as the bit rate for the generated audio files, as the new files cannot have higher bit rates than the original ones.

- The default TTS language is set to English (your local variant would automatically be selected), and you can modify this to any other supported language and local language accent by providing these after the <b>"language:"</b> argument, the language and its accent being separated by colons. For example, setting the default language to Canadian French would require you to pass in the following additional argument when running the code: "language: fr:ca", with the language ("fr" for French) preceding the accent ("ca" for Canadian). Note that the language and accent are separated by a colon. Please consult the gTTS documentation for the letter codes for the different languages and accents: https://gtts.readthedocs.io/en/v2.2.1/_modules/gtts/lang.html and https://gtts.readthedocs.io/en/latest/module.html#logging.

- The <b>"pause_after_tts:"</b> and <b>"pause_after_song"</b> arguments define the duration of the silent segment after the TTS-rendered
introduction to the music piece and after the song, respectively. You can modify the default duration of these silent segments (half a second for the pause after the introductions and 1 second for the pause after songs) by passing in the number of seconds (in decimal form and without units) after the <b>"pause_after_tts:"</b> and <b>"pause_after_song:"</b> arguments, respectively, when running the code. For example, 'py radio_tts.py "pause_after_tts:1" "pause_after_song:1.5"' would result in a 1 second pause after the TTS introductions and 1.5 seconds after the songs. Please note that any existing silent segments at the start and end of the songs are trimmed by the code before adding these pauses.

-The default audio file format of the generated audio files is ".mp3" because of its prevalence. However, should you like to export your files in another format supported by ffmpeg, (such as ".m4a" or ".wav" files), simply enter the letters and numbers comprising the extension of your chosen audio file type, excluding the period, after the <b>"file_format:"</b> argument when running the Python code. For example, py radio_tts "intro" "file_format:m4a" would generate ".m4a" audio files.

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
