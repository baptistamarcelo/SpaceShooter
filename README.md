# SpaceShooter

Assets: https://opengameart.org/content/space-shooter-redux

Sounds: https://www.kenney.nl/

Music: https://oblidivmmusic.blogspot.com/

## Install   
    pip install -r requirements.txt
  
## Run
    python main.py

## Known issues on MacOS
Pygame might present issues when running on MacOS, if you experience any problems see the potential fixes below:

* Partially-filled window  
    Move the window to force a refresh

* Game too slow
    * FIX 1 - enabling low resolution  
       Find the Python icon in the dock below
        > Right click on Python > Options > Show in Finder

       In Finder select the Python application
       
       >  Right click on Python > Get Info > check the box:

          Open in low resolution
    * FIX 2 - disabling background image
       > On `src/background.py` disable the line: 
           
          screen.blit(self.surface, (0, self.pos_y_1))
