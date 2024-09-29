import sys
from PhotoSaver import PhotoSaver

user_input = input('Enter VK user ID: ')
if user_input.isdigit():
    user_id = int(user_input)
else:
    print('Incorrect user id')
    sys.exit()

user_input = input('Enter album id (profile (default), wall, saved ): ')
if user_input == '':
    album_id = 'profile'
elif user_input in ['', 'profile', 'wall', 'saved']:
    album_id = user_input
else:
    print('Incorrect album id')
    sys.exit()

user_input = input('How many photos to save? (default - 5) : ')
if user_input == '':
    photo_count = 5
elif user_input.isdigit() and int(user_input) > 0:
    photo_count = int(user_input)
else:
    print('Incorrect photo_count')
    sys.exit()

user_id = '36201576'
saver = PhotoSaver()
saver.save_photo(user_id, album_id, photo_count)
