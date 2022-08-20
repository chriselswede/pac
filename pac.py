#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from PIL import Image
import os, sys, shutil

def printHelp():
    print("                                                                                                                                   ")    
    print("DESCRIPTION:                                                                                                                       ")
    print(" The Photo Album Creator, PAC, automatically creates a simple html/css photo album from photos in a folder                         ")
    print("                                                                                                                                   ")
    print("AUTHOR: Christian Hansen                                                                                                           ")
    print("                                                                                                                                   ")
    print("                                                                                                                                   ")
    print("INPUT ARGUMENTS:                                                                                                                   ")
    print(" -sf     full path to source folder, i.e. the location of all original photos                                                      ")
    print(" -pf     full path of the folder for the home page to be made, i.e. the location of index.html, pages, pictures, and thumbnails    ")
    print("         Note: any already existing content in this folder will automatically be deleted                                           ")
    print(" -hp     height for created pictures in pixels, default: 2000                                                                      ")
    print(" -ht     height for created thumbnails in pixels, default: 400                                                                     ")
    print(" -pr     pictures per row in the gallery, if screen is wide enough, default: 4                                                     ")
    print(" -t1     title, first part, for space use _, default: Photo Gallery                                                                ")
    print(" -t2     title, second part, for space use _, default: <current year>                                                              ")
    print(" -tx     text for information in the galler, for space use _, default: ''                                                          ")
    print("                                                                                                                                   ")
    print("                                                                                                                                   ")
    print(" EXAMPLE:                                                                                                                          ")
    print(" python pac.py -sf Example_Source_Folder -pf Example_Home_Page_with_Gallery                                                        ")
    print("                                                                                                                                   ")
    print(" EXAMPLE with flag file:                                                                                                           ")
    print(" python pac.py -ff pac_example_flag_file.cfg                                                                                       ")
    print("                                                                                                                                   ")
    os._exit(1)
    
def printDisclaimer():
    print("                                                                                                                                   ")    
    print("ANY USAGE OF PAC ASSUMES THAT YOU HAVE UNDERSTOOD AND AGREED THAT:                                                                 ")
    print(" 1. PAC is open source                                                                                                             ") 
    print(' 2. PAC is provided "as is"                                                                                                        ')
    print(' 3. PAC is to be used on "your own risk"                                                                                           ')
    os._exit(1)


######################## FUNCTION DEFINITIONS ################################

def checkIfAcceptedFlag(word):
    if not word in ["-h", "--help", "-d", "--disclaimer", "-ff", "-sf", "-pf", "-hp", "-ht", "-pr", "-t1", "-t2", "-tx"]:
        print("INPUT ERROR: ", word, " is not one of the accepted input flags. Please see --help for more information.")
        os._exit(1)

def getParameterFromFile(flag, flag_string, flag_value, flag_file, flag_log, parameter):
    if flag == flag_string:
        parameter = flag_value
        flag_log[flag_string] = [flag_value, flag_file]
    return parameter

def getParameterListFromFile(flag, flag_string, flag_value, flag_file, flag_log, parameter, delimeter = ','):
    if flag == flag_string:
        parameter = [x for x in flag_value.split(delimeter)]
        flag_log[flag_string] = [flag_value, flag_file]
    return parameter

def getParameterFromCommandLine(sysargv, flag_string, flag_log, parameter):
    if flag_string in sysargv:
        flag_value = sysargv[sysargv.index(flag_string) + 1]
        parameter = flag_value
        flag_log[flag_string] = [flag_value, "command line"]
    return parameter

def getParameterListFromCommandLine(sysargv, flag_string, flag_log, parameter, delimeter = ','):
    if flag_string in sysargv:
        parameter = [x for x in sysargv[  sysargv.index(flag_string) + 1   ].split(delimeter)]
        flag_log[flag_string] = [','.join(parameter), "command line"]
    return parameter

