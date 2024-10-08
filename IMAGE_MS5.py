import numpy as np
import cvzone.HandTrackingModule
from cvzone.HandTrackingModule import HandDetector
import numpy
import cv2
import serial

q1 = [46.01166532, 44.79925415, 43.56785109, 42.31855603, 41.05257326, 39.77121793, 38.47592396, 37.16825234,
      35.8498997, 34.52270604, 33.18866114, 31.84990843, 30.50874556, 29.16762055, 27.82912293, 26.49596931,
      25.17098312, 23.85706899, 22.55718223, 21.27429467, 20.01135822, 18.77126783, 17.5568255, 16.37070706,
      15.21543312, 14.09335018, 13.00659223, 11.95709989, 10.94659393, 9.976580441, 9.048355832, 8.163016047,
      7.321469111, 6.524450142, 5.772538016, 5.066172921, 4.405674194, 3.791257926, 3.223053917, 2.70112172,
      2.225465543, 1.796047898, 1.412801926, 1.075642378, 0.7844752698, 0.5392062412, 0.3397476705, 0.1860246009,
      0.0779795294, 0.01557610976, -0.001198190283, 0.02766955227, 0.1022183591, 0.222513, 0.3886426385, 0.6007184492,
      0.8588701703, 1.16324154, 1.513984559, 1.911252508, 2.355191658, 2.84593159, 3.383574084, 3.968180519,
      4.599757781, 5.278242716, 6.003485209, 6.775230061, 7.593097926, 8.456565693, 9.364946798, 10.31737212,
      11.31277227, 12.34986208, 13.42712845, 14.54282244, 15.6949567, 16.88130916, 18.09943358, 19.34668274, 20.6202118,
      21.91704202, 23.23407642, 24.56814612, 25.91605339, 27.27461493, 28.64070289, 30.01128214, 31.38344203,
      32.7544216, 34.12162787, 35.48264707, 36.83524947, 38.17738851, 39.50719552, 40.82297111, 42.12317439,
      43.40641135, 44.67142297, 45.91706832, 47.14233755]
q2 = [71.51401771, 70.9053654, 70.33316285, 69.79876067, 69.30351968, 68.84880293, 68.43596568, 68.06634287,
      67.74123388, 67.46188453, 67.22946649, 67.04505443, 66.90960161, 66.82391459, 66.7886284, 66.80418308, 66.8708032,
      66.9884814, 67.15696719, 67.37576183, 67.64411972, 67.96105644, 68.32536297, 68.73562544, 69.19024924,
      69.68748684, 70.22546446, 70.80221541, 71.41570613, 72.06386405, 72.74460215, 73.45584068, 74.19552547,
      74.96164303, 75.7522323, 76.56539342, 77.39929363, 78.25217075, 79.12233452, 80.00816616, 80.90811642,
      81.82070246, 82.74450372, 83.67815713, 84.62035169, 85.56982263, 86.52534534, 87.48572895, 88.44980989,
      89.41644522, 90.384506, 91.3528705, 92.3204175, 93.28601939, 94.24853545, 95.206805, 96.15964058, 97.10582122,
      98.04408577, 98.97312636, 99.89158212, 100.7980331, 101.690995, 102.5689138, 103.4301622, 104.2730365,
      105.0957546, 105.8964568, 106.6732074, 107.4239995, 108.1467627, 108.8393735, 109.4996693, 110.1254669,
      110.7145837, 111.2648632, 111.7742034, 112.2405877, 112.6621181, 113.0370468, 113.3638117, 113.6410611,
      113.8676812, 114.0428153, 114.1658762, 114.2365514, 114.2548001, 114.2208435, 114.1351481, 113.9984034,
      113.811496, 113.5754807, 113.2915515, 112.9610121, 112.5852491, 112.1657065, 111.7038644, 111.2012198,
      110.6592717, 110.0795128, 109.463404]
q3 = [41.9407235188107, 42.5979138336871, 43.2937762415001, 44.027357802091, 44.7974945767784, 45.602813249295,
      46.4417357490884, 47.3124872502746, 48.2131077918112, 49.1414677163055, 50.0952870441917, 51.0721587801702,
      52.0695759871104, 53.084962262425, 54.1157050242534, 55.1591907787532, 56.2128413213626, 57.2741496537647,
      58.340714303094, 59.4102707326949, 60.4807186447623, 61.5501441898579, 62.616836396804, 63.679297486767,
      64.7362470987149, 65.7866189281432, 66.8295617482174, 67.8644169817757, 68.890712503788, 69.9081442547557,
      70.9165585112442, 71.9159336469193, 72.9063620922679, 73.8880330524094, 74.8612163935274, 75.8262479707944,
      76.7835165513254, 77.7334523880476, 78.6765174249351, 79.6131970593104, 80.5439933502165, 81.4694195399942,
      82.3899957459107, 83.3062456769401, 84.2186942349724, 85.1278658676486, 86.0342835499675, 86.9384682824734,
      87.8409390042483, 88.7422128284057, 89.6428055158458, 90.5432321093658, 91.4440076546183, 92.3456479367586,
      93.2486701618448, 94.1535935101308, 95.0609394843403, 95.9712319698959, 96.8849969160358, 97.8027615370141,
      98.7250529215307, 99.6523959267333, 100.585310221424, 101.524306332639, 102.469880542176, 103.42250847691,
      104.382637241598, 105.350675958299, 106.326984606127, 107.31186110262, 108.305526636902, 109.308109357896,
      110.31962663912, 111.339966283466, 112.368867191562, 113.40590018589, 114.450449844867, 115.501698336791,
      116.558612330233, 117.619936268025, 118.684179962029, 119.749633680162, 120.814368587576, 121.876254436217,
      122.932981738171, 123.982089857218, 125.021000006615, 126.047051848889, 127.057542217763, 128.049764437291,
      129.021046793437, 129.96878889638, 130.890494924457, 131.783803025249, 132.646510431358, 133.47659410073,
      134.272226897236, 135.031789479867, 135.753878170183, 136.43730713329, 137.081117229212]
