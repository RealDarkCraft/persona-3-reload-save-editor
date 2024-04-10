CREDITS = "https://github.com/afkaf/Python-GVAS-JSON-Converter"
import json, binascii,time, os, tempfile, struct, sys
from SavConverter import sav_to_json, read_sav, json_to_sav, load_json

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
    def Load(self,i,mdd,e,make_bak):
        try:
            dec_data = Encryption().XORshift(i+"\\"+e,"ae5zeitaix1joowooNgie3fahP5Ohph","dec")            
            with tempfile.NamedTemporaryFile(mode='wb',suffix='.sav', delete=False) as temp_file:
                temp_file.write(dec_data)
                temp_file_path = temp_file.name
                temp_file.flush
            json_data= sav_to_json(read_sav(temp_file_path), string = True)
            os.remove(temp_file_path)
            comp=True
        except:
            os.remove(temp_file_path)
            dec_data=open(i+"\\"+e,"rb").read()
            with tempfile.NamedTemporaryFile(mode='wb',suffix='.sav', delete=False) as temp_file:
                temp_file.write(dec_data)
                temp_file_path = temp_file.name
                temp_file.flush
            json_data= sav_to_json(read_sav(temp_file_path), string = True)
            os.remove(temp_file_path)
            comp=False
            
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json', delete=False) as temp_file:
            temp_file.write(json_data)
            temp_file_path = temp_file.name
            temp_file.flush
        return Persona3Save(temp_file_path,mdd,i,e,make_bak,comp)
