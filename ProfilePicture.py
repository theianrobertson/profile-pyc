#Imports in some packages.
import mechanize
import cookielib
import datetime
from PIL import Image, ImageFilter
from twython import Twython
import base64

def newspaper_file(filename):
    '''
    Reaches out to a newspaper and grabs a picture.
    '''

    # Opens up a browser instance in mechanize 
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    
    # Set how the mechanize browser handles some options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        
    #This is hard-wired to grab the Globe and Mail.
    dater = int(datetime.date.today().strftime("%d"))
    img_url = 'http://webmedia.newseum.org/newseum-multimedia/dfp/jpg{0}/lg/CAN_TGAM.jpg'.format(dater)
    
    print 'Getting url: {0}'.format(img_url)
    data = br.open(img_url).read()
    save = open(filename, 'wb')
    save.write(data)
    save.close()


def splice_image(newspaper_file, base_file, new_file):
    '''
    Splices a new newspaper cover into the base picture
    '''
    
	#Opens the two images:
    im = Image.open(base_file)
    impage = Image.open(newspaper_file)

    #Blurs
    imblur = impage.filter(ImageFilter.GaussianBlur(radius=1))

    #Now splice together and save
    mask = impage.convert('L')
    mask = Image.eval(mask, lambda x: 0 if x >= 240 else 255)
    im.paste(imblur, (950, 110), mask=mask)
    imResize = im.resize((597,600), Image.ANTIALIAS)
    imResize.save(new_file, 'JPEG', quality=90)



def post_to_twitter(filename):
	'''
	Posts the actual image to the twitters.
	Requires a keys.json file, with app_key
	'''
	with open('keys.json') as f:
		keys = eval(f.read())
	
	#Grabs the connection to twitter
	twitter = Twython(app_key,
					  app_secret,
					  oauth_token,
					  oauth_token_secret)
	
	with open(filename, "rb") as image_file:
    	encoded_string = base64.b64encode(image_file.read())
	
	print 'Posting to twitter'
	i = twitter.update_profile_image(image=encoded_string)


if __name__ == "__main__":

    news_file = 'img/' + datetime.date.today().strftime("%Y%m%d") + '.jpg'
    new_file = 'newimage.jpg'
    base_file = 'baseimage.jpg'
    
    #Grabs the stuff
    newspaper_file(news_file)
    splice_image(news_file, base_file, new_file)
    post_to_twitter(new_file)
