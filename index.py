import requests
from bs4 import BeautifulSoup

searchQuery = input("Entrez le nom du produit recherché : ")

file = open("../tp-scrapping/main.html", "w")
file.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <title>Python Parsing</title>
</head>
<body>
<ul class="list-group">''')

for counter in range(1, 30):
    if counter == 1:
        page2 = requests.get(
            f'https://chocobonplan.com/?s={searchQuery}&asl_active=1&p_asid=1&p_asl_data=cXRyYW5zbGF0ZV9sYW5nPTAmc2V0X2ludGl0bGU9Tm9uZSZzZXRfaW5jb250ZW50PU5vbmUmc2V0X2lucGFnZXM9Tm9uZSZjdXN0b21zZXQlNUIlNUQ9YnA=')
    else:
        page2 = requests.get(
            f'https://chocobonplan.com/page/{counter}/?s={searchQuery}&asl_active=1&p_asid=1&p_asl_data=cXRyYW5zbGF0ZV9sYW5nPTAmc2V0X2ludGl0bGU9Tm9uZSZzZXRfaW5jb250ZW50PU5vbmUmc2V0X2lucGFnZXM9Tm9uZSZjdXN0b21zZXQlNUIlNUQ9YnA%3D')

    soupdata = BeautifulSoup(page2.content, "html.parser")

    results2 = soupdata.find_all("a", class_="row result-search")

    for result2 in results2:
        links = result2['href']

        images = result2.find_all("img")
        titles = result2.find_all('div', 'result-search__title')

        for img in images:
            src = img['src']

            file.write(f'''
            <li class="list-group-item" style="display: flex; justify-content: space-between; align-items: center; padding: 20px 50px">
                <img src={src} class="card-img-top" style="max-width: 200px"/>
            ''')

        for title in titles:

            file.write(f'''
                <h5>{" ".join(title.text.split())}</h5>
                <a href={links} class="btn btn-primary" >Voir l'offre</a>
            </li>
            ''')

        requests.post('http://localhost:3000/results', {"title": " ".join(title.text.split()), "img_src": src, "link": links})

file.write('''
        </ul>
    </body>
</html>
''')
