from django.shortcuts import render


def get_whether(city_name):
    city_name=city_name.replace(" ","+")
    import requests
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f"https://www.google.com/search?q=weather+{city_name}").text
    return html_content


def home(request):
    
    if request.method == "GET":
        
        if request.GET.get('city'):

            html_content = get_whether(request.GET.get('city'))

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            result = dict()
            
            try :
                result['region'] = soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
                result['temp'] = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
                
                #creating a list of string containing time , day , whether condition 
                time_day_cond = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split()
            
                # removing the condition string part from the above
                time_day = time_day_cond[:-2]
                result['timeday'] = " ".join(time_day)

                #getting the condition only 
                result['cond'] = time_day_cond[-1]
                
            # if the google result not containing the selectors(becuase of wrong city entry)
            # set the region as an error message
            except AttributeError:
                result["region"] = 'Oops,Invalid city name.'


            return render(request,'index.html',{'whether':result})

    return render(request,"index.html")

