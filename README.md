
VIRTUAL HAND-TRACKED KEYBOARD
===============================

Created using:
- OpenCV
- cvzone HandTrackingModule
- MediaPipe (via cvzone)
- Pillow (PIL)
- NumPy

This project implements a virtual keyboard that you can interact with using your hands via webcam.
It uses real-time hand tracking to detect finger gestures and simulate keyboard input.

-------------------
FEATURES
-------------------
✔ Real-time hand tracking via webcam  
✔ Alphabet, Number, and Special Character keyboards  
✔ Caps Lock support (⇪ key)  
✔ Mode switching via "123", "#@!", and "ABC"  
✔ Space and Delete keys  
✔ Unicode and special character support  
✔ Both hands supported for input  
✔ Placeholder text box (PIL-rendered) with overflow handling  
✔ Transparent buttons (adjustable via alpha blending)

-------------------
REQUIREMENTS
-------------------
Python 3.x

Install dependencies:

pip install opencv-python
pip install cvzone
pip install numpy
pip install pillow

-------------------
FILES
-------------------
- complex.py          : The full implementation of the virtual keyboard
- Arial Unicode.ttf   : Font file used to support Unicode characters (place in the same directory)
- README.txt          : This documentation

-------------------
HOW TO RUN
-------------------
1. Connect a webcam
2. Run the main script:

   python complex.py     OR      python3 complex.py

3. Show your hand to the webcam.
4. Use your index finger to hover over keys.
5. Pinch your thumb and index finger together to "click" a key.
6. Type with either hand.
7. Press 'q' to quit.

-------------------
NOTES
-------------------
- The keyboard starts in "Alphabet" mode.
- Press "⇪" to toggle caps lock (alphabet only).
- Press "123" for numbers, "#@!" for special characters, and "ABC" to return to alphabets.
- The placeholder text box handles long input and displays it cleanly.

-------------------
TO CUSTOMIZE
-------------------
- To change keyboard layouts: edit `keys_alpha`, `keys_numeric`, `keys_special` in the code.
- To adjust transparency: modify `alpha` in the `Button.draw()` method.
- To save text input: modify the `finaltext` logic at the end of the script.

-------------------
CREDITS
-------------------
Developed by Heeta Bhanushali  
Hand tracking powered by cvzone + MediaPipe  
Keyboard rendering via OpenCV + PIL

-------------------
LICENSE
-------------------
This project is open-source for personal and educational use only.