def create_pictures(path_source_pictures, path_target, base_height, allowed_extensions_source_pictures):
    list_source_pictures = os.listdir(path_source_pictures)
    for source_picture in list_source_pictures:
        if source_picture.split(".")[1] in allowed_extensions_source_pictures:
            img = Image.open(path_source_pictures+"\\"+source_picture)
            img = resize_image(img, base_height)
            img.save(path_target+"\\"+source_picture, "JPEG")

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def resize_image(img, base_height):
    try:
        image_rotation = img.getexif()[274]
        if image_rotation in (1, 3):  #landscape, then size[0] is width
            hpercent = (base_height/float(img.size[1]))
            wsize = int((float(img.size[0])*float(hpercent)))
        elif image_rotation == 6: #portrait, then size[0] is height
            hpercent = (base_height/float(img.size[0]))
            wsize = int((float(img.size[1])*float(hpercent)))
        else:
            print("ERROR, TODO, add more rotations")
            os._exit(1)
        img = reorient_image(img)
        img = img.resize((wsize,base_height))
        return img
    except (KeyError, AttributeError, TypeError, IndexError):
        print("ERROR in resize_image; it did not work to resize image.")
        os._exit(1)

def reorient_image(img):
    try:
        image_exif = img._getexif()
        image_orientation = image_exif[274]
        if image_orientation in (2,'2'):
            return img.transpose(Image.FLIP_LEFT_RIGHT)
        elif image_orientation in (3,'3'):
            return img.transpose(Image.Transpose.ROTATE_180)
        elif image_orientation in (4,'4'):
            return img.transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (5,'5'):
            return img.transpose(Image.Transpose.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (6,'6'):
            return img.transpose(Image.Transpose.ROTATE_270)
        elif image_orientation in (7,'7'):
            return img.transpose(Image.Transpose.ROTATE_270).transpose(Image.FLIP_TOP_BOTTOM)
        elif image_orientation in (8,'8'):
            return img.transpose(Image.Transpose.ROTATE_90)
        else:
            return img
    except (KeyError, AttributeError, TypeError, IndexError):
        print("ERROR in reorient_image; it did not work to rotate image")
        os._exit(1)


def create_pages_style_cheet(path_pages):
    stylefile = open(path_pages+"\\style.css", "w")
    ############# body #################
    stylefile.write("body {\n")
    stylefile.write("\tmargin: 0;\n")
    stylefile.write("\tbackground-color: #222;\n")
    stylefile.write("}\n")
    ############# picture #############
    stylefile.write(".picture {\n")
    stylefile.write("\tbackground-color: #222;\n")
    stylefile.write("\tcolor: #eee;\n")
    stylefile.write("\tpadding: 1rem;\n")
    stylefile.write("\theight: 95vh;\n")
    stylefile.write("\twidth: 98%;\n")
    stylefile.write("}\n")
    ############## img ###############
    stylefile.write(".picture img{\n")
    stylefile.write("\tmargin: auto;\n")
    stylefile.write("\tdisplay: block;\n")
    stylefile.write("\tmax-width: 98%;\n")
    stylefile.write("\tmax-height: 98%;\n")
    stylefile.write("}\n")
    ############## arrows ###############
    stylefile.write(".arrow_box_left{\n")
    stylefile.write("\tposition: absolute;left:0;top:20%;\n")
    stylefile.write("\tbackground: transparent;\n")
    stylefile.write("\theight: 70vh;\n")
    stylefile.write("\twidth: 20%;\n")
    stylefile.write("\tfont-size: 7vw;\n")
    stylefile.write("\tcolor: grey;\n")
    stylefile.write("\tmargin: auto;\n")
    stylefile.write("\ttext-align: center;\n")
    stylefile.write("}\n")
    stylefile.write(".arrow_box_left:hover{\n")
    stylefile.write("\tcolor: white;\n")
    stylefile.write("}\n")
    stylefile.write(".arrow_box_right{\n")
    stylefile.write("\tposition: absolute;right:0;top:20%;\n")
    stylefile.write("\tbackground: transparent;\n")
    stylefile.write("\theight: 70vh;\n")
    stylefile.write("\twidth: 20%;\n")
    stylefile.write("\tfont-size: 7vw;\n")
    stylefile.write("\tcolor: grey;\n")
    stylefile.write("\tmargin: auto;\n")
    stylefile.write("\ttext-align: center;\n")
    stylefile.write("}\n")
    stylefile.write(".arrow_box_right:hover{\n")
    stylefile.write("\tcolor: white;\n")
    stylefile.write("}\n")
    stylefile.write(".arrow_box_left_up{\n")
    stylefile.write("\tposition: absolute;left:0;top:0;\n")
    stylefile.write("\tbackground: transparent;\n")
    stylefile.write("\theight: 20vh;\n")
    stylefile.write("\twidth: 20%;\n")
    stylefile.write("\tfont-size: 7vw;\n")
    stylefile.write("\tcolor: grey;\n")
    stylefile.write("\tmargin: auto;\n")
    stylefile.write("\ttext-align: center;\n")
    stylefile.write("}\n")
    stylefile.write(".arrow_box_left_up:hover{\n")
    stylefile.write("\tcolor: white;\n")
    stylefile.write("}\n")
    stylefile.flush()
    stylefile.close()

def create_main_style_sheet(path_home_page):
    stylefile = open(path_home_page+"\\style.css", "w")
    ############# * #################
    stylefile.write("*{\n")
    stylefile.write("\tmargin: 0;\n")
    stylefile.write("\tpadding: 0;\n")
    stylefile.write("\tbox-sizing: border-box;\n")
    stylefile.write("\tfont-family: 'Poppins', sans-serif;\n")
    stylefile.write("}\n")
    ############# container #############
    stylefile.write(".container{\n")
    stylefile.write("\tdisplay: flex;\n")
    stylefile.write("\tflex-direction: column;\n")
    stylefile.write("\tjustify-content: center;\n")
    stylefile.write("\talign-items: center;\n")
    stylefile.write("\ttext-align: center;\n")
    stylefile.write("\tmargin: 40px 10px 10px 10px;\n")
    stylefile.write("}\n")
    ############## heading ###############
    stylefile.write(".container .heading{\n")
    stylefile.write("\twidth: 50%;\n")
    stylefile.write("\tpadding-bottom: 50px;\n")
    stylefile.write("}\n")
    ############## h3 ###############
    stylefile.write(".container .heading h3{\n")
    stylefile.write("\tfont-size: 3em;\n")
    stylefile.write("\tfont-weight: bolder;\n")
    stylefile.write("\tpadding-bottom: 10px;\n")
    stylefile.write("\tborder-bottom: 3px solid #222;\n")
    stylefile.write("}\n")
    ############## h3sub ###############
    stylefile.write(".container .heading h3 h3sub{\n")
    stylefile.write("\tfont-weight: 100;\n")
    stylefile.write("}\n")
    ############## text ###############
    stylefile.write(".container .heading text{\n")
    stylefile.write("\tfont-size: 40;\n")
    stylefile.write("}\n")
    ############## box ################
    stylefile.write(".container .box{\n")
    stylefile.write("\tdisplay: flex;\n")
    stylefile.write("\tflex-direction: column;\n")
    stylefile.write("\tjustify-content: space-between;\n")
    stylefile.write("\talign-items: center;\n")
    stylefile.write("}\n")
    ############## row #################
    stylefile.write(".container .box .row{\n")
    stylefile.write("\tdisplay: flex;\n")
    stylefile.write("\twidth: 100%;\n")
    stylefile.write("\tjustify-content: space-between;\n")
    stylefile.write("\tflex-direction: row;\n")
    stylefile.write("}\n")
    ############### image ###############
    stylefile.write(".container .box .row .image{\n")
    stylefile.write("\tmargin-left: 10px;\n")
    stylefile.write("\tmargin-right: 10px;\n")
    stylefile.write("\tmargin-top: 10px;\n")
    stylefile.write("\tmargin-bottom: 10px;\n")
    stylefile.write("}\n")
    ############### img ##################
    stylefile.write(".container .box .row .image img{\n")
    stylefile.write("\tborder-radius: 5px;\n")
    stylefile.write("\ttransition: 0.1s;\n")
    stylefile.write("\theight: 20vh;\n")
    stylefile.write("}\n")
    stylefile.write(".container .box .row .image img:hover{\n")
    stylefile.write("\ttransform: scale(1.05);\n")
    stylefile.write("}\n")
    ############### @media : phone screen : row --> column ###############
    #stylefile.write("@media only screen and (max-width: 769px){\n")
    stylefile.write("@media only screen and (max-width: 1000px){\n")
    stylefile.write("\t.container .box .row{\n")
    stylefile.write("\t\tflex-direction: column;\n")
    stylefile.write("\t}\n")
    stylefile.write("\t.container .box .row .image img{\n")
    stylefile.write("\t\theight: 40vh;\n")
    stylefile.write("\t}\n")
    stylefile.write("\t.container .heading{\n")
    stylefile.write("\t\twidth: 100%;\n")
    stylefile.write("\t}\n")
    stylefile.write("\t.container .heading h3{\n")
    stylefile.write("\t\tfont-size: 2em;\n")
    stylefile.write("\t}\n")
    stylefile.write("}\n")
    stylefile.flush()
    stylefile.close()

def create_picture_pages(path_home_page):
    path_target = path_home_page+"\\pages"
    list_pictures = os.listdir(path_home_page+"\\pictures")
    for picture in list_pictures:
        previous_page = get_previous_cyclic(list_pictures, picture).replace('.jpg','.html')
        next_page = get_next_cyclic(list_pictures, picture).replace('.jpg','.html')
        pagefile = open(path_target+"\\"+picture.replace(".jpg", ".html"), "w")
        pagefile.write("<!DOCTYPE html>\n")   
        pagefile.write('<html lang="en">\n')
        pagefile.write('<head>\n\t<title>Picture Page of '+picture+'</title>\n\t<link rel="stylesheet" type="text/css" href="style.css">\n</head>\n')
        pagefile.write("<body>\n")
        pagefile.write('\t<a href="../pages/'+previous_page+'"><div class="arrow_box_left">\n')
        pagefile.write('\t\t&#8249;\n')  
        pagefile.write('\t</div></a>\n')  
        pagefile.write('\t<a href="../pages/'+next_page+'"><div class="arrow_box_right">\n')
        pagefile.write('\t\t&#8250;\n')  
        pagefile.write('\t</div></a>\n') 
        pagefile.write('\t<a href="../index.html"><div class="arrow_box_left_up">\n')
        pagefile.write('\t\t&#8598;\n')  
        pagefile.write('\t</div></a>\n') 
        pagefile.write('\t<div class="picture">\n')
        pagefile.write('\t\t<a href="../pictures/'+picture+'"><img src="../pictures/'+picture+'" alt="'+picture+'"></a>\n')
        pagefile.write('\t</div>\n') 
        pagefile.write('</body>\n')
        pagefile.write('</html>\n')
        pagefile.flush()
        pagefile.close()

def create_main_page(path_home_page, pics_per_row, title_1st, title_2nd, text):
    indexfile = open(path_home_page+"\\index.html", "w")
    indexfile.write("<!DOCTYPE html>\n")   
    indexfile.write('<html lang="en">\n')
    indexfile.write('<head>\n\t<title>Photo Gallery</title>\n\t<link rel="stylesheet" type="text/css" href="style.css">\n</head>\n')
    indexfile.write("<body>\n")
    indexfile.write('\t<div class="container">\n')
    indexfile.write('\t\t<div class="heading">\n')
    indexfile.write('\t\t\t<h3>'+title_1st+' <h3sub>'+title_2nd+'</h3sub></h3>\n')
    if text:
        indexfile.write('\t\t\t<p>&nbsp;</p>\n')
        indexfile.write('\t\t\t<text>'+text+'</text>\n')  
    indexfile.write('\t\t</div>\n')
    indexfile.write('\t\t<div class="box">\n')           
    list_thumbnails = os.listdir(path_home_page+"\\thumbnails")
    chunks_thumbnails = [list_thumbnails[x:x+pics_per_row] for x in range(0, len(list_thumbnails), pics_per_row)]
    for chunk in chunks_thumbnails:
        indexfile.write('\t\t\t<div class="row">\n')
        for thumbnail in chunk:
            indexfile.write('\t\t\t\t<div class="image">\n')
            indexfile.write('\t\t\t\t\t<a href="pages/'+thumbnail.replace(".jpg",".html")+'"><img src="thumbnails/'+thumbnail+'" alt="'+thumbnail+'"></a>\n')
            indexfile.write('\t\t\t\t</div>\n')
        indexfile.write('\t\t\t</div>\n') 
    indexfile.write('\t\t</div>\n') 
    indexfile.write('\t</div>\n')
    indexfile.write('</body>\n')
    indexfile.write('</html>\n')
    indexfile.flush()
    indexfile.close()
            
def get_previous_cyclic(list_of_elements, element):
    length_of_list = len(list_of_elements)
    if length_of_list < 1:
        print("ERROR; the list of elements is empty.")
        os._exit(1)
    index_of_element = list_of_elements.index(element)
    if index_of_element == 0:
        previous_index = length_of_list - 1
    else:
        previous_index = index_of_element - 1
    return list_of_elements[previous_index]

def get_next_cyclic(list_of_elements, element):
    length_of_list = len(list_of_elements)
    if length_of_list < 1:
        print("ERROR; the list of elements is empty.")
        os._exit(1)
    index_of_element = list_of_elements.index(element)
    if index_of_element == length_of_list - 1:
        next_index = 0
    else:
        next_index = index_of_element + 1
    return list_of_elements[next_index]

def make_folders(list_of_folders):
    for folder in list_of_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

######################## main #############################################

def main():

    #####################  CHECK PYTHON VERSION ###########
    if sys.version_info[0] != 3:
        print("VERSION ERROR: PAC is only supported for Python 3.x.x") 
        os._exit(1)
 
    #####################   DEFAULTS   ####################
    flag_files = []    #default: no configuration input file
    path_source_pictures = ""
    allowed_extensions_source_pictures = ['jpg', 'JPG']
    path_home_page = ""
    base_height_pictures = "2000"   # pictures should all have same height
    base_height_thumbnails = "400"  # thumbnails should all have same height 
    pics_per_row = "4"   
    title_1st = "Photo Gallery"
    title_2nd = str(date.today().year)
    text = ""

    #####################  CHECK INPUT ARGUMENTS #################
    if len(sys.argv) == 1:
        print("INPUT ERROR: pac needs input arguments. Please see --help for more information.")
        os._exit(1) 
    if len(sys.argv) != 2 and len(sys.argv) % 2 == 0:
        print("INPUT ERROR: Wrong number of input arguments. Please see --help for more information.")
        os._exit(1)
    for i in range(len(sys.argv)):
        if i % 2 != 0:
            if sys.argv[i][0] != '-':
                print("INPUT ERROR: Every second argument has to be a flag, i.e. start with -. Please see --help for more information.")
                os._exit(1)    

    #####################  PRIMARY INPUT ARGUMENTS   ####################
    flag_log = {}     
    if '-h' in sys.argv or '--help' in sys.argv:
        printHelp()   
    if '-d' in sys.argv or '--disclaimer' in sys.argv:
        printDisclaimer()
    flag_files = getParameterListFromCommandLine(sys.argv, '-ff', flag_log, flag_files)    

    ############ CONFIGURATION FILE ###################
    for flag_file in flag_files:
        with open(flag_file, 'r') as fin:
            for line in fin:
                firstWord = line.strip(' ').split(' ')[0]  
                if firstWord[0:1] == '-':
                    checkIfAcceptedFlag(firstWord)
                    flagValue = line.strip(' ').split('"')[1].strip('\n').strip('\r') if line.strip(' ').split(' ')[1][0] == '"' else line.strip(' ').split(' ')[1].strip('\n').strip('\r')
                    path_source_pictures                = getParameterFromFile(firstWord, '-sf', flagValue, flag_file, flag_log, path_source_pictures)
                    path_home_page                      = getParameterFromFile(firstWord, '-pf', flagValue, flag_file, flag_log, path_home_page)
                    base_height_pictures                = getParameterFromFile(firstWord, '-hp', flagValue, flag_file, flag_log, base_height_pictures)
                    base_height_thumbnails              = getParameterFromFile(firstWord, '-ht', flagValue, flag_file, flag_log, base_height_thumbnails)
                    pics_per_row                        = getParameterFromFile(firstWord, '-pr', flagValue, flag_file, flag_log, pics_per_row)
                    title_1st                           = getParameterFromFile(firstWord, '-t1', flagValue, flag_file, flag_log, title_1st)
                    title_2nd                           = getParameterFromFile(firstWord, '-t2', flagValue, flag_file, flag_log, title_2nd)
                    text                                = getParameterFromFile(firstWord, '-tx', flagValue, flag_file, flag_log, text)
                    

    #####################   INPUT ARGUMENTS (these would overwrite whats in the configuration file(s))   ####################
    for word in sys.argv:
        if word[0:1] == '-':
            checkIfAcceptedFlag(word)
    path_source_pictures                = getParameterFromCommandLine(sys.argv, '-sf', flag_log, path_source_pictures)
    path_home_page                      = getParameterFromCommandLine(sys.argv, '-pf', flag_log, path_home_page)
    base_height_pictures                = getParameterFromCommandLine(sys.argv, '-hp', flag_log, base_height_pictures)
    base_height_thumbnails              = getParameterFromCommandLine(sys.argv, '-ht', flag_log, base_height_thumbnails)
    pics_per_row                        = getParameterFromCommandLine(sys.argv, '-pr', flag_log, pics_per_row)
    title_1st                           = getParameterFromCommandLine(sys.argv, '-t1', flag_log, title_1st)
    title_2nd                           = getParameterFromCommandLine(sys.argv, '-t2', flag_log, title_2nd)
    text                                = getParameterFromCommandLine(sys.argv, '-tx', flag_log, text)

    ############ CHECK AND CONVERT INPUT PARAMETERS #################
    ### path_source_pictures, -sf
    if not path_source_pictures:
        print("INPUT ERROR: -sf must be provided, Please see --help for more information.")
        os._exit(1)
    ### path_home_page, -pf
    if not path_home_page:
        print("INPUT ERROR: -pf must be provided, Please see --help for more information.")
        os._exit(1)
    ### base_height_pictures, -hp
    if not is_integer(base_height_pictures):
        print("INPUT ERROR: -hp must be an integer, Please see --help for more information.")
        os._exit(1)
    base_height_pictures = int(base_height_pictures)
    ### base_height_thumbnails, -ht
    if not is_integer(base_height_thumbnails):
        print("INPUT ERROR: -ht must be an integer, Please see --help for more information.")
        os._exit(1)
    base_height_thumbnails = int(base_height_thumbnails)
    ### pics_per_row, -pr
    if not is_integer(pics_per_row):
        print("INPUT ERROR: -pr must be an integer, Please see --help for more information.")
        os._exit(1)
    pics_per_row = int(pics_per_row)
    ### title_1st, -t1
    title_1st = title_1st.replace('_', ' ')
    ### title_2nd, -t2
    title_2nd = title_2nd.replace('_', ' ')
    ### text, -tx
    text = text.replace('_', ' ')

    #################### FOLDERS ###############
    if not os.path.exists(path_source_pictures):
        print("ERROR; the picture source folder, provided by -sf, does not exist.")
        os._exit(1)
    if not os.path.exists(path_home_page):
        os.makedirs(path_home_page)
    else:
        #TEMP
        shutil.rmtree(path_home_page)
        os.makedirs(path_home_page)
        #print("ERROR; the homepage source folder already exists.")
        #os._exit(1)
    path_thumbnails = path_home_page + "\\thumbnails"
    path_pictures = path_home_page + "\\pictures"
    path_pages = path_home_page + "\\pages"
    make_folders([path_thumbnails, path_pictures, path_pages])

    ##################### CREATE PICTURES ###############
    create_pictures(path_source_pictures, path_thumbnails, base_height_thumbnails, allowed_extensions_source_pictures)
    create_pictures(path_source_pictures, path_pictures, base_height_pictures, allowed_extensions_source_pictures)

    ###################### CREATE STYLE SHEETS #################
    create_main_style_sheet(path_home_page)
    create_pages_style_cheet(path_pages)
              
    ###################### CREATE PAGES #################
    create_picture_pages(path_home_page)
    create_main_page(path_home_page, pics_per_row, title_1st, title_2nd, text)
              
              
if __name__ == '__main__':
    main()
                        

