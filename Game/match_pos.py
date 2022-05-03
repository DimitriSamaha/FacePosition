import cv2
import random as rand
import time
from manage import add_score, scan_face


def main(user:str):

    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    h, w = img.shape[:2]
    h = int(h*1.2)
    w = int(w*1.2)
    
    # initiate x and y
    x = rand.randint(20, w-200)
    y = rand.randint(20, h-200)
    
    start_time = time.time()
    # Initiate the score value to incriment it in the loop
    score = 0
    # Random flip img or not
    if rand.randint(0, 1) == 0:
        flip = True
    else:
        flip = False
    print("The image is flipped?", flip)
    # Win boolean
    won = True

    # Loop till score = 10
    while score != 10:
        if time.time() - start_time > 60:
            won = False
            break

        ret, img = cap.read()

        # Resize img
        img = cv2.resize(img, (w, h))

        # Flip the image horizontaly if flip==true
        if flip:
            img = cv2.flip(img, 1)

        # Get face data from scan_face function
        data_list = scan_face(img)

        # Get image
        img = data_list[0]

        # Wait two seconds before start
        if time.time() - start_time > 2:
            
            # check if there is only one face by checking that the data_list contains 3 arguments
            if len(data_list) == 3 :
                # Change the w and h of data_list to be realistic
                if data_list[2][0] > 200:
                    data_list[2][0] = (200)
                if data_list[2][1] > 200:
                    data_list[2][1] = (200)

                # check if the face is in the rectangle drawn to change coordinates
                if abs(data_list[1][0]  - x) < 20 and abs(data_list[1][1] - y) < 20:
                    score += 1
                    img[ :, :, 1] = 255
                    x = rand.randint(20, w-200)
                    y = rand.randint(20, h-200)
                    
                # Draw the rectangle
                cv2.rectangle(img, (x, y), (x+data_list[2][0], y+data_list[2][1]), (0, 255, 255),  4)

            # Write the score using puText()
            cv2.putText(img, "score: " + str(score), (30, 30), 1, 1, [255, 125, 0], 2)
            cv2.putText(img, "time: " + str(round((time.time()-start_time-2), 1)), (w-100, 30), 1, 1, [255, 125, 0], 2)
        # Write Username
        cv2.putText(img, f"{user}", (30,h-10), 4, 1, [255, 125, 0], 1)
        
        # cv2 functions to display the image
        cv2.imshow('Match the position', img)
        key = cv2.waitKey(1)
        if key == 32:
            won = False
            break
            

    # If score == 10 
    if won:
        # Calculate the time to reach score = 10  
        end_time = time.time()
        final_time = end_time - start_time - 2
        final_time = round(final_time, 1)
        # Print score at the end
        print("Your time to score 10 points was " + str(final_time) + " seconds")
        # Cheque if user is signed in to add in sql database
        if user[:4].lower() != "guest":
            add_score(user, "M", final_time)
        # Display score at the end
        img[ :, :, :] = 255
        cv2.putText(img, "Your final time is : ", (int(100*1.2) , int(200*1.2)), 1, 3, [0, 0, 0], 5)
        cv2.putText(img, str(final_time), (int(240*1.2), int(300*1.2)), 1, 5, [0, 0, 0], 5)
        cv2.imshow('Match the position', img)
        key = cv2.waitKey(5000)
        if key == 32:
            print("You left")
            exit()
        
    # If time > 60s and score != 10
    else:
        # Print score at the end
        print("You lost, you did only", str(score), "points")
        # Display score at the end
        img[ :, :, :] = 255
        cv2.putText(img, "You lost! You only did:", (int(80*1.2) , int(200*1.2)), 1, 3, [0, 0, 0], 5)
        cv2.putText(img, str(score), (int(180*1.2), int(300*1.2)), 1, 5, [0, 0, 0], 5)
        cv2.putText(img, "/10 points", (int(220*1.2), int(300*1.2)), 1, 3, [0, 0, 0], 5)
        cv2.imshow('Match the position', img)
        key = cv2.waitKey(5000)
        if key == 32:
            print("You left")
            exit()


if __name__ == "__main__":
    main("Guest")
