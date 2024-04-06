CREDITS = """
https://github.com/afkaf/Python-GVAS-JSON-Converter
https://github.com/illusion0001/P3R-Save-EnDecryptor
"""


import json, binascii,time, os, tempfile, struct
from SavConverter import sav_to_json, read_sav, json_to_sav, load_json
from SavConverter import obj_to_json, print_json, get_object_by_path, insert_object_by_path, replace_object_by_path, update_property_by_path

class Encryption:
    def __init__(self):
        pass
    def XORshift(self,file,key,mode):
        keylen=len(key)
        with open(file,'rb') as f:
            data1=f.read()
        filesize=os.path.getsize(file)
        crypt_data = bytearray(filesize)

        for i in range(filesize):
            key_idx = i % keylen
            if mode == "dec":
                bVar1=data1[i]^ord(key[key_idx])
                crypt_data[i] = (bVar1 >> 4 & 3 | (bVar1 & 3) << 4 | bVar1 & 0xcc)
            elif mode == "enc":
                crypt_data[i]=((((data1[i] & 0xff) >> 4) & 3 | (data1[i] & 3) << 4 | data1[i] & 0xcc) ^ ord(key[key_idx]))
        return crypt_data
class OpenSave:
    def __init__(self):
        pass
    def Load(self,i,mdd):
        dec_data = Encryption().XORshift(i,"ae5zeitaix1joowooNgie3fahP5Ohph","dec")
        with open("decrypted.txt","wb") as f:
            f.write(dec_data)
        with tempfile.NamedTemporaryFile(mode='wb',suffix='.sav', delete=False) as temp_file:
            temp_file.write(dec_data)
            temp_file_path = temp_file.name
            temp_file.flush
        json_data= sav_to_json(read_sav(temp_file_path), string = True)
        os.remove(temp_file_path)
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json', delete=False) as temp_file:
            temp_file.write(json_data)
            temp_file_path = temp_file.name
            temp_file.flush
        return Persona3Save(temp_file_path,mdd)
