import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
def dataset():
    #load csv file 
    return name

def facebookscrap(user):
    sections = {
        'photo_url': {'src':'//div[@id="objects_container"]//a/img[@alt][1]'},
        'tagline': {'txt':'//*[@id="root"]/div[1]/div[1]/div[2]/div[2]'},
        'about': {'txt':'//div[@id="bio"]/div/div[2]/div'},
        'quotes': {'txt':'//*[@id="quote"]/div/div[2]/div'},
        'rel': {'txt':'//div[@id="relationship"]/div/div[2]'},
        'rel_partner': {'href':'//div[@id="relationship"]/div/div[2]//a'},
        'details': {'table':'(//div[2]/div//div[@title]//'},
        'work': {'workedu':'//*[@id="work"]/div[1]/div[2]/div'},
        'education': {'workedu':'//*[@id="education"]/div[1]/div[2]/div'},
        'family': {'fam':'//*[@id="family"]/div/div[2]/div'},
        'life_events': {'years':'(//div[@id="year-overviews"]/div[1]/div[2]/div[1]/div/div[1])'},
        'facebook_id':{'txt':'/html/body/div[1]/div[1]/div[4]/div/div/div/div[1]/div[3]/div/div/div/div[1]'},
        'Instagram':{'txt':'/html/body/div/div/div[2]/div/div[1]/div[4]/div/div[2]/div[2]/table/tbody/tr/td[2]/div'},
        'birthday':{'txt':'/html/body/div/div/div[2]/div/div[1]/div[6]/div/div[2]/div[1]/table/tbody/tr/td[2]/div'},
        'gender':{'txt':'/html/body/div[1]/div[1]/div[4]/div/div/div/div[1]/div[4]/div/div[2]/div/div[1]'},
        'mobile':{'txt':"/html/body/div[1]/div/div[4]/div/div/div/div[1]/div[5]/div/div[4]/div/div[1]/span/span"},
        'mutual':{'txt':"/html/body/div/div/div[2]/div/div[1]/div[2]/div[1]/h3"},
        'Relationship':{'txt':"/html/body/div/div/div[2]/div/div[1]/div[7]/div/div[2]/div/div/div"},
        'Email':{'txt':'/html/body/div/div/div[2]/div/div[1]/div[5]/div/div[2]/div[2]/table/tbody/tr/td[2]/div/a'}
    }
    driver = webdriver.Firefox(executable_path='path_of_geckodriver')
    # driver.maximize_window()
    print("Logging in....")
    driver.get("Your profile url")
    element = driver.find_element_by_id("email")
    element.send_keys('email_here')
    element = driver.find_element_by_id("pass")
    element.send_keys('password_here')
    element = driver.find_element_by_id("loginbutton")
    element.click()
    print("Logged in....")
    
    driver.get("https://mobile.facebook.com/search/top/?q="+user)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    f = soup.find('div',{'id':'root'})
    l=[]
    for j in f.find_all('a',href=True):
        try:
            l.append(j['href'].split('?')[0])    
        except:
            pass
    l = list(set(l))
    
    h=[]
    ki=[]
    lh=[]
    mkk=[]
    for username in l:
        try:
            driver.get("https://mbasic.facebook.com"+username+"/about")
            name=driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/span/div/span/strong')
            d = {'name': name.text}
            x = driver.find_element_by_xpath
            xs = driver.find_elements_by_xpath
            for k,v in sections.items():
                    try:
                        if 'src' in v:
                            d[str(k)] = x(v['src']).get_attribute('src')
                        elif 'txt' in v:
                            d[str(k)] = x(v['txt']).text
                        elif 'href' in v:
                            d[str(k)] = x(v['href']).get_attribute('href')[8:].split('?')[0]
                        elif 'table' in v:
                            d['details'] = []
                            rows = xs(v['table']+'td[1])')
                            for i in range (1, len(rows)+1):
                                deets_key = x(v['table']+'td[1])'+'['+str(i)+']').text
                                deets_val = x(v['table']+'td[2])'+'['+str(i)+']').text
                                d['details'].append({deets_key:deets_val})
                        elif 'workedu' in v:
                            d[str(k)] = []
                            base = v['workedu']
                            rows = xs(base)
                            for i in range (1, len(rows)+1):
                                dd = {}
                                dd['link'] = x(base+'['+str(i)+']'+'/div/div[1]//a').get_attribute('href')[8:].split('&')[0].split('/')[0]
                                dd['org'] = x(base+'['+str(i)+']'+'/div/div[1]//a').text
                                dd['lines'] = []
                                lines = xs(base+'['+str(i)+']'+'/div/div[1]/div')
                                for l in range (2, len(lines)+1):
                                    line = x(base+'['+str(i)+']'+'/div/div[1]/div'+'['+str(l)+']').text
                                    dd['lines'].append(line)
                                d[str(k)].append(dd)
                        elif 'fam' in v:
                            d[str(k)] = []
                            base = v['fam']
                            rows = xs(base)
                            for i in range (1, len(rows)+1):
                                d[str(k)].append({
                                    'name': x(base+'['+str(i)+']'+'//h3[1]').text,
                                    'rel': x(base+'['+str(i)+']'+'//h3[2]').text,
                                    'alias': x(base+'['+str(i)+']'+'//h3[1]/a').get_attribute('href')[8:].split('?')[0]
                                })
                        elif 'life_events' in k:
                            d[str(k)] = []
                            base = v['years']
                            years = xs(base)
                            for i in range (1,len(years)+1):
                                year = x(base+'['+str(i)+']'+'/div[1]').text
                                events = xs(base+'['+str(i)+']'+'/div/div/a')
                                for e in range(1,len(events)+1):
                                    event = x('('+base+'['+str(i)+']'+'/div/div/a)'+'['+str(e)+']')
                                    d[str(k)].append({
                                        'year': year,
                                        'title': event.text,
                                        'link': event.get_attribute('href')[8:].split('refid')[0]
                                    })
                
                    except Exception:
                        pass
            lh.append(d)
            
            
            info_str = ""
            
            for key in d.keys():
                    h=[]
                    info_str = info_str + key.upper()+": "
                    if type(d[key]) is list:
                        info_str += "\n"
                        for itm in d[key]:
                            if type(itm) is dict:
                                #print(itm)
                                for kff in itm.keys():
                                    info_str = info_str + "\t"+kff.upper()+": "+str(itm[kff])+"\n"

                    else:
                        info_str = info_str + d[key]+"\n"
                    h.append(info_str)
                    mkk.append(info_str)



        except:
            pass
   
    
    
    driver.quit()
    return(pd.DataFrame(lh))
def ifd():
    if(len(fbdb())==0):
        df['id']=[i for i in range(len(df))]
    else:
        df['id'] = [i+1 for i in range(max(fbdb().id),len(df)+max(fbdb().id))]
    return df['id']

def connectdb():
    #connect to database 
    return db
def update():  
        
        y= connectdb()
        fd=#table

        import json
        records = json.loads(df.T.to_json()).values()
        for r in records:
            fd.insert(r)
        print('done')
def fbdb():
    y= connectdb()
    df=y['fund_facebook']
    
    k = []
    for x in df.find():
        k.append(x)
    df = pd.DataFrame(k)
    try:
        df=df.drop('_id',axis=1)
    except:
        pass
    return df
        
if __name__=='__main__':
    start = time.time()
    
    for i in dataset():
        df=facebookscrap(i)
        time.sleep(30)
        ifd()
        update()
        print(i)
    final = time.time()-start
    print(final/60/60/24)
        
