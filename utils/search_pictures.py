from icrawler.builtin import GoogleImageCrawler

def download(query, path, limit = 5):
    google_crawler = GoogleImageCrawler(feeder_threads=1,
        parser_threads=2,
        downloader_threads=4,
        storage={'root_dir': path})
    google_crawler.crawl(keyword=query, offset=0, max_num=limit, min_size=(200,200), max_size=None)