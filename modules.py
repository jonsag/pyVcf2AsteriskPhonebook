#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import asyncio, configparser, json, os, re, sys, time, vobject

from panoramisk import Manager

config = configparser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

# handle errors
def onError(errorCode, extra):
    print("\nError:")
    if errorCode in(1, 2): # print error information, print usage and exit
        print(extra)
        usage(errorCode)
    elif errorCode in (3, 5, 7): # print error information and exit
        print(extra)
        sys.exit(errorCode)
    elif errorCode == 4: # print error information and return running program
        print(extra)
        return
        
# print usage information        
def usage(exitCode):
    print("\nUsage:")
    print("----------------------------------------")
    print("%s " % sys.argv[0])
    
    print("\n%s -i <path to vCard file>" % sys.argv[0])
    print("    Open file")
    
    print("\n%s -i <path to vCard file> -w " % sys.argv[0])
    print("    Open file and write/update asterisk database")
    
    print("\n%s -i <path to vCard file> -o <output file>" % sys.argv[0])
    print("    Open file and create a new file with lines like:")
    print('        "Name";Number;')
    
    print("\n%s -v" % sys.argv[0])
    print("    Verbose output")
    
    print("\n%s -h" % sys.argv[0])
    print("    Show help")

    sys.exit(exitCode)
    
def printVcard(vCardObject, verbose):
    print("----------")
    
    vCardObject.prettyPrint()

    print()
    print()
    
    print(vCardObject)
    
    print()
    print()
    
    print(vCardObject.contents)
    
    print()
    print()
    
    for key in vCardObject.contents:
        print(key)
        print(vCardObject.contents[key])

        data = vCardObject.contents[key]
        for obj in data:
            print(obj.value)
            
        print()

def tidyPhoneNumber(config, num):
  num = re.sub("^\+", "00", num)    # +39 -> 0039
  num = re.sub("\D", "", num)       # remove all non-digits
  if 'phone' in config:
    if 'nationalprefix' in config['phone']:
      num = re.sub("^" + config['phone']['nationalprefix'] + "0*", "0", num)    # strip own national prefix
    if 'domesticprefix' in config['phone']:
      num = re.sub("^[^0]", "0" + config['phone']['domesticprefix'], num)       # add domestic prefix, if missing
  return num

def processVCard(vCardObject, writeDB, outFile, lines, verbose):
    if "tel" in vCardObject.contents:
        print("\n----------\nFound telephone number...")

        name = ""
        num = ""
        line = ""
        
    
        for telNo in vCardObject.contents['tel']:
            if verbose:
                print("Before tidying: %s" % telNo.value)
                
            num = tidyPhoneNumber(config, telNo.value)
            
            if num and "fn" in vCardObject.contents:
                name = vCardObject.fn.value
            elif num and "org" in vCardObject.contents:
                name = vCardObject.org.value
                    
            if name and num:
                
                if writeDB:
                    line = '%s;%s;' % (name, num)
                    lines.append(line)
                    print("Adding/updating Number: %s Name: %s ..." % (num, name))
                if outFile:
                    line = '"%s";%s;' % (name, num)
                    lines.append(line)
                    print("Appending to file: %s" % line)
    
    return(lines)
        
async def writeToDB(lines, verbose):
    print("\n----------\nWriting to asterisk database...")
    
    ami = Manager(loop=asyncio.get_event_loop(), 
                    host = config['ami']['host'],
                    port = config['ami']['port'],
                    username = config['ami']['user'],
                    secret = config['ami']['pass'])
    
    await ami.connect()
    for line in lines:
        lineSplit = line.split(';')
        name = lineSplit[0].replace("'", "").replace("[", "").replace("]", "")
        num = lineSplit[1]
        if verbose:
            print("Adding name: %s \t Number: %s" % (name, num))      
        ami_result = await ami.send_action({"Action": "DBPut", "Family": "cidname", "Key": num, "Val": name})
        if verbose:
            print(ami_result.Response)
        else:
            print(".", end='')
    
    ami.close()
    if not verbose:
        print()
                
def readVcard(inFile, writeDB, outFile, verbose):
    print("Processing...")
    
    lines = []
    
    if verbose:
        print("----------")
    
    f = open(inFile, "r")
             
    vcard = vobject.readComponents(f)
    
    noOfCards = 1
    
    vo = next(vcard, None)

    while vo is not None:
        noOfCards += 1
        
        if verbose:
            printVcard(vo, verbose)
            
        lines = processVCard(vo, writeDB, outFile, lines, verbose)
        
        vo = next(vcard, None)
        
    if outFile and lines:
        fileName = "%s-%s.csv" % (outFile, time.strftime("%Y%m%d-%H%M%S"))
        f = open(fileName, "w")
        print("\n----------\nWriting to file...")
        
        for line in lines:
            f.write(line + "\n")
        f.close()
        
    if writeDB and lines:
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(writeToDB(lines, verbose))
        loop.close()
        
        
        
        
    if outFile:
        print("\n----------\nWrote %s entries to %s" % (noOfCards, fileName))
    elif writeDB:
        print("\n----------\nAdded/updated %s entries to asterisk phonebook" % noOfCards)
    else:
        print("\n----------\nNo of vcards: " % noOfCards)