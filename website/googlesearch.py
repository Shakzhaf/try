from apiclient.discovery import build
import pickle
#api_key='AIzaSyB7Dk9LOuWmpGx8CWkwBVL9_6itzl8rRKU'   #project1
#api_key='AIzaSyCu7s2IVDXU62gjiQ__O18MqdXWWxDbsBU'   #project1
#api_key='AIzaSyA7b6ewgE5-eHZqCV8fAQDUBOAXGB4U_eE'   #project2

#search_engine_id='015065351241375742654:cuvgckgk3ds'
#resource = build("customsearch", 'v1', developerKey=api_key).cse()

def search__(query, number_of_query=10):
    result_list=[]
    result_link=[]
    result_title=[]
    result_desc=[]
    for i in range(1,number_of_query,10):
        result=resource.list(q=query, cx=search_engine_id,start=i).execute()
        for item in result['items']:
            result_link=item['link']
            result_title=item['title']
            try:
                result_desc=item['pagemap']['metatags'][0]['og:description']
            except:
                result_desc='description not found'
            result_list.append([result_title,result_link,result_desc])
        
    return result_list

def search(query, number_of_query=10):
    with open ('tensorflow_results', 'rb') as fp:
        result_list = pickle.load(fp)
        return result_list[:number_of_query]