from xml.dom.minidom import parse
import xml.etree.ElementTree as ET
#xml文件删除节点
parts=[]
staffs=[1,2]
def xml_new(xml):
    for i in staffs:
        dom = parse(xml)
        rootdata = dom.documentElement
        measures = rootdata.getElementsByTagName('measure')
        for measure in measures:
            if measure.hasAttribute("number"):
                itemlists = measure.getElementsByTagName('note')
                parts.append(measure.getAttribute("number"))
                for itemlist in itemlists:
                    staff = itemlist.getElementsByTagName("staff")[0]
                    if int(staff.childNodes[0].data)==i:
                        measure.removeChild(itemlist)
        with open("G:\music\\staff"+str(i)+".xml", 'w', encoding='utf-8') as f:
            dom.writexml(f, addindent='\t', newl='\n', encoding='utf-8')
def Druation(x):
    dom = parse(x)
    rootdata = dom.documentElement
    attributes=rootdata.getElementsByTagName('attributes')
    times=rootdata.getElementsByTagName('time')
    for attribute in attributes:
        standard=attribute.getElementsByTagName("divisions")[0]
        standard=standard.childNodes[0].data
        standard=int(standard)
    for time in times:
        beat=time.getElementsByTagName("beats")[0]
        beat=beat.childNodes[0].data
        beat=int(beat)
    durations=standard*beat
    return durations

#xml增加节点以及属性
#staff1
def staff1(staff1,durations):
    tree = ET.parse(staff1)
    root = tree.getroot()
    newNodeStr = 'note'
    newNode = ET.Element(newNodeStr)
    newNoderest= ET.Element('rest')
    newNodeName = ET.Element('duration')
    newNodeName.text =str(durations)
    newNodestaff = ET.Element('staff')
    newNodestaff.text = '1'
    newNode.append(newNoderest)
    newNode.append(newNodeName)
    newNode.append(newNodestaff)
    for i in range(int(len(parts)/len(staffs)-1)):
        root[-1][i+1].insert(0, newNode)
    root[-1][0].insert(3, newNode)
    tree.write('G:\music\\new_staff2.xml',encoding="utf-8",xml_declaration=True)
#staff2

def staff2(staff2,durations):
    tree = ET.parse(staff2)
    root = tree.getroot()
    newNodeStr = 'note'
    newNode = ET.Element(newNodeStr)
    newNoderest= ET.Element('rest')
    newNodeName = ET.Element('duration')
    newNodeName.text =str(durations)
    newNodestaff = ET.Element('staff')
    newNodestaff.text = '2'
    newNode.append(newNoderest)
    newNode.append(newNodeName)
    newNode.append(newNodestaff)
    for i in range(int(len(parts)/len(staffs)-1)):
        root[-1][i].insert(50, newNode)
    root[-1][int(len(parts)/len(staffs)-1)].insert(-1, newNode)
    tree.write('G:\music\\new_staff1.xml',encoding="utf-8",xml_declaration=True)

if __name__ == '__main__':
    xml="G:\music\休止符测试2.xml"
    xml_1="G:\music\\staff1.xml"
    xml_2="G:\music\\staff2.xml"
    durations=Druation(xml)
    xml_path=xml_new(xml)
    durations1=staff1(xml_1,durations)
    durations2=staff2(xml_2,durations)



