import cv2
import matplotlib.pyplot as plt

def crop_stats(f):
    img = cv2.imread(f)

    # Size of the image in pixels (size of orginal image) 
    # (This is not mandatory) 
    width = img.shape[1]
    height = img.shape[0]

    team_1_top_ratio = (1080 - 800) / 1080
    team_1_bottom_ratio = (1080 - 635) / 1080

    team_2_top_ratio = (1080 - 505) / 1080
    team_2_bottom_ratio = (1080 - 345) / 1080

    team_1_left_ratio = (1920 - 1075) / 1920
    team_1_right_ratio = (1920 - 1570) / 1920

    # Setting the points for cropped image 
    left = width - int(team_1_left_ratio * width)
    right = width - int(team_1_right_ratio * width)

    top_1 = int(team_1_top_ratio * height)
    bottom_1 = int(team_1_bottom_ratio * height)

    top_2 = int(team_2_top_ratio * height)
    bottom_2 = int(team_2_bottom_ratio * height)

    # Cropped image of above dimension 
    # (It will not change orginal image) 
    im1 = img[top_1 : bottom_1, left : right]
    im2 = img[top_2 : bottom_2, left : right]
    
    dir_1 = f.split('.')[0] + '_' + 'team1_stats.png' 
    dir_2 = f.split('.')[0] + '_' + 'team2_stats.png'

    # Shows the image in image viewer 
    cv2.imwrite(dir_1, im1)
    cv2.imwrite(dir_2, im2)

    return dir_1, dir_2

def crop_teams(f):
    img = cv2.imread(f)

    # Size of the image in pixels (size of orginal image) 
    # (This is not mandatory) 
    width = img.shape[1]
    height = img.shape[0]
    print(width, height)


    team_1_top_ratio = (1080 - 800) / 1080
    team_1_bottom_ratio = (1080 - 635) / 1080

    team_2_top_ratio = (1080 - 505) / 1080
    team_2_bottom_ratio = (1080 - 345) / 1080

    team_1_left_ratio = (1920 - 690) / 1920
    team_1_right_ratio = (1920 - 1035) / 1920

    # Setting the points for cropped image 
    left = width - int(team_1_left_ratio * width)
    right = width - int(team_1_right_ratio * width)

    print(left, right)

    top_1 = int(team_1_top_ratio * height)
    bottom_1 = int(team_1_bottom_ratio * height)

    top_2 = int(team_2_top_ratio * height)
    bottom_2 = int(team_2_bottom_ratio * height)

    # Cropped image of above dimension 
    # (It will not change orginal image) 
    im1 = img[top_1 : bottom_1, left : right]
    im2 = img[top_2 : bottom_2, left : right]
    
    # Shows the image in image viewer 
    cv2.imwrite(f.split('.')[0] + '_' + 'team1_names.png',im1)
    cv2.imwrite(f.split('.')[0] + '_' + 'team2_names.png',im2)
