# pyVcf2AsteriskPhonebook

Convert a google contacts vcf export to a csv in the format: "name";phone number; phone number

## RasPBX

### Install prerequisites

Connect via ssh  

    # apt install git python3-pip  

    # apt install emacs #(optional)  

Install python modules  

    # pip3 install panoramisk vobject  

### Configuration

Edit manager.conf  

    # emacs /etc/asterisk/manager.conf

Uncomment line to include new file

>include manager_custom.conf

Create new file  

    # emacs /etc/asterisk/manager_custom.conf

>[carddavimport]  
> secret = YourSecretPassword  
> permit = 127.0.0.1/255.255.255.0  
> write = system  

Restart asterisk  

    # asterisk -r

    raspbx*CLI> core restart now  

### Install software

Download sources  

    # git clone https://github.com/jonsag/pyVcf2AsteriskPhonebook  
    # cd pyVcf2AsteriskPhonebook  

Copy config  

    # cp cp config.ini.example config.ini  

Edit config.ini entering your own variables  

    # emacs config.ini  

