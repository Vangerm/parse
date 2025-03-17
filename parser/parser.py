class Parser:
    __ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    __HEADERS = [
        {
            "Accept": __ACCEPT,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        },
        {
            "Accept": __ACCEPT,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        },
        {
            "Accept": __ACCEPT,
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; Pixel 3)"
        },
        {
            "Accept": __ACCEPT,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
        },
        {
            "Accept": __ACCEPT,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0)"
        },
        {
            "Accept": __ACCEPT,
            "User-Agent": "Mozilla/5.0 (Linux; Ubuntu; X11; rv:92.0) Gecko/20100101 Firefox/92.0"
        },
        {
            "Accept": __ACCEPT,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        },
        {
            "Accept": __ACCEPT,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0"
        },
        {
            "Accept": __ACCEPT,
            "User-Agent": "Opera/68.0.3618.173 (Windows NT 10.0; Win64; x64) Presto/2.12.388 Version/12.16"
        }]

    def discharge_categories(self, urls: list[str]):
        pass
