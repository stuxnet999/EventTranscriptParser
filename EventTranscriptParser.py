__author__ = "Abhiram Kumar P (stuxnet999)"

import json
import os
from unittest import result
import sqlalchemy as sql
import sqlalchemy.orm as sql_orm
import csv
import argparse

def EdgeBrowsingHistory(session, output_directory):
    result = session.execute(sql.text('SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = "1" and events_persisted.full_event_name LIKE "%Aria.218d658af29e41b6bc37144bd03f018d.Microsoft.WebBrowser.HistoryJournal%")'))
    history_events = result.fetchall()

    if len(history_events) == 0:
        print("Microsoft Edge browsing history events not recorded in this database. Will not create CSV")
        return
    else:
        print("{} events related to browsing history from MS Edge found. Extracting & writing to CSV. Note - Some events might not contain URLs and will be skipped.".format(len(history_events)))
        browsinghistory_csv = open(os.path.join(output_directory, "Edge Browsing History.csv"), "w", newline='')
        browsinghistory_csv_writer = csv.writer(browsinghistory_csv, dialect='excel')
        browsinghistory_csv_writer.writerow(["Visited URL", "Visit Timestamp (UTC)", "Refer URL", "SID"])

        for events in history_events:
            row_list = []
            temp_json = json.loads(events[1])

            if 'navigationUrl' in temp_json['data']:
                row_list.append(temp_json['data']['navigationUrl'])
                row_list.append(temp_json['data']['Timestamp'].replace("T"," ").replace("Z",""))

                if 'referUrl' in temp_json['data']:
                    row_list.append(temp_json['data']['referUrl'])
                else:
                    row_list.append("")
                
                row_list.append(events[0])
                browsinghistory_csv_writer.writerow(row_list)
        browsinghistory_csv.close()
    return

def ApplicationInventory(session, output_directory):
    result = session.execute(sql.text('SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 31 and events_persisted.full_event_name="Microsoft.Windows.Inventory.Core.InventoryApplicationAdd")'))
    application_inventory = result.fetchall()

    if len(application_inventory) == 0:
        print("Application inventory events not recorded in this database. Will not create CSV")
    else:
        print("{} events related to application inventory found. Extracting & writing to CSV".format(len(application_inventory)))
        application_inventory_csv = open(os.path.join(output_directory,"Application Inventory.csv"),"w", newline='')
        application_inventory_csv_writer = csv.writer(application_inventory_csv, dialect='excel')
        application_inventory_csv_writer.writerow(["Application Name", "Installation Directory", "Installation Timestamp (UTC)", "Publisher", "Application Version", "SID"])

        for apps in application_inventory:
            row_list = []
            temp_json = json.loads(apps[1])
            row_list.append(temp_json['data']['Name'])
            row_list.append(temp_json['data']['RootDirPath'])
            row_list.append(temp_json['data']['InstallDate'])
            row_list.append(temp_json['data']['Publisher'])
            row_list.append(temp_json['data']['Version'])
            row_list.append(apps[0])
            if len(set(row_list)) != 1:
                application_inventory_csv_writer.writerow(row_list)
        application_inventory_csv.close()
    return

def ApplicationExecution(session, output_directory):
    result = session.execute(sql.text('SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 25 and events_persisted.full_event_name="Win32kTraceLogging.AppInteractivitySummary")'))
    execution_list = result.fetchall()

    if len(execution_list) == 0:
        print("Win32k.TraceLogging.AppInteractivitySummary not recorded in this database. Will not create CSV")
    else:
        print("{} events related to application execution found. Extracting & writing to CSV".format(len(execution_list)))
        execution_list_csv = open(os.path.join(output_directory, "Application Execution.csv"), "w", newline='')
        execution_list_csv_writer = csv.writer(execution_list_csv, dialect='excel')
        execution_list_csv_writer.writerow(["Binary Name", "Execution Timestamp (UTC)", "SHA1 Hash", "Compiler Timestamp (UTC)", "SID"])

        for binaries in execution_list:
            row_list = []
            temp_json = json.loads(binaries[1])
            temp_binary_list = temp_json['data']['AppId'].split('!')

            if temp_binary_list[0][0] == "W":
                binary_hash = temp_binary_list[1][4:]
                compiler_timestamp = temp_json['data']['AppVersion'].split('!')[0].replace("/","-").replace(":", " ", 1)
                binary_name = temp_json['data']['AppVersion'].split('!')[2]
            elif temp_binary_list[0][0] == "U":
                binary_hash = ""
                compiler_timestamp = temp_json['data']['AppVersion'].split('!')[1].replace("/","-").replace(":", " ", 1)
                binary_name = temp_json['data']['AppVersion'].split('!')[3]

            row_list.append(binary_name)
            row_list.append(temp_json['time'].replace("T"," ").replace("Z",""))
            row_list.append(binary_hash)
            row_list.append(compiler_timestamp)
            row_list.append(binaries[0])
            execution_list_csv_writer.writerow(row_list)
        execution_list_csv.close()
    return

