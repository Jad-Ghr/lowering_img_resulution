import struct


#....................................................Mix_the_photo...............................................


def mix(row2,width,div):
    row1 = [0]*(width*3)
    red = 0
    blue = 0
    green = 0
    for i in range(width):

        if ( i % div == 0 and i != 0):
            
            
            # Normalize colors to ensure they're within the 0-255 range
            red = min(max(red // div, 0), 255)
            blue = min(max(blue // div, 0), 255)
            green = min(max(green // div, 0), 255)

            # Apply the averaged colors to four pixels in the row
            for j in range(div):
                row1[(i - j) * 3] = red
                row1[(i - j) * 3 + 1] = blue
                row1[(i - j) * 3 + 2] = green


            red = 0
            blue = 0
            green = 0


        red += row2[ i * 3 ]
        blue += row2[ i * 3 + 1 ]
        green += row2[ i * 3 + 2 ]


    return row1


#....................................................main_reading_part...........................................


def img(path):
    # Suppose we have a byte sequence: 0x01 0x00 0x02 0x00 0x0A 0x00 0x00 0x00
    # It represents two 16-bit (2-byte) unsigned integers and one 32-bit (4-byte) unsigned integer

    binary_data = b'\x01\x00\x02\x00\x0A\x00\x00\x00'

    # Use struct.unpack to extract the integers
    # 'H' represents 2-byte unsigned integers, 'I' represents a 4-byte unsigned integer
    values = struct.unpack('HHI', binary_data)

    print(values)  # Output: (1, 2, 10)


    # reading the photo ? : my idea is using reding as binary and read every character
    img_file = open(path,"rb") 
    low_img_file = open("img_file.bmp","wb")
    
    #read 14 bit file header and then read 40 bit info header
    file_header = img_file.read(14)
    file_info = img_file.read(20)
    low_img_file.write(file_header)
    low_img_file.write(file_info)
    

    print(file_header) # output: b'BM\x8a{\x0c\x00\x00\x00\x00\x00\x8a\x00'


    file_type = struct.unpack("H",file_header[0:2])[0]
    file_size = struct.unpack("I",file_header[2:6])[0]
    offset_data = struct.unpack("I",file_header[10:14])[0]


    print(file_info) # output: <_io.BufferedReader name='sample_640 426.bmp'>


    width = struct.unpack("I",file_info[4:8])[0]
    height = struct.unpack("I",file_info[8:12])[0]
    bit_count=struct.unpack("H",file_info[14:16])[0]
    
    
    low_img_file.write(img_file.read(offset_data - 20))
    
    
    # Ensure it's a valid BMP file

    if(file_type != 0x4D42):
        print("Error: Not a valid BMP file.")
        return


    # Ensure it is a 24-bit BMP file
    if bit_count != 24:
        print("Error: Only 24-bit BMP files are supported.")
        return


    print(f"file_size: {file_size}")
    print(f"file_type: {file_type}")
    print(f"file_offset: {offset_data}")
    print(f"Image dimensions: {width}x{height}")
    print(f"Bit depth: {bit_count}-bit")

    # Seek to the beginning of pixel data
    img_file.seek(offset_data)

    # Calculate row padding (each row must be aligned to a multiple of 4 bytes)
    row_padding = ( 4 - ( width * 3 ) % 4 ) % 4

    # pixel loop

    t=0
    print(f"The file is in part: {0}%")
    for y in range(height):
        row = img_file.read(width*3)
        row2=[0]*(width*3)
        for x in range(width):


            blue=row[x*3]
            green=row[x*3+1]
            red=row[x*3+2]
            
            
            # print(f"Pixel ({x},{y}) : Red : {red} Green : {green} Blue : {blue}")


            #filling the new image of file
            row2[x*3]=red
            row2[x*3+1]=blue
            row2[x*3+2]=green

        #The file where are filling this is the last part

        row2=mix(row2,width,8)

        low_img_file.write(bytes(row2)+bytes(row_padding))
        img_file.read(row_padding)



        s = round((y*100)/height) 
        if s > t + 9 :
            t = s
            print(f"The file is in part: {t}%")




    low_img_file.write(img_file.read(68))


    #Closing folders


    low_img_file.close()
    img_file.close()


if(__name__=="__main__"):
    img("images.bmp")