class Persona3Save:
    def __init__(self,i,mdd,ww,qq,make_bak,comp):
        self.padding={"UInt32Property":"04000000","Int8Property":"01000000","UInt16Property":"02000000"}
        self.encrypted=comp
        self.make_bak_file=make_bak
        self.filenamestart=ww
        self.filenameend=qq
        with open(i,"r") as f:
            self.js=json.load(f)
        os.remove(i)
        self.LoadData()
        #self.js=self.SaveByNameN(self.js, "UInt32Property", 0, 8,5352)# 16386
        #print(self.debug_GetIdByValue(self.js,"UInt32Property",0,16386))
        #print(self.debug_GetIdByValue(self.js,"UInt32Property",0,393312))
        
        #print(self.debug_GetIdByValue(self.js,"UInt32Property",0,23))
        
        
        #print(self.LoadByNameN(self.js, "UInt32Property", 0,99358))
        
        
        #Start 257 -> 265
        #self.js=self.SaveByNameN(self.js, "UInt32Property", 0, 265,1929)
        
        
        
        #self.js=self.SaveByNameN(self.js, "UInt32Property", 0, 29,131125)
        #print(self.LoadByNameN(self.js, "UInt32Property", 0,1928))
        if mdd==0:
            while True:
                command=input("(type help to see comand): ").lower()
                if command == None:
                    pass
                elif command == "edit lastname":
                    self.LastName()
                elif command == "edit money":
                    self.Money()
                elif command == "edit date":
                    self.Date()
                elif command == "edit playtime":
                    self.Playtime()
                elif command == "edit firstname":
                    self.FirstName()
                elif command == "edit characters" or command == "edit character":
                    self.Characters()
                elif command == "edit socialrank" or command == "edit socialranks":
                    self.Socialrank()
                elif command == "edit dangerous":
                    self.Dangerous()
                elif command == "get" or command[0:4] == "get ":
                    a=command.split(" ")
                    if len(a) == 2:
                        try:
                            z=self.SaveHeader[a[1]]
                            print("")
                            print(z)
                        except:
                            try:
                                if type(self.Data[a[1]]) != dict:
                                    print("")
                                    print(self.Data[a[1]])
                                else:
                                    print("")
                                    print(None)
                            except:
                                pass
                elif command=="print":
                    print("")
                    for i in self.SaveHeader.keys():
                        if not "len" in i.lower():
                            print(i)
                    for i in self.Data.keys():
                        print(i)
                elif command == "json":
                    with open("n_json.txt","w") as f:
                        json.dump(self.js, f, indent=4)
                elif command == "save":
                    self.SaveChange()
                elif command == "help":
                    print("")
                    print("exit|quit : to exit\nsave : save edited data in the save file\nprint : show editable value\nedit 'value_name' : edit the value of 'value_name'\nget 'value_name' : get the value of 'value_name'")
                elif command == "exit" or command == "quit":
                    break
                else:
                    print("Invalid | type help to see possible commnad/value to modify")
    def LoadData(self):
        self.filename=self.LoadByName(self.js[1]["value"],"SaveSlotName",1,1)
        self.SaveHeader={}
        
        self.SaveHeader["lastname"]=self.LoadByName(self.js[1]["value"],"LastName",1,1)
        self.SaveHeader["firstname"]=self.LoadByName(self.js[1]["value"],"FirstName",1,1)
        self.SaveHeader["LenLastName"]=len(self.SaveHeader["lastname"])
        self.SaveHeader["LenFirstName"]=len(self.SaveHeader["firstname"])
        self.Data={}
        self.Data["money"]=self.LoadByNameN(self.js, "UInt32Property", 0,7257)
        self.Data["playtime"] = self.LoadByNameN(self.js, "UInt32Property", 0,12832)
        self.Data["characters"]={self.SaveHeader["firstname"].lower():{"current_pv":13070,"current_pc":13071,"level":13074,"exp":13075},"yukari":{"current_pv":13246,"current_pc":13247,"level":13263,"exp":13264},"junpei":{"current_pv":13422,"current_pc":13423,"level":13439,"exp":13440}}
        self.Data["dangerous"]={"player_x":self.LoadByNameN(self.js, "UInt32Property", 0,5219),"player_y":self.LoadByNameN(self.js, "UInt32Property", 0,5220),"player_direction":self.LoadByNameN(self.js, "UInt32Property", 0,5218)}#"player_z":self.LoadByNameN(self.js, "UInt32Property", 0,5221)}
        self.Data["socialrank"] = {"academics":5352,"charm":5354,"courage":5356}
        self.Data["date"]={"time":1929,"day":1928,"dayskip":1930}
    def SaveChange(self):
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json', delete=False) as temp_file:
            json.dump(self.js, temp_file, indent=2)
            temp_file_path = temp_file.name
            temp_file.flush
        binary_save = json_to_sav(load_json(temp_file_path))
        
        os.remove(temp_file_path)
        if self.encrypted == True:
            with tempfile.NamedTemporaryFile(mode='wb',suffix='.sav', delete=False) as temp_file:
                temp_file.write(binary_save)
                temp_file_path = temp_file.name
                temp_file.flush
            enc_data = Encryption().XORshift(temp_file_path,"ae5zeitaix1joowooNgie3fahP5Ohph","enc")
            os.remove(temp_file_path)
        else:
            enc_data=binary_save
        if self.make_bak_file == True:
            if os.path.isdir(self.filenamestart+"\\backup") == False:
                os.mkdir(self.filenamestart+"\\backup")
            with open(f"{self.filenamestart}\\{self.filenameend}","rb") as fr:
                back_data=fr.read()
            with open(f"{self.filenamestart}\\backup\\{str(int(time.time()))+'_'+self.filenameend}","wb") as fb:
                fb.write(back_data)            
        with open(f"{self.filenamestart}\\{self.filenameend}","wb") as f:
            f.write(enc_data)
    def int_to_hex(self,int_value):
        return ''.join([(hex(int_value)[2:].zfill(8))[i:i+2] for i in range(6, -2, -2)])
    def debug_GetIdByValue(self,js,name,header,value):
        d=[]
        if header == 0:
            for i in js[:]:
                if i["type"]== name:
                    if i["value"]==value:
                        d.append((int.from_bytes(binascii.unhexlify(i["padding"]),byteorder="little")))
        return d
    def SaveByNameN(self,js, name, header, nvar,n,after=None):
        xx=False
        padd=0
        if header == 0:
            for i in js[:]:
                padd+=1
                if i["type"]== name:
                    if xx==True:
                        js.insert(padd,{
                        "type": "UInt32Property",
                        "name": "SaveDataArea",
                        "padding_static": "04000000",
                        "padding": self.int_to_hex(n),
                        "value": nvar
                        })
                        xx==False
                    if int.from_bytes(binascii.unhexlify(str(i["padding"])),byteorder="little") == n:
                        i["value"]=nvar
                        return js
                    elif int.from_bytes(binascii.unhexlify(str(i["padding"])),byteorder="little") == after:
                        xx=True
        if after==None:
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
    def SaveByName(self, js, name, mode, header, nvar, typee, lenn=None, dummy=None):
        c = 0
        d = 0
        r = False
        x_hex=-1
        for i in js[:]:
            try:
                if i["name"] == name:
                    js.remove(i)
            except:
                pass
        x_padding=-1
        x_value=-1
        if mode == 0:
            nbr=1
        elif mode == 1:
            nbr=len(nvar)
        for i in range(nbr):
            try:
                if mode == 1:
                    x_value+=1
                    number=hex(ord(nvar[x_value])).replace("0x","")
                    if len(number)%2==1:
                        number=f"0{number}"
                    number = self.split_string(number,2)
                    for ise in number:
                        x_padding+=1
                        js.insert(len(js)-1, {"type":typee,"name":name,"padding_static":self.padding[typee],"padding":self.int_to_hex(x_padding),"value":int.from_bytes(binascii.unhexlify(ise), byteorder="big", signed=True)})
                
                elif mode == 0:
                    js.insert(len(js)-1, {"type":typee,"name":name,"padding_static":self.padding[typee],"padding":self.int_to_hex(0),"value":nvar})
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
                        if i["type"]=="StrProperty":
                            return i["value"]
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
                return binascii.unhexlify(tmp).decode("utf-8", errors="ignore")
            return binascii.unhexlify(tmp)
        return None
    def str_to_int(self,i):
        strr=""
        for a in i:
            strr+=hex(ord(a))[2:].zfill(2)
        return int.from_bytes(binascii.unhexlify(strr),byteorder="little")    
    def split_string(self,string,nbr,val=False):
        if val == True:
            string=binascii.hexlify(string.encode()).decode()
        new_lst=[]
        iq=0
        strr=""
        for i in string:
            iq+=1
            strr+=i
            if iq == nbr:
                iq=0
                new_lst.append(strr)
                strr=""
        if strr != "":
            new_lst.append(strr)
        return new_lst
                
            
            
    """ Method """
    
    def LastName(self):
        while True:
            new_name=input("New LastName (10 char max | put nothing to cancel): ")
            if len(new_name)<=10 and len(new_name)>0:
                aaa=True
                for i in new_name:
                    if len(binascii.hexlify(i.encode()).decode()) > 2:
                        aaa=False
                if aaa == True:
                    self.js[1]["value"]=self.SaveByName(self.js[1]["value"],"LastName",1,1,new_name,"Int8Property",self.SaveHeader["LenLastName"],'{"type": "Int8Property", "name": name,"padding_static":static,"padding":self.int_to_hex(x_hex), "value": ord(nvar[c - 1])}')
                    self.SaveHeader["lastname"] = new_name
                    self.SaveHeader["LenLastName"]=len(new_name)
                    new_name = self.split_string(new_name,8,True)
                    counter=0
                    for i in [0,0,0,0,0,0,0,0]:
                        self.js=self.DelByNameN(self.js, "UInt32Property", 0,17950+counter)
                    counter=0
                    for i in new_name:
                        counter+=1
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, int.from_bytes(binascii.unhexlify(i),byteorder="little"),17950+counter)
                    

                    
                    """
                    if len(new_name) < 5:
                        a=1
                    elif len(new_name) <9:
                        a=2
                    else:
                        a=3
                    if a == 1:
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name),17951)
                        self.js=self.DelByNameN(self.js, "UInt32Property", 0,17952)
                        self.js=self.DelByNameN(self.js, "UInt32Property", 0,17953)
                    elif a ==2:
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[0:4]),17951)
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[4:len(new_name)]),17952)
                        self.js=self.DelByNameN(self.js, "UInt32Property", 0,17953)
                    elif a ==3:
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[0:4]),17951)
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[4:8]),17952)
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[8:len(new_name)]),17953)
                    """
                        
                    print(new_name)
                    break
            elif len(new_name)==0:
                break
    def FirstName(self):
        while True:
            new_name=input("New FirstName (10 char max | put nothing to cancel): ")
            if len(new_name)<=10 and len(new_name)>0:
                aaa=True
                for i in new_name:
                    if len(binascii.hexlify(i.encode()).decode()) > 2:
                        aaa=False
                if aaa == True:
                    self.js[1]["value"]=self.SaveByName(self.js[1]["value"],"FirstName",1,1,new_name,"Int8Property",self.SaveHeader["LenFirstName"],'{"type": "Int8Property", "name": name,"padding_static":static,"padding":self.int_to_hex(x_hex), "value": ord(nvar[c - 1])}')
                    self.SaveHeader["firstname"] = new_name
                    self.SaveHeader["LenFirstName"]=len(new_name)
                    new_name = self.split_string(new_name,8,True)
                    counter=0
                    for i in [0,0,0,0,0,0,0,0]:
                        self.js=self.DelByNameN(self.js, "UInt32Property", 0,17934+counter)
                    counter=0
                    for i in new_name:
                        counter+=1
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, int.from_bytes(binascii.unhexlify(i),byteorder="little"),17934+counter)
                    
                    """
                    if len(new_name) < 5:
                        a=1
                    elif len(new_name) <9:
                        a=2
                    else:
                        a=3
                    if a == 1:
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name),17935)
                        self.js=self.DelByNameN(self.js, "UInt32Property", 0,17936)
                        self.js=self.DelByNameN(self.js, "UInt32Property", 0,17937)
                    elif a ==2:
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[0:4]),17935)
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[4:len(new_name)]),17936)
                        self.js=self.DelByNameN(self.js, "UInt32Property", 0,17937)
                    elif a ==3:
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[0:4]),17935)
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[4:8]),17936)
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, self.str_to_int(new_name[8:len(new_name)]),17937)
                    """
                    print(new_name)
                    break
            elif len(new_name)==0:
                break
    def Characters(self):
        characters = [self.SaveHeader["firstname"].lower(),"yukari","junpei"]
        
        while True:
            print(f"\nChose the characters to edit (put nothing to exit 'Characters' editing) :\n    1 : {self.SaveHeader['firstname']}\n    2 : {characters[1][0:1].upper()+characters[1][1:len(characters[1])]}\n    3 : {characters[2][0:1].upper()+characters[2][1:len(characters[2])]}")
            a = input().lower()
            if a in ["1","2","3"]:
                if a == "1":
                    bbc=self.SaveHeader['firstname']
                else:
                    bbc=characters[int(a)-1][0:1].upper()+characters[int(a)-1][1:len(characters[int(a)-1])]
                while True:
                    command = input(f"(type help to see comand) ('{bbc}' stats editing) :  ").lower()
                    if command == "edit current_pv":
                        while True:
                            z=input(F"New {bbc} PV (to increase Max PV, increase the Level) (999 max | put nothing to cancel): ")
                            if z == "":
                                break
                            else:
                                try:
                                    z=int(z)
                                    if z>0 and z < 1000:
                                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,self.Data["characters"][characters[int(a)-1]]["current_pv"])
                                        break
                                except:
                                    pass
                    elif command == "edit current_pc":
                        while True:
                            z=input(F"New {bbc} PC (to increase Max PC, increase the Level) (999 max | put nothing to cancel): ")
                            if z == "":
                                break
                            else:
                                try:
                                    z=int(z)
                                    if z>0 and z < 1000:
                                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,self.Data["characters"][characters[int(a)-1]]["current_pc"])
                                        break
                                except:
                                    pass
                    elif command == "edit level":
                        while True:
                            z=input(F"New {bbc} Level (99 max | put nothing to cancel): ")
                            if z == "":
                                break
                            else:
                                try:
                                    z=int(z)
                                    if z>0 and z < 100:
                                        if a == "1":
                                            self.js[1]["value"]=self.SaveByName(self.js[1]["value"],"PlayerLevel",0,1,z,"UInt32Property")
                                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,self.Data["characters"][characters[int(a)-1]]["level"])
                                        break
                                except:
                                    pass
                    elif command == "edit exp":
                        while True:
                            z=input(F"New {bbc} Exp (4294967295 max | put nothing to cancel): ")
                            if z == "":
                                break
                            else:
                                try:
                                    z=int(z)
                                    if z>0 and z < 4294967296:
                                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,self.Data["characters"][characters[int(a)-1]]["exp"])
                                        break
                                except:
                                    pass
                    
                    
                    elif command=="print":
                        for i in self.Data["characters"][characters[int(a)-1]].keys():
                            print(i)
                    elif command == "get" or command[0:4] == "get ":
                        av=command.split(" ")
                        if len(av) == 2:
                            try:
                                print("")
                                print(self.LoadByNameN(self.js, "UInt32Property", 0,self.Data["characters"][characters[int(a)-1]][av[1]]))
                            except Exception as e:
                                pass
                    elif command == "back":
                        break
                    elif command == "help":
                        print("")
                        print(f"back : to exit {bbc} editing\nprint : show editable value name\nedit 'value_name' : edit the value of 'value_name'\nget 'value_name' : get the value of 'value_name'")
            elif a == None:
                pass
            
            elif a == "":
                break
    def Relationship(self):
        pass
    def Socialrank(self):
        while True:
            command = input(f"(type help to see comand) (social-rank editing) :  ")
            if command == "edit charm":
                while True:
                    z=input(F"New charm (100 max | put nothing to cancel): ")
                    if z == "":
                        break
                    else:
                        try:
                            z=int(z)
                            if z>0 and z < 101:
                                self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,self.Data["socialrank"]["charm"])
                                break
                        except:
                            pass
            elif command == "edit academics":
                while True:
                    z=input(F"New academics (230 max | put nothing to cancel): ")
                    if z == "":
                        break
                    else:
                        try:
                            z=int(z)
                            if z>0 and z < 231:
                                self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,self.Data["socialrank"]["academics"])
                                break
                        except:
                            pass
            elif command == "edit courage":
                while True:
                    z=input(F"New courage (80 max | put nothing to cancel): ")
                    if z == "":
                        break
                    else:
                        try:
                            z=int(z)
                            if z>0 and z < 81:
                                self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,self.Data["socialrank"]["courage"])
                                break
                        except:
                            pass
            
            
            elif command=="print":
                for i in self.Data["socialrank"].keys():
                    print(i)
            elif command == "get" or command[0:4] == "get ":
                av=command.split(" ")
                if len(av) == 2:
                    try:
                        print("")
                        print(self.LoadByNameN(self.js, "UInt32Property", 0,self.Data["socialrank"][av[1]]))
                    except Exception as e:
                        pass
            elif command == "back":
                break
            elif command == "help":
                print("")
                print(f"back : to exit social-rank editing\nprint : show editable value name\nedit 'value_name' : edit the value of 'value_name'\nget 'value_name' : get the value of 'value_name'")


        
        
        
        
    def Playtime(self):
        while True:#8205188
            try:
                play = input("New Playtime (max 107998200 | put nothing to cancel): ")
                play=int(play)
                if play >= 0 and play <= 107998200:
                    self.js[1]["value"]=self.SaveByName(self.js[1]["value"],"PlayTime",0,1,play,"UInt32Property")
                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0, play,12832)
                    self.Data["playtime"] = play
                    print(play)
                    break
            except:
                try:
                    if len(play)==0:
                        break
                except:
                    pass
    def Dangerous(self):
        while True:
            command = input(f"(type help to see comand) (unkwnown|dangerous|could break save) editing :  ").lower()
            if command == "edit player_x":
                while True:
                    z=input(F"New player_x (4294967295 max | put nothing to cancel): ")
                    if z == "":
                        break
                    else:
                        try:
                            z=int(z)
                            if z>0 and z <= 4294967295:
                                self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,5219)
                                break
                        except:
                            pass
            elif command == "edit player_y":
                while True:
                    z=input(F"New player_y (4294967295 max | put nothing to cancel): ")
                    if z == "":
                        break
                    else:
                        try:
                            z=int(z)
                            if z>0 and z <= 4294967295:
                                self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,5220)
                                break
                        except:
                            pass
            elif command == None:#"edit player_z":
                while True:
                    z=input(F"New player_z (4294967295 max | put nothing to cancel | UNCONFIRMED VALUE ID !): ")
                    if z == "":
                        break
                    else:
                        try:
                            z=int(z)
                            if z>0 and z <= 4294967295:
                                self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,5221)
                                break
                        except:
                            pass
            elif command == "edit player_direction":
                while True:
                    z=input(F"New player_z (4294967295 max | put nothing to cancel): ")
                    if z == "":
                        break
                    else:
                        try:
                            z=int(z)
                            if z>0 and z <= 4294967295:
                                self.js=self.SaveByNameN(self.js, "UInt32Property", 0, z,5218)
                                break
                        except:
                            pass
            elif command=="print":
                for i in self.Data["dangerous"].keys():
                    print(i)
            elif command == "get" or command[0:4] == "get ":
                a=command.split(" ")
                if len(a) == 2:
                    try:
                        print("")
                        print(self.Data["dangerous"][a[1]])
                    except:
                        pass
            elif command == "back":
                break
            elif command == "help":
                print("")
                print(f"back : to exit |dangerous editing\nprint : show editable value name\nedit 'value_name' : edit the value of 'value_name'\nget 'value_name' : get the value of 'value_name'")
            self.Data["dangerous"]={"player_x":self.LoadByNameN(self.js, "UInt32Property", 0,5219),"player_y":self.LoadByNameN(self.js, "UInt32Property", 0,5220),"player_z":self.LoadByNameN(self.js, "UInt32Property", 0,5221),"player_direction":self.LoadByNameN(self.js, "UInt32Property", 0,5218)}
    def Date(self):
        timedata= [["Very early morning",257],["Early morning",258],["Morning",259],["Lunch break",260],["Afternoon",261], ["After school",262],["Evening",263],["Dark Hour",264],["Late evening",265]]
        daydata=[[30,31,30,31,31,30,31,30,31,31,28,31],{2009:["April","May","Juin","July","August","September","October","November","December"],2010:["January","Febuary","March"]}]
        while True:
            command = input(f"(type help to see comand) (date editing) :  ")
            if command == "edit day":
                while True:
                    z=input(F"Choose Year (2009-2010) (put nothing to cancel): ")
                    if z == "":
                        break
                    else:
                        try:
                            z=int(z)
                            if z == 2009 or z == 2010:
                                while True:
                                    print("Choose Month (put nothing to cancel) :")
                                    counter=0
                                    for az in daydata[1][z]:
                                        counter+=1
                                        print(f"    {counter} : {az}")
                                    z2=input()                    
                                    if z2 == "":
                                        break
                                    else:
                                        try:
                                            z2=int(z2)
                                            if (z == 2009 and (z2>0 and z2<10)) or (z == 2010 and (z2>0 and z2<4)):
                                                z2-=1
                                                if z == 2010:
                                                    z2+=9
                                                while True:
                                                    offset=0                                                        
                                                    if z2 > 0:
                                                        for iu in range(z2):
                                                            offset+=daydata[0][iu]
                                                    item = input(f"Choose Day ({daydata[0][z2]} Max) (put nothing to cancel) :")
                                                    if item == "":
                                                        break
                                                    else:
                                                        try:
                                                            item = int(item)
                                                            if (item > 0 and item < daydata[0][z2]):
                                                                item=(offset+item)-1
                                                                self.js=self.SaveByNameN(self.js, "UInt32Property", 0, item,1928)
                                                                self.js=self.SaveByNameN(self.js, "UInt32Property", 0, item,1930)
                                                                break
                                                        except:
                                                            pass
                                                            
                                                            
                                                break
                                        except:
                                            pass
                                break
                        except:
                            pass
            elif command == None:#"edit day-skip":
                while True:
                    print(f"Chosse new hour (put nothing to cancel) (bad modification could break/soft-lock the game but you may fix it (not sure) by re-editing the save)\n    1 : {timedata[0][0]}\n    2 : {timedata[1][0]}\n    3 : {timedata[2][0]}\n    4 : {timedata[3][0]}\n    5 : {timedata[4][0]}\n    6 : {timedata[5][0]}\n    7 : {timedata[6][0]}\n    8 : {timedata[7][0]}\n    9 : {timedata[8][0]}")
                    z=input()
                    try:
                        z=int(z)
                        if z>0 and z < 10:
                            self.js=self.SaveByNameN(self.js, "UInt32Property", 0, timedata[z-1][1],self.Data["date"]["time"])
                            break
                    except:
                          try:
                              if len(z)==0:
                                  break
                          except:
                              pass
            elif command == "edit time":
                while True:
                    print(f"Chosse new hour (put nothing to cancel) (bad modification could break/soft-lock the game but you may fix it (not sure) by re-editing the save)\n    1 : {timedata[0][0]}\n    2 : {timedata[1][0]}\n    3 : {timedata[2][0]}\n    4 : {timedata[3][0]}\n    5 : {timedata[4][0]}\n    6 : {timedata[5][0]}\n    7 : {timedata[6][0]}\n    8 : {timedata[7][0]}\n    9 : {timedata[8][0]}")
                    z=input()
                    try:
                        z=int(z)
                        if z>0 and z < 10:
                            self.js=self.SaveByNameN(self.js, "UInt32Property", 0, timedata[z-1][1],self.Data["date"]["time"])
                            break
                    except:
                          try:
                              if len(z)==0:
                                  break
                          except:
                              pass
            elif command=="print":
                for i in self.Data["date"].keys():
                    print(i)
            elif command == "get" or command[0:4] == "get ":
                av=command.split(" ")
                if len(av) == 2:
                    try:
                        print("")
                        if av[1] == "time":
                            print(timedata[(self.LoadByNameN(self.js, "UInt32Property", 0,self.Data["date"][av[1]])-257)][0])
                        else:
                            print(self.LoadByNameN(self.js, "UInt32Property", 0,self.Data["date"][av[1]]))
                    except Exception as e:
                        pass
            elif command == "back":
                break
            elif command == "help":
                print("")
                print(f"back : to exit date editing\nprint : show editable value name\nedit 'value_name' : edit the value of 'value_name'\nget 'value_name' : get the value of 'value_name'")

    
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
if len(sys.argv) >1:
    try:
        a=sys.argv[1].replace('"',"")
        a=OpenSave().Load(os.path.split(os.path.abspath(a))[0],0,os.path.split(os.path.abspath(a))[1],True)
    except FileNotFoundError:
        raise FileNotFoundError("Bad path\n")
    except PermissionError:
        raise FileNotFoundError("Permission error or Bad path error\n")
    except Exception as e:
        if "Failed to read HeaderProperty" in str(e):
            raise Exception("Invalid file format (not persona 3 reload GVAS)")
else:
    while True:
        try:
            a=input("Persona3 Reload sav path : ").replace('"',"")
            a=OpenSave().Load(os.path.split(os.path.abspath(a))[0],0,os.path.split(os.path.abspath(a))[1],True)
        except FileNotFoundError:
            print("Bad path\n")
        except PermissionError:
            print("Permission error or Bad path error\n")
        except Exception as e:
            if "Failed to read HeaderProperty" in str(e):
                raise Exception("Invalid file format (not persona 3 reload GVAS)")
