# pyVcf2AsteriskPhonebook

Convert a google contacts vcf export to a csv in the format: "name";phone number; phone number

## RasPBX

### Install prerequisites

Connect via ssh  

    # apt install git python3-pip  

    # apt install emacs #(optional)  

Install python modules  

    # pip3 install lxml panoramisk vobject  

### Asterisk configuration

#### Alternative 1: Edit files

Edit manager.conf  

    # emacs /etc/asterisk/manager.conf

Uncomment line to include new file

>include manager_custom.conf

Create new file  

    # emacs /etc/asterisk/manager_custom.conf

>[vcardimport]  
> secret = YourSecretPassword  
> permit = 127.0.0.1/255.255.255.0  
> write = system  

Restart asterisk  

    # rasterisk -x 'manager reload'  

or  

    # asterisk -r

    raspbx*CLI> core restart now

#### Alternative 2: Use web UI

Use the FreePBX web console to add the user vcardimport.  

This will make an entry in /etc/asterisk/manager_additional.conf, like  

>[vcardimport]  
>secret = YourSecretPassword  
>deny=0.0.0.0/0.0.0.0  
>permit=127.0.0.1/255.255.255.0  
>read = system,call,log,verbose,command,agent,user,config,dtmf,reporting,cdr,dialplan,originate  
>write = system,call,log,verbose,command,agent,user,config,dtmf,reporting,cdr,dialplan,originate  
>writetimeout = 100  

### Install software

Download sources  

    # git clone https://github.com/jonsag/pyVcf2AsteriskPhonebook  
    # cd pyVcf2AsteriskPhonebook  

Copy config  

    # cp cp config.ini.example config.ini  

Edit config.ini entering your own variables  

    # emacs config.ini  
