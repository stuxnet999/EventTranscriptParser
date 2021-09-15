__author__ = "Abhiram Kumar" 

import json
import pandas as pd
import sqlite3
import argparse
import os

def BrowserHistoryParse(f):
    conn = sqlite3.connect(f)
    cursor = conn.cursor()
    BrowserHistoryTable = pd.read_sql_query("SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where tag_descriptions.tag_id = 1", conn)
    payload = BrowserHistoryTable['payload'].values.tolist()
    sid = BrowserHistoryTable['sid'].values.tolist()
    payload_navigation_URL = []
    payload_navigation_URL_time = []
    payload_navigation_URL_date = []
    true_sid = []
    for i in range(len(payload)):
        temp = json.loads(payload[i])
        if (temp['data'].__contains__("navigationUrl") == True) and len(temp['data']['navigationUrl']) > 0: 
            payload_navigation_URL.append(temp['data']['navigationUrl'])
            true_sid.append(sid[i])
            timestamp = (temp['data']['Timestamp']).replace("T", " ").replace("Z", "")
            timestamp = timestamp.split(" ")
            payload_navigation_URL_date.append(timestamp[0])
            payload_navigation_URL_time.append(timestamp[1] + " UTC")

    temp_dict = {'SID': true_sid,'Date': payload_navigation_URL_date, 'Time': payload_navigation_URL_time, 'VisitedURL': payload_navigation_URL}
    return temp_dict

def SoftwareInventory(f):
    conn = sqlite3.connect(f)
    SoftwareInventoryTable = pd.read_sql_query("""SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 31 and events_persisted.full_event_name="Microsoft.Windows.Inventory.Core.InventoryApplicationAdd")""", conn)
    payload = SoftwareInventoryTable['payload'].values.tolist()
    sid = SoftwareInventoryTable['sid'].values.tolist()
    Program_Name = []
    Path = []
    OSVersionAtInstallTime = []
    InstallDate = []
    AppVersion = []
    true_sid = []

    for i in range(len(payload)):
        temp = json.loads(payload[i])
        Program_Name.append(temp['data']['Name'])
        Path.append(temp['data']['RootDirPath'])
        OSVersionAtInstallTime.append(temp['data']['OSVersionAtInstallTime'])
        if len(temp['data']['InstallDate']) > 0:
            InstallDate.append(temp['data']['InstallDate'] + " UTC")
        else:
            InstallDate.append("NULL")
        AppVersion.append(temp['data']['Version'])
        true_sid.append(sid[i])

    SoftwareInventorydict = {'SID': true_sid, 'Program Name': Program_Name, 'Install Path': Path, 'Install Date': InstallDate, 'Program Version': AppVersion, 'OS Version at Install Time': OSVersionAtInstallTime}
    return SoftwareInventorydict

def WlanScanResults(f):
    conn = sqlite3.connect(f)
    cursor = conn.cursor()
    wlan_scan_results_table = pd.read_sql_query("""SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 11 and events_persisted.full_event_name = "WlanMSM.WirelessScanResults")""", conn)
    payload = wlan_scan_results_table['payload'].values.tolist()
    sid = wlan_scan_results_table['sid'].values.tolist()
    ssid = []
    mac_addr = []
    time = []
    true_sid = []

    for i in range(len(payload)):
        temp = json.loads(payload[i])
        scan_results_list = temp['data']['ScanResults'].split('\n')
        for j in range(len(scan_results_list) - 1):
            temp_list = scan_results_list[j].split('\t')
            ssid.append(temp_list[0])
            mac_addr.append(temp_list[2])
            time.append(temp['time'])
            true_sid.append(sid[i])

    WlanScanDict = {'SID': true_sid, 'Time': time, 'SSID': ssid, 'MAC Address': mac_addr}
    return WlanScanDict

