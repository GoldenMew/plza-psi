# PLZA Party Save Injector
<sub>This project is not associated with TPC (The Pokémon Company), GameFreak, Nintendo nor any other entity.</sub>

---


## What's this?
A *very* simple save editor for PLZA for exporting and importing party pokemon as pk9 files using [plza-save-utils](https://github.com/azalea-w/plza-save-utils)


## Dependencies
- Python 3.13 (other versions of Python 3 should work too)

## How to use

1. Dump your save file using JKSV or similar
2. Copy your save file to your PC
3. Download latest release ZIP from the [Releases](https://github.com/azalea-w/plza-psi/releases) Section
4. Open your shell (powershell or cmd for windows)
5. Run the Script like `python <path/to/main.py>`!

When importing it will output a new file with `_modified` appended to the filename, just restore that save using JKSV or similar and you should be good to go!

When exporting it will output a new file with `_PartySlot` and the slot number you have chosen appended to the filename. This can be edited with a hex editor or by opening in the current version of pkhex (until pkhex is updated for PLZA, it will not be able to interpret the file correctly or limit you to legal choices. I recommend doing this with caution as the saved file will likely not be legal.).

## Thanks to:
- The maintainers of [PKHeX](https://github.com/kwsch/PKHeX/)
- https://github.com/azalea-w for creating plza-save-utils and plza-qse which this is created from.
- GameFreak for creating the game

(I am by no means an expert at this, and I have very little programming experience. I have thrown this together while awaiting the pkhex update)
