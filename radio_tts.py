from alive_progress import alive_bar
import csv
from midi2audio import FluidSynth
import glob
from gtts import gTTS
import math
import os
from os import path
from pydub import AudioSegment
import pydub.scipy_effects
from pydub.silence import detect_leading_silence
from pydub.utils import mediainfo
import random
import re
import shutil
import sys


#Should you like to preface each Text to speech (TTS)-rendered
#file name with phrases such as "The next piece is", you
#would pass in the "intro" argument when running the code,
#and the "intro" variable would then be set to "True".
intro = False

#Should you wish to build on the TTS-rendered file
#name by adding some text of your choosing that would further
#describe the song or the artist, you may pass in the argument
#"custom" when running the code.
#A CSV file with equal signs ("=") as a delimiter in-between
#fields will be generated and the program will exit at that
#point. You will then amend the CSV file (found within the "In"
#subfolder of the "Music_Files" folder) with your desired script
#at selected points in the playlist. To do this, simply paste
#your track description in the appropriate row of the fifth
#column ("E" column in LibreOffice Calc), save the file as a CSV
#and then run the Python code once again without the "custom"
#argument (which effectively bypasses audio file generation)
#in order to generate the music files with custom TTS-rendered
#introductions.
custom = False

#Should you want to shuffle the items of a playlist, which would
#be useful if you enjoy listening to mixes and want to ensure that
#each successive song receives a different introduction, you would
#then add the "shuffle" argument when running the Python code
shuffle = False

#Should you like to merge the audio files to generate a block of
#music pieces, each preceded by their TTS-rendered file name, simply
#pass in "merge:minutes" as an additional argument while running the
#code, where you would change "minutes" for the maximal number of minutes
#(as a decimal number, without units) that the block duration will be.
#For example, 'py radio_tts.py merge_length:25.5' would merge the audio
#files until the next file would go over the maximal merged playlist
#duration of 25 minutes and 30 seconds, before moving on to the generation
#of the next merged playlist.
merge_length = None
#The counter "merged_audio_duration" will keep track of the current duration
#(in milliseconds) of the merged audio block.
merged_audio_duration = 0
#The counter "playlist_number" will be added to the merged playlist file name,
#and then incremented for the next merged file.
playlist_number = 1
#The list "merged_tracks_indices" will keep track of the music piece indices
#that were included in each merged file, and the boundaries will be included
#in the file name, such that you could refer to the CSV file to find out
#which tunes are included in a given merged file.
merged_tracks_indices = []

#Should you want to add more music files to an existing CSV file,
#which you placed within the "In" subfolder of the "Music_Files" folder,
#simply pass in the "append" argument when running the code and they will
#be appended to the end of it.
append = False
write_vs_append = "w"

#The default audio file format of the generated audio files is ".mp3" because
#of its prevalence. However, should you like to export your files in another
#format supported by ffmpeg, (such as ".m4a" or ".wav" files), simply enter
#the letters and numbers comprising the extension of your chosen audio file
#type, excluding the period, after the "file_format:" argument when running
#the Python code. For example, py radio_tts "intro" "file_format:m4a" would
#generate ".m4a" audio files.
file_format = "mp3"
output_file_extension = ".mp3"

#Should you want to normalize the volume of your tracks, you could then pass
#in the "normalization:target dBFS" argument when running the code, with "target dBFS"
#being your target decibels relative to full scale (or dBFS for short). The default
#target dBFS is set to -20 dB and will change to any number you provide after the colon.
#The code will then perform average amplitude normalization according to the difference
#between the target dBFS and that of the audio track being normalized. This difference
#will then be used to apply gain correction to the audiosegment.
target_dBFS = None

#The default bit rate is set to 256 kbps. Should you want to bring
#it down to 128 kbps (or any other value), simply enter the number
#(without units) after the "bit_rate:" argument when running the code.
#The code will then select the minimum between the original track bit rate
#and the default or specified bit rate as the bit rate for the generated
#audio files, as the new files cannot have higher bit rates than the
#original ones.
target_bit_rate = 256

#The default language is set to English (your local variant would automatically
#be selected), and you can modify this to any other supported language and
#local language accent by providing these after the "language:" argument,
#the language and its accent being separated by colons. For example, setting
#the default language to Canadian French would require you to pass in the
#following additional argument when running the code: "language:fr:ca",
#with the language ("fr" for French) preceding the accent ("ca" for Canadian).
#Note that the language and accent are separated by a colon. Please consult
#the gTTS documentation for the letter codes for the different languages
#and accents: https://gtts.readthedocs.io/en/v2.2.1/_modules/gtts/lang.html
#and https://gtts.readthedocs.io/en/latest/module.html#logging.
language = "en"
accent = None

#The "pause_after_tts" and "pause_after_song" variables define
#the duration of the silent segment after the TTS-rendered
#introduction to the music piece and after the song, respectively.
#You can modify the default duration of these silent segments
#(half a second for the pause after the introductions and 1 second
#for the pause after songs) by passing in the number of seconds
#(in decimal form and without units) after the "pause_after_tts:"
#and "pause_after_song:" arguments, respectively, when running the
#code. For example, 'py radio_tts.py "pause_after_tts:1" "pause_after_song:1.5"'
#would result in a 1 second pause after the TTS introductions and 1.5 seconds
#after the songs. Please note that any existing silent segments at the
#start and end of the songs are trimmed by the code before adding these
#pauses.
pause_after_song = AudioSegment.silent(duration=1000)
pause_after_tts = AudioSegment.silent(duration=500)

#The "len_previous_csv" variable (initialized at 0) is
#overwritten with the number of entries of a previous
#CSV file, should the "append" option be selected. This
#Allows to update the "index_string" variable to account
#for the fact that the tracks will be appended after the
#existing ones in the CSV file, and therefore their indices
#will start at the one following the last index of the CSV.
len_previous_csv = 0

#The variable "csv_file_path" will store the name of
#the working CSV file, while "old_csv_file_path" will
#contain the name of the original CSV file, to minimize
#data loss problems in the event that the program would
#crash (see explanations below).
csv_file_path = None
old_csv_file_path = None

if len(sys.argv) > 1:
    #The "try/except" statement will
    #intercept any "ValueErrors" and
    #ask the users to correctly enter
    #the desired values for the variables
    #directly after the colon separating
    #the variable name from the value.
    try:
        for i in range(1, len(sys.argv)):
            if sys.argv[i][:5].strip().lower() == "intro":
                intro = True
            elif sys.argv[i][:6].strip().lower() == "custom":
                custom = True
            elif sys.argv[i][:7].strip().lower() == "shuffle":
                shuffle = True
            elif sys.argv[i][:6].strip().lower() == "merge:":
                merge_length = math.floor(float(sys.argv[i][6:].strip())*60000)
            elif sys.argv[i][:6].strip().lower() == "append":
                append = True
                write_vs_append = "a"
            elif sys.argv[i][:12].strip().lower() == "file_format:":
                file_format = sys.argv[i][12:].strip().lower()
                if file_format in ["aac", "m4a"]:
                    file_format = "mp4"
                    output_file_extension = ".m4a"
                else:
                    output_file_extension = "." + sys.argv[i][12:].strip()
            elif sys.argv[i][:9].strip().lower() == "normalize":
                normalize_split = [element for element in sys.argv[i].strip().split(":") if element != ""]
                if len(normalize_split) > 1:
                    target_dBFS = int(normalize_split[1].strip())
                else:
                    target_dBFS = -20
            elif sys.argv[i][:9].strip().lower() == "bit_rate:":
                target_bit_rate = int(sys.argv[i][9:].strip())
            elif sys.argv[i][:9].strip().lower() == "language:":
                language_accent = sys.argv[i][9:].strip().lower().split(":")
                language = language_accent[0].strip()
                if len(language_accent) > 1 and language_accent[1] != "":
                    accent = language_accent[1].strip()
            elif sys.argv[i][:17].strip().lower() == "pause_after_song:":
                pause_after_song = AudioSegment.silent(duration= math.floor(float(sys.argv[i][17:].strip())*1000))
            elif sys.argv[i][:16].strip().lower() == "pause_after_tts:":
                pause_after_tts = AudioSegment.silent(duration= math.floor(float(sys.argv[i][16:].strip())*1000))

    except Exception as e:
        print(e)
        sys.exit('\nPlease pass in each argument within quotes and separated by a space. ' +
        'Furthermore, when passing in durations (in seconds) of the silent segment after the TTS-rendered ' +
        'introduction to a music piece ("pause_after_tts:") and after a song ("pause_after_song:"), ' +
        'or the maximal duration of merged files (in minutes), make sure to pass in the numbers ' +
        '(in decimal form and without units) after the colon of these arguments.' +
        '\nFor instance, (py radio_tts.py "shuffle" "intro" "pause_after_song:1.5" "pause_after_tts:1" ' +
        'merge:25.5) would indicate that there should be a 1.5 second pause after songs and ' +
        '1 second silence after the TTS introductions, and that the merged files should have a ' +
        'maximal duration of 25 minutes and 30 seconds.')