def UserDefault(f, file):
    conn = sqlite3.connect(f)
    user_default_table = pd.read_sql_query("""SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 11 and events_persisted.full_event_name = "Census.Userdefault")""", conn)
    payload = user_default_table['payload'].values.tolist()
    sid = user_default_table['sid'].values.tolist()
    true_sid = []
    temp_file = open(file, "w")
    for i in range(len(payload)):
        temp = json.loads(payload[i])
        temp_file.write("Device Make: " + temp['ext']['protocol']['devMake'] + "\n")
        temp_file.write("Device Model: "+ temp['ext']['protocol']['devModel']+ "\n")
        temp_file.write("Timezone: "+ temp['ext']['loc']['tz'] + "\n")
        true_sid.append(sid[i])
        temp_file.write("Default Browser: "+ temp['data']['DefaultBrowserProgId'] + "\n")
        temp_list = temp['data']['DefaultApp'].split('|')
        for j in range(len(temp_list)):
            temp_file.write(temp_list[j]+ "\n")
        temp_file.write("----------------------------------\n\n")
    return temp_file

def PhysicalDiskInfo(f, file):
    conn = sqlite3.connect(f)
    physicaldisk_info_table = pd.read_sql_query("""SELECT events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 11 and events_persisted.full_event_name = "Microsoft.Windows.Inventory.General.InventoryMiscellaneousPhysicalDiskInfoAdd")""", conn)
    payload = physicaldisk_info_table['payload'].values.tolist()
    temp_file = open(file, "w")
    for i in range(len(payload)):
        temp = json.loads(payload[i])
        temp_file.write("Device Id: "+ temp['data']['DeviceId'] + "\n")
        temp_file.write("Serial Number: "+ temp['data']['SerialNumber'] + "\n")
        temp_file.write("Size (in bytes): "+ temp['data']['Size'] + "\n")
        temp_file.write("Number of partitions: "+ str(temp['data']['NumPartitions']) + "\n")
        temp_file.write("Bytes per sector: "+ str(temp['data']['BytesPerSector']) + "\n")
        temp_file.write("Media type: "+ temp['data']['MediaType'] + "\n")
        temp_file.write("----------------------------------\n\n")
    return temp_file

def WiFiConnectedEvents(f):
    conn = sqlite3.connect(f)
    wifi_connected_events_table = pd.read_sql_query("""SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 11 and events_persisted.full_event_name = "Microsoft.OneCore.NetworkingTriage.GetConnected.WiFiConnectedEvent")""", conn)
    payload = wifi_connected_events_table['payload'].values.tolist()
    sid = wifi_connected_events_table['sid'].values.tolist()
    interfaceGuid = []
    interfaceType = []
    interfaceDescription = []
    ssid = []
    authAlgo = []
    bssid = []
    apManufacturer = []
    apModelName = []
    apModelNum = []
    true_sid = []

    for i in range(len(payload)):
        temp = json.loads(payload[i])
        interfaceGuid.append(temp['data']['interfaceGuid'])
        interfaceType.append(temp['data']['interfaceType'])
        interfaceDescription.append(temp['data']['interfaceDescription'])
        ssid.append(temp['data']['ssid'])
        authAlgo.append(temp['data']['authAlgo'])
        bssid.append(temp['data']['bssid'])
        apManufacturer.append(temp['data']['apManufacturer'])
        apModelName.append(temp['data']['apModelName'])
        apModelNum.append(temp['data']['apModelNum'])
        true_sid.append(sid[i])

    wifi_connected_results_dict = {'SID': true_sid, 'SSID': ssid, 'BSSID': bssid, 'AP Manufacturer': apManufacturer, 'AP Model Name': apModelName, 'AP Model No.': apModelNum, 'Interface Type': interfaceType, 'Interface GUID': interfaceGuid, 'Interface Description': interfaceDescription}
    return wifi_connected_results_dict

def PnPDeviceParse(f):
    conn = sqlite3.connect(f)
    pnp_device_table = pd.read_sql_query("""SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 11 and events_persisted.full_event_name = "Microsoft.Windows.Inventory.Core.InventoryDevicePnpAdd")""", conn)
    payload = pnp_device_table['payload'].values.tolist()
    sid = pnp_device_table['sid'].values.tolist()
    true_sid = []
    installdate = []
    firstinstalldate = []
    model = []
    manufacturer = []
    service = []
    parent_id = []
    object_id = []

    for i in range(len(payload)):
        temp = json.loads(payload[i].encode('unicode_escape'))
        true_sid.append(sid[i])
        parent_id.append(temp['data']['ParentId'])
        object_id.append(temp['data']['baseData']['objectInstanceId'])
        installdate.append(temp['data']['InstallDate'])
        firstinstalldate.append(temp['data']['FirstInstallDate'])
        model.append(temp['data']['Model'])
        manufacturer.append(temp['data']['Manufacturer'])
        service.append(temp['data']['Service'])
    pnp_device_dict = {'SID': true_sid, 'Object ID': object_id, 'Install Date': installdate, 'First Install Date': firstinstalldate, 'Model': model, 'Manufacturer': manufacturer, 'Service': service, 'Parent ID': parent_id}
    return pnp_device_dict


if __name__=="__main__":

    event_transcript_parser=argparse.ArgumentParser(
    description='''EventTranscript.db parser by Abhiram Kumar.''',
    epilog= '''For any queries, please reach out to me via Twitter - @_abhiramkumar''')
    
    event_transcript_parser.add_argument('-f','--file', required=True, help="Please specify the path to EventTranscript.db")
    event_transcript_parser.add_argument('-o','--output-dir', required=True, help="Please specify the output directory")
    
    parser, empty_list = event_transcript_parser.parse_known_args()


    print("""\033[1;97m  _____                 _     _____                              _       _     ____                          
 | ____|_   _____ _ __ | |_  |_   _| __ __ _ _ __  ___  ___ _ __(_)_ __ | |_  |  _ \ __ _ _ __ ___  ___ _ __ 
 |  _| \ \ / / _ \ '_ \| __|   | || '__/ _` | '_ \/ __|/ __| '__| | '_ \| __| | |_) / _` | '__/ __|/ _ \ '__|
 | |___ \ V /  __/ | | | |_    | || | | (_| | | | \__ \ (__| |  | | |_) | |_  |  __/ (_| | |  \__ \  __/ |   
 |_____| \_/ \___|_| |_|\__|   |_||_|  \__,_|_| |_|___/\___|_|  |_| .__/ \__| |_|   \__,_|_|  |___/\___|_|   
                                                                  |_|                                        \033[0m\n""")
    
    print("Author: Abhiram Kumar (Twitter: @_abhiramkumar)\nGithub: https://github.com/stuxnet999/EventTranscriptParser\n")
    print("-"*50)

    if os.path.exists(parser.file):
        if not os.path.isdir(parser.output_dir):
            os.makedirs(parser.output_dir)

        BrowsingHistory = BrowserHistoryParse(parser.file)
        df = pd.DataFrame(BrowsingHistory)
        outfile = os.path.join(parser.output_dir, "BrowserHistory.csv")
        df.to_csv(outfile, index=False) 
        print ("Output written to " + os.path.abspath(outfile))

        software_inventory = SoftwareInventory(parser.file)
        df = pd.DataFrame(software_inventory)
        outfile = os.path.join(parser.output_dir, "SoftwareInventory.csv")
        df.to_csv(outfile, index=False)
        print ("Output written to " + os.path.abspath(outfile))

        WlanScan = WlanScanResults(parser.file)
        df = pd.DataFrame(WlanScan)
        outfile = os.path.join(parser.output_dir, "WlanScan.csv")
        df.to_csv(outfile, index=False)
        print ("Output written to " + os.path.abspath(outfile))

        pnp_device = PnPDeviceParse(parser.file)
        df = pd.DataFrame(pnp_device)
        outfile = os.path.join(parser.output_dir, "PnpDeviceInstall.csv")
        df.to_csv(outfile, index=False)
        print ("Output written to " + os.path.abspath(outfile))
        
        wificonnectedevents = WiFiConnectedEvents(parser.file)
        df = pd.DataFrame(wificonnectedevents)
        outfile = os.path.join(parser.output_dir, "WiFiConnectedEvents.csv")
        df.to_csv(outfile, index=False)
        print ("Output written to " + os.path.abspath(outfile))

        outfile = os.path.join(parser.output_dir, "UserDefaults.txt")
        userdefaults = UserDefault(parser.file, outfile)
        print ("Output written to " + os.path.abspath(outfile))
        userdefaults.close()
            
        outfile = os.path.join(parser.output_dir, "PhysicalDiskInfo.txt")
        physical_disk_info = PhysicalDiskInfo(parser.file, outfile)
        print ("Output written to " + os.path.abspath(outfile))
        physical_disk_info.close()

    else:
        print(parser.print_help())
