import os
import re
import traceback
import sys

fix_path=os.path.dirname(os.path.abspath(__file__))
def analyze(file):
    templist=[line.strip() for line in open(os.path.join(fix_path,file)) if line.strip()!=""]

    nandid =templist[templist.index('NAND Configuration:')+1].split()[1]
    config_code = '0016LT'
    regulatory_num = "A2649"
    clrc = 'A'
    lcm=templist[templist.index('Test Name: ["Display" | "Read_LCM_SN_from_diags" | ""]')+3]
    lcm_sn =lcm[13:33]+lcm[48:51]

    alert_sn='Error**'
    receiver_1='Error**'
    wifivendor='Error**'
    for i,item in enumerate(templist):
        try:
                
            if '(RX ==> Dut):syscfg print Mod#' in item:
                mpn =templist[i+1]
            elif '(RX ==> Dut):syscfg print MLB#' in item:
                mlbsn=templist[i+1]
            elif 'Reading Arc SN' in item:
                alert_sn=re.findall('Reading Arc SN \((.*)\)',item)[0]
            elif '(RX ==> Dut):syscfg print Regn' in item:
                region_code=templist[i+1]
            elif '(RX ==> Dut):syscfg print MdlC' in item:
                receiver_1=re.findall('receiver_1=(.*?);',templist[i+1])[0]
                wifivendor = re.findall('wifi_module_vendor=(.*)', templist[i + 1])[0]
            elif ": Read_Back_SN" in item:
                back_nvm_barcode=re.findall('Serial Number: (.*)',templist[i+3])[0]
            elif "(RX ==> Dut):NANDInfoTool" in item:
                nandidvendor=re.findall('Vendor:\s+(.*)',templist[i+2])[0]
            elif "(RX ==> Dut):nandcsid" in item:
                nandid=re.findall('FCE0 = (.*)',templist[i+2])[0]
            elif ": Read_Front_SN_From_Diag" in item:
                front_nvm_barcode = re.findall('Serial Number: (.*)', templist[i + 3])[0]
            elif "(RX ==> Dut):wifi --properties module-revision" in item:
                wifiver=re.findall('V=(.*)\"', templist[i + 1])[0]
            elif "pack-sn: " in item:
                battery_sn=re.findall('pack-sn: \"(.*)\"', item)[0]
            elif ": Read_Banff_SN_From_Diag" in item:
                juliet_sn=re.findall('Serial Number: (.*)', templist[i+3])[0]
            elif "(RX ==> Dut):sn" in item:
                fatp_sn=re.findall('Serial: (.*)',templist[i+1])[0]
        except Exception as E1:
            print("Error :",file, os.linesep, traceback.format_exc())
 
    flex_8 = ''
    pearl_sn=''
    coil_sn=''
    back_nvm_barcode1=''
    file=open(os.path.join(fix_path,'GU_Info.csv'),'a')
    file.write('USN,KEYNAME,KEYVALUE\n')
    file.write(fatp_sn+',back_nvm_barcode1,*\n')
    file.write('back_nvm_barcode1*,back_nvm_barcode,' + back_nvm_barcode+'\n')
    file.write(fatp_sn + ',mlbsn,' + mlbsn + '\n')
    file.write(fatp_sn + ',config_code,' + config_code + '\n')
    file.write(fatp_sn + ',regulatory_num,' + regulatory_num + '\n')
    file.write(fatp_sn + ',flex_8,*\n')
    file.write('flex_8*,coil_sn,'+coil_sn+'\n')
    file.write(fatp_sn + ',mpn,' + mpn + '\n')
    file.write(fatp_sn + ',region_code,' + region_code + '\n')
    file.write(fatp_sn + ',battery_sn,' + battery_sn + '\n')
    file.write(fatp_sn + ',lcm_sn,' + lcm_sn + '\n')
    file.write(fatp_sn + ',pearl_sn,*\n')
    file.write('pearl_sn*,juliet_sn,'+juliet_sn+'\n')
    file.write('pearl_sn*,front_nvm_barcode,' + front_nvm_barcode + '\n')
    file.write(fatp_sn + ',nandid::' + nandid + ','+nandidvendor+'\n')
    file.write(fatp_sn + ',wifivendor::' + wifiver + ','+wifivendor+'\n')
    file.write(mlbsn + ',nandid::' + nandid + ','+nandidvendor+'\n')
    file.write(mlbsn + ',fgsn,' + fatp_sn+'\n')
    file.write(fatp_sn + ',alert_sn,' + alert_sn + '\n')
    file.write(fatp_sn + ',clrc,' + clrc + '\n')
    file.write(fatp_sn + ',receiver_1,' + receiver_1 + '\n')
    file.write(lcm_sn[:17] +',fgsn,*\n')
    file.write('\n')
    file.close()


print(fix_path)

file = open(os.path.join(fix_path, 'GU_Info.csv'), 'w')
file.close()
templist=os.listdir(fix_path)
for file in templist:
    if file.endswith('.txt') :
        print(file)
        analyze(file)