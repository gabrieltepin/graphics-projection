from PIL import Image
import numpy as np
import sys
import os

def projection(backgroundPath, texturePath, coordinates):
    def texture_color(x, y, w, h, c):
        return c[round(x) % w, -round(y) % h]

    def linear_equation_resolver(X, Y):
        A = np.array([
            [ X[0][0], X[0][1], X[0][2], 0, 	  0, 	   0, 		0, 		 0, 	  0, 	   -Y[0][0], 0, 	   0,        0        ],
            [ 0, 	   0, 		0, 		 X[0][0], X[0][1], X[0][2], 0, 		 0, 	  0, 	   -Y[0][1], 0, 	   0, 	     0        ],
            [ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		X[0][0], X[0][1], X[0][2], -Y[0][2], 0, 	   0,        0        ],

            [ X[1][0], X[1][1], X[1][2], 0, 	  0, 	   0, 	 	0, 		 0, 	  0, 	   0, 		 -Y[1][0], 0, 	     0        ],
            [ 0, 	   0, 		0, 		 X[1][0], X[1][1], X[1][2], 0, 		 0, 	  0, 	   0, 		 -Y[1][1], 0, 	     0        ],
            [ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		X[1][0], X[1][1], X[1][2], 0, 		 -Y[1][2], 0, 	     0        ],

            [ X[2][0], X[2][1], X[2][2], 0, 	  0, 	   0, 		0, 		 0, 	  0, 	   0, 		 0, 	   -Y[2][0], 0        ],
            [ 0, 	   0, 		0, 		 X[2][0], X[2][1], X[2][2], 0, 		 0, 	  0, 	   0, 		 0, 	   -Y[2][1], 0        ],
            [ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		X[2][0], X[2][1], X[2][2], 0, 		 0, 	   -Y[2][2], 0        ],

            [ X[3][0], X[3][1], X[3][2], 0, 	  0, 	   0, 		0, 		 0, 	  0, 	   0, 		 0, 	   0, 	     -Y[3][0] ],
            [ 0, 	   0,		0,	 	 X[3][0], X[3][1], X[3][2], 0, 		 0, 	  0, 	   0, 		 0, 	   0, 	     -Y[3][1] ],
            [ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		X[3][0], X[3][1], X[3][2], 0, 		 0, 	   0, 	     -Y[3][2] ],

            [ 0, 	   0, 		0, 		 0, 	  0, 	   0, 		0, 		 0, 	  0, 	   1, 		 0, 	   0, 	    0 ]
        ])

        B = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])

        try: 
            S = np.linalg.solve(A, B)
        except:
            print('Singular Matrix, no determined solution')

        return np.linalg.inv(np.array([
            [S[0], S[1], S[2]],
            [S[3], S[4], S[5]],
            [S[6], S[7], S[8]]
        ]))

    print("Projecting " + texturePath + " into " + backgroundPath)

    try:
        background = Image.open(backgroundPath)
    except:
        print ("Could not open/read file: " + backgroundPath)
        sys.exit()
    
    try:
        texture = Image.open(texturePath)
    except:
        print ("Could not open/read file: " + texturePath)
        sys.exit()

    texture_width, texture_height = texture.size
    texture_colors = texture.load()
    texture_coordinates = [
        [0,texture_height-1,1],
        [texture_width-1,texture_height-1,1],
        [texture_width-1,0,1],
        [0,0,1],
    ]

    background_width, background_height = background.size
    background_coordinates = [[coordinate[0], coordinate[1], 1] for coordinate in coordinates]

    # resolving the linear equation for the projection matrix
    tranformation = linear_equation_resolver(texture_coordinates, background_coordinates)

    # iterating over background image pixels
    for x_background in range(background_width):
        for y_background in range(background_height):
            background_coordinate = (x_background, y_background, 1) # RP2

            # associated coordinates in texture
            texture_coordinate = np.dot(tranformation, background_coordinate) # RP2
            x_texture = texture_coordinate[0]/texture_coordinate[2]
            y_texture = texture_coordinate[1]/texture_coordinate[2] 

            # if texture rectangle inside boundaries then apply color
            if 0 < x_texture and x_texture < texture_width and 0 < y_texture and y_texture < texture_height:
                background.putpixel(
                    (x_background,y_background), 
                    texture_color(x_texture, y_texture, texture_width, texture_height, texture_colors)
                )
    
    texture_title = os.path.splitext(texturePath)[0].split("/")[1]
    background_title = os.path.splitext(backgroundPath)[0].split("/")[1]

    # resultPath = "results/"+texturePath.split("/")[1]+'in'+backgroundPath.split("/")[1]
    resultPath = "results/" + texture_title + "_in_" + background_title + ".jpeg"
    print("Projection saved in " + resultPath + "\n")
    background.save(resultPath)
    return background
