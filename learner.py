from ctypes import windll
# work around for high dpi stuff
user32 = windll.user32
user32.SetProcessDPIAware()
import pytesseract
import time
import pyautogui as pg
import cv2
import numpy as np
from PIL import ImageGrab, Image
import os
import csv

def start_screen_difference(screen, bounds, base_img):
	# home bounds are a tuple of numbers for the slice. This is probably going to change.
	partial = screen[bounds[0]:bounds[1],bounds[2]:bounds[3]]
	total_img = np.subtract(partial,base_img)
	return int(np.sum(np.sum(total_img)))
	
def determine_score(screen, bounds,previous_score):
	partial = screen[bounds[0]:bounds[1],bounds[2]:bounds[3]]
	partial = cv2.cvtColor(partial, cv2.COLOR_BGR2GRAY)
	ret, partial = cv2.threshold(partial, 180, 255, cv2.THRESH_BINARY_INV)
	score_str = pytesseract.image_to_string(Image.fromarray(partial), config='-l eng --oem 1 --psm 3')

	if score_str.isdigit() and int(score_str) > previous_score:
		return int(score_str)

	return previous_score

def main(): 
	
	pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract' # locate pytesseract for score recognition
	frame_bounds = (0,240,3840,2060) # set frame bounds for game in full screen browser. Represents actual pyautogui coordinates
	home_bounds = (260,610,1300,2150) # set bounds for homescreen identification. Currently represents slice values in tuple format
	score_bounds = (1700,1775,205,450)
	start_button_loc = (1929,1280) # pyautogui coordinates for start button click
	finish_time = time.time() + 14400 # current time + four hours
	home_base_img = cv2.imread("home_base.png") # comparison image for home page. Need to change if home_bounds tuple changes.
	round_num = 0

	# perform the play/learn cycle for a set amount of time
	while time.time() < finish_time:

		# open a csv file to write positions to
		csv_path = "training_locations\\" + str(round_num) + ".csv"
		csv_handle = open(csv_path, "w")
		csv_writer = csv.writer(csv_handle)

		# create a directory to save images to
		saved_images_directory = "training_images\\" + str(round_num)
		os.mkdir(saved_images_directory)

		# press the button to start a round. Currently has to be started manually the first time.
		print("CLICKING START")
		pg.click(x=start_button_loc[0], y=start_button_loc[1])
		time.sleep(2) # wait for screen fade to start acting

		time_step = 0
		score = 0

		current_screen = np.array(ImageGrab.grab(bbox=frame_bounds))
		# while the start screen isn't the current screen
		while start_screen_difference(current_screen,home_bounds,home_base_img) != 0:
			# write full size image out
			cv2.imwrite((saved_images_directory + "\\" + str(time_step) + ".jpg"), current_screen)
			cursor_pos = pg.position()
			# TODO: add speed capabilities and add to csv
			# NOTE: score is not written to csv because determining score in round causes framerate issues
			csv_writer.writerow([cursor_pos[0],cursor_pos[1]])


			# save position and score for training	

			# predict action
			# take action

			# new screen grab
			current_screen = np.array(ImageGrab.grab(bbox=frame_bounds))
			time_step += 1

		round_num += 1
		csv_handle.close()

		# training

if __name__ == '__main__':
    main()