def UserDefaults(session, txt_dir):
    result = session.execute(sql.text('SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 11 and events_persisted.full_event_name = "Census.Userdefault")'))
    defaults_list = result.fetchall()
    if len(defaults_list) == 0:
        print("Device census events relating to user default settings not recorded in database. Will not create text file")
    else:
        print("{} events related to user default app preferences found. Extracting and writing to text file".format(len(defaults_list)))
        userdefaults_file = open(os.path.join(txt_dir, "UserDefaults.txt"), "w")
        for defaults in defaults_list:
            temp_json = json.loads(defaults[1])
            userdefaults_file.write("====Record Start====\n")
            userdefaults_file.write("Recorded at: " + temp_json['time'].replace("T", " ").replace("Z", "") + "\n")
            userdefaults_file.write("Default browser: " + temp_json['data']['DefaultBrowserProgId'] + "\n")
            userdefaults_file.write("---Default Apps---")
            temp_list = temp_json['data']['DefaultApp'].split('|')
            for apps in temp_list:
                userdefaults_file.write(apps + "\n")
            userdefaults_file.write("====Record End====\n")
        userdefaults_file.close()
    return

def WiFiConnectedEvents(session, csv_dir):
    result = session.execute(sql.text('SELECT events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 11 and events_persisted.full_event_name = "Microsoft.OneCore.NetworkingTriage.GetConnected.WiFiConnectedEvent")'))
    wifi_connections_list = result.fetchall()

    if len(wifi_connections_list) == 0:
        print("WiFi connection events have not been recorded in the database. Will not create CSV")
    else:
        print("{} events associated with successful WiFi connections found. Extracting and writing to CSV".format(len(wifi_connections_list)))

        wifi_connections_file = open(os.path.join(csv_dir, "WiFi Successful Connections.csv"), "w", newline='')
        wifi_connections_csv_writer = csv.writer(wifi_connections_file, dialect='excel')
        wifi_connections_csv_writer.writerow(["WiFi SSID", "WiFi BSSID", "WiFi Connection Time (UTC)", "AP Manufacturer", "AP Model Name", "AP Model No.", "Authentication Algorithm", "Cipher Algo"])

        for wifi in wifi_connections_list:
            row_list = []
            temp_json = json.loads(wifi[0])
            row_list.append(temp_json['data']['ssid'])
            row_list.append(temp_json['data']['bssid'])
            row_list.append(temp_json['time'].replace('T', " ").replace('Z', ""))
            row_list.append(temp_json['data']['apManufacturer'])
            row_list.append(temp_json['data']['apModelName'])
            row_list.append(temp_json['data']['apModelNum'])
            row_list.append(temp_json['data']['authAlgo'])
            row_list.append(temp_json['data']['cipherAlgo'])
            wifi_connections_csv_writer.writerow(row_list)
        wifi_connections_file.close()
    return

def SRUMAppActivity(session, csv_dir):
    result = session.execute(sql.text('SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 24 and events_persisted.full_event_name = "Microsoft.Windows.SRUM.Telemetry.AppTimelines")'))
    srum_app_activity_list = result.fetchall()

    if (len(srum_app_activity_list) == 0):
        print("Application activity fetched from SRUM not recorded in database. Will not create CSV")
    else:
        print("{} events associated with application activity within SRUM found. Extracting and writing to CSV".format(len(srum_app_activity_list)))
        SRUMAppActivity_file = open(os.path.join(csv_dir, "SRUM Application Execution Activity.csv"), "w", newline='')
        SRUMAppActivity_csv_writer = csv.writer(SRUMAppActivity_file, dialect='excel')

        SRUMAppActivity_csv_writer.writerow(["SID", "EventTranscriptDB Record Time (UTC)", "Application Start Time (UTC)", "Application Name", "Compiler Timestamp (UTC)"])

        for event in srum_app_activity_list:
            temp_json = json.loads(event[1])

            for apps in temp_json['data']['records']:
                row_list = []
                row_list.append(event[0])
                row_list.append(temp_json['time'].replace("T", " ").replace("Z",""))
                row_list.append(apps['startTime'].replace("T", " ").replace("z", ""))

                if "W:" in apps['appId']:
                    row_list.append(apps['appId'][4:])
                    row_list.append(apps['appVer'].split('!', 1)[0].replace("/", "-").replace(":", " ", 1))
                elif "U:" in apps['appId']:
                    row_list.append(apps['appId'][2:])
                    row_list.append(apps['appVer'].split('!')[1].replace("/", "-").replace(":", " ", 1))
                else:
                    row_list.append(apps['appId'])
                    row_list.append("N/A")
                SRUMAppActivity_csv_writer.writerow(row_list)
        SRUMAppActivity_file.close()
    return

