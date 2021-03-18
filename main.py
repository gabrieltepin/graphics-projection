from tools import homography

image1 = homography.projection('assets/guernica.jpeg', 'assets/homer.jpeg', [(34, 22), (392, 269), (395, 506), (38, 630)])

image2 = homography.projection('assets/army.jpeg', 'assets/cs.jpeg', [(383, 49), (440, 19), (447, 110), (388, 113)])
