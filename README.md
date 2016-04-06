Reading glasses for people with visual impairment
=================================================

Motivation
----------

A teacher at the Faculty of Automation and Computer Science / UPB suggested they had worked on a similar project, but did not follow through with a viable prototype. He told of the research they did, mainly interviewing people with severe visual impairment. To be more specific, an old couple, both with total blindness. When asked what they'd wish for the most, their reply was (and this is a paraphrase) : "I wish I could read. A newspaper, the medicine bottle's label, a book, anything.".

While there are books in Braille (and in more efficient tactile alphabets), they have to be specially ordered and they’re much bigger than their printed counterparts. Additionally, a source such as a newspaper would cost a lot to print daily in Braille: a specialised printer, installing and assigning someone to ensure image captions are either left out or supplemented, plus you couldn’t print it on low quality paper, you need a cardboard.

Moreover, even if there are a lot of applications for smartphones and desktop computers, a lot of the information “outdoors” (especially in Romania) comes in the form of written or printed text.

This small project tries to answer the above problems by making a cheap, yet profficient device prototype that could help a visually impaired person do what most of us take for granted: read.

Principle
---------

The device should be head-mounted. For starters, I've literally strapped a webcamera to my forehead to test this. For a better prototype, I've found some cheapo "spycams" that double as webcams if you plug them in a USB port (most of them even have microphones).

Holding an item (newspaper, book, receipt, etc) should prompt it to track it (meanshift), apply an OCR on the image (or the smaller region of interest), and then read it out loud (via text-to-speech) for the user.


Stuff used
----------

[Python 2.7](https://www.python.org/)

[OpenCV 2](http://opencv.org/)

[PyTesseract](https://pypi.python.org/pypi/pytesseract/0.1) and [Google Tesseract](https://github.com/tesseract-ocr)

[pyttsx](https://pypi.python.org/pypi/pyttsx) and [eSpeak](http://espeak.sourceforge.net/)