def WLANScanResults(session, csv_dir):
    result = session.execute(sql.text('SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 11 and events_persisted.full_event_name = "WlanMSM.WirelessScanResults")'))
    wlan_scan_list = result.fetchall()

    if len(wlan_scan_list) == 0:
        print("Events associated with WLAN (WiFi) scan not recorded in database. Will not create CSV")
    else:
        print("{} events associated to WLAN scan found in database. Extracting and writing to CSV".format((len(wlan_scan_list))))

        wlan_scan_file = open(os.path.join(csv_dir, "WLAN Scan Results.csv"), "w", newline='')
        wlan_scan_csv_writer = csv.writer(wlan_scan_file, dialect='excel')

        wlan_scan_csv_writer.writerow(["SSID", "MAC Address", "Scan Record Timestamp (UTC)", "Interface GUID"])

        for scan in wlan_scan_list:
            temp_json = json.loads(scan[1])

            for devices in temp_json['data']['ScanResults'].split('\n'):
                row_list = []
                wlan_scan_entry = devices.split('\t')
                if wlan_scan_entry[0] != '':
                    row_list.append(wlan_scan_entry[0])
                    row_list.append(wlan_scan_entry[2])
                    row_list.append(temp_json['time'].replace("T", " ").replace("Z", ""))
                    row_list.append(temp_json['data']['InterfaceGuid'])
                    wlan_scan_csv_writer.writerow(row_list)
                else:
                    continue
        wlan_scan_file.close()
    return

def SRUMNetworkUsageActivity(session, csv_dir):
    result = session.execute(sql.text('SELECT events_persisted.sid, events_persisted.payload from events_persisted inner join event_tags on events_persisted.full_event_name_hash = event_tags.full_event_name_hash inner join tag_descriptions on event_tags.tag_id = tag_descriptions.tag_id where (tag_descriptions.tag_id = 24 and events_persisted.full_event_name = "Microsoft.Windows.SrumSvc.DataUsageAggregateTimer")'))
    network_usage_list = result.fetchall()

    if len(network_usage_list) == 0:
        print("Events associated with application network usage (from SRUM) not recorded in database. Will not create CSV.")
    else:
        print("{} events associated to App network usage found. Extracting and writing to CSV".format((len(network_usage_list))))

        network_usage_file = open(os.path.join(csv_dir, "SRUM Application Network Usage.csv"), "w", newline='')
        net_usage_csv_writer = csv.writer(network_usage_file, dialect='excel')

        net_usage_csv_writer.writerow(["Event Recorded Timestamp (UTC)", "Application Name", "Bytes Sent", "Bytes Received", "Interface GUID", "SID"])

        for event in network_usage_list:
            row_list = []
            temp_json = json.loads(event[1])
            row_list.append(temp_json['time'].replace("T"," ").replace("Z", ""))
            row_list.append(temp_json['data']['applicationName'])
            row_list.append(temp_json['data']['bytesSent'])
            row_list.append(temp_json['data']['bytesRecieved'])
            row_list.append(temp_json['data']['interfaceGuid'])
            row_list.append(event[0])
            net_usage_csv_writer.writerow(row_list)
        network_usage_file.close()
    return

if __name__=="__main__":
    event_transcript_parser=argparse.ArgumentParser(
    description='''EventTranscript.db parser by Abhiram Kumar.''',
    epilog= '''For any queries, please reach out to me via Twitter - @_abhiramkumar''')
    
    event_transcript_parser.add_argument('-f','--file', required=True, help="Please specify the path to EventTranscript.db")
    event_transcript_parser.add_argument('-o','--output-dir', required=True, help="Please specify the output directory")

    args = event_transcript_parser.parse_args()

    print("Windows Diagnostic Data - EventTranscript.db Parser\n")
    
    print("Author: Abhiram Kumar (Twitter: @_abhiramkumar)\nGitHub: https://github.com/stuxnet999/EventTranscriptParser")
    print("-"*50 + "\n")

    if os.path.exists(args.file):
        if not os.path.isdir(args.output_dir):
            os.makedirs(args.output_dir)
        
        db_path = args.file
        out_dir = args.output_dir
        engine = sql.create_engine('sqlite:///{}'.format(db_path))
        Session = sql_orm.sessionmaker(engine)
        session = Session()

        EdgeBrowsingHistory(session, out_dir)
        ApplicationInventory(session, out_dir)
        ApplicationExecution(session, out_dir)
        UserDefaults(session, out_dir)
        WiFiConnectedEvents(session, out_dir)
        SRUMAppActivity(session, out_dir)
        WLANScanResults(session, out_dir)
        SRUMNetworkUsageActivity(session, out_dir)