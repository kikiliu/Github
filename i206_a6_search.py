# -*- coding: utf-8 -*-
"""All class are stored in search.py and shared by three required python files"""
import search
import webbrowser
    
if __name__ == '__main__':
    sandbox_url = 'http://courses.ischool.berkeley.edu/i206/f13/a6-sandbox/index.html'
    scheduler = search.Scheduler()
    downloader = search.Downloader()
    index_builder = search.Index_builder()
    
    """Traverse web and load inverted index & document instances"""
    scheduler.add_url(sandbox_url)    
    doc_dict = {}           #key of document id and value of document instance
    while True:                       
        next_url = scheduler.get_next_url()
        if next_url == None:
            break
        else:
            page_data = downloader.download(next_url)
            doc = search.Document(page_data,next_url)
            doc_dict[doc.doc_id] = doc

            for word in doc.get_words().keys():
                index_builder.add_word(word, doc.doc_id)
            for anchor in doc.get_anchors(next_url):
                scheduler.add_url(anchor.link)                
    
    """Process query and retrive documents"""
    print """Please input your query:"""
    user_input = raw_input()
    query = search.Query(user_input)
    query_words = query.parse_query()
    
    list_of_doc_lists = []
    for word in query_words:        
        list_of_doc_lists.append(index_builder.retrieve_doc(word))
    aggregator = search.Aggregator()
    doc_intersect = aggregator.get_intersect(list_of_doc_lists)
    documents = []
    if doc_intersect != None:
        for docid in doc_intersect:
            documents.append(doc_dict[docid])
            
    """Render search results"""    
    result = search.Result_Page()
    result.render_result_page(documents)
    webbrowser.open(result.render_result_page(documents))