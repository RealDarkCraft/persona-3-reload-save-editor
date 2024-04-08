# Persona3 Reload | Save Editor (Steam)
A tool to edit : Money, Firstname, Lastname, Characters stats (actually
only for you'r character, Yukari and Junpei), playtime and (x_pos,y_pos,z_pos 
(z_pos function ca be wrong) : [DANGEROUS MODIFICATION] (because if you write bad data in you'r character can be stuck))...

(You can see all command by typing "help")

Actually I test with only one save so idk if it's work for all save

(the options to modify player_z could be wrong)

Launch Editor.py (SavConverter folder need to be in the same emplacement that Editor.py)
After put the path of your sav, after you wan get/modify the value and save the file
(if you want to recover your file by default when saving the
program backup the file to : {original-file-path}/backup/{timestamp}_{filename}.sav


I could possibly add other functions (Persona, object, character location...).

But I can't guarantee anything, as the game saves data (GVAS) in a way that's hard to understand

(for example, depending on the size of the firstname/lastname, it may be saved separately in 3 values,
as the game uses values as UInt32 for saving).


Credits :
https://github.com/afkaf/Python-GVAS-JSON-Converter
