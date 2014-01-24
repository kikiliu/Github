"""All class are stored in search.py and shared by three required python files"""
import search  

if __name__ == '__main__':
    sandbox_url = 'http://courses.ischool.berkeley.edu/i206/f13/a6-sandbox/index.html'
    scheduler = search.Scheduler()
    downloader = search.Downloader()
    
    scheduler.add_url(sandbox_url)

    while True:                       
        next_url = scheduler.get_next_url()
        if next_url == None:
            break
        else:
            page_data = downloader.download(next_url)
            doc = search.Document(page_data,next_url)
            for anchor in doc.get_anchors(next_url):
                scheduler.add_url(anchor.link)
    scheduler.print_pages_found()