import re 
import pandas as pd
from collections import Counter
from rapidfuzz import fuzz

msg = "You won lottery , please click on the link to avail your prizes https://www.goog1e.com/, you can also go with Claim now https://fake-bank.xyz/login"


df = pd.read_csv("spam2.csv", encoding='latin-1')
words = []
ignore_words = [
    "www",
    "https",
    "http",
    "com",
    "org",
    "gov",
    "co",
    "net",
    "edu",
    "in",
    "uk"
]
suspicious_keywords = {
    "login": 20,
    "firebaseapp": 30,
    "weeblysite": 25,
    "blogspot": 20,
    "workers": 15,
    "clone": 20,
    "email": 10,
    "indexphp": 15
}

def extract_url(text):
    pattern = r'https?://\S+'
    urls = re.findall(pattern, text)
    cleaned_urls = []

    for url in urls:
        url = url.rstrip('.,!?)]}"\'')
        cleaned_urls.append(url)
        
    return cleaned_urls 



def extract_domain_tokens(url):

    domain = url.split("//")[-1].split("/")[0]

    domain = domain.replace("www.", "")

    domain = domain.split(".")[0]

    tokens = re.split(r'[-_]', domain)

    return tokens

def analyze_url(url):
    
    score = 0
    general_tld = [
       'org',
       'com',
       'in',
       'gov',
       'io',
       'co',
       'info'
    ]

    brands = [
    "google",
    "paytm",
    "amazon",
    "facebook",
    "instagram",
    "microsoft",
    "whatsapp",
    "netflix",
    "apple",
    "youtube",
    "twitter",
    "linkedin",
    "github",
    "wikipedia",
    "wordpress",
    "pinterest",
    "vimeo",
    "reuters",
    "bing",
    "nature",
    "wiley",
    "gnu",
    "ibm",
    "weibo",
    "weebly",
    "imdb",
    "discord",
    "bloomberg",
    "statista",
    "unsplash",
    "etsy",
    "openai",
    "mysql",
    "canva",
    "stripe",
    "gitlab",
    "wired",
    "ebay",
    "stackoverflow",
    "substack",
    "hubspot",
    "usatoday",
    "aol",
    "blogger",
    "cnet",
    "mit",
    "harvard",
    "stanford",
    "berkeley",
    "unesco",
    "nasa",
    "cdc",
    "telegram",
    "outlook",
    "sharepoint",
    "twitch",
    "discord",
    "paypal",
    "shopify",
    "amazonpay",
    "cloudfront",
    "googleusercontent",
    "firebaseapp",
    "duckdns",
    "blogspot",
    "godaddysites"
]
   
    brand_matches = []

    tokens = extract_domain_tokens(url)

    for token in tokens:

     for brand in brands:

        similarity = fuzz.ratio(token.lower(), brand.lower())

        if similarity > 80 and token.lower() != brand.lower():

            score += 40

            brand_matches.append({
                "fake": token,
                "real": brand,
                "similarity": similarity
            })

  

    def count_subdomains (url):
        domain = url.split('//')[-1].split('/')[0]
        parts = domain.split('.')
        if parts[0] == "www":
         parts = parts[1:]
        return max(len(parts) -2,0)
    
    def extract_tld(url):

     domain = url.split('//')[-1].split('/')[0]

     parts = domain.split('.')

     return parts[-1]
    
    
    url_length = len(url)
    is_https = url.startswith('https://')
    subdomain_count = count_subdomains(url)
    digit_count = sum(char.isdigit() for char in url)
    hyphen_count = url.count('-')
    tld = extract_tld(url)

    if not is_https:
          score +=20
    
    
    if tld not in general_tld:
          score +=30

   

    if subdomain_count >= 1:
        score += 20
    
    if digit_count > 2:
     score += 15

    if hyphen_count > 1:
        score += 15

    detected_keywords = []

    for word, risk in suspicious_keywords.items():

     if word in url.lower():

        score += risk

        detected_keywords.append(word)
    
    if score >= 60:
     risk = "Dangerous"

    elif score >= 30:
     risk = "Suspicious"

    else:
     risk = "Safe"
    

    return {
        "url": url,
        "url_length": url_length,
        "is_https": is_https,
        "subdomain_count": subdomain_count,
        "digit_count": digit_count,
        "hyphen_count": hyphen_count,
        "tld": tld,
        "score": score,
        "detected_keywords": detected_keywords,
        "risk": risk,
        "brand_matches": brand_matches,
    }


    
urls = extract_url(msg)

phishing_df = df[df['label'] == 0] 
text_data = phishing_df['URL'] + "" + phishing_df['Title']
text_data  = text_data.str.lower()

for text in text_data:
    found = re.findall(r'[a-zA-Z]+',str(text))
    for word in found:
     word = word.lower()

     if len(word) > 3 and word not in ignore_words:
        words.append(word)

counter = Counter(words)

# print(counter.most_common(50))    

results = []
for url in urls:

    result = analyze_url(url)
    results.append(result)

    print(result)
    
     

