def newspaper_file(filename):
    '''
    Reaches out to a newspaper and grabs a picture.
    '''
    # Which modules to use
    import mechanize
    import cookielib
    import urllib
    import logging
    import sys
    import os
    import random
    import time
    import datetime
    from subprocess import Popen, PIPE
    
    # Opens up a browser instance in mechanize 
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    
    # Grabs the user ID (won't work if your Unix ID <> SSO ID)
    p = Popen(['id', '-u', '-n'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
    sso_eid = p.stdout.read().rstrip()
    
    # Grabs the SSO password from ftppwd - see https://pulse.kdc.capitalone.com/docs/DOC-3753
    p = Popen(['/prod/user/home/user/util/bin/ftppwd', 'SSO', sso_eid], stdout=PIPE, stderr=PIPE, stdin=PIPE)
    sso_pwd = p.stdout.read().rstrip()
    
    # Set how the mechanize browser handles some options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
    # Capital One Proxy
    br.set_proxies({"http": "proxy.kdc.capitalone.com:8099"})
    # Proxy password
    br.add_proxy_password(sso_eid, sso_pwd)
    
    #This is hard-wired to grab the Globe and Mail.
    img_url = 'http://webmedia.newseum.org/newseum-multimedia/dfp/jpg'
    img_url += str(int(datetime.date.today().strftime("%d")))
    img_url += '/lg/CAN_TGAM.jpg'
    
    data = br.open(img_url).read()
    save = open(filename, 'wb')
    save.write(data)
    save.close()



def splice_image(newspaper_file, base_file, new_file):
    '''
    Splices a new newspaper cover into your base picture
    '''
    
    #Grabs some bits from PIL
    from PIL import Image, ImageFilter

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


def profile_post(picture, userID):
    '''
    This posts a picture to a specific user's main profile photo.
    '''
    
    # Which modules to use
    import mechanize
    import cookielib
    import urllib
    import logging
    import sys
    import os
    import random
    import time
    from subprocess import Popen, PIPE

    # Sets some variables
    in_folder = '/prod/user/sam/can/card/canada/non_npi/rck097/pulse_profile_moreso/'
    out_file = in_folder + 'all_users.txt'

    # Opens up a browser instance in mechanize 
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Grabs the user ID (won't work if your Unix ID <> SSO ID)
    p = Popen(['id', '-u', '-n'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
    sso_eid = p.stdout.read().rstrip()

    # Grabs the SSO password from ftppwd - see https://pulse.kdc.capitalone.com/docs/DOC-3753
    p = Popen(['/prod/user/home/user/util/bin/ftppwd', 'SSO', sso_eid], stdout=PIPE, stderr=PIPE, stdin=PIPE)
    sso_pwd = p.stdout.read().rstrip()

    # Set how the mechanize browser handles some options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Capital One Proxy
    br.set_proxies({"http": "proxy.kdc.capitalone.com:8099"})
    # Proxy password
    br.add_proxy_password(sso_eid, sso_pwd)

    # Tries to open a Pulse page
    url = 'https://pulse.kdc.capitalone.com/people/RCK097'
    r = br.open(url)

    # Logs in to Pulse
    # Sleeps a bit to give time 
    time.sleep(1)
    br.select_form("login")
    br.form['usr_name'] = sso_eid
    br.form['usr_password'] = sso_pwd
    br.submit()

    #url = 'https://pulse.kdc.capitalone.com/avatar-userupload!inputImage.jspa?targetUser=44003'
    #
    #r = br.open(url)
    #txt = r.read()
    #
    #br.select_form(nr=0)
    #br.form.add_file(open(picture), 'text/plain', 'newimage.jpg')
    #br.form.set_all_readonly(False)
    #resp = br.submit()
    #
    #br.select_form(nr=0)
    #br.form.set_all_readonly(False)
    #br['cropX'] = '62'
    #br['cropY'] = '1'
    #br['cropWidth'] = '370'
    #br['cropHeight'] = '370'
    #br.submit()

    #Uploads to your first profile image
    url = 'https://pulse.kdc.capitalone.com/edit-profile-avatar!inputImage.jspa?imageIndex=1&targetUser='
    url += userID

    r = br.open(url)
    txt = r.read()
    time.sleep(1)
    
    #Pushes the picture
    br.select_form(nr=0)
    br.form.add_file(open(picture), 'text/plain', picture)
    br.form.set_all_readonly(False)
    resp = br.submit()
    time.sleep(1)
    
    #Submits the form (crop)
    br.select_form(nr=0)
    br.form.set_all_readonly(False)
    br['cropX'] = '62'
    br['cropY'] = '1'
    br['cropWidth'] = '375'
    br['cropHeight'] = '375'
    br.submit()

    #Something about avatars
    br.select_form(nr=0)
    br.form.set_all_readonly(False)
    br.submit()


if __name__ == "__main__":
    import datetime
    news_file = 'img/' + datetime.date.today().strftime("%Y%m%d") + '.jpg'
    userID = '44003'
    new_file = 'newimage.jpg'
    base_file = 'baseimage.jpg'
    
    #Grabs the stuff
    newspaper_file(news_file)
    splice_image(news_file, base_file, new_file)
    profile_post(new_file, userID)
