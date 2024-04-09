# Persona3 Reload | Save Editor
Could work for other version like microsoft-store or PS4 (but i don't make test with it because i don't have these versions)

( For PS4/PS5 (and maybe for xbox/microsoft-store ?) save you need to decrypt the save yourself [you can use this method : https://www.youtube.com/watch?v=QA1lLxn_klA] (this method works for PS4 but I don't know if it work for PS5) )

A tool to edit : Money, Firstname, Lastname, Characters stats (actually
only for you'r character, Yukari and Junpei), playtime, social-rank and (x_pos,y_pos 
: [DANGEROUS MODIFICATION] (because if you write bad data in x_pos or y_pos, you'r character can be stuck))...

(You can see all command by typing "help")

Actually I test with only one save so idk if it's work for all save

With a save editor, it can be easy to destroy/softlock your save, so be careful (each time you save with the save editor, it creates a backup, so you can try to use these backups in case of problems).

Launch Editor.py (SavConverter folder need to be in the same emplacement that Editor.py)
After put the path of your sav, after you wan get/modify the value and save the file
(if you want to recover your file by default when saving the
program backup the file to : {original-file-path}/backup/{timestamp}_{filename}.sav


I could possibly add other functions (Persona, items, character location...).

But I can't guarantee anything, as the game saves data (GVAS) in a way that's hard to understand

(for example, depending on the size of the firstname/lastname, it may be saved separately in 3 values,
as the game uses values as UInt32 for saving).


Credits :
https://github.com/afkaf/Python-GVAS-JSON-Converter