q4 = [90.00000166, 90.00000124, 90.00000122, 90.00000121, 90.00000119, 90.00000118, 90.00000116, 90.00000115,
      90.00000113, 90.00000111, 90.00000109, 90.00000107, 90.00000105, 90.00000103, 90.00000101, 90.00000098,
      90.00000096, 90.00000094, 90.00000091, 90.00000089, 90.00000086, 90.00000084, 90.00000081, 90.00000078,
      90.00000076, 90.00000531, 90.00000512, 90.00000493, 90.00000473, 90.00000454, 90.00000435, 90.00000415,
      90.00000396, 90.00000376, 90.00000357, 90.00000337, 90.00000318, 90.00000298, 90.00000278, 90.00000259,
      90.00000239, 90.00000219, 90.00000199, 90.00000179, 90.00000159, 90.00000139, 90.00000119, 90.00000098,
      90.00000078, 90.00000057, 90.00000036, 90.00000016, 89.99999995, 89.99999974, 89.99999953, 89.99999931,
      89.9999991, 89.99999888, 89.99999867, 89.99999845, 89.99999824, 89.99999802, 89.9999978, 89.99999758, 89.99999737,
      89.99999715, 89.99999693, 89.99999672, 89.99999651, 89.99999629, 89.99999609, 89.99999588, 89.99999568,
      89.99999548, 89.99999529, 89.9999951, 89.99999492, 89.99999474, 89.99999457, 89.99999923, 89.99999921,
      89.99999919, 89.99999917, 89.99999915, 89.99999913, 89.99999911, 89.99999909, 89.99999908, 89.99999906,
      89.99999905, 89.99999903, 89.99999902, 89.99999901, 89.99999899, 89.99999898, 89.99999897, 89.99999896,
      89.99999895, 89.99999894, 89.99999224, 89.99999218]

try:
    ser = serial.Serial('COM4', 9600)
    print("arduino tamam ")
except:
    print(" Connecttt arduinooooo")

cap = cv2.VideoCapture(0)
success, initial = cap.read()
cv2.imwrite("frame%d.jpg", initial)
cv2.imshow("captured", initial)

detector = HandDetector(detectionCon=0.8, maxHands=2)
Left = False
Right = False
Both_flag = False
iter_left = 0
iter_right = 0
iter_both = 0

while True:

    # Get image frame
    success, img = cap.read()
    img = cv2.addWeighted(img, 1.5, np.zeros_like(img), 0, 0)  # brightening
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_histo = cv2.equalizeHist(gray_image)

    cv2.imshow('original', img)
    cv2.imshow('gray', gray_image)
    cv2.imshow('histogram', gray_histo)

    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    cv2.imshow('img', img)
    # hands = detector.findHands(img, draw=False)  # without draw
    if hands:

        # Hand 1

        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        if len(hands) != 2:
            print(handType1)
            if handType1 == "Left":
                iter_left = iter_left + 1
                if iter_left == 20 and not Left:
                    print("Left")
                    iter_left = 0
                    iter_right = 0
                    iter_both = 0
                    message = "Left#"
                    ser.write(message.encode())
                    print("Left sent")
                    Right = False
                    Left = True
                    Both_flag = False
            else:
                iter_right = iter_right + 1
                if iter_right == 20 and not Right:
                    print("Right")
                    iter_left = 0
                    iter_right = 0
                    iter_both = 0
                    message = "Right#"
                    ser.write(message.encode())
                    print("right sent")
                    Left = False
                    Right = True
                    Both_flag = False
            # fingers1 = detector.fingersUp(hand1)
        else:
            iter_both = iter_both + 1
            if iter_both == 20 and not Both_flag:
                print("Both")
                iter_left = 0
                iter_right = 0
                iter_both = 0
                message = "Both#"
                ser.write(message.encode())
                print("Both sent")

                Left = False
                Right = False
                Both_flag = True

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()
