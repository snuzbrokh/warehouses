def findFeatures(text):
    '''
    Takes listing text data and performs search of various keywords
    to find listing information
    '''
    height_patterns = [r'(\d+)\'? (\w+) (\w+)?',\
                       r'(\w+) (\w+)'
           ]
    features = ['drive','loading', 'dock','air', 'grade','security', \
                'restrooms','truck','fenced','phase',\
                'ground']
    # Check every pattern in the text, break when found. 
    
    dict_ = {
        'driveIns' : 1, # assume every warehouse has a place to pull up to
        'loadingDocks' : 0,
        '3phasePower': 0,
        'restrooms' : 0,
        'AC' : 0,
        'fenced' : 0
        }
    
    for pattern in height_patterns:
        g = re.findall(pattern,text)
        if g:
            #if 'grade' in g[0]:
            g = [x for group in g for x in group]
            for feat in features:
                try:
                    i = g.index(feat)
                    num = g[i-1]
                    
                    if feat in ['drive','grade','ground'] and num.isdigit():
                        dict_['driveIns'] = g[i-1]
                    if feat in ['loading','truck','dock'] and num.isdigit() and g[i+1] in ['dock','docks','well','wells','stall','stalls']:
                        dict_['loadingDocks'] = g[i-1]
                    if feat == 'phase' and num.isdigit():
                        dict_['3phasePower'] = 1
                    if feat in ['bathrooms','restrooms']:
                        dict_[feat] = 1
                    if feat == 'air' and g[i+1] == 'conditioning':
                        dict_['AC'] = 1
                    if feat == 'fenced':
                        dict_[feat] = 1
                    #print(g)                                
                    #print(dict_)
                except:
                    continue
    return dict_