class Persona3Save:
    def __init__(self,i,mdd):
        with open(i,"r") as f:
            self.js=json.load(f)
        os.remove(i)
        self.LoadData()
        
        """
        #self.js=self.SaveByNameN(self.js, "UInt32Property", 0, 87,87443)
        print(self.debug_GetIdByValue(self.js,"UInt32Property",0,51))
        # player actual pv = 13070
        # player actual pc = 13071
        #97203    45850
        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, 120,13071)
        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, 120,13246)
        #print(self.debug_GetIdByValue(self.js,"UInt32Property",0,41))
        """
        if mdd==0:
            while True:
                command=input("(type help to see comand): ").lower()
                """if command == "edit lastname":
                    self.LastName()"""
                elif command == "edit money":
                    self.Money()
                """elif command == "edit firstname":
                    self.FirstName()"""
                elif command == "edit characters" or command == "edit character":
                    self.Characters()
                elif command == "get" or command[0:4] == "get ":
                    a=command.split(" ")
                    if len(a) == 2:
                        try:
                            print("\n")
                            print(self.SaveHeader[a[1]])
                            print("\n")
                        except:
                            try:
                                print("\n")
                                if type(self.Data[a[1]]) != dict: 
                                    print(self.Data[a[1]])
                                else:
                                    print(None)
                                print("\n")
                            except:
                                pass
                elif command=="print":
                    for i in self.SaveHeader.keys():
                        if not "len" in i.lower():
                            print(i)
                    for i in self.Data.keys():
                        print(i)
                elif command == "json":
                    with open("json.txt","w") as f:
                        json.dump(self.js, f, indent=4)
                elif command == "save":
                    self.SaveChange()
                elif command == "help":
                    print("exit|quit : to exit\nsave : save edited data in the save file\nprint : show editable value name\nedit 'value_name' : edit the value of 'value_name'\nget 'value_name' : get the value of 'value_name'")
                elif command == "exit" or command == "quit":
                    exit()
                else:
                    print("Invalid | type help to see possible commnad/value to modify")
    def LoadData(self):
        self.SaveHeader={}
        self.SaveHeader["lastname"]=self.LoadByName(self.js[1]["value"],"LastName",1,1)
        self.SaveHeader["firstname"]=self.LoadByName(self.js[1]["value"],"FirstName",1,1)
        self.SaveHeader["LenLastName"]=len(self.SaveHeader["lastname"])
        self.SaveHeader["LenFirstName"]=len(self.SaveHeader["firstname"])
        self.Data={}
        self.Data["money"]=self.LoadByNameN(self.js, "UInt32Property", 0,7257)
        self.Data["characters"]={}
    
    def SaveChange(self):
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json', delete=False) as temp_file:
            json.dump(self.js, temp_file, indent=2)
            temp_file_path = temp_file.name
            temp_file.flush
        binary_save = json_to_sav(load_json(temp_file_path))
        
        os.remove(temp_file_path)
        with tempfile.NamedTemporaryFile(mode='wb',suffix='.sav', delete=False) as temp_file:
            temp_file.write(binary_save)
            temp_file_path = temp_file.name
            temp_file.flush
        enc_data = Encryption().XORshift(temp_file_path,"ae5zeitaix1joowooNgie3fahP5Ohph","enc")
        os.remove(temp_file_path)
        with open("SaveData001.sav","wb") as f:
            f.write(enc_data)
    def int_to_hex(self,int_value):
        return ''.join([(hex(int_value)[2:].zfill(8))[i:i+2] for i in range(6, -2, -2)])
    def debug_GetIdByValue(self,js,name,header,value):
        d=[]
        if header == 0:
            for i in js[:]:
                if i["type"]== name:
                    if i["value"]==value:
                        d.append(int.from_bytes(binascii.unhexlify(i["padding"]),byteorder="little"))
        return d
    def SaveByNameN(self,js, name, header, nvar,n):
        if header == 0:
            for i in js[:]:
                if i["type"]== name:
                    if int.from_bytes(binascii.unhexlify(str(i["padding"])),byteorder="little") == n:
                        i["value"]=nvar
                        return js
        js.insert(len(js)-1,{
        "type": "UInt32Property",
        "name": "SaveDataArea",
        "padding_static": "04000000",
        "padding": self.int_to_hex(n),
        "value": nvar
        })
        return js
    def DelByNameN(self,js, name, header, n):
        if header == 0:
            for i in js[:]:
                if i["type"]== name:
                    if int.from_bytes(binascii.unhexlify(str(i["padding"])),byteorder="little") == n:
                        js.remove(i)
                        return js
    def SaveByName(self, js, name, mode, header, nvar, static, lenn=None, dummy=None):
        c = 0
        d = 0
        r = False
        x_hex=-1
        for i in js[:]:
            d += 1
            if header == 1:
                try:
                    if i["name"] == name:
                        if c < len(nvar) and not r:
                            x_hex+=1
                            c += 1
                            i["value"] = ord(nvar[c - 1])
                            i["padding"]=self.int_to_hex(x_hex)
                        else:
                            r = True
                            js.remove(i)
                    elif c != 0 and c < len(nvar):
                        c+=1
                        x_hex+=1
                        
                        js.insert(d-1, eval(dummy))
                except:
                    pass
        return js
    def LoadByNameN(self,js, name, header,n):
        if header == 0:
            for i in js[:]:
                if i["type"]== name:
                    if int.from_bytes(binascii.unhexlify(i["padding"]),byteorder="little") == n:
                        return i["value"]
        return None
    def LoadByName(self,js,name,mode,header):
        tmp=[]
        c=0
        for i in js:                
            if header==1:
                try:
                    if i["name"]==name:
                        tmp.append([int.from_bytes(binascii.unhexlify(i["padding"]),byteorder="little"),binascii.hexlify((i["value"]).to_bytes(1, byteorder='big', signed=True)).decode()])
                except:
                    pass
            else:
                if c>1:
                    try:
                        if i["name"] == name:
                            tmp+=format((i["value"]& 0xFFFFFFFF), '08x')  
                    except:
                        pass
                c+=1
        a=sorted(tmp, key=lambda x: x[0])
        tmp=""
        for i in a:
            tmp+=i[1]
        if len(tmp)>0:
            if mode==1:
                return binascii.unhexlify(tmp).decode("utf-8")
            return binascii.unhexlify(tmp)
        return None
    def str_to_int(self,i):
        strr=""
        for a in i:
            strr+=hex(ord(a))[2:].zfill(2)
        return int.from_bytes(binascii.unhexlify(strr),byteorder="little")    
    
    """ Method """
    
    def LastName(self):
        while True:
            new_name=input("New LastName (10 char max | put nothing to cancel): ")
            if len(new_name)<=10 and len(new_name)>0:
                self.js[1]["value"]=self.SaveByName(self.js[1]["value"],"LastName",1,1,new_name,"01000000",self.SaveHeader["LenLastName"],'{"type": "Int8Property", "name": name,"padding_static":static,"padding":self.int_to_hex(x_hex), "value": ord(nvar[c - 1])}')
                self.SaveHeader["lastname"] = new_name
                self.SaveHeader["LenLastName"]=len(new_name)
                if len(new_name) < 5:
                    a=1
                elif len(new_name) <9:
                    a=2
                else:
                    a=3
                if a*4 <len(new_name):
                    a+=1
                if a == 1:
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name),17951)
                    #self.js=self.DelByNameN(self.js, "UInt32Property", 0,17952)
                    #self.js=self.DelByNameN(self.js, "UInt32Property", 0,17953)
                elif a ==2:
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[4:4]),17951)
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[4:len(new_name)]),17952)
                    #self.js=self.DelByNameN(self.js, "UInt32Property", 0,17953)
                elif a ==3:
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[4:4]),17951)
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[4:8]),17952)
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[8:len(new_name)]),17953)
                    
                    
                print(new_name)
                break
            elif len(new_name)==0:
                break
    def FirstName(self):
        while True:
            new_name=input("New FirstName (10 char max | put nothing to cancel): ")
            if len(new_name)<=10 and len(new_name)>0:
                self.js[1]["value"]=self.SaveByName(self.js[1]["value"],"FirstName",1,1,new_name,"01000000",self.SaveHeader["LenFirstName"],'{"type": "Int8Property", "name": name,"padding_static":static,"padding":self.int_to_hex(x_hex), "value": ord(nvar[c - 1])}')
                self.SaveHeader["firstname"] = new_name
                self.SaveHeader["LenFirstName"]=len(new_name)
                if len(new_name) < 5:
                    a=1
                elif len(new_name) <9:
                    a=2
                else:
                    a=3
                if a*4 <len(new_name):
                    a+=1
                if a == 1:
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name),17935)
                elif a ==2:
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[4:4]),17935)
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[4:len(new_name)]),273022976)
                elif a ==3:
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[4:4]),17935)
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[4:8]),273022976)
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[8:len(new_name)]),289800192)
                    
                    
                print(new_name)
                break
            elif len(new_name)==0:
                break
    def Characters(self):
        self.Data["characters"]={self.SaveHeader["lastname"].lower():{"current_pv":13070,"current_pc":13071}}
        characters = [self.SaveHeader["lastname"].lower()]#,"yukari","junpei"]
        while True:
            print(f"\nChose the characters to edit (put nothing to exit Characters editing) :\n    {characters[0]}\n    {characters[1]}\n    {characters[2]}")
            a = input().lower()
            if a == characters[0]:
                while True:
                    command = input(f"(type help to see comand) ({characters[0]} stats editing) :  ").lower()
                    if command == "edit current_pv":
                        while True:
                            z=input(F"New {characters[0]} PV (Max PV is calculated by the game) (999 max | put nothing to cancel): ")
                            if z == "":
                                break
                            else:
                                try:
                                    z=int(z)
                                    if z>-1 and z < 1000:
                                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,13070)
                                        break
                                except:
                                    pass
                    elif command == "edit current_pc":
                        while True:
                            z=input(F"New {characters[0]} PC (Max PC is calculated by the game) (999 max | put nothing to cancel): ")
                            if z == "":
                                break
                            else:
                                try:
                                    z=int(z)
                                    if z>-1 and z < 1000:
                                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,13071)
                                        break
                                except:
                                    pass
                        
                    elif command=="print":
                        for i in self.Data["characters"][characters[0]].keys():
                            print(i)
                    elif command == "get" or command[0:4] == "get ":
                        a=command.split(" ")
                        if len(a) == 2:
                            try:
                                print("\n")
                                print(self.LoadByNameN(self.js, "UInt32Property", 0,self.Data["characters"][characters[0]][a[1]]))
                                print("\n")
                            except:
                                pass
                    elif command == "back":
                        break
                    elif command == "help":
                        print(f"back : to exit {characters[0]} editing\nprint : show editable value name\nedit 'value_name' : edit the value of 'value_name'\nget 'value_name' : get the value of 'value_name'")
            elif a == None:
                pass
            
            elif a == "":
                break
    
    
    
    def Money(self):
        while True:
            try:
                new_name=input("New FirstName (9999999 max | put nothing to cancel): ")
                new_name=int(new_name)
                if new_name>=0 and new_name<=9999999:
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, new_name,7257)
                    self.Data["money"]=new_name
                    print(new_name)
                    break
            except:
                try:
                    if len(new_name)==0:
                        break
                except:
                    pass
a=OpenSave().Load("bak_SaveData001 - Copie.sav",0)
print(a.Data)