# Harvard CS50's Introduction to Computer Science Final Project

This is my final project for CS50 course. It doesn't have a particular name, but let's call it a TextHider.

# TextHider

The goal of the project was to create a program, that would be capable of hiding text messages in images.
And that's basically what this program does. The technique is called Steganography.

I decided to use the simplest approach, which is modifying the LSB (Least Significant Bit).
This Program only supports PNG files (Sorry). Nevertheless, it will tell you if your image's type or mode, format, etc 
is not supported.

As you can see, it consists of 3 python scripts: 

cover.py - covers the message in the image.
discover.py - (surprisingly) discovers the message from the image. 
helpers.py - just some common functions used in both scripts.
hack.py - will be a script that brute forcely tries to discover the message without the key.

The program has a CLI (Command Line Interface), and it shows what arguments it expects.

# Usage:

To install all the dependencies:

```bash
pip install -r requirements.txt
```


To cover your message in the image:

```bash
python3 cover.py hermione.png "I am a hacker" -o hidden-hermione.png
Key: R374L104O485
```

To discover your message from the image:

```bash
python3 discover.py hidden-hermione.png R374L104O485
```

# What the heck is key?

When you run cover.py with your PNG image, script will return you a key, that discover.py expects in order to discover the hidden message. So please, don't lose it.

Basically ,that's it, just clone this repository to your workspace and play around.

# CS50 rocks!

Thanks to CS50! Amazing Course, I' ve gained a lot of knowledge and become a much better software developer!
On to creating cool programs and changing the world!
