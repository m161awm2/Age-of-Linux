# main.py
import curses
from game import run

curses.wrapper(run)