#The song files (all files not having a ".csv" extension within the "In" subfolder
#of the "Music_Files" folder) are stored within the "song_files" list. The CSV
#files within the same folder are stored in the "csv_file_paths" list.
cwd = os.getcwd()
song_files = glob.glob(os.path.join(cwd, "Music_Files", "In", "*.*"))
song_files = [file for file in song_files if file.split(".")[-1].lower() != "csv"]
if song_files == []:
    sys.exit('\nPlease include at least one audio file within the "In" subfolder of your working folder.')
else:
    song_files.sort()
csv_file_paths = glob.glob(os.path.join(cwd, "Music_Files", "In", "*.csv"))

#Should there be exactly two CSV files within the "In" subfolder of the "Music_Files" folder,
#and should these share the same file name, except that one of them has the "(delete this if
#the program has crashed)" suffix, it  most likely means that the program has crashed during
#its previous run. The file with a suffix is created as a safeguard in these cases, to avoid
#losing the data from the original CSV file. The original CSV file is only overwritten with the
#contents of the working file ending with the "(delete this if the program has crashed)" at the
#very last step of the code, if everything else has run smoothly.
if (len(csv_file_paths) == 2 and
(" (delete this if the program has crashed).csv" in csv_file_paths[0] and
csv_file_paths[0][:(delete_index := (csv_file_paths[0].find(" (delete this if the program has crashed).csv")))] ==
csv_file_paths[1][:delete_index] or
" (delete this if the program has crashed).csv" in csv_file_paths[1] and
csv_file_paths[1][:(delete_index := (csv_file_paths[1].find(" (delete this if the program has crashed).csv")))] ==
csv_file_paths[0][:delete_index])):
    #The following "for" loop cycles through both CSV files and deletes the
    #one having the "(delete this if the program has crashed)" suffix, as it
    #is most likely incomplete, as a result of the program crashing. The original
    #file without the suffix is then used to generate another working file
    #(with the suffix), of which the path is stored in the "csv_file_path" variable.
    #The path of the original file is itself stored in the "old_csv_file_path" variable.
    for i in range(2):
        if " (delete this if the program has crashed).csv" in csv_file_paths[i]:
            os.remove(csv_file_paths[i])
            if i == 0:
                old_csv_file_path = csv_file_paths[1]
                csv_file_path = csv_file_paths[1][:-4] + " (delete this if the program has crashed).csv"
                shutil.copy(csv_file_paths[1], csv_file_path)
            else:
                old_csv_file_path = csv_file_paths[0]
                csv_file_path = csv_file_paths[0][:-4] + " (delete this if the program has crashed).csv"
                shutil.copy(csv_file_paths[0], csv_file_path)
            break

#Should there otherwise be more than one CSV file in the "In" subfolder of the
#"Music_Files" folder, an error message will be displayed so that you might only
#include one CSV file within this folder.
elif len(csv_file_paths) > 1:
    sys.exit('\nPlease include only one CSV file containing the list of ' +
    'file names within the "Music_Files" folder. To make things clear, ' +
    'another CSV file should be located in the "Intros_CSV" folder, comprising ' +
    'a list of phrases (such as "The next piece is") that would preface ' +
    'each TTS-rendered file name.')
#If there is exactly one CSV file within the "In" subfolder of the "Music_files"
#folder, then its path will be stored in the "old_csv_file_path" variable and
#a working copy of the file will be generated with the "(delete this if the
#program has crashed)" suffix, of which the path will be stored in the
#"csv_file_path" variable.
elif len(csv_file_paths) == 1:
    old_csv_file_path = csv_file_paths[0]
    csv_file_path = csv_file_paths[0][:-4] + " (delete this if the program has crashed).csv"
    shutil.copy(csv_file_paths[0], csv_file_path)

#Should there be no CSV files within the "In" subfolder of the
#"Music_Files" folder, then the "csv_file_path" variable's value
#would still be "None". A new CSV file would then be created,
#named "songTitle_path_number.csv", where the underscores delimit
#the different columns of the CSV file. The first column
#(column "A" in LibreOffice Calc) would consist of the song
#title, column "B" comprises the file path, column "C" contains
#the track number and column "D" indicates the duration of the audio
#files. Should you want to add more detailed TTS descriptions
#to your musical tracks that would be included after the TTS
#segment containing the track name, you would paste the
#text in column "E" of the corresponding song's row.
if csv_file_path == None:
    csv_file_path = os.path.join(cwd, 'Music_Files', 'In', 'songTitle_path_index_time_comment.csv')
    with open(csv_file_path, write_vs_append, newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='=')
        for i in range(len(song_files)):
            #The "tts_text" variable stores the string of the song name
            #(which corresponds to its file name, after the removal of the
            #extension and the path root). The '.replace("\\", "/")' method
            #is used to ensure Windows compatibility.
            tts_text = "".join(song_files[i].split(".")[:-1]).replace("\\", "/").split("/")[-1]
            csv_writer.writerow([tts_text, song_files[i]])

#The CSV file (that was either just created above if
#there wasn't initially a CSV file within the "In"
#subfolder of the "Music_Files" folder, or if there
#was one and the user wants to either shuffle the tracks,
#and/or append new ones) is opened and the "song_list" list
#is populated with all the rows of the CSV file.
with open(csv_file_path, newline="") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='=')
    song_list = [row for row in csv_reader if row != []]
if append == True:
    #The "len_previous_csv" variable (initialized at 0) is
    #overwritten with the number of entries of a previous
    #CSV file, should the "append" option be selected. This
    #Allows to update the "index_string" variable to account
    #for the fact that the tracks will be appended after the
    #existing ones in the CSV file, and therefore their indices
    #will start at the one following the last index of the CSV.
    len_previous_csv = len(song_list)
    #If the "append" option has been selected, then the songs
    #to be added to the list won't necessarily be those already
    #present on the original CSV. Therefore, the songs found within
    #the "Music_Files" folder will be added to a reinitialized
    #"song_list". The "write_vs_append" variable will be equal
    #to "a" should the "append" option be selected. Otherwise,
    #it will be equal to "w" (which overwrites the file instead
    #of adding to it).
    song_list = []
    with open(csv_file_path, write_vs_append, newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='=')
        for i in range(len(song_files)):
            tts_text = "".join(song_files[i].split(".")[:-1]).replace("\\", "/").split("/")[-1]
            song_list.append([tts_text, song_files[i]])

len_song_list = len(song_list)

with alive_bar(len_song_list) as bar:
    #Should you have selected to include introductions to the TTS-generated
    #file names, such as "The next song is", then the "intro" variable would
    #be set to "True". A list of intros "list_intros" is then populated
    #with all the different options that you have included in the CSV file
    #within the "Intros_CSV folder".
    if intro == True:
        intro_csv_files = glob.glob(os.path.join(cwd, "Intros_CSV", "*.csv"))
        if intro_csv_files == [] or len(intro_csv_files) > 1:
            sys.exit('Please include one CSV file in the "Intros_CSV" folder, '+
            'listing the introductory phrases to the music pieces, such as "The next piece is".')
        else:
            with open(intro_csv_files[0], newline="") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='=')
                list_intros = [row for row in csv_reader]

            #The list "random_intro_indices" is populated with random numbers within
            #the range of the length of number of different introductions within the
            #"list_intros" list. Should your number of songs exceed the different number
            #of introductions in "list_intros", some random introduction indices are
            #sampled without replacement until all introduction indices are allocated,
            #and then a fresh randomized introduction index range is generated in the
            #while loop. The while loop repeats until the number of random indices within
            #"random_intro_indices" is equal to the number of songs in "song_list".
            #The expression "k=min(len_song_list-len(random_intro_indices), len(list_intros)"
            #means that the number of random indices sampled will be the minimum between
            #the total available introduction indices within "list_intros" and the remaining
            #indices to be added to "random_intro_indices" in order to match the length
            #of "song_list".
            random_intro_indices = []
            while len(random_intro_indices) < len_song_list:
                random_intro_indices += random.sample(range(len(list_intros)), k=min(len_song_list-len(random_intro_indices), len(list_intros)))
            #The following "for" loop ensures that successive elements within
            #"random_intro_indices" are not the same. When matching successive
            #random indices are found, the last of these is changed for another
            #sampled random element, provided that itself does not match the previous
            #or next one in "random_intro_indices".
            for i in range(1, len(random_intro_indices)):
                if random_intro_indices[i] == random_intro_indices[i-1]:
                    new_random_index = random.sample(range(len(list_intros)), k=1)[0]
                    while (new_random_index == random_intro_indices[i-1] or
                    i < len(list_intros)-1 and new_random_index == random_intro_indices[i+1]):
                        new_random_index = random.sample(range(len(list_intros)), k=1)[0]
                    random_intro_indices[i] = new_random_index

    #Should the "append" option not be selected and the CSV file contain
    #a different number of rows than the number of songs in the "In"
    #subfolder of the "Music_Files" folder, or if there are the same number
    #of tracks in both locations but some files were renamed ("missing_files
    #!= set()") then a warning will be printed.
    missing_files = set()
    problem = False
    for i in range(len_song_list):
        if not os.path.exists(song_list[i][1]):
            missing_files.add(song_list[i][0])

        if problem == False:
            if len_song_list > len(song_files) and append == False:
                print('\n\nNote: There are more track entries in your CSV file (number of rows) ' +
                'than the number of music pieces included in the "In" subfolder of ' +
                'the "Music_Files" folder. If you intended to add more files to an existing ' +
                'CSV file, you would then need to pass in the "append" argument when running the code. ' +
                '\n\nOtherwise, the same audio tracks are present in the "In" folder and the CSV file')
                problem = True
            elif len_song_list == len(song_files) and missing_files != set():
                print('\n\nWarning: The file paths in the CSV file differ from those of the music pieces included ' +
                'in the "In" subfolder of the "Music_Files" folder. Should you have modified the audio file ' +
                'names, you would need to either update those changes in the CSV file or delete the CSV file ' +
                'run the code again to obtain an updated CSV file.')
                problem = True
            if len_song_list < len(song_files) and append == False:
                print('\n\nNote: There are less track entries in your CSV file (number of rows) ' +
                'than the number of music pieces included in the "In" subfolder of ' +
                'the "Music_Files" folder.')
                problem = True
                if append == False:
                    print('If you intended to add more files to an existing ' +
                    'CSV file, you would then need to pass in the "append" argument when running the code. ' +
                    '\n\nOtherwise, please delete the CSV file (be sure to make a backup if you added some ' +
                    'additional TTS script in column "E") and run the code again')
        #Should the "missing_files" set not equal an empty set, then it means
        #that there were some files in the CSV that aren't found within the "In"
        #folder. The code will then print those and exit if the "append" option
        #wasn't selected. In other words, if the "append" section is selected,
        #the "song_list" items are taken directly form the audio files found
        #within the "In" folder and not from the previous CSV file, so no such
        #issues would be observed.
        if missing_files != set():
            print('The following files present in the "B" column of the CSV file are not found ' +
            'within the "In" folder:')
            for missing_file in missing_files:
                print("\n- " + missing_file)
            sys.exit()

    #The list "song_list" is shuffled if
    #the "shuffle" argument was passed in
    #when running the code.
    if shuffle == True:
        random.shuffle(song_list)

    with open(csv_file_path, write_vs_append, newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='=')
        #The "index_list" list will keep track of the track indices
        #("index_string"), such that merged files could have their
        #first and last track index displayed in the file name for
        #easy reference to the tracks in the CSV file.
        index_list = []
        for i in range(len_song_list):
            #The "len_previous_csv" variable (initialized at 0) is
            #overwritten with the number of entries of a previous
            #CSV file, should the "append" option be selected. This
            #Allows to update the "index_string" variable to account
            #for the fact that the tracks will be appended after the
            #existing ones in the CSV file, and therefore their indices
            #will start at the one following the last index of the CSV.
            index_string = str(len_previous_csv + i + 1)
            index_list.append(index_string)
            #If there was no CSV file within the "In" subfolder of the
            #"Music_Files" folder, then the CSV files only consisted of
            #two columns, the file name in column "A" and complete path
            #in column "B". In such cases, the track index would need to
            #be appended to the "song_list" list derived from the CSV contents.
            #Otherwise, if a CSV file was already in the "In" folder, then
            #the value of the third element of "song_list" will be updated
            #by indexing song_list at song index "i" and then at index 2.
            #In all cases, the "index_string" will be padded with zeros
            #to its left up to a maximum of four digits overall.
            if len(song_list[i]) > 2:
                song_list[i][2] = (4-len(index_string))*"0" + index_string
            else:
                song_list[i].append((4-len(index_string))*"0" + index_string)

        #If the "shuffle" option was selected,
        #the "song_list" will be sorted according
        #to the integer value of "index_string",
        #to ensure that the track indexes of the
        #shuffled songs are in ascending order.
        if shuffle == True:
            song_list.sort(key=lambda x: int(x[2]))

        #The function "audio_parameters()" extracts the parenthesized values of the SoundFont
        #number and "target_dBFS" from the end of the SoundFont files (".sf2") and audio files.
        #This will allow to pair up MIDI files with their respective SoundFont files, and to
        #override any default or user selected values of "target_dBFS" that would otherwise
        #apply to all audio files. Any "target_dBFS" values found at the end of SoundFont files
        #will apply to all the MIDI files of matching SoundFont number. For example, the target
        #dBFS of -25 dB from the SountFont file named "Piano(1 -25).sf2" would apply to all of
        #the midi files of the following format: "MIDI_file_name(1).mid". Furthermore, you can
        #further fine-tune the normalization process by specifying a target dBFS for a given
        #audio file, by including it within parentheses at the end of the file name. For instance,
        #the MIDI file with the following file name "MIDI_file_name(-28 1).mid" would have a
        #target dBFS of -28 dB, in spite of the "Piano(1 -25).sf2" file which would still apply the
        #-25 dB target dBFS to the other MIDI files of the same SoundFont number (1). For other
        #audio file types than midi, just add the target dBFS within parentheses at the end of
        #the file name (ex: "mp3_file_name(-27).mp3") and the default -20 dB or any other value
        #that you passed in with the "normalize:" argument would still apply to the other audio
        #files that do not end with such a parenthesized expression.
        def audio_parameters(file_name):
            dBFStarget_soundfont_matches_split = None
            #The r"[(](-\d+[ \d+]*|[\d+ ]*-\d+|\d+)[)]\Z" pattern will look for the presence of
            #a parenthesized expression at the end ("\Z") of "file name" that either contains
            #a negative integer ("-\d+") by itself or preceded or followed by a positive integer
            #("\d+") with one space in-between the two instances. For example: the file name
            #extracted from a MIDI file "Harpsichord Sonata in D, catalog K 141, by (it)Domenico
            #Scarlatti(it)(-20 3)" would return "[-20, 3]", with "-20" being the new value of the
            #target dBFS ("target_dBFS"), and "3" being the SoundFont file number included in
            #the working folder. Another match that the "finditer" function can return is a
            #single positive integer by itself ("\d+"), to indicate the SoundFont file number,
            #with the "target_dBFS" being the default one or the one specified after the
            #"normalize:" argument.
            dBFStarget_soundfont_hits = re.finditer(r"[(](-\d+[ \d+]*|[\d+ ]*-\d+|\d+)[)]\Z", file_name)
            #The strip() method will remove spaces after the opening parenthesis and before
            #the closing parenthesis. For example: ( 2 -30 ) will return (2 -30)
            #(without the parentheses). The contents of the parentheses will then be split
            #along spaces to separate the SoundFont number from the target dBFS and then
            #each resulting string will be converted into integers using a map() method.
            dBFStarget_soundfont_matches =[m.group(1).strip().split(" ") for m in dBFStarget_soundfont_hits if m.group(1)]
            dBFStarget_soundfont_matches = [list(map(int, element)) for element in dBFStarget_soundfont_matches]
            if dBFStarget_soundfont_matches:
                #As the "list(map())" method introduced a new layer of lists, it is
                #now removed by indexing the first element of "dBFStarget_soundfont_matches".
                dBFStarget_soundfont_matches = dBFStarget_soundfont_matches[0]
            return dBFStarget_soundfont_matches

        #The file extensions for all audio files in the "song_list" list are gathered in the list
        #"file_extensions". This will allow to determine whether or not an audio file is a MIDI
        #file, which must be rendered using a SoundFont, in an extra step when compared to other
        #audio files.
        file_extensions = [song_list[i][1].split(".")[-1].lower() for i in range(len(song_list))]
        #The list "list_soundfonts_dBFStarget" will contain the SoundFont number and target dBFS values
        #extracted from the parenthesized expression at the end of the SoundFont (".sf2") file names.
        list_soundfonts_dBFStarget = []
        #Should there be at least one MIDI in the "In" subfolder of the "Music_Files" folder,
        #then the code will search for SoundFont files (".sf2"), which are required to render
        #the MIDI files. The SF2 file names will be submitted to the "audio_parameters()" function
        #in order to extract the SoundFont number and target dBFS, if present within parentheses
        #at the end of the file name.
        if "mid" in file_extensions:
            path_sf2 = os.path.join(cwd, "*.sf2")
            sf2_files = glob.glob(path_sf2)
            if sf2_files == []:
                sys.exit('\n\nPlease include at least one SoundFont (".sf2") file within your working folder.')
            else:
                len_sf2_files = len(sf2_files)
                for i in range(len_sf2_files):
                    sf2_file_name = "".join(sf2_files[i].split(".")[:-1]).replace("\\", "/").split("/")[-1]
                    dBFStarget_soundfont_file = audio_parameters(sf2_file_name)
                    if dBFStarget_soundfont_file:
                        #The elements of the list "dBFStarget_soundfont_file" are sorted in reverse order,
                        #in order to have the positive SoundFont number first, followed by the negative
                        #target dBFS.
                        list_soundfonts_dBFStarget.append(sorted(dBFStarget_soundfont_file, reverse = True))

                #If "list_soundfonts_dBFStarget = []" this means that none of the "sf2" files in the working folder
                #have parenthesized SoundFont numbers nor target dBFS values. This is only acceptable if there is
                #only one "sf2" file within the working folder, as all of the MIDIs could be rendered from that file.
                #If "list_soundfonts_dBFStarget != []" and each item of the list "sf2_files" has returned a positive
                #number corresponding to the SoundFont number (or if there was only one file in "sf2_files"), then the
                #corresponding "sf2" file path is concatenated to each element of "list_soundfonts_dBFStarget" before
                #sorting it along the first element, corresponding to the SountFont number if "len_sf2_files" is
                #greater than one.
                if list_soundfonts_dBFStarget == [] and len_sf2_files == 1:
                    list_soundfonts_dBFStarget = [sf2_files[0]]
                elif (list_soundfonts_dBFStarget != [] and len(list_soundfonts_dBFStarget) == len_sf2_files and
                (len_sf2_files == 1 or (len_sf2_files > 1 and all([element[0] > 0 for element in list_soundfonts_dBFStarget])))):
                    list_soundfonts_dBFStarget = [list_soundfonts_dBFStarget[i] + [sf2_files[i]] for i in range(len_sf2_files)]
                    list_soundfonts_dBFStarget.sort(key = lambda x:x[0])
                else:
                    sys.exit('\n\nPlease add the SoundFont file number in parentheses at the end of the SoundFont file name. ' +
                    'This will allow the code to match the SoundFont number of the MIDI files to that of the SoundFont file.' +
                    'For example: "midi_file(1).mid" would be rendered using the SoundFont file "piano_soundfont(1).sf2".' +
                    'Should you also want to specify a target dBFS for a given SoundFont file that will be applied to all ' +
                    'MIDI files of the matching SoundFont number, enter the negative decibel value (without units) in the same ' +
                    'parenthesis, separated by a space from the SoundFont number. For example: "midi_file(1).mid" would be rendered ' +
                    'using the SoundFont file "piano_soundfont(1 -30).sf2", with a target dBFS of -30 dB. Furthermore, should you ' +
                    'like to specify a target dBFS that would apply to a single MIDI file, simply enter it along with the SoundFont ' +
                    'number within parentheses at the end of the MIDI file name. For instance, the target dBFS of -35 dB would be ' +
                    'used to render the MIDI file with the following name "other_midi_file(-35 1).mid", and the -30 dB target dBSF of ' +
                    'the "piano_soundfont(1 -30).sf2" would then only apply to "midi_file(1).mid".')

        for i in range(len_song_list):
            #The variable "TTS_text_file_name", initialized to "None",
            #for every new song in "song_list", will contain the contents
            #of "song_list[i][0]", excluding any parenthesized expression
            #at the end of the file name containing the "soundfont_number"
            #and "target_dBFS".
            TTS_text_file_name = None
            #The variable "old_target_dBFS", initialized to "None" for
            #every new song in "song_list", will store the initial
            #value of "target_dBFS" before giving precedence to any
            #values of "target_dBFS" found in the SoundFont (".sf2")
            #or audio file names. Upon rendering the song, the value
            #of "target_dBFS" will be reverted back to that of "old_target_dBFS",
            #in order to preserve the general settings defined when passing
            #in the "normalize:" argument or the default value of "target_dBFS"
            #of -20 dB.
            old_target_dBFS = None
            #The variable "soundfont_number", initialized to "None" for
            #every new song in "song_list", will contain the parenthesized
            #sound font number found at the end of the SoundFont (".sf2") and
            #corresponding MIDI (".mid") files. Its value will be updated to that
            #of the SoundFont file found in the working folder, should there only
            #be one "sf2" file in that location.
            soundfont_number = None
            #An "Intro" folder (with the mention in its name that it should be deleted
            #should the program have crashed before it is automatically deleted) is
            #created in the working folder. This folder will contain the mp3 files of
            #the TTS generated introductions and file names, and will be deleted once
            #the TTS files have been merged with the songs. To my knowledge, the gTTS
            #output files must be in mp3 format.
            intro_path = os.path.join(cwd, "Intro (delete this if the program has crashed)")
            if not os.path.exists(intro_path):
                os.makedirs(intro_path)
            #An "Audiosegment" object is instantiated from the song path in the "try" statement.
            #The original bit rate would then be stored within the variable "original_bitrate",
            #and the minimum between this and the default bit rate or the one specified
            #by the user will be selected as the bit rate for exporting the audio files, as
            #the output bit rate cannot exceed the original bit rate.
            #Also, should you have provided a value for "target_dBFS" and/or SoundFont number
            #(for MIDI files specifically) for a specific song within parentheses at the end
            #of the file name, this information would be extracted at this point, and the
            #file name would be updated to remove such parenthesized expressions, so that
            #they wouldn't appear in the final file names nor in the TTS-rendered text.
            try:
                dBFStarget_soundfont = audio_parameters(song_list[i][0])
                if dBFStarget_soundfont or len(list_soundfonts_dBFStarget) == 1:
                    #Removing the parenthesized expressions at the end of the file names, of
                    #which the contents were returned by the "audio_parameters()" function.
                    TTS_text_file_name = song_list[i][0].replace("(" + " ".join(map(str, dBFStarget_soundfont)) + ")", "")
                    #Cycling through every element of the list "dBFStarget_soundfont", returned
                    #by the "audio_parameters()" function. If the current audio file is a MIDI
                    #file and the value of the element is positive, it is stored in "soundfont_number",
                    #as any other values returned by the function would be negative and correspond
                    #to the updated value of "target_dBFS" for this audio track.
                    for j in range(len(dBFStarget_soundfont)):
                        if dBFStarget_soundfont[j] >= 0 and file_extensions[i] == "mid":
                            soundfont_number = dBFStarget_soundfont[j]
                        elif dBFStarget_soundfont[j] < 0:
                            old_target_dBFS = target_dBFS
                            target_dBFS = dBFStarget_soundfont[j]
                    #Should the audio track be a MIDI file and the "soundfont_number"
                    #not be addigned, given that the MIDI file did not end in a parenthesized
                    #positive number (ex: "midi_file_name(-25).mid"), and since there has to
                    #be at least one SoundFont file in the working folder a this point (because
                    #otherwise the above code would have run ("sys.exit('\n\nPlease include at
                    #least one SoundFont (".sf2") file within your working folder.')"), it can
                    #be deduced that the MIDI files correspond to the first (or only) element
                    #of list_soundfonts_dBFStarget. Should you have placed multiple SoundFont
                    #files within the working folder containing a parenthesized positive
                    #"soundfont_number" value at the end of their names, the code would still
                    #select the first of these, and you would need to ensure that the proper
                    #SoundFont was selected. Otherwise, you would need to add the SoundFont
                    #information at the end of your MIDI file name (ex: "midi_file_name(1 -25).mid").
                    if file_extensions[i] == "mid" and soundfont_number == None:
                        for j in range(len(list_soundfonts_dBFStarget[0])):
                            if isinstance(list_soundfonts_dBFStarget[0][j], int)  and  list_soundfonts_dBFStarget[0][j] >= 0:
                                soundfont_number = list_soundfonts_dBFStarget[0][j]
                                break
                #The following "if" statement will extract the parenthesized "soundfont_number"
                #and "target_dBFS" values found at the end of the SoundFont "sf2" file names that
                #were returned by the "dBFStarget_soundfont_file = audio_parameters(sf2_file_name)"
                #code above and then stored within the "list_soundfonts_dBFStarget" list, along
                #with the corresponding path of the "sf2" files.
                #A "FluidSynth" object is instantiated from the "sf2" file path at index 2 of
                #an element of "list_soundfonts_dBFStarget" of which the "soundfont_number"
                #matches that of the MIDI file being rendered at index "i" of the "for i in
                #range(len_song_list)" loop. As a reminder, the individual elements of
                #"list_soundfonts_dBFStarget" contain in sequence the "soundfont_number",
                #"target_dBFS" and "sf2" file path for a given SoundFont, with the possibility
                #of only containing one, or the other, or none of "soundfont_number" and "target_dBFS"
                #(the latter case being if the "sf2" didn't contain any parenthesized information,
                #ex: "Piano.sf2").
                if file_extensions[i] == "mid":
                    fs = None
                    for j in range(len(list_soundfonts_dBFStarget)):
                        #Should the element of "list_soundfonts_dBFStarget" under
                        #investigation have a length of three or more, it means that
                        #it contains in sequence values of "soundfont_number", "target_dBFS"
                        #and the "sf2" file path for that SoundFont file. Provided that
                        #the "sf2" "soundfont_number" matches that of the MIDI file, these
                        #values are then stored in the corresponding variables, with
                        #"target_dBFS" only being updated if its value is "None", meaning
                        #that the MIDI file didn't contain a parenthesized "target_dBFS"
                        #value that would otherwise take precedence over any "target_dBFS"
                        #specified in the "sf2" file name.
                        if len(list_soundfonts_dBFStarget[j]) > 2:
                            if soundfont_number == list_soundfonts_dBFStarget[j][0]:
                                fs = FluidSynth(list_soundfonts_dBFStarget[j][2])
                                if old_target_dBFS == None:
                                    old_target_dBFS = target_dBFS
                                    target_dBFS = list_soundfonts_dBFStarget[j][1]
                                break
                        #Should the current element of "list_soundfonts_dBFStarget"
                        #under investigation have a length of two, it means that it
                        #contains either "soundfont_number" (a positive integer) or
                        #"target_dBFS" (a negative integer), followed by the path of
                        #the "sf2" file. The "if" and "elif" statements deal with
                        #these possibilities, with the "soundfont_number" being checked
                        #first in case a matching "soundfont_number" to that of the
                        #current MIDI file can be found.
                        elif len(list_soundfonts_dBFStarget[j]) == 2:
                            if (list_soundfonts_dBFStarget[j][0] >= 0 and
                            soundfont_number == list_soundfonts_dBFStarget[j][0]):
                                fs = FluidSynth(list_soundfonts_dBFStarget[j][1])
                                break
                            #The "elif" statement only applies should there only be
                            #one SoundFont file within the working folder and the
                            #parenthesized value at the end of the "sf2" file name
                            #is negative, meaning that it designates the value of
                            #"target_dBFS" for that SoundFont file. Once again,
                            #the value of "target_dBFS" is only updated if that
                            #of "old_target_dBFS" be "None", in order to give
                            #precedence to the "target_dBFS" found in the MIDI
                            #file name, as mentioned above.
                            elif (len_sf2_files == 1 and
                            list_soundfonts_dBFStarget[j][0] < 0):
                                 fs = FluidSynth(list_soundfonts_dBFStarget[j][1])
                                 if old_target_dBFS == None:
                                     old_target_dBFS = target_dBFS
                                     target_dBFS = list_soundfonts_dBFStarget[j][0]
                    #As there is at least one SoundFont file within the working
                    #folder at this point in the code, should a "FluidSynth" object
                    #not yet have been instantiated, it is instantiated now using the
                    #first (or only) "sf2" file in the "sf2_files" list. This will
                    #ensure that the MIDI songs are rendered and that you will be able
                    #to check if the correct "sf2" was selected. This would give reliable
                    #results should only one "sf2" file be in the working folder and
                    #should all of the MIDI files require be rendered using that
                    #SoundFont file. In this case, you wouldn't need to provide parenthesized
                    #values of "soundfont_number" at the end of the SoundFont (".sf2") and
                    #MIDI (".mid") file names. In all other cases, you should include this
                    #information in the SoundFont and MIDI file names.
                    if not fs:
                        fs = FluidSynth(sf2_files[0])

                    #The MIDI files are rendered as WAV files using the "fs" FluidSynth objects
                    #instantiated above using the paths of the selected SoundFont file. The
                    #WAV files are then used to instantiate an AudioSegment object for the
                    #audio files.
                    fs.midi_to_audio(song_list[i][1], os.path.join(intro_path, 'midi2wav.wav'))
                    song_audiosegment = AudioSegment.from_wav(os.path.join(intro_path, "midi2wav.wav"))
                    bit_rate = str(target_bit_rate) + "k"
                #If the file extension wasn't ".mid", it is used to instantiate an Audiosegment
                #object for the audio files, using the file extension at index "i" of the
                #"file_extensions" list. As mentioned above, the minimum between the original
                #bitrate and that specified in the "target_bit_rate" variable is stored in the
                #"bit_rate" variable, as the bit rate of the outputted audio track cannot exceed
                #that of the original track.
                else:
                    song_audiosegment = AudioSegment.from_file(song_list[i][1], format=file_extensions[i])
                    original_bitrate = int(mediainfo(song_list[i][1])['bit_rate'])
                    if math.ceil(original_bitrate)/1000 < target_bit_rate:
                        bit_rate = str(math.ceil(original_bitrate/1000)) + "k"
                    else:
                        bit_rate = str(target_bit_rate) + "k"

                #If the "normalization" option was selected, the code will perform
                #average amplitude normalization according to the difference between the
                #target decibels relative to full scale (dBFS, "target_dBFS") and
                #the dBFS determined for the audiosegment. This difference ("delts_dBFS")
                #is then used to apply gain correction to the audiosegment.
                if target_dBFS:
                    delta_dBFS = target_dBFS - song_audiosegment.dBFS
                    song_audiosegment = song_audiosegment.apply_gain(delta_dBFS)
                    if old_target_dBFS and old_target_dBFS != target_dBFS:
                        target_dBFS = old_target_dBFS

                #Credit goes to MiChen00 for the solution proposed to trim the leading and trailing silences
                #of the music pieces (https://stackoverflow.com/questions/29547218/remove-silence-at-the-
                #beginning-and-at-the-end-of-wave-files-with-pydub)
                trim_leading_silence = lambda song_audiosegment: song_audiosegment[detect_leading_silence(song_audiosegment) :]
                trim_trailing_silence = lambda song_audiosegment: trim_leading_silence(song_audiosegment.reverse()).reverse()
                strip_silence = lambda song_audiosegment: trim_trailing_silence(trim_leading_silence(song_audiosegment))
            except Exception as e:
                sys.exit('\n\nThere was a problem when running the code: \n' + str(e))

            #The variable "TTS_text_file_name", initialized to "None",
            #for every new song in "song_list", will contain the contents
            #of "song_list[i][0]", excluding any parenthesized expression
            #at the end of the file name containing the "soundfont_number"
            #and "target_dBFS". If there was no such parenthesized expression
            #at the end of "song_list[i][0]", then the value of "TTS_text_file_name"
            #will be set to that of the original file "song_list[i][0]".
            if not TTS_text_file_name:
                TTS_text_file_name = song_list[i][0]

            #The usual "song_list" elements are comprised of four elements: the file name (index 0),
            #the complete path (index 1), the track number (index 2) and the duration of the generated
            #audio file (index 3, which is only added at the very end of the code and is bypassed should
            #the "custom option be selected"). Should a CSV containing a more detailed TTS script in
            #the column "E" of the CSV file have been included in the "In" subfolder of the "Music_Files"
            #folder, then the resulting "song_list" derived this CSV file would have an additional
            #non-empty string at index 4 for the songs having text in column "E". The other songs
            #without more detailed TTS script would contain an empty string at index 4 of "song_list".
            #For the latter songs, the value of "tts_text" would then be their file name, stored at
            #index 0 of their corresponding "i" element of "song_list".

            #The elements of "song_list" with a longer length (len(song_list[i]) > 4) are
            #analyzed before those with a shorter length, to avoid false positives. If the
            #CSV file contains columns "A", "B", "C", "D" and "E" (at least) and that the
            #contents of column "E" ("song_list[i][4]") are an empty string and the contents
            #of column "D" ("song_list[i][3]") is either an empty string or numeric once that
            #the colons and periods have been removed, it means that the user hasn't provided
            #an additional song description in either columns "D" nor "E", and so the value of
            #"tts_text" is assigned as the file name ("TTS_text_file_name").
            if (len(song_list[i]) > 4 and song_list[i][4] == "" and
            (song_list[i][3] == "" or (str(song_list[i][3]).replace(":", "").replace(".", "")).isnumeric())):
                tts_text = TTS_text_file_name

            #Once again, the elements of "song_list" with a longer length (len(song_list[i]) > 4)
            #are analyzed before those with a shorter length, to avoid false positives.
            #The songs with additional TTS scripts in the column "E" of the CSV
            #file would then have the value of "tts_text" be the concatenation of
            #the file name at index 0 of their corresponding "i" element of "song_list",
            #a spacer, and then the more detailed TTS string found at index 4.
            elif len(song_list[i]) > 4 and song_list[i][4] != "":
                #If the music piece ends with a closing parenthesis
                #(likely from a closing language tag), the TTS rendition
                #will already have a closing inflection at the end of the
                #introduction ("TTS_text_file_name"). Also, a period must not
                #be the very first character (preceded or not by spaces) in
                #a new language TTS script, as it would be read "dot".
                if TTS_text_file_name[-1] == ")":
                    tts_text = TTS_text_file_name + " " + song_list[i][4]
                else:
                    tts_text = TTS_text_file_name + ". " + song_list[i][4]

            #The two following "elif" statements are similar to the "if" and "elif"
            #statements above.
            elif (len(song_list[i]) < 4 or len(song_list[i]) > 3 and
            (song_list[i][3] == "" or (str(song_list[i][3]).replace(":", "").replace(".", "")).isnumeric())):
                tts_text = TTS_text_file_name

            #The difference between this "elif" statement and the first "elif" statement
            #('elif len(song_list[i]) > 4 and song_list[i][4] != "":') is that it deals
            #with users mistakenly adding the additional song descriptions in the "D"
            #column instead of the "E" column. This is most likely to happen after
            #generating a CSV with the "merge" option selected, where the audio file
            #creation is bypassed, and therefore the column "D" of the CSV doesn't
            #contain the audio file durations. However, deduces that the content of
            #"song_list[i][3]" is the descriptions, provided that it is not an empty
            #string (like the first "elif") or a numeric string once the colons and
            #periods have been removed.
            elif (len(song_list[i]) > 3 and song_list[i][3] != "" and
            not (str(song_list[i][3]).replace(":", "").replace(".", "")).isnumeric()):
                if TTS_text_file_name[-1] == ")":
                    tts_text = TTS_text_file_name + " " + song_list[i][3]
                else:
                    tts_text = TTS_text_file_name + ". " + song_list[i][3]

            #The variable "file_name_for_export" stores the name of the
            #final individual audio tracks that will be exported in the
            #"Out" subfolder of the "Music_Files" folder. The name consists
            #of the zero-padded track number (stored in index 2 of the
            #corresponding element "i" of the list "song_list"), followed
            #by a hyphen and the name of the file TTS_text_file_name. Should
            #the resulting name exceed 250 characters, it is truncated to
            #250 chars.
            file_name_for_export = song_list[i][2] + "-" + TTS_text_file_name
            if len(file_name_for_export) > 250:
                file_name_for_export = file_name_for_export[:251]

            #When you pass in the "custom" argument when running the code,
            #the actual audio file generation is bypassed in order to
            #gain access to the CSV file more quickly. You would then need
            #to add your more detailed song descriptions in the column "E" of
            #the CSV file, and include the saved file in the "In" subfolder of
            #the "Music_Files" subfolder and run the Python code again, this time
            #without the "custom" argument, to allow for audio file generation.
            if custom == True:
                #Now that an "Audiosegment" object has successfully been
                #instantiated for the song at index "i" of "song_list",
                #the contents of "song_list" at index "i" are written to
                #the CSV file for later reference.
                csv_writer.writerow(song_list[i])
            else:
                #The "find_language_tags()" function will allow to locate the
                #language tags (ex: "(fr ca)Frédéric Chopin(fr ca)" for Canadian French)
                #flanking a subsection of the TTS script in a different language. The
                #TTS voice will then be selected according to these tags, for better
                #pronounciation of the text, albeit with a different voice. The default
                #subtext_accent (such as "ca" above for Canadian French) is set to "None",
                #as every language has a default setting based on your geographical location.
                #The "start_index" counter is initialized to zero and will effectively "walk"
                #along the TTS script in order to detect all of the language tags.
                subtext_accent = None
                start_index = 0
                def find_language_tags(matches_subtext_language, start_index):
                    start_index_closing = 0
                    end_index_opening = 0
                    #The "re.finditer" pattern r"(([(][^)]{2,}[)]).+\2*)" corresponds
                    #to two matching parenthesized expressions containing at least two
                    #characters not equal to a closing parenthesis. The two parenthesized
                    #expressions would be separated by one or more characters of any type (".+").
                    #"\2*" corresponds to the group 2, so the first of the matching parenthesized
                    #expressions (for example "(fr ca)" in "(fr ca)Frédéric Chopin(fr ca)"), which
                    #is also represented as "lang.group(2)" in the rather expansive list comprehension
                    #below. You just need to read the local variable assignments (:=) to get a sense of
                    #the slicing of "tts_text" in the middle element of each generated list, which
                    #corresponds to the text in-between the two parenthesized expressions (so "Frédéric
                    #Chopin" in "(fr ca)Frédéric Chopin(fr ca)". The last element of the lists
                    #("start_index_closing + len(lang.group(2)") stores the index following the
                    #closing parenthesis of the second language tag (so the location designated
                    #by the asterisk in "(fr ca)Frédéric Chopin(fr ca)*") Probably due to an
                    #unspecific regex pattern, some other unmatched parenthesized expressions
                    #were also captured by the "re.finditer" method. To ensure that these are
                    #not included in the list comprehension, the following condition was added:
                    #"tts_text[start_index:].count(lang.group(2)) > 1", thus ensuring that each
                    #parenthesized expression included in the list comprehension has at least one
                    #matching parenthesized expression in the remainder of the TTS string.
                    subtext_language = re.finditer(r"(([(][^)]{2,}[)]).+\2*)", tts_text[start_index:])
                    new_matches_subtext_language = [[lang.group(2),  tts_text[(end_index_opening := start_index + lang.end(2)):
                    (start_index_closing := end_index_opening + tts_text[end_index_opening:].find(lang.group(2)))],
                    start_index_closing + len(lang.group(2))] for lang in subtext_language if tts_text[start_index:].count(lang.group(2)) > 1]
                    #If the list comprehension hasn't yielded an empty list,
                    #its results are concatenated with the previous hits stored
                    #in the list "matches_subtext_language", and the "start_index"
                    #is updated to the position right after the closing parenthesis
                    #of the closing language tag in the hit ("matches_subtext_language[-1][2]").
                    if new_matches_subtext_language != []:
                        matches_subtext_language += new_matches_subtext_language
                        start_index = matches_subtext_language[-1][2]
                    return matches_subtext_language, start_index

                #The list "matches_subtext_language_before" stores the list of
                #language tag hits before further recursions of the "find_language_tags()"
                #function. This will allow to break out of the "while" loop if no further
                #matchign language tags were found in the remainder of the TTS string
                #("matches_subtext_language_before == matches_subtext_language and
                #start_index_before == start_index").
                matches_subtext_language_before = []
                matches_subtext_language = []
                while start_index < len(tts_text):
                    matches_subtext_language_before = matches_subtext_language
                    start_index_before = start_index
                    matches_subtext_language, start_index = find_language_tags(matches_subtext_language, start_index)

                    if matches_subtext_language_before == matches_subtext_language and start_index_before == start_index:
                        break

                #If matching language tags have been located in the TTS string, the string will be
                #split along these into individual strings to remove the tags, leaving behind the text
                #that will be found in the "file_name_for_export". Each segment will be stored within
                #the "text_split_list" list. The "start_index" will walk along the file name string
                #("TTS_text_file_name"). The remainder of the string after the last closing language tag is
                #added to the end of "text_split_list" after the "for" loop is done by slicing "tts_text"
                #starting from the index after the last closing parenthesis of the last closing language tag,
                #up to the end of "tts_text" ("tts_text[matches_subtext_language[-1][2]:]").
                if matches_subtext_language != []:
                    text_split_list = []
                    start_index = 0
                    for j in range(len(matches_subtext_language)):
                        text_split_list += tts_text[start_index:matches_subtext_language[j][2]].split(matches_subtext_language[j][0])
                        start_index = matches_subtext_language[j][2]
                    text_split_list += [tts_text[matches_subtext_language[-1][2]:]]
                    #The empty strings left over from the split methods are filtered out.
                    text_split_list = [element for element in text_split_list if element != ""]
                    #The value of "file_name_for_export" is then assembled by concatenating
                    #the zero-padded track number ("song_list[i][2]"), a hyphen and the joined
                    #text upon removing the language tags ('".join(text_split_list)').
                    file_name_for_export = song_list[i][2] + "-" + "".join(text_split_list)
                    #Once again, should the number of characters of "file_name_for_export"
                    #exceed 250, it will be sliced to the first 250 characters.
                    if len(file_name_for_export) > 250:
                        file_name_for_export = file_name_for_export[:251]

                    #The following nested "for" loops will generate TTS segments
                    #for each of the different language portions of the list
                    #"text_split_list". The nested loop is required, as the list
                    #"matches_subtext_language" only contains matching language
                    #tags and the text enclosed in them, while the list "text_split_list"
                    #contains all of text segments after splitting along the language
                    #tags. This will allow to locate which segments need to be rendrered
                    #in the default language and accent.
                    for j in range(len(text_split_list)):
                        for k in range(len(matches_subtext_language)):
                            #The following list comprehension will provide the
                            #language and accent (if applicable) for the language
                            #tag at index "k" in the "matches_subtext_language" list.
                            #The index zero of the element k corresponds to the first of
                            #the matching language tags (for example "(fr ca)" in
                            #"(fr ca)Frédéric Chopin(fr ca)"). The parentheses are then
                            #sliced out ("[1:-1]") and the remaining language tag is split
                            #along spaces and filtered to remove empty strings. This would
                            #give ["fr", "ca"] in the above example.
                            language_accent_split = [element for element
                            in matches_subtext_language[k][0][1:-1].split(" ") if element != ""]
                            subtext_language = language_accent_split[0].strip().lower()
                            #If the length of "language_accent_split" is greater than one,
                            #it means that there is an accent in addition to a language.
                            if len(language_accent_split) > 1:
                                subtext_accent = language_accent_split[1].strip().lower()

                            #Recall that the index 1 of the elements of the list
                            #"matches_subtext_language" ("matches_subtext_language[k][1]")
                            #contains the text that is flanked by two matching language tags
                            #in the original string with the language tags.
                            #If "text_split_list[0].strip() != matches_subtext_language[0][1].strip()",
                            #then it means that the file name does not begin with a language tag, and
                            #so the introduction string (such as "The next song is") can be merged
                            #with the first segment "text_split_list[0]", with a " " spacer.
                            #This will ensure that there are minimal individual TTS Audiosegments to
                            #be concatenated together, making for a smoother TTS output.
                            if intro == True and j == 0 and k == 0 and text_split_list[j].strip() != matches_subtext_language[k][1].strip():
                                random_intro = list_intros[random_intro_indices.pop(0)][0]
                                text_split_list[j] = random_intro + " " + text_split_list[j].replace(" ,", ",")
                                #Should there be on or more spaces before a comma, these will be removed.
                                text_split_list[j] = re.sub(r'[" "]+,', r",", text_split_list[j])
                                #If a space wasn't included after a comma, it will be introduced.
                                text_split_list[j] = re.sub(r'(,(\S))', r", \2", text_split_list[j])
                            #If the text flanked by two matching language tags corresponds to
                            #the current segment under investigation ("text_split_list[j]"),
                            #then the TTS file is generated with the extracted "subtext_language"
                            #and "subtext_accent" (if present). Once a match is found, the
                            #"for k in range(len(matches_subtext_language)):" is broken.
                            if text_split_list[j] == matches_subtext_language[k][1]:
                                if subtext_accent:
                                    tts = gTTS(text_split_list[j], lang=subtext_language, tld=subtext_accent)
                                else:
                                    tts = gTTS(text_split_list[j], lang=subtext_language)
                                tts.save(os.path.join(intro_path, str(j) + ".mp3"))
                                break
                            #Upon reaching the last of the language tags, if no matching
                            #text segments in "text_split_list[j]" and "matches_subtext_language[k][1]"
                            #is found, it means that this segment is to be generated using the default
                            #language and accent (if applicable).
                            elif k == len(matches_subtext_language)-1:
                                if accent:
                                    tts = gTTS(text_split_list[j], lang=language, tld=accent)
                                else:
                                    tts = gTTS(text_split_list[j], lang=language)
                                tts.save(os.path.join(intro_path, str(j) + ".mp3"))

                    #The following "for" loop concatenates the TTS mp3 files generated
                    #in the above nested "for" loops.
                    for j in range(len(text_split_list)):
                        #The concatenated Audiosegment "track_audio" will begin with
                        #the TTS-rendered introduction phrase (such as "The next song is:"),
                        #provided that "intro" option has been selected and that the file
                        #name begins with a language tag. In this case the following is True,
                        #"text_split_list[0].strip() == matches_subtext_language[0][1].strip()".
                        #The Audiosegments of the subsequent mp3 files for each element of
                        #"text_split_list" that were generated above will then be added in
                        #sequence to "track_audio".
                        if j == 0:
                            if intro == True and text_split_list[0].strip() == matches_subtext_language[0][1].strip():
                                random_intro = list_intros[random_intro_indices.pop(0)][0] + " "
                                if accent:
                                    tts = gTTS(random_intro, lang=language, tld=accent)
                                else:
                                    tts = gTTS(random_intro, lang=language)
                                tts.save(os.path.join(intro_path, 'Intro.mp3'))
                                track_audio = (AudioSegment.from_mp3(os.path.join(intro_path, 'Intro.mp3')) +
                                AudioSegment.from_mp3(os.path.join(intro_path, str(j) + ".mp3")))
                            #If the "intro" option wasn't selected, or if it was selected and the file name
                            #didn't start with a language tag (see the "if intro == True and j == 0 and k == 0 and
                            #text_split_list[j].strip() != matches_subtext_language[k][1].strip():" statement above)
                            #then the concatenated audio TTS file will start at the first TTS-rendered element of
                            #"text_split_list".
                            else:
                                track_audio = AudioSegment.from_mp3(os.path.join(intro_path, str(j) + ".mp3"))
                        #The Audiosegments of the subsequent mp3 files for each element of
                        #"text_split_list" that were generated above will then be added in
                        #sequence to "track_audio".
                        else:
                            track_audio += AudioSegment.from_mp3(os.path.join(intro_path, str(j) + ".mp3"))
                    #The pauses after the TTS segment and after the song are added before and after the
                    #"song_audiosegment", respectively.
                    track_audio += pause_after_tts + song_audiosegment + pause_after_song
                    #The duration of the individual track is stored
                    #in the "track_duration" variable.
                    track_duration = len(track_audio)
                    #Once the final concatenated individual audiosegment comprising the
                    #introduction (if applicable), song name and song itself along with
                    #the silences has been assembled, it will be exported to an audio file
                    #if the "merge" mode hasn't been selected.
                    if merge_length == None:
                        track_audio.export(os.path.join(cwd, 'Music_Files', 'Out', file_name_for_export + output_file_extension), format=file_format, bitrate=bit_rate)
                    #If the "merge" mode has been selected, the audiosegments will instead
                    #be concatenated until the addition of the next audiosegment would result
                    #in a merged file with a duration exceeding the specified period, or until
                    #the end of the song list is reached.
                    else:
                        #The first audiosegment to be merged will go through the "if" statement below.
                        #The list "merged_tracks_indices" will keep track of the track numbers that
                        #constitute a merged file. #The duration of the individual track is stored
                        #in the "track_duration" variable, while that of
                        #the merged track is stored in "merged_audio_duration".
                        if merged_audio_duration == 0:
                            merged_audio = track_audio
                            merged_audio_duration = track_duration
                            merged_tracks_indices = [index_list[i]]
                        #The subsequent audiosegments will enter this "else" statement.
                        else:
                            #If there is still room in the merged file for another song,
                            #then it will be added at the end of the merged audiosegment.
                            #The values of "merged_audio_duration" will be updated to reflect
                            #the added duration of the appended audiosegment.
                            #The track index is added to "merged_tracks_indices".
                            if track_duration + merged_audio_duration < merge_length:
                                merged_audio += track_audio
                                merged_audio_duration += track_duration
                                merged_tracks_indices.append(index_list[i])
                            #If there isn't enough room for the next track in the merged audiosegment,
                            #then it will be exported as an audio file, with the name "Playlist ", followed
                            #by the "playlist_number" and the first and last track indices of the merged
                            #audiosegment. This will allow for easy reference to the CSV to find out which
                            #tracks are included in a merged playlist.
                            else:
                                #If there is more than one track in the merged audiosegment,
                                #the first and last track numbers will be included in the name.
                                if len(merged_tracks_indices) > 1:
                                    track_numbers = (" (tracks number " + str(merged_tracks_indices[0]) +
                                    "-" + str(merged_tracks_indices[-1]) + ")")
                                #If only one audiosegment fits within the "merge_length", then it
                                #will be the sole track in this playlist. Consequently, only its
                                #track number will be provided.
                                else:
                                    track_numbers = " (track number " + str(merged_tracks_indices[0]) + ")"
                                merged_audio.export(os.path.join(cwd, 'Music_Files', 'Out', "Playlist " +
                                str(playlist_number) + track_numbers + output_file_extension), format=file_format, bitrate=bit_rate)
                                #The "playlist_number" counter is incremented.
                                playlist_number+=1
                                #The "merged_audio" is reset to the song that couldn't fit into
                                #the playlist that was just exported as a audio file. The "merged_audio_duration"
                                #and "merged_tracks_indices" are also updated to reflect the start
                                #of a new playlist.
                                merged_audio = track_audio
                                merged_audio_duration = track_duration
                                merged_tracks_indices = [index_list[i]]
                                merged_tracks_indices.append(index_list[i])
                                #If the song to be merged is the last one, it will
                                #be the sole track of the last playlist.
                                if i == len_song_list-1:
                                    merged_audio.export(os.path.join(cwd, 'Music_Files', 'Out', "Playlist " +
                                    str(playlist_number) + " (track number " + index_list[i] + ")" + output_file_extension), format=file_format, bitrate=bit_rate)

                #If no matching language tags were found in the TTS script,
                #A very similar approach to that of the "if" statement is
                #taken, except that as no splitting of the TTS script takes place,
                #the "random_intro" string can be merged to the string of the
                #file name ("TTS_text_file_name"), with a spacer (" ") in-between.
                else:
                    if intro == True:
                        random_intro = list_intros[random_intro_indices.pop(0)][0] + " "
                        if accent:
                            tts = gTTS(random_intro + " " + TTS_text_file_name, lang=language, tld=accent)
                        else:
                            tts = gTTS(random_intro + " " + TTS_text_file_name, lang=language)

                        tts.save(os.path.join(intro_path, 'Intro.mp3'))
                    else:
                        if accent:
                            tts = gTTS(TTS_text_file_name, lang=language, tld=accent)
                        else:
                            tts = gTTS(TTS_text_file_name, lang=language)
                        tts.save(os.path.join(intro_path, 'Intro.mp3'))
                    track_audio = AudioSegment.from_mp3(os.path.join(intro_path, 'Intro.mp3'))
                    track_audio += pause_after_tts + song_audiosegment + pause_after_song
                    track_duration = len(track_audio)
                    if merge_length == None:
                        track_audio.export(os.path.join(cwd, 'Music_Files', 'Out', file_name_for_export + output_file_extension), format=file_format, bitrate=bit_rate)
                    else:
                        if merged_audio_duration == 0:
                            merged_audio = track_audio
                            merged_audio_duration = track_duration
                            merged_tracks_indices = [index_list[i]]
                        else:
                            if track_duration + merged_audio_duration < merge_length:
                                merged_audio += track_audio
                                merged_audio_duration += track_duration
                                merged_tracks_indices.append(index_list[i])
                            else:
                                if len(merged_tracks_indices) > 1:
                                    track_numbers = (" (tracks number " + str(merged_tracks_indices[0]) +
                                    "-" + str(merged_tracks_indices[-1]) + ")")
                                else:
                                    track_numbers = " (track number " + str(merged_tracks_indices[0]) + ")"
                                merged_audio.export(os.path.join(cwd, 'Music_Files', 'Out', "Playlist " +
                                str(playlist_number) + track_numbers + output_file_extension), format=file_format, bitrate=bit_rate)
                                playlist_number+=1
                                merged_audio = track_audio
                                merged_audio_duration = track_duration
                                merged_tracks_indices = [index_list[i]]
                                merged_tracks_indices.append(index_list[i])
                                if i == len_song_list-1:
                                    merged_audio.export(os.path.join(cwd, 'Music_Files', 'Out', "Playlist " +
                                    str(playlist_number) + " (track number " + index_list[i] + ")" + output_file_extension), format=file_format, bitrate=bit_rate)

                #The track durations are expressed as strings with the following
                #format: "hours:minutes:seconds.milliseconds" and stored in the
                #variable "track_duration_csv_string", which will be added to
                #the index 3 of the song_list[i] and the "D" column of the CSV
                #file. First, the total number of milliseconds in the audiosegment
                #("track_duration") is divided (floor division) by 3600000, which
                #is the number of milliseconds in an hour. The floor division gives
                #the integer number of hours of audio file. The remainder is determined
                #by subtracting the floor division from the regular division, which
                #is then multiplied by sixty minutes per hour to get the raw number
                #of minutes (containing decimals). The integer number of minutes is
                #obtained by subtracting the number_of_minutes_raw modulus one (which
                #gives the remainder decimals) from number_of_minutes_raw. A similar
                #Approach is used for seconds and milliseconds.
                number_of_hours = track_duration // 3600000
                number_of_minutes_raw = (track_duration / 3600000 - number_of_hours) * 60
                number_of_minutes = number_of_minutes_raw - number_of_minutes_raw % 1
                number_of_seconds_raw = number_of_minutes_raw % 1 * 60
                number_of_seconds = number_of_seconds_raw - number_of_seconds_raw % 1
                number_of_milliseconds = math.floor(number_of_seconds_raw % 1 * 1000)

                track_duration_csv_string = (str(math.floor(number_of_hours)) + ":" +
                str(math.floor(number_of_minutes)) + ":" +
                str(math.floor(number_of_seconds)) + "." + str(number_of_milliseconds))

                #If the length of the "i" element of the "song_list" list is
                #at least four and the value of the fourth index is not an
                #empty string nor numeric once the colons and periods are removed,
                #then it can be inferred that an additional song description has
                #mistakenly been placed in column "D" of the CSV file instead of "E".
                if (len(song_list[i]) > 3 and song_list[i][3] != "" and
                not (str(song_list[i][3]).replace(":", "").replace(".", "")).isnumeric()):
                    #If the length of the "i" element of the "song_list" list is
                    #at least five, then the fifth index can be indexed for
                    #reassignment without causing an IndexError. The contents
                    #of "song_list[i][3]" are then moved to the next index, in order
                    #to be able to preserve the additional description in its right place
                    #and to place the track duration where the description was originally.
                    if len(song_list[i]) > 4:
                        song_list[i][4] = song_list[i][3]
                    #Otherwise, the list must be appended with "song_list[i][3]"
                    #to avoid an IndexError.
                    else:
                        song_list[i].append(song_list[i][3])
                    #The value of song_list[i][3] is then overwritten
                    #with that of "track_duration_csv_string"
                    song_list[i][3] = track_duration_csv_string
                #If no misplaced song descriptions have been located,
                #and the length of the list allows it, then the value
                #of "song_list[i][3]" is assigned to "track_duration_csv_string"
                elif len(song_list[i]) > 3:
                    song_list[i][3] = track_duration_csv_string
                #Otherwise "track_duration_csv_string" is appended to
                #avoid an IndexError.
                elif len(song_list[i]) == 3:
                    song_list[i].append(track_duration_csv_string)
                #If the "custom" option wasn't selected, then the
                #audio files were generated, their duration was
                #determined and they were stored in "song_list[i][3]".
                #These changes can now be reflected in the updated CSV file.
                csv_writer.writerow(song_list[i])
                #After the audio files have been exported, the temporary folder
                #"Intro (delete this if the program has crashed)" and its
                #contents can be removed
                shutil.rmtree(intro_path)
            bar()

#If the code has proceded up to here without problems,
#the temporary CSV file will overwrite the contents of
#the "old_csv_file_path" (minus the "(delete this if the
#program has crashed)" suffix), and the temporary file
#will be removed. This is a safeguard to prevent information
#loss in the event of the program crashing.
if old_csv_file_path and os.path.exists(csv_file_path):
    shutil.copy(csv_file_path, old_csv_file_path)
    os.remove(csv_file_path)
