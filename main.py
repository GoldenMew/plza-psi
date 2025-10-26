##* code created using https://github.com/azalea-w/plza-qse as a base

import os
from pathlib import Path
import sys
from pokecrypto import PokeCrypto
from lib.plaza.crypto import HashDB, SwishCrypto, FnvHash
from lib.plaza.types import HashDBKeys

PokeParty   =  FnvHash.hash_fnv1a_32("PokeParty_Data")

SRC_PATH = Path(__file__).parent

save_file_magic = bytes([
    0x17, 0x2D, 0xBB, 0x06, 0xEA
])
pokeBytes = 344
bufferBytes = 136
def main():
    print("PLZA Party Save Injector")
    print()
    file_path = input("Enter Save File Path: ")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    with open(file_path, "rb") as f:
        data = f.read()

    if not data.startswith(save_file_magic):
        print("File is not a PLZA save file")
        sys.exit(1)

    try:
        blocks = SwishCrypto.decrypt(data)
    except Exception as e:
        print(f"Error decrypting save file: {e}")
        sys.exit(1)

    print(f"> Decrypted {len(blocks)} Blocks. <")
    hash_db = HashDB(blocks)

    party_data = hash_db[PokeParty].data
    partyNo = 0
    for i in range(6):
        if not party_data[i*(pokeBytes+bufferBytes):i*(pokeBytes+bufferBytes)+1] == bytearray(b'\x00'):
            partyNo += 1
    def menu_loop():
        print(f"""
    You have {partyNo} Pokemon in your party.
    Options (Input the option number):
        1: Export Party Pokemon
        2: Import Party Pokemon
        3: Quit
    """)

        option = input(">>> ").strip()

        if option not in ["1", "2", "3"]:
            print("Invalid Option Picked!")

        if option == "3": return
        if option == "2":
            poke_path = input("Enter Pk9 File Path: ")
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return menuloop()
            with open(poke_path, "rb") as f:
                pokedata = f.read()
            try:
                pokedata = bytearray(pokedata)
            except:
                print("File is not a valid pk9 file")
                return menu_loop()
            if len(pokedata)<344:
                print("File is not a valid pk9 file")
                return menu_loop()
            print(f"Which Party Slot should the file be imported to?")
            slot = input(">>> ").strip()
            if slot not in ["1", "2", "3", "4", "5", "6"]:
                print("Invalid Option Picked!")
                return menu_loop()
            else:
                slotStart = 0+(int(slot)-1)*(pokeBytes+bufferBytes)
                slotEnd = pokeBytes+(int(slot)-1)*(pokeBytes+bufferBytes)
                party_data[slotStart:slotEnd] = PokeCrypto.EncryptArray9(pokedata)
                hash_db[PokeParty].change_data(party_data)
                output_path = file_path + "_modified"
                if os.path.exists(output_path):
                    print(f"{output_path} already exists! Please remove and try again.")
                    return menu_loop()
                else:
                    with open(output_path, "wb") as f:
                        f.write(SwishCrypto.encrypt(hash_db.blocks))
                    print(f"Modified file saved at {output_path}.")
                    return menu_loop()
                
        if option == "1":
            print(f"Which Party Slot should be exported?")
            slot = input(">>> ").strip()
            if slot not in ["1", "2", "3", "4", "5", "6"]:
                print("Invalid Option Picked!")
                return menu_loop()
            elif int(slot) > partyNo:
                print("Party Slot is empty.")
                return menu_loop()
            else:
                output_path = f"{file_path}_PartySlot{slot}.pk9"
                if os.path.exists(output_path):
                    print(f"{output_path} already exists! Please remove and try again.")
                    return menu_loop()
                else:
                    slotStart = 0+(int(slot)-1)*(pokeBytes+bufferBytes)
                    slotEnd = pokeBytes+(int(slot)-1)*(pokeBytes+bufferBytes)
                    pokeData = party_data[slotStart:slotEnd]
                    output = PokeCrypto.DecryptArray9(pokeData)
                    with open(output_path, "wb") as f:
                        f.write(output)
                    print(f"Exported Party Slot {slot} to {output_path}.")
                return menu_loop()
    menu_loop()
if __name__ == "__main__":
    main()
