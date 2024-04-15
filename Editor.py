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
                elif command == "edit persona" or command == "edit personas":
                    self.Personas()
                elif command == "edit playtime":
                    self.Playtime()
                elif command == "edit difficulty":
                    self.Difficulty()
                elif command == "edit sociallink" or command == "edit sociallinks" or command == "edit social-link" or command == "edit social-links" or command == "edit social link" or command == "edit social links":
                    self.Sociallink()
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
        self.Data["date"]={"time":1929,"day":1928}#dayskip = 1930
        self.Data["personavalueid"]={"persona":[13086,13098,13110,13122,13134,13146,13158],"level":[13087,13099,13111,13123,13135,13147,13159],"exp":[13088,13100,13112,13124,13136,13148,13160],"skill_slot_1":[13089,13101,13113,13125,13137,13149,13161],"skill_slot_2":[13090,13102,13114,13126,13138,13150,13162],"skill_slot_3":[13091,13103,13115,13127,13139,13151,13163],"skill_slot_4":[13092,13104,13116,13128,13140,13152,13164],"fo_ma_en_ag":[13093,13105,13117,13129,13141,13153,13165],"ch":[13094,13106,13118,13130,13142,13154,13166]}#,"skill_slot_4":[0,0,0,0,13143,0]}
        self.Data["sociallink"]={"aigis":5342,"nyx annihilation team":5340,"kamiki":5338,"suemitsu":5336,"hayase":5334,"mutatsu":5332,"tanaka":5330,"bebe":5328,"pharos":5326,"maiko":5324,"nishiwaki":5322,"hiraga":5320,"maya":5318,"fushimi":5316,"miyamoto":5314,"takeba":5312,"kitamura":5310,"odagiri":5308,"kirijo":5306,"yamagishi":5304,"tomochika":5302,"sees":5300}
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
    def Sociallink(self):
        character_name=['SEES', 'Tomochika', 'Yamagishi', 'Kirijo', 'Odagiri', 'Kitamura', 'Takeba', 'Miyamoto', 'Fushimi', 'Maya', 'Hiraga', 'Nishiwaki', 'Maiko', 'Pharos', 'Bebe', 'Tanaka', 'Mutatsu', 'Hayase', 'Suemitsu', 'Kamiki', 'Nyx Annihilation Team', 'Aigis']
        
        while True:
            print(f"\nChose the social-link to edit (put nothing to exit 'Social-Link' editing) :")
            counter=0
            for i in character_name:
                counter+=1
                print(f"    {counter} : {i}")      
            a = input().lower()
            if a in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']:
                bbc=character_name[int(a)-1].lower()
                bbc2=character_name[int(a)-1]
                while True:
                    command = input(f"(type help to see comand) (Social-Link editing {bbc2}): ")
                    int("00000032",16)
                    if command == "edit level":
                        integer = self.LoadByNameN(self.js, "UInt32Property", 0,self.Data["sociallink"][bbc])
                        if integer == None:
                            integer = 0
                        load=binascii.hexlify(int.to_bytes(integer,4,byteorder="big")).decode()
                        level_load=load[4:len(load)]
                        point_load=load[0:4]
                        while True:
                            new_level=input(f"New {bbc2} relation level (10 max | put nothing to cancel): ")
                            try:
                                new_level= int(new_level)
                                if new_level > 0 and new_level <= 10:
                                    if new_level == 10:
                                        point_load = "0000"
                                    load=point_load+binascii.hexlify(int.to_bytes(new_level,2,byteorder="big")).decode()
                                    self.js=self.SaveByNameN(self.js, "UInt32Property", 0,int(load,16),self.Data["sociallink"][bbc])
                                elif new_level == 0:
                                    self.js=self.DelByNameN(self.js, "UInt32Property", 0,self.Data["sociallink"][bbc])
                                new_bin="0b"
                                for iuesn in self.Data["sociallink"].values():
                                    tempp=self.LoadByNameN(self.js, "UInt32Property", 0,iuesn)
                                    if tempp != None and tempp > 0:
                                        new_bin+="1"
                                    else:
                                        new_bin+="0"
                                new_bin=eval(new_bin)
                                self.js=self.SaveByNameN(self.js, "UInt32Property", 0,new_bin,103)
                                break
                            except:
                                if new_level == "":
                                    break
                    elif command == "edit point":
                        integer = self.LoadByNameN(self.js, "UInt32Property", 0,self.Data["sociallink"][bbc])
                        if integer == None:
                            integer = 0
                        load=binascii.hexlify(int.to_bytes(integer,4,byteorder="big")).decode()
                        level_load=load[4:len(load)]
                        point_load=load[0:4]
                        while True:
                            new_point=input(f"New {bbc2} relation points (100 max | put nothing to cancel): ")
                            try:
                                new_point= int(new_point)
                                if new_point > 0 and new_point <= 100:
                                    if int(level_load,16) < 10 and int(level_load,16) > 0:
                                        load=binascii.hexlify(int.to_bytes(new_point,2,byteorder="big")).decode()+level_load
                                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0,int(load,16),self.Data["sociallink"][bbc])
                                        break
                                    else:
                                        print("Can't edit point if relation level is 10 or 0")
                                        break
                            
                            except Exception as e:
                                print(e)
                                if new_point == "":
                                    break                    
                    elif command=="print":
                        print("level\npoints")
                    elif command == "get" or command[0:4] == "get ":
                        integer = self.LoadByNameN(self.js, "UInt32Property", 0,self.Data["sociallink"][bbc])
                        load=binascii.hexlify(int.to_bytes(integer,4,byteorder="big")).decode()
                        level_load=load[4:len(load)]
                        point_load=load[0:4]
                        av=command.split(" ")
                        if len(av) == 2:
                            if av[1] == "level" or av[1] == "levels":
                                print(f'\n{int(level_load,16)}')  
                            elif av[1] == "point" or av[1] == "points":
                                print(f"\n{int(point_load,16)}")
                    elif command == "back":
                        break
                    elif command == "help":
                        print("")
                        print(f"back : to exit {bbc2} relation editing\nprint : show editable value name\nedit 'value_name' : edit the value of 'value_name'\nget 'value_name' : get the value of 'value_name'")
            elif a == "":
                break
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
    def Difficulty(self):
        difficultydata={"Beginner":2166366214,"Easy":2166374406,"Normal":2166390790,"Hard":2166423558,"Maniac":100794368}
        difficultychoose=["Beginner","Easy","Normal","Hard","Maniac"]
        while True:
            print("Choose Difficulty (put nothing to cancel :")
            counter=0
            for i in difficultychoose:
                counter+=1
                print(f"    {counter} : {i}")
            ss=input()
            if ss == "":
                break
            else:
                try:
                    ss=int(ss)
                    if ss > 0 and ss <= 5:
                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, difficultydata[difficultychoose[ss-1]],384)
                        break
                except:
                    pass
    
    def Date(self):
        timedata= [["Very early morning",257],["Early morning",258],["Morning",259],["Lunch break",260],["Afternoon",261], ["After school",262],["Evening",263],["Dark Hour",264],["Late evening",265]]
        daydata=[[30,31,30,31,31,30,31,30,31,31,28,4],{2009:["April","May","Juin","July","August","September","October","November","December"],2010:["January","Febuary","March"]}]
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
                                                            if (item > 0 and item <= daydata[0][z2]):
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
    def Personas(self):
        personaid=[["( You'r Skill ID )",-1],["Io",1],["Isis",2],["Hermès",3],["Trismégiste",4],["Oni",60]]
        skillid=[["( You'r Skill ID )",-1],["Agi",10],["Nu",89]]
        skillname={-1:"( You'r Skill ID )",10:"Agi",89:"Nu"}
        while True:
            try:
                answer = input("Choose personas slot (1-6) (put nothing to cancel): ")
                answer = int(answer)
                if answer >= 1 and answer <= 6:
                    while True:
                        command=input(f"(type help to see comand) (Personas slot {answer} editing): ").lower()
                        if command == None:
                            pass
                        elif command == "edit persona":
                            while True:
                                counter=0
                                print("Choose new personas (put nothing to cancel):")
                                for i in personaid:
                                    counter+=1
                                    print(f"    {counter} : {i[0]}")
                                persona_answer=input("")
                                try:
                                    persona_answer=int(persona_answer)
                                    if persona_answer > 0 and persona_answer <= len(personaid) and personaid[persona_answer-1][1] != -1:
                                        personas_new_value = int.from_bytes(binascii.unhexlify((personaid[persona_answer-1][1]).to_bytes(2, byteorder='little').hex()+"01"),byteorder="big")
                                    elif persona_answer > 0 and persona_answer <= len(personaid):
                                        while True:
                                            persona_input_id = input("Persona ID (put nothing to cancle) (bad Persona ID could crash the game): ")
                                            try:
                                                persona_input_id = int(persona_input_id)
                                                if persona_input_id >= 0:
                                                    personas_new_value = int.from_bytes(binascii.unhexlify((persona_input_id).to_bytes(2, byteorder='little').hex()+"01"),byteorder="big")
                                                    break
                                            except:
                                                if persona_input_id == "":
                                                    break
                                    verify_bool=False
                                    for verify in self.Data["personavalueid"]["persona"]:
                                        if verify != self.Data["personavalueid"]["persona"][answer-1]:
                                            if self.LoadByNameN(self.js, "UInt32Property", 0,verify) == personas_new_value:
                                                verify_bool = True
                                    if verify_bool == False:
                                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, personas_new_value,self.Data["personavalueid"]["persona"][answer-1])
                                        break
                                    elif verify_bool == True:
                                        print("\n\nCan't have double persona")
                                except Exception as e:
                                    if persona_answer == "":
                                        break
                        elif command == "edit level":
                            while True:
                                new_level=input("Choose persona's level (99 max) (put nothing to cancel): ")
                                try:
                                    new_level=int(new_level)
                                    if new_level > 0 and new_level <= 99:
                                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, new_level,self.Data["personavalueid"]["level"][answer-1])
                                        break
                                except Exception as e:
                                    print(e)
                                    if new_level == "":
                                        break
                        elif command == "edit exp":
                            while True:
                                new_exp=input("Choose persona's exp (4294967295 max) (put nothing to cancel): ")
                                try:
                                    new_exp=int(new_exp)
                                    if new_exp > 0 and new_exp <= 4294967295:
                                        self.js=self.SaveByNameN(self.js, "UInt32Property", 0, new_exp,self.Data["personavalueid"]["exp"][answer-1])
                                        break
                                except:
                                    if new_exp == "":
                                        break
                        elif command == "edit skill":
                            skill_process=["skill_slot_1","skill_slot_2","skill_slot_3","skill_slot_4"]
                            skill_list=[]
                            try:
                                for skill_i in skill_process:
                                    if skill_i == "skill_slot_4":
                                        pass
                                    skill_tmp=self.LoadByNameN(self.js, "UInt32Property", 0,self.Data["personavalueid"][skill_i][answer-1])
                                    skill_tmp=binascii.hexlify(int.to_bytes(skill_tmp,4,byteorder="big")).decode()
                                    if skill_tmp[0:4] != "0000":
                                        skill_list.append(int(skill_tmp[0:4],16))
                                    if skill_tmp[4:len(skill_tmp)] != "0000":
                                        skill_list.append(int(skill_tmp[4:len(skill_tmp)],16))
                            except:
                                pass
                            while True:
                                print("Skills : (type ('add' to add skill and 'del 'numero'' to remove skill) (you can't add to an non-empty place)")
                                counter = 0
                                for iss in skill_list:
                                    counter+=1
                                    try:
                                        print(f"    {counter} : {skillname[iss]}")
                                    except:
                                        print(f"    {counter} : {iss}")
                                command2 = input("Add or Del skill: ")
                                try:
                                    if command2.split(" ")[0].lower() == "del":
                                        if len(command2.split(" ")) > 1:
                                            if int(command2.split(" ")[1]) > 0 and int(command2.split(" ")[1]) <= len(skill_list):
                                                counter2=0
                                                lenn=len(skill_list)
                                                for ibn in range(lenn):
                                                    counter2+=1
                                                    if counter2 == int(command2.split(" ")[1]):
                                                        del skill_list[ibn]
                                                        break
                                    elif command2 == "add" and len(skill_list) < 8:
                                        while True:
                                            counter2=0
                                            for ibn in skillid:
                                                counter2+=1
                                                print(f"    {counter2} : {ibn[0]}")
                                            skill2_answer=input()
                                            try:
                                                skill2_answer=int(skill2_answer)
                                                if skill2_answer > 0 and skill2_answer <= len(skillid):
                                                    if skillid[skill2_answer-1][1] > -1:
                                                        skill_list.append(skillid[skill2_answer-1][1])
                                                    else:
                                                        while True:
                                                            skill_input_id = input("Skill ID (put nothing to cancle) (bad Skill ID could crash the game): ")
                                                            try:
                                                                skill_input_id = int(skill_input_id)
                                                                if skill_input_id >= 0:
                                                                    skill_list.append(skill_input_id)
                                                                    break
                                                            except:
                                                                if skill_input_id == "":
                                                                    break
                                                    break
                                            except Exception as e:
                                                print(e)
                                                if skill2_answer == "":
                                                    break
                                    elif command2 == "":
                                        print(True)
                                        counter=0
                                        val1=""
                                        val2=""
                                        val3=""
                                        val4=""
                                        for iuio in skill_list:
                                            counter+=1
                                            if counter < 3:
                                                val1+=(iuio).to_bytes(2, byteorder='big').hex()
                                            elif counter < 5:
                                                val2+=(iuio).to_bytes(2, byteorder='big').hex()
                                            elif counter < 7:
                                                val3+=(iuio).to_bytes(2, byteorder='big').hex()
                                            else:
                                                val4+=(iuio).to_bytes(2, byteorder='big').hex()
                                            
                                        if val1 != "":
                                            self.js=self.SaveByNameN(self.js, "UInt32Property", 0, int(val1,16),self.Data["personavalueid"]["skill_slot_1"][answer-1])
                                        else:
                                            self.js=self.DelByNameN(self.js, "UInt32Property", 0,self.Data["personavalueid"]["skill_slot_1"][answer-1])
                                        if val2 != "":
                                            self.js=self.SaveByNameN(self.js, "UInt32Property", 0, int(val2,16),self.Data["personavalueid"]["skill_slot_2"][answer-1])
                                        else:
                                            self.js=self.DelByNameN(self.js, "UInt32Property", 0,self.Data["personavalueid"]["skill_slot_2"][answer-1])
                                        if val3 != "":
                                            self.js=self.SaveByNameN(self.js, "UInt32Property", 0, int(val3,16),self.Data["personavalueid"]["skill_slot_3"][answer-1])
                                        else:
                                            self.js=self.DelByNameN(self.js, "UInt32Property", 0,self.Data["personavalueid"]["skill_slot_3"][answer-1])
                                        if val4 != "":
                                            print(True)
                                            self.js=self.SaveByNameN(self.js, "UInt32Property", 0, int(val4,16),self.Data["personavalueid"]["skill_slot_4"][answer-1])
                                            print(False)
                                        else:
                                            self.js=self.DelByNameN(self.js, "UInt32Property", 0,self.Data["personavalueid"]["skill_slot_4"][answer-1])
                                        break
                                except:
                                    pass
                        elif command == "edit stats":
                            varr=["Fo","Ma","En","Ag","Ch"]
                            fomaenag = ""
                            ch = ""
                            for inns in varr:
                                while True:#_ch
                                    inputt=input(f"Set new {inns} (max 99): ")
                                    try:
                                        inputt=int(inputt)
                                        if inputt > 0 and inputt < 100:
                                            if inns == "Ch":
                                                ch = self.js=self.SaveByNameN(self.js, "UInt32Property", 0, inputt,self.Data["personavalueid"]["ch"][answer-1])
                                                break
                                            else:
                                                fomaenag+=(inputt).to_bytes(1, byteorder='little').hex()
                                                break
                                    except:
                                        pass
                            
                            self.js=self.SaveByNameN(self.js, "UInt32Property", 0, int.from_bytes(binascii.unhexlify(fomaenag),byteorder="big"),self.Data["personavalueid"]["fo_ma_en_ag"][answer-1])
                                            
                        elif command=="print":
                            print("")
                            stat_show = False
                            skill_show = False
                            for i in self.Data["personavalueid"].keys():
                                if (i == "fo_ma_en_ag" or i == "ch"):
                                    if (stat_show == False):
                                        print("stats")
                                        stat_show=True
                                elif ("skill_slot_" in i):
                                    if (skill_show == False):
                                        print("skill")
                                        skill_show = True
                                else:
                                    print(i)
                        elif command == "help":
                            print("")
                            print("back : to exit persona slot {answer} editing\nprint : show editable value\nedit 'value_name' : edit the value of 'value_name'")
                        elif command == "back":
                            break 
            except:
                if answer == "":
                    break
    
    def Money(self):
        while True:
            try:
                new_name=input("New Money (9999999 max | put nothing to cancel): ")
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
            #a=input("Persona3 Reload sav path : ").replace('"',"")
            a=r"C:\Users\Célestin\AppData\Roaming\Sega\P3R\Steam\76561198877134182\SaveData003.sav"
            a=OpenSave().Load(os.path.split(os.path.abspath(a))[0],0,os.path.split(os.path.abspath(a))[1],True)
        except FileNotFoundError:
            print("Bad path\n")
        except PermissionError:
            print("Permission error or Bad path error\n")
        except Exception as e:
            if "Failed to read HeaderProperty" in str(e):
                raise Exception("Invalid file format (not persona 3 reload GVAS)")
