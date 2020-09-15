
# before running this function - create two blank data frames
# initialDF and fixedDF
def prepareDataframe (initialDF, fixedDF):
    initialDF = incidentDF[['Incident Description', 'Outcome']].copy()
    # need to reindex
    initialDF.reset_index(drop=True, inplace=True)
    # lowercase each description
    initialDF['Incident Description'] = classificationDF['Incident Description'].str.lower()

    # grab all text together
    initial_desc = initialDF['Incident Description'].str.split(' ')
    initial_desc.head()
    # create blank dataframe for tokenized words
    initial_desc_nopunc = []

    # remove punctuation
    for desc in incident_desc:
        desc = [x.strip(string.punctuation) for x in desc]
        initial_desc_nopunc.append(desc)
        initial_desc_nopunc[0]
        # this is a list with the text rejoined, not tokenized
        initital_desc_final = [" ".join(text) for text in initial_desc_nopunc]

    # need to replace "/" with space
    # need to replace the "-" with a space
    # remove extra spaces
    noslash = []
    for desc in incident_desc_final:
        desc = desc.replace("/", " ")
        desc = desc.replace("-", " ")
        desc = desc.replace("  ", " ")
        desc = desc.replace("  ", " ")
        noslash.append(desc)
        noslash[0]

    initialDescDF = []
    initialDescDF = pd.DataFrame(noslash, columns=['Incident Description'])

    # now need to do stopwords
    # remove stop words
    stopWords = nltk.corpus.stopwords.words('english')
    len(stopWords)
    # for Incident Description
    # add some additional stop words after review of the words
    incmoreStopWords = ["michael", "john", "robert", "todd", "rodriguez", "englehart", "mark", "rudy",
                        "david", "bruce", "gary", "james", "will", "william", "linda", "richard", "joseph",
                        "chris", "ferraro", "paul", "thomas", "jose", "pletcher", "levine", "christopher",
                        "jacobson", "mike", "contessa", "krubera", "gullo", "morales", "edward", "belmont", 
                        "jeremiah", "chad", "ray", "patrick", "tr", "trn", "jr", "'s", "r", "j", "l"]

    incstopWords = stopWords + incmoreStopWords
    len(incstopWords)

    initialDescDF['Desc NoStops'] = initialDescDF['Incident Description'].apply(lambda x: ' '.join([word for word in x.split() if word not in incstopWords]))

    # now create final frame with merged information and fixed descriptions
    initialDF['Fixed Incident Description'] = incidentDescDF['Desc NoStops']
    fixedDF = initialDF[['Fixed Incident Description', 'Outcome']]
    fixedDF.columns = ['Incident Description', 'Outcome']

    # need to create the proper frame now with each Incident Description tokeninized as in the fClassDF
    # which as all the stop words and punctuation, etc. removed
    # create list of phrase documents as (list of words, label)
    # first tokenize all the Incident Descriptions
    fixedDF['Tokenized'] = fixedDF.apply(lambda row: nltk.word_tokenize(row['Incident Description']), axis=1)

    #documents = [(desc, outcome) for outcome in outcomeList]
    # for desc in 
    fixed_tokens_list = fixedDF['Tokenized'].tolist()
    fixed_outcome_list = fixedDF['Outcome'].tolist()

    # merge the lists togeter
    fixedList = merge(fixed_tokens_list, fixed_outcome_list)
    # shuffle the list
    random.shuffle(fixedList)
    return fixedList
