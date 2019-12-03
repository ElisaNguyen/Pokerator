def conceptnet_request(word, relation):
    url = 'http://api.conceptnet.io/c/en/' + word + '?rel=/r/' + relation + '&limit=10'
    print(url)
    response = requests.get(url).json()
    df = pd.DataFrame(response['edges'])
    surface_texts = list(df[df['rel'].apply(lambda e: dict(e)['label'] == relation)]['surfaceText'])
    words = [e.replace('[', '').replace(']', '') for e in re.findall("\[+[a-z A-Z]+\]+", str(surface_texts))]
    words = list(set(words))
    if word in words:
        words.remove(word)
    return surface_texts, words