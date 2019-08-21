from xml.dom.minidom import parse
import pandas as pd
import itertools
dom=parse("G:\music\休止符测试2.xml")
rootdata=dom.documentElement
metronomes=rootdata.getElementsByTagName('metronome')
times=rootdata.getElementsByTagName('time')
measures=rootdata.getElementsByTagName('measure')
# 读取速率
for metronome in metronomes:
    per_minute=metronome.getElementsByTagName("per-minute")[0]
    per_minute=per_minute.childNodes[0].data
    per_minute=int(per_minute)
#读取节拍
for time in times:
    beat_type=time.getElementsByTagName("beat-type")[0]
    beat_type=beat_type.childNodes[0].data
    beat_type=int(beat_type)
parts = []
v_durations=[]
v_staffs=[]
v_steps = []
v_octaves = []
v_alter=[]
#提取音符开始的时刻
for measure in measures:
    durations = []
    staffs = []
    if measure.hasAttribute("number"):
        parts.append(measure.getAttribute("number"))
        itemlists = measure.getElementsByTagName('note')
        for itemlist in itemlists:
            duration = itemlist.getElementsByTagName("duration")[0]
            durations.append(duration.childNodes[0].data)
            staff = itemlist.getElementsByTagName("staff")[0]
            staffs.append(staff.childNodes[0].data)
            pitchs=itemlist.getElementsByTagName('pitch')
            steps = []
            octaves = []
            alters=[]
            for pitch in pitchs:
                if len(pitch.getElementsByTagName("step"))>0:
                    step=pitch.getElementsByTagName("step")[0]
                    steps.append(step.childNodes[0].data)
                else:
                    steps.append(0)
                if len(pitch.getElementsByTagName("octave"))>0:
                    octave=pitch.getElementsByTagName("octave")[0]
                    octaves.append(octave.childNodes[0].data)
                else:
                    octaves.append(0)
                if len(pitch.getElementsByTagName("alter"))>0:
                    alter=pitch.getElementsByTagName("alter")[0]
                    alters.append(alter.childNodes[0].data)
                else:
                    alters.append(0)
            v_steps.append(steps)
            v_octaves.append(octaves)
            v_alter.append(alters)
    v_durations.append(durations)
    v_staffs.append(staffs)
v_parts=[]
for i in parts:
    i=int(i)
    i=[i]*len(v_durations[i-1])
    v_parts.append(i)
v_steps=pd.DataFrame(v_steps)
v_octaves=pd.DataFrame(v_octaves)
v_alter=pd.DataFrame(v_alter)
v_parts= list(itertools.chain.from_iterable(v_parts))
v_durations= list(itertools.chain.from_iterable(v_durations))
v_staffs= list(itertools.chain.from_iterable(v_staffs))
v_durations=pd.DataFrame(v_durations)
v_staffs=pd.DataFrame(v_staffs)
v_parts=pd.DataFrame(v_parts)
data=pd.concat([v_parts,v_staffs,v_steps,v_octaves,v_alter,v_durations],axis=1)
data.columns=["part","track","step","octave","alter","time"]
data=data.fillna(0)
def key_number(j):
    if j=="A":
        j=49
    if j=="B":
        j=51
    if j=="C":
        j=40
    if j=="D":
        j=42
    if j=="E":
        j=44
    if j=="F":
        j=45
    if j=="G":
        j=47
    return j
fmat=lambda x:key_number(x)
data["step"]=data["step"].map(fmat)
fmat_int=lambda x:int(x)
data=data.applymap(fmat_int)
data["key"]=(data["octave"]-4)*12+data["step"]+data["alter"]
data["dete"]=data["step"].map(lambda x:1 if x>0 else 0)
data["key"]=data["key"]*data["dete"]
#分轨分别计算各自的音符起始时间
t=(60/per_minute)*(4/beat_type)
track1=data[data["track"]==1]
track1=track1.reset_index(drop=True)
track1["startime"]=track1["time"].cumsum()
track1["startmoment"]=(track1["startime"]-track1["time"])*t
track1["endmoment"]=track1["startime"]*t
track2=data[data["track"]==2]
track2=track2.reset_index(drop=True)
track2["startime"]=track2["time"].cumsum()
track2["startmoment"]=(track2["startime"]-track2["time"])*t
track2["endmoment"]=track2["startime"]*t
track1.to_excel("G:\music\\track1.xlsx")
track2.to_excel("G:\music\\track2.xlsx")









