# Persona3 Reload | Save Editor (Steam)
A tool to edit : Money, Firstname, Lastname (can don't work), Player current PC/PV
I could possibly add other functions (Persona, object, character location...)
(Firstanme and Lastname options is actually disable)

Actually I test with only one save so idk if it's work for all save

To edit save, put the path of you'r file a the end of GVAS.py (warning, you can put a file with any
name at input and the program will save the output save at : {save_slot_name}.sav (relative path)
(so make sure you have backup the save because actually there no feature to backup the save in the program)

But I can't guarantee anything, as the game saves data (GVAS) in a way that's hard to understand
(for example, depending on the size of the firstname/lastname, it may be saved separately in 3 values,
as the game uses values as UInt32 for saving).



Credits :
https://github.com/afkaf/Python-GVAS-JSON-